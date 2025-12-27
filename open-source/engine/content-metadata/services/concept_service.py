"""
Concept Service for VisualVerse Content Metadata Service

Business logic layer for managing concepts, handling the complexity of linking
concepts to parent/child concepts (graph relationships) before saving to database.
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from datetime import datetime

from ..models.concept import Concept
from ..models.subject import Subject
from ..models.concept_relationship import ConceptRelationship
from ..models.content_item import ContentItem

logger = logging.getLogger(__name__)

class ConceptService:
    """Service for concept management operations"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def validate_subject_exists(self, subject_id: str) -> bool:
        """Validate that a subject exists"""
        return self.db.query(Subject).filter(Subject.id == subject_id).first() is not None
    
    def list_concepts(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        search_term: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        include_relationships: bool = False,
        include_content: bool = False
    ) -> Dict[str, Any]:
        """
        List concepts with filtering, pagination, and search
        
        Args:
            page: Page number (1-based)
            page_size: Items per page
            filters: Dictionary of filters to apply
            search_term: Text search term
            sort_by: Field to sort by
            sort_order: Sort direction ('asc' or 'desc')
            include_relationships: Whether to include relationship data
            include_content: Whether to include content item counts
            
        Returns:
            Dictionary with items, total count, and pagination info
        """
        try:
            # Build base query
            query = self.db.query(Concept).join(Subject)
            
            # Apply filters
            if filters:
                if 'subject_id' in filters:
                    query = query.filter(Concept.subject_id == filters['subject_id'])
                if 'difficulty_level' in filters:
                    query = query.filter(Concept.difficulty_level == filters['difficulty_level'])
                if 'is_published' in filters:
                    query = query.filter(Concept.is_published == filters['is_published'])
                if 'created_by' in filters:
                    query = query.filter(Concept.created_by == filters['created_by'])
            
            # Apply search
            if search_term:
                search_pattern = f"%{search_term}%"
                query = query.filter(
                    or_(
                        Concept.name.ilike(search_pattern),
                        Concept.description.ilike(search_pattern),
                        Concept.content.ilike(search_pattern)
                    )
                )
            
            # Apply sorting
            sort_field = self._get_sort_field(sort_by)
            if sort_field:
                if sort_order == "desc":
                    query = query.order_by(desc(sort_field))
                else:
                    query = query.order_by(asc(sort_field))
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * page_size
            concepts = query.offset(offset).limit(page_size).all()
            
            # Convert to response format
            items = []
            for concept in concepts:
                concept_data = self._format_concept(concept, include_relationships, include_content)
                items.append(concept_data)
            
            # Calculate pagination metadata
            has_next = (page * page_size) < total
            has_previous = page > 1
            
            return {
                'items': items,
                'total': total,
                'page': page,
                'page_size': page_size,
                'has_next': has_next,
                'has_previous': has_previous,
                'total_pages': (total + page_size - 1) // page_size
            }
            
        except Exception as e:
            logger.error(f"Error listing concepts: {e}")
            raise
    
    def get_concept(
        self,
        concept_id: str,
        include_relationships: bool = False,
        include_content: bool = False,
        include_prerequisites: bool = False,
        include_dependents: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Get a single concept by ID with optional related data
        
        Args:
            concept_id: Concept identifier
            include_relationships: Include all concept relationships
            include_content: Include associated content items
            include_prerequisites: Include prerequisite concepts
            include_dependents: Include concepts that depend on this concept
            
        Returns:
            Concept data dictionary or None if not found
        """
        try:
            concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
            if not concept:
                return None
            
            return self._format_concept(
                concept,
                include_relationships=include_relationships,
                include_content=include_content,
                include_prerequisites=include_prerequisites,
                include_dependents=include_dependents
            )
            
        except Exception as e:
            logger.error(f"Error getting concept {concept_id}: {e}")
            raise
    
    def create_concept(self, concept_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new concept with validation
        
        Args:
            concept_data: Concept data dictionary
            
        Returns:
            Created concept data
        """
        try:
            # Validate required fields
            required_fields = ['id', 'subject_id', 'name', 'difficulty_level']
            for field in required_fields:
                if field not in concept_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate subject exists
            if not self.validate_subject_exists(concept_data['subject_id']):
                raise ValueError(f"Subject '{concept_data['subject_id']}' does not exist")
            
            # Validate difficulty level
            difficulty = concept_data['difficulty_level']
            if not isinstance(difficulty, int) or not (1 <= difficulty <= 5):
                raise ValueError("Difficulty level must be an integer between 1 and 5")
            
            # Create concept
            concept = Concept(**concept_data)
            self.db.add(concept)
            self.db.commit()
            self.db.refresh(concept)
            
            # Handle prerequisites if provided
            if 'prerequisites' in concept_data and concept_data['prerequisites']:
                self._create_prerequisite_relationships(concept.id, concept_data['prerequisites'])
            
            return self._format_concept(concept)
            
        except IntegrityError as e:
            self.db.rollback()
            if "concepts.id" in str(e):
                raise ValueError(f"Concept ID '{concept_data['id']}' already exists")
            raise ValueError(f"Database integrity error: {e}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating concept: {e}")
            raise
    
    def update_concept(self, concept_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing concept
        
        Args:
            concept_id: Concept identifier
            updates: Dictionary of fields to update
            
        Returns:
            Updated concept data
        """
        try:
            concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
            if not concept:
                raise ValueError(f"Concept '{concept_id}' not found")
            
            # Validate subject if being updated
            if 'subject_id' in updates:
                if not self.validate_subject_exists(updates['subject_id']):
                    raise ValueError(f"Subject '{updates['subject_id']}' does not exist")
            
            # Validate difficulty level if being updated
            if 'difficulty_level' in updates:
                difficulty = updates['difficulty_level']
                if not isinstance(difficulty, int) or not (1 <= difficulty <= 5):
                    raise ValueError("Difficulty level must be an integer between 1 and 5")
            
            # Update fields
            for field, value in updates.items():
                if hasattr(concept, field) and field not in ['id', 'created_at', 'created_by']:
                    setattr(concept, field, value)
            
            self.db.commit()
            self.db.refresh(concept)
            
            return self._format_concept(concept)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating concept {concept_id}: {e}")
            raise
    
    def delete_concept(self, concept_id: str) -> bool:
        """
        Delete a concept and its relationships
        
        Args:
            concept_id: Concept identifier
            
        Returns:
            True if successful
        """
        try:
            concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
            if not concept:
                return False
            
            # Delete concept (this will cascade to relationships)
            self.db.delete(concept)
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting concept {concept_id}: {e}")
            return False
    
    def create_relationship(
        self,
        source_concept_id: str,
        target_concept_id: str,
        relationship_type: str,
        strength: Optional[float] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a relationship between concepts
        
        Args:
            source_concept_id: Source concept ID
            target_concept_id: Target concept ID
            relationship_type: Type of relationship
            strength: Relationship strength (0.0-1.0)
            description: Relationship description
            
        Returns:
            Created relationship data
        """
        try:
            # Validate concepts exist
            source = self.db.query(Concept).filter(Concept.id == source_concept_id).first()
            if not source:
                raise ValueError(f"Source concept '{source_concept_id}' not found")
            
            target = self.db.query(Concept).filter(Concept.id == target_concept_id).first()
            if not target:
                raise ValueError(f"Target concept '{target_concept_id}' not found")
            
            # Check if relationship already exists
            existing = self.db.query(ConceptRelationship).filter(
                and_(
                    ConceptRelationship.source_concept_id == source_concept_id,
                    ConceptRelationship.target_concept_id == target_concept_id,
                    ConceptRelationship.relationship_type == relationship_type
                )
            ).first()
            
            if existing:
                raise ValueError(f"Relationship already exists between {source_concept_id} and {target_concept_id}")
            
            # Create relationship
            relationship_data = {
                'source_concept_id': source_concept_id,
                'target_concept_id': target_concept_id,
                'relationship_type': relationship_type
            }
            
            if strength is not None:
                if not (0.0 <= strength <= 1.0):
                    raise ValueError("Relationship strength must be between 0.0 and 1.0")
                relationship_data['strength'] = strength
            
            if description:
                relationship_data['description'] = description
            
            relationship = ConceptRelationship(**relationship_data)
            self.db.add(relationship)
            self.db.commit()
            self.db.refresh(relationship)
            
            return self._format_relationship(relationship)
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Database integrity error: {e}")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating relationship: {e}")
            raise
    
    def delete_relationship(
        self,
        source_concept_id: str,
        target_concept_id: str,
        relationship_type: str
    ) -> bool:
        """
        Delete a specific relationship between concepts
        
        Args:
            source_concept_id: Source concept ID
            target_concept_id: Target concept ID
            relationship_type: Type of relationship
            
        Returns:
            True if successful
        """
        try:
            relationship = self.db.query(ConceptRelationship).filter(
                and_(
                    ConceptRelationship.source_concept_id == source_concept_id,
                    ConceptRelationship.target_concept_id == target_concept_id,
                    ConceptRelationship.relationship_type == relationship_type
                )
            ).first()
            
            if not relationship:
                return False
            
            self.db.delete(relationship)
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting relationship: {e}")
            return False
    
    def get_concept_dependencies(self, concept_id: str) -> Dict[str, Any]:
        """
        Get all dependencies for a concept
        
        Args:
            concept_id: Concept identifier
            
        Returns:
            Dictionary with prerequisites and dependents
        """
        try:
            # Get prerequisites (concepts this concept depends on)
            prerequisites = self.db.query(ConceptRelationship).filter(
                and_(
                    ConceptRelationship.target_concept_id == concept_id,
                    ConceptRelationship.relationship_type == 'prerequisite'
                )
            ).all()
            
            # Get dependents (concepts that depend on this concept)
            dependents = self.db.query(ConceptRelationship).filter(
                and_(
                    ConceptRelationship.source_concept_id == concept_id,
                    ConceptRelationship.relationship_type == 'prerequisite'
                )
            ).all()
            
            # Format results
            prerequisites_data = []
            for rel in prerequisites:
                source_concept = self.db.query(Concept).filter(Concept.id == rel.source_concept_id).first()
                if source_concept:
                    prerequisites_data.append({
                        'concept': self._format_concept(source_concept),
                        'relationship': self._format_relationship(rel)
                    })
            
            dependents_data = []
            for rel in dependents:
                target_concept = self.db.query(Concept).filter(Concept.id == rel.target_concept_id).first()
                if target_concept:
                    dependents_data.append({
                        'concept': self._format_concept(target_concept),
                        'relationship': self._format_relationship(rel)
                    })
            
            return {
                'concept_id': concept_id,
                'prerequisites': prerequisites_data,
                'dependents': dependents_data,
                'prerequisite_count': len(prerequisites_data),
                'dependent_count': len(dependents_data)
            }
            
        except Exception as e:
            logger.error(f"Error getting concept dependencies: {e}")
            raise
    
    def advanced_search(
        self,
        query: Optional[str] = None,
        subject_ids: Optional[List[str]] = None,
        difficulty_levels: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        has_content: Optional[bool] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "relevance",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """
        Advanced search for concepts with multiple criteria
        
        Args:
            query: Text query for search
            subject_ids: List of subject IDs to filter by
            difficulty_levels: List of difficulty levels to filter by
            tags: List of tags to filter by
            has_content: Filter concepts with/without content
            page: Page number
            page_size: Items per page
            sort_by: Sort field
            sort_order: Sort direction
            
        Returns:
            Search results with pagination
        """
        try:
            # Build base query with joins
            search_query = self.db.query(Concept).join(Subject)
            
            # Apply text search
            if query:
                search_pattern = f"%{query}%"
                search_query = search_query.filter(
                    or_(
                        Concept.name.ilike(search_pattern),
                        Concept.description.ilike(search_pattern),
                        Concept.content.ilike(search_pattern)
                    )
                )
            
            # Apply filters
            if subject_ids:
                search_query = search_query.filter(Concept.subject_id.in_(subject_ids))
            
            if difficulty_levels:
                search_query = search_query.filter(Concept.difficulty_level.in_(difficulty_levels))
            
            if tags:
                # Search in tags array (PostgreSQL specific)
                tag_conditions = []
                for tag in tags:
                    tag_conditions.append(Concept.tags.contains(tag))
                search_query = search_query.filter(or_(*tag_conditions))
            
            if has_content is not None:
                if has_content:
                    # Concepts with at least one content item
                    content_subquery = self.db.query(ContentItem.concept_id).distinct()
                    search_query = search_query.filter(Concept.id.in_(content_subquery))
                else:
                    # Concepts without content
                    content_subquery = self.db.query(ContentItem.concept_id).distinct()
                    search_query = search_query.filter(~Concept.id.in_(content_subquery))
            
            # Apply sorting
            if sort_by == "relevance" and query:
                # For text search, order by relevance (simple implementation)
                if sort_order == "desc":
                    search_query = search_query.order_by(desc(Concept.name))
                else:
                    search_query = search_query.order_by(asc(Concept.name))
            else:
                sort_field = self._get_sort_field(sort_by)
                if sort_field:
                    if sort_order == "desc":
                        search_query = search_query.order_by(desc(sort_field))
                    else:
                        search_query = search_query.order_by(asc(sort_field))
            
            # Get total count
            total = search_query.count()
            
            # Apply pagination
            offset = (page - 1) * page_size
            concepts = search_query.offset(offset).limit(page_size).all()
            
            # Convert to response format
            items = []
            for concept in concepts:
                concept_data = self._format_concept(concept, include_content=True)
                items.append(concept_data)
            
            return {
                'items': items,
                'total': total,
                'page': page,
                'page_size': page_size,
                'search_criteria': {
                    'query': query,
                    'subject_ids': subject_ids,
                    'difficulty_levels': difficulty_levels,
                    'tags': tags,
                    'has_content': has_content
                }
            }
            
        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            raise
    
    def get_popular_learning_paths(
        self,
        subject_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get popular learning paths based on completion rates and engagement
        
        Args:
            subject_id: Optional subject filter
            limit: Maximum number of paths to return
            
        Returns:
            List of popular learning paths with metadata
        """
        try:
            # This is a simplified implementation
            # In a real system, you'd track user engagement and completion rates
            
            from ..models.learning_path import LearningPath
            from ..models.user_progress import UserProgress
            
            # Build query for learning paths
            query = self.db.query(LearningPath)
            
            if subject_id:
                query = query.filter(LearningPath.subject_id == subject_id)
            
            learning_paths = query.filter(
                LearningPath.is_published == True
            ).order_by(
                desc(LearningPath.created_at)
            ).limit(limit).all()
            
            # Format results
            paths = []
            for path in learning_paths:
                # Get concept count for this path
                concept_count = self.db.query(func.count(Concept.id)).join(
                    LearningPath.concepts
                ).filter(
                    Concept.id == path.id
                ).scalar()
                
                paths.append({
                    'id': path.id,
                    'name': path.name,
                    'description': path.description,
                    'difficulty_level': path.difficulty_level,
                    'estimated_duration': path.estimated_duration,
                    'concept_count': concept_count,
                    'created_by': path.created_by,
                    'created_at': path.created_at.isoformat() if path.created_at else None
                })
            
            return paths
            
        except Exception as e:
            logger.error(f"Error getting popular learning paths: {e}")
            raise
    
    def get_concept_recommendations(
        self,
        concept_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get recommended concepts based on relationships and patterns
        
        Args:
            concept_id: Concept identifier
            limit: Maximum number of recommendations
            
        Returns:
            List of recommended concepts
        """
        try:
            # Get concepts that are related to this concept
            related_relationships = self.db.query(ConceptRelationship).filter(
                or_(
                    ConceptRelationship.source_concept_id == concept_id,
                    ConceptRelationship.target_concept_id == concept_id
                )
            ).all()
            
            # Extract related concept IDs
            related_concept_ids = set()
            for rel in related_relationships:
                if rel.source_concept_id != concept_id:
                    related_concept_ids.add(rel.source_concept_id)
                if rel.target_concept_id != concept_id:
                    related_concept_ids.add(rel.target_concept_id)
            
            if not related_concept_ids:
                return []
            
            # Get the actual concepts
            related_concepts = self.db.query(Concept).filter(
                Concept.id.in_(list(related_concept_ids))
            ).filter(Concept.is_published == True).limit(limit).all()
            
            # Format results
            recommendations = []
            for concept in related_concepts:
                recommendations.append(self._format_concept(concept))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting concept recommendations: {e}")
            raise
    
    def _create_prerequisite_relationships(self, concept_id: str, prerequisite_ids: List[str]):
        """Create prerequisite relationships for a concept"""
        try:
            for prereq_id in prerequisite_ids:
                # Check if prerequisite exists
                if not self.db.query(Concept).filter(Concept.id == prereq_id).first():
                    logger.warning(f"Prerequisite concept '{prereq_id}' does not exist, skipping")
                    continue
                
                # Create prerequisite relationship
                relationship = ConceptRelationship(
                    source_concept_id=prereq_id,
                    target_concept_id=concept_id,
                    relationship_type='prerequisite',
                    strength=1.0
                )
                self.db.add(relationship)
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error creating prerequisite relationships: {e}")
            raise
    
    def _get_sort_field(self, sort_by: str):
        """Get the SQLAlchemy field for sorting"""
        sort_mapping = {
            'name': Concept.name,
            'difficulty': Concept.difficulty_level,
            'created': Concept.created_at,
            'updated': Concept.updated_at,
            'duration': Concept.estimated_duration
        }
        return sort_mapping.get(sort_by)
    
    def _format_concept(
        self,
        concept: Concept,
        include_relationships: bool = False,
        include_content: bool = False,
        include_prerequisites: bool = False,
        include_dependents: bool = False
    ) -> Dict[str, Any]:
        """Format concept for API response"""
        data = {
            'id': concept.id,
            'subject_id': concept.subject_id,
            'subject_name': concept.subject.name if concept.subject else None,
            'name': concept.name,
            'description': concept.description,
            'content': concept.content,
            'difficulty_level': concept.difficulty_level,
            'estimated_duration': concept.estimated_duration,
            'tags': concept.tags or [],
            'learning_objectives': concept.learning_objectives or [],
            'prerequisites': concept.prerequisites or [],
            'metadata': concept.metadata or {},
            'is_published': concept.is_published,
            'created_by': concept.created_by,
            'created_at': concept.created_at.isoformat() if concept.created_at else None,
            'updated_at': concept.updated_at.isoformat() if concept.updated_at else None
        }
        
        # Include relationships if requested
        if include_relationships:
            relationships = self.db.query(ConceptRelationship).filter(
                or_(
                    ConceptRelationship.source_concept_id == concept.id,
                    ConceptRelationship.target_concept_id == concept.id
                )
            ).all()
            
            data['relationships'] = [self._format_relationship(rel) for rel in relationships]
        
        # Include content count if requested
        if include_content:
            content_count = self.db.query(func.count(ContentItem.id)).filter(
                ContentItem.concept_id == concept.id
            ).scalar()
            data['content_count'] = content_count or 0
        
        # Include prerequisites if requested
        if include_prerequisites:
            prereqs = self.db.query(ConceptRelationship).filter(
                and_(
                    ConceptRelationship.target_concept_id == concept.id,
                    ConceptRelationship.relationship_type == 'prerequisite'
                )
            ).all()
            
            prereq_concepts = []
            for rel in prereqs:
                prereq_concept = self.db.query(Concept).filter(Concept.id == rel.source_concept_id).first()
                if prereq_concept:
                    prereq_concepts.append(self._format_concept(prereq_concept))
            
            data['prerequisites'] = prereq_concepts
        
        # Include dependents if requested
        if include_dependents:
            dependents = self.db.query(ConceptRelationship).filter(
                and_(
                    ConceptRelationship.source_concept_id == concept.id,
                    ConceptRelationship.relationship_type == 'prerequisite'
                )
            ).all()
            
            dependent_concepts = []
            for rel in dependents:
                dependent_concept = self.db.query(Concept).filter(Concept.id == rel.target_concept_id).first()
                if dependent_concept:
                    dependent_concepts.append(self._format_concept(dependent_concept))
            
            data['dependents'] = dependent_concepts
        
        return data
    
    def _format_relationship(self, relationship: ConceptRelationship) -> Dict[str, Any]:
        """Format relationship for API response"""
        return {
            'id': relationship.id,
            'source_concept_id': relationship.source_concept_id,
            'target_concept_id': relationship.target_concept_id,
            'relationship_type': relationship.relationship_type,
            'strength': relationship.strength,
            'description': relationship.description,
            'created_at': relationship.created_at.isoformat() if relationship.created_at else None
        }