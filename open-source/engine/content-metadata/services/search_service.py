"""
Search Service for VisualVerse Content Metadata Service

Implements basic text search and vector search logic to find concepts
based on user queries with relevance scoring and faceted search capabilities.
"""

from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func, text
from sqlalchemy.sql import case
import logging
import re
from collections import Counter
from datetime import datetime, timedelta

from ..models.concept import Concept
from ..models.subject import Subject
from ..models.content_item import ContentItem
from ..models.user_progress import UserProgress

logger = logging.getLogger(__name__)

class SearchService:
    """Service for search operations across concepts and content"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def search_concepts(
        self,
        query: str,
        subject_ids: Optional[List[str]] = None,
        difficulty_levels: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        content_types: Optional[List[str]] = None,
        date_range: Optional[Dict[str, str]] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "relevance",
        sort_order: str = "desc"
    ) -> Dict[str, Any]:
        """
        Search concepts with comprehensive filtering and relevance scoring
        
        Args:
            query: Search query string
            subject_ids: List of subject IDs to filter by
            difficulty_levels: List of difficulty levels (1-5)
            tags: List of tags to filter by
            content_types: List of content types to filter by
            date_range: Date range filter {'start': '2023-01-01', 'end': '2023-12-31'}
            page: Page number (1-based)
            page_size: Items per page
            sort_by: Sort field ('relevance', 'name', 'created', 'difficulty')
            sort_order: Sort direction ('asc' or 'desc')
            
        Returns:
            Dictionary with search results, facets, and metadata
        """
        try:
            start_time = datetime.now()
            
            # Build the base query with joins
            search_query = self.db.query(Concept).join(Subject)
            
            # Apply text search with relevance scoring
            if query.strip():
                search_query, relevance_scores = self._apply_text_search(search_query, query)
            else:
                relevance_scores = {}
            
            # Apply filters
            filters_applied = []
            
            if subject_ids:
                search_query = search_query.filter(Concept.subject_id.in_(subject_ids))
                filters_applied.append(f"subjects: {len(subject_ids)} selected")
            
            if difficulty_levels:
                search_query = search_query.filter(Concept.difficulty_level.in_(difficulty_levels))
                filters_applied.append(f"difficulty: {difficulty_levels}")
            
            if tags:
                search_query = self._apply_tag_filter(search_query, tags)
                filters_applied.append(f"tags: {', '.join(tags)}")
            
            if content_types:
                search_query = self._apply_content_type_filter(search_query, content_types)
                filters_applied.append(f"content types: {', '.join(content_types)}")
            
            if date_range:
                search_query = self._apply_date_filter(search_query, date_range)
                filters_applied.append(f"date range: {date_range['start']} to {date_range['end']}")
            
            # Get total count before pagination
            total_results = search_query.count()
            
            # Apply sorting
            search_query = self._apply_sorting(search_query, sort_by, sort_order, relevance_scores, query)
            
            # Apply pagination
            offset = (page - 1) * page_size
            results = search_query.offset(offset).limit(page_size).all()
            
            # Calculate search time
            search_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Format results with additional metadata
            formatted_results = []
            for concept in results:
                result_data = self._format_search_result(concept, relevance_scores.get(concept.id, 0))
                formatted_results.append(result_data)
            
            # Generate facets for filtered results
            facets = self._generate_facets(search_query)
            
            return {
                'items': formatted_results,
                'total': total_results,
                'page': page,
                'page_size': page_size,
                'search_time_ms': round(search_time, 2),
                'query': query,
                'facets': facets,
                'filters_applied': filters_applied,
                'has_next': (page * page_size) < total_results,
                'has_previous': page > 1
            }
            
        except Exception as e:
            logger.error(f"Error in concept search: {e}")
            raise
    
    def search_suggestions(
        self,
        query: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get search suggestions based on partial input
        
        Args:
            query: Partial search query
            limit: Maximum number of suggestions
            
        Returns:
            List of search suggestions
        """
        try:
            if not query.strip():
                return []
            
            # Get concept name suggestions
            name_suggestions = self.db.query(Concept.name, Concept.id, Subject.name.label('subject_name')).join(
                Subject
            ).filter(
                Concept.name.ilike(f"%{query}%")
            ).filter(
                Concept.is_published == True
            ).order_by(Concept.name).limit(limit).all()
            
            # Get tag suggestions
            tag_suggestions = self.db.query(
                func.unnest(Concept.tags).label('tag'),
                func.count(Concept.id).label('frequency')
            ).filter(
                Concept.tags.isnot(None),
                Concept.is_published == True
            ).group_by(
                func.unnest(Concept.tags)
            ).having(
                func.unnest(Concept.tags).ilike(f"%{query}%")
            ).order_by(
                desc('frequency')
            ).limit(limit).all()
            
            # Format suggestions
            suggestions = []
            
            # Add concept suggestions
            for suggestion in name_suggestions:
                suggestions.append({
                    'type': 'concept',
                    'text': suggestion.name,
                    'id': suggestion.id,
                    'subject': suggestion.subject_name,
                    'relevance': len(query) / len(suggestion.name)
                })
            
            # Add tag suggestions
            for suggestion in tag_suggestions:
                suggestions.append({
                    'type': 'tag',
                    'text': suggestion.tag,
                    'frequency': suggestion.frequency,
                    'relevance': len(query) / len(suggestion.tag)
                })
            
            # Sort by relevance and limit
            suggestions.sort(key=lambda x: x['relevance'], reverse=True)
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Error getting search suggestions: {e}")
            return []
    
    def get_popular_searches(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get popular search terms based on search index usage
        
        Args:
            limit: Maximum number of popular searches to return
            
        Returns:
            List of popular search terms with counts
        """
        try:
            # This is a placeholder implementation
            # In a real system, you'd track search queries and their frequency
            
            # For now, return commonly searched concepts as "popular"
            popular_concepts = self.db.query(
                Concept.name,
                Concept.id,
                Subject.name.label('subject_name'),
                func.count(UserProgress.id).label('access_count')
            ).join(
                Subject
            ).outerjoin(
                UserProgress
            ).filter(
                Concept.is_published == True
            ).group_by(
                Concept.id, Concept.name, Subject.name
            ).order_by(
                desc('access_count')
            ).limit(limit).all()
            
            return [
                {
                    'term': concept.name,
                    'type': 'concept',
                    'count': concept.access_count,
                    'subject': concept.subject_name
                }
                for concept in popular_concepts
            ]
            
        except Exception as e:
            logger.error(f"Error getting popular searches: {e}")
            return []
    
    def get_trending_concepts(
        self,
        subject_id: Optional[str] = None,
        days: int = 7,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get trending concepts based on recent user activity
        
        Args:
            subject_id: Optional subject filter
            days: Number of days to look back
            limit: Maximum number of concepts to return
            
        Returns:
            List of trending concepts with activity metrics
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Build query for trending concepts
            query = self.db.query(
                Concept,
                func.count(UserProgress.id).label('recent_activity'),
                func.count(func.distinct(UserProgress.user_id)).label('unique_users')
            ).outerjoin(
                UserProgress
            ).filter(
                Concept.is_published == True,
                UserProgress.created_at >= cutoff_date
            )
            
            if subject_id:
                query = query.filter(Concept.subject_id == subject_id)
            
            trending = query.group_by(Concept.id).order_by(
                desc('recent_activity'),
                desc('unique_users')
            ).limit(limit).all()
            
            return [
                {
                    'concept': self._format_search_result(concept, 0),
                    'recent_activity': activity,
                    'unique_users': unique_users,
                    'activity_score': activity + (unique_users * 0.5)  # Weighted score
                }
                for concept, activity, unique_users in trending
            ]
            
        except Exception as e:
            logger.error(f"Error getting trending concepts: {e}")
            return []
    
    def get_related_concepts(
        self,
        concept_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get concepts related to a given concept based on various factors
        
        Args:
            concept_id: Concept to find relations for
            limit: Maximum number of related concepts
            
        Returns:
            List of related concepts with similarity scores
        """
        try:
            # Get the source concept
            source_concept = self.db.query(Concept).filter(Concept.id == concept_id).first()
            if not source_concept:
                return []
            
            # Find concepts in the same subject with similar difficulty
            subject_related = self.db.query(Concept).filter(
                and_(
                    Concept.subject_id == source_concept.subject_id,
                    Concept.id != concept_id,
                    Concept.is_published == True,
                    abs(Concept.difficulty_level - source_concept.difficulty_level) <= 1
                )
            ).limit(limit).all()
            
            # Find concepts with overlapping tags
            tag_related = []
            if source_concept.tags:
                for concept in self.db.query(Concept).filter(
                    and_(
                        Concept.id != concept_id,
                        Concept.is_published == True,
                        Concept.tags.isnot(None)
                    )
                ):
                    if concept.tags and source_concept.tags:
                        overlap = set(concept.tags) & set(source_concept.tags)
                        if overlap:
                            similarity_score = len(overlap) / len(set(concept.tags) | set(source_concept.tags))
                            tag_related.append((concept, similarity_score))
            
            # Combine and rank results
            related_concepts = []
            
            # Add subject-related concepts
            for concept in subject_related:
                related_concepts.append({
                    'concept': self._format_search_result(concept, 0),
                    'relationship_type': 'same_subject',
                    'similarity_score': 0.3
                })
            
            # Add tag-related concepts
            tag_related.sort(key=lambda x: x[1], reverse=True)
            for concept, score in tag_related[:limit]:
                related_concepts.append({
                    'concept': self._format_search_result(concept, 0),
                    'relationship_type': 'similar_tags',
                    'similarity_score': score
                })
            
            # Sort by similarity score and limit
            related_concepts.sort(key=lambda x: x['similarity_score'], reverse=True)
            return related_concepts[:limit]
            
        except Exception as e:
            logger.error(f"Error getting related concepts: {e}")
            return []
    
    def _apply_text_search(self, query, search_term: str) -> Tuple[any, Dict[str, float]]:
        """
        Apply text search with relevance scoring
        
        Returns:
            Tuple of (modified_query, relevance_scores_dict)
        """
        try:
            # Clean and prepare search terms
            search_terms = self._tokenize_query(search_term)
            if not search_terms:
                return query, {}
            
            # Build relevance scoring
            relevance_scores = {}
            
            # Create search conditions for different fields
            name_conditions = []
            description_conditions = []
            content_conditions = []
            tag_conditions = []
            
            for term in search_terms:
                name_conditions.append(Concept.name.ilike(f"%{term}%"))
                description_conditions.append(Concept.description.ilike(f"%{term}%"))
                content_conditions.append(Concept.content.ilike(f"%{term}%"))
                tag_conditions.append(Concept.tags.contains(term))
            
            # Combine conditions with OR for each field
            name_condition = or_(*name_conditions) if name_conditions else None
            description_condition = or_(*description_conditions) if description_conditions else None
            content_condition = or_(*content_conditions) if content_conditions else None
            tag_condition = or_(*tag_conditions) if tag_conditions else None
            
            # Build the full search condition
            search_conditions = []
            if name_condition:
                search_conditions.append(name_condition)
            if description_condition:
                search_conditions.append(description_condition)
            if content_condition:
                search_conditions.append(content_condition)
            if tag_condition:
                search_conditions.append(tag_condition)
            
            if search_conditions:
                query = query.filter(or_(*search_conditions))
            
            # Calculate relevance scores for each concept
            concepts = query.all()
            for concept in concepts:
                score = self._calculate_relevance_score(concept, search_terms)
                relevance_scores[concept.id] = score
            
            return query, relevance_scores
            
        except Exception as e:
            logger.error(f"Error applying text search: {e}")
            return query, {}
    
    def _tokenize_query(self, query: str) -> List[str]:
        """Tokenize search query into terms"""
        # Simple tokenization - split on whitespace and remove punctuation
        tokens = re.findall(r'\b\w+\b', query.lower())
        return [token for token in tokens if len(token) >= 2]
    
    def _calculate_relevance_score(self, concept: Concept, search_terms: List[str]) -> float:
        """Calculate relevance score for a concept and search terms"""
        try:
            score = 0.0
            
            # Title matches (highest weight)
            title_lower = concept.name.lower() if concept.name else ""
            for term in search_terms:
                if term in title_lower:
                    if title_lower == term:
                        score += 10.0  # Exact match
                    elif title_lower.startswith(term):
                        score += 8.0   # Prefix match
                    else:
                        score += 5.0   # Partial match
            
            # Description matches
            if concept.description:
                desc_lower = concept.description.lower()
                for term in search_terms:
                    if term in desc_lower:
                        score += 3.0
            
            # Content matches
            if concept.content:
                content_lower = concept.content.lower()
                for term in search_terms:
                    if term in content_lower:
                        score += 1.0
            
            # Tag matches
            if concept.tags:
                for term in search_terms:
                    for tag in concept.tags:
                        if term in tag.lower():
                            score += 2.0
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
            return 0.0
    
    def _apply_tag_filter(self, query, tags: List[str]):
        """Apply tag filter to query"""
        tag_conditions = []
        for tag in tags:
            tag_conditions.append(Concept.tags.contains(tag))
        
        if tag_conditions:
            return query.filter(or_(*tag_conditions))
        return query
    
    def _apply_content_type_filter(self, query, content_types: List[str]):
        """Apply content type filter based on associated content"""
        content_subquery = self.db.query(ContentItem.concept_id).filter(
            ContentItem.content_type.in_(content_types)
        ).distinct()
        
        return query.filter(Concept.id.in_(content_subquery))
    
    def _apply_date_filter(self, query, date_range: Dict[str, str]):
        """Apply date range filter"""
        try:
            start_date = datetime.fromisoformat(date_range['start'])
            end_date = datetime.fromisoformat(date_range['end'])
            
            return query.filter(
                and_(
                    Concept.created_at >= start_date,
                    Concept.created_at <= end_date
                )
            )
        except Exception as e:
            logger.warning(f"Invalid date range format: {e}")
            return query
    
    def _apply_sorting(self, query, sort_by: str, sort_order: str, relevance_scores: Dict[str, float], search_query: str):
        """Apply sorting to query"""
        if sort_by == "relevance" and search_query.strip() and relevance_scores:
            # Sort by relevance score
            concept_ids = list(relevance_scores.keys())
            relevance_scores_list = [relevance_scores.get(cid, 0) for cid in concept_ids]
            
            # This is a simplified approach - in a real system you'd use CASE statements
            return query.order_by(desc(func.array_position(concept_ids, Concept.id)))
        
        # Standard field-based sorting
        sort_mapping = {
            'name': Concept.name,
            'created': Concept.created_at,
            'updated': Concept.updated_at,
            'difficulty': Concept.difficulty_level
        }
        
        sort_field = sort_mapping.get(sort_by, Concept.created_at)
        
        if sort_order == "desc":
            return query.order_by(desc(sort_field))
        else:
            return query.order_by(asc(sort_field))
    
    def _generate_facets(self, query) -> Dict[str, Any]:
        """Generate facet counts for the current filtered results"""
        try:
            # Get distinct subjects with counts
            subjects = self.db.query(
                Subject.id,
                Subject.name,
                func.count(Concept.id).label('count')
            ).join(Concept).group_by(Subject.id, Subject.name).all()
            
            # Get difficulty level distribution
            difficulties = self.db.query(
                Concept.difficulty_level,
                func.count(Concept.id).label('count')
            ).group_by(Concept.difficulty_level).all()
            
            # Get popular tags
            tags = self.db.query(
                func.unnest(Concept.tags).label('tag'),
                func.count(Concept.id).label('count')
            ).filter(
                Concept.tags.isnot(None)
            ).group_by(
                func.unnest(Concept.tags)
            ).order_by(desc('count')).limit(20).all()
            
            # Get content types
            content_types = self.db.query(
                ContentItem.content_type,
                func.count(func.distinct(ContentItem.concept_id)).label('concept_count')
            ).group_by(ContentItem.content_type).all()
            
            return {
                'subjects': [
                    {'id': subject.id, 'name': subject.name, 'count': subject.count}
                    for subject in subjects
                ],
                'difficulty_levels': [
                    {'level': difficulty.difficulty_level, 'count': difficulty.count}
                    for difficulty in difficulties
                ],
                'tags': [
                    {'tag': tag.tag, 'count': tag.count}
                    for tag in tags
                ],
                'content_types': [
                    {'type': ct.content_type, 'concept_count': ct.concept_count}
                    for ct in content_types
                ]
            }
            
        except Exception as e:
            logger.error(f"Error generating facets: {e}")
            return {}
    
    def _format_search_result(self, concept: Concept, relevance_score: float = 0.0) -> Dict[str, Any]:
        """Format a concept for search results"""
        # Get content count
        content_count = self.db.query(func.count(ContentItem.id)).filter(
            ContentItem.concept_id == concept.id
        ).scalar() or 0
        
        # Get user progress stats
        user_count = self.db.query(func.count(func.distinct(UserProgress.user_id))).filter(
            UserProgress.concept_id == concept.id
        ).scalar() or 0
        
        result = {
            'id': concept.id,
            'name': concept.name,
            'description': concept.description,
            'difficulty_level': concept.difficulty_level,
            'estimated_duration': concept.estimated_duration,
            'tags': concept.tags or [],
            'is_published': concept.is_published,
            'subject_id': concept.subject_id,
            'subject_name': concept.subject.name if concept.subject else None,
            'created_by': concept.created_by,
            'created_at': concept.created_at.isoformat() if concept.created_at else None,
            'updated_at': concept.updated_at.isoformat() if concept.updated_at else None,
            'content_count': content_count,
            'user_count': user_count
        }
        
        if relevance_score > 0:
            result['relevance_score'] = relevance_score
        
        return result