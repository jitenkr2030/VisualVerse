"""
Concepts API Routes for VisualVerse Content Metadata Service

API endpoints for CRUD operations on concepts with dependency injection
for database session management.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
import logging

from ..app.database import get_db_session
from ..models.concept import Concept
from ..models.subject import Subject
from ..services.concept_service import ConceptService
from ..services.search_service import SearchService
from ...common.schemas.base_response import (
    BaseResponse, success_response, error_response, paginated_response,
    ResponseBuilder, ValidationMessage, ValidationSeverity
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/concepts", tags=["concepts"])

# Dependency to get database session
db_dependency = Depends(get_db_session)

# Dependency to get concept service
concept_service_dependency = Depends(lambda db=db_dependency: ConceptService(db))

# Dependency to get search service
search_service_dependency = Depends(lambda db=db_dependency: SearchService(db))

@router.get("", response_model=BaseResponse)
async def list_concepts(
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency,
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    
    # Filtering
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    difficulty_level: Optional[int] = Query(None, ge=1, le=5, description="Filter by difficulty level (1-5)"),
    is_published: Optional[bool] = Query(None, description="Filter by publication status"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    
    # Search
    search: Optional[str] = Query(None, description="Search in name and description"),
    
    # Sorting
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    
    # Include related data
    include_relationships: bool = Query(False, description="Include concept relationships"),
    include_content: bool = Query(False, description="Include associated content items")
):
    """
    List concepts with filtering, pagination, and search capabilities.
    
    Supports:
    - Pagination with configurable page size
    - Filtering by subject, difficulty, publication status, creator
    - Text search in name and description
    - Sorting by various fields
    - Optional inclusion of relationships and content
    """
    try:
        # Build filters
        filters = {}
        if subject_id:
            filters['subject_id'] = subject_id
        if difficulty_level is not None:
            filters['difficulty_level'] = difficulty_level
        if is_published is not None:
            filters['is_published'] = is_published
        if created_by:
            filters['created_by'] = created_by
        
        # Execute search and pagination
        result = service.list_concepts(
            page=page,
            page_size=page_size,
            filters=filters,
            search_term=search,
            sort_by=sort_by,
            sort_order=sort_order,
            include_relationships=include_relationships,
            include_content=include_content
        )
        
        return paginated_response(
            data=result['items'],
            page=page,
            page_size=page_size,
            total_items=result['total'],
            message=f"Retrieved {len(result['items'])} concepts",
            metadata={
                "filters_applied": filters,
                "search_term": search,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "has_next": result['has_next'],
                "has_previous": result['has_previous']
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing concepts: {e}")
        return error_response(
            message="Failed to retrieve concepts",
            code="CONCEPTS_LIST_ERROR",
            details=str(e)
        )

@router.get("/{concept_id}", response_model=BaseResponse)
async def get_concept(
    concept_id: str = Path(..., description="Concept ID"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency,
    include_relationships: bool = Query(False, description="Include concept relationships"),
    include_content: bool = Query(False, description="Include associated content items"),
    include_prerequisites: bool = Query(False, description="Include prerequisite concepts"),
    include_dependents: bool = Query(False, description="Include concepts that depend on this concept")
):
    """
    Get a single concept by ID with optional related data inclusion.
    
    Can include:
    - Concept relationships (prerequisites, related concepts, etc.)
    - Associated content items
    - Prerequisite concepts
    - Concepts that depend on this concept
    """
    try:
        concept = service.get_concept(
            concept_id=concept_id,
            include_relationships=include_relationships,
            include_content=include_content,
            include_prerequisites=include_prerequisites,
            include_dependents=include_dependents
        )
        
        if not concept:
            return error_response(
                message="Concept not found",
                code="CONCEPT_NOT_FOUND",
                details=f"Concept with ID '{concept_id}' does not exist"
            )
        
        return success_response(
            data=concept,
            message="Concept retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting concept {concept_id}: {e}")
        return error_response(
            message="Failed to retrieve concept",
            code="CONCEPT_GET_ERROR",
            details=str(e)
        )

@router.post("", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_concept(
    concept_data: Dict[str, Any],
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Create a new concept.
    
    Required fields:
    - id: Unique identifier
    - subject_id: ID of the subject this concept belongs to
    - name: Concept name
    - difficulty_level: Difficulty level (1-5)
    
    Optional fields:
    - description: Detailed description
    - content: Rich content/markdown
    - estimated_duration: Estimated learning time in minutes
    - tags: List of tags
    - learning_objectives: List of learning objectives
    - prerequisites: List of prerequisite concept IDs
    - metadata: Additional metadata
    - created_by: ID of the user creating the concept
    """
    try:
        # Validate required fields
        required_fields = ['id', 'subject_id', 'name', 'difficulty_level']
        missing_fields = [field for field in required_fields if field not in concept_data]
        
        if missing_fields:
            return error_response(
                message="Missing required fields",
                code="MISSING_REQUIRED_FIELDS",
                details=f"Required fields: {', '.join(missing_fields)}"
            )
        
        # Validate subject exists
        if not service.validate_subject_exists(concept_data['subject_id']):
            return error_response(
                message="Invalid subject",
                code="INVALID_SUBJECT",
                details=f"Subject with ID '{concept_data['subject_id']}' does not exist"
            )
        
        # Create concept
        concept = service.create_concept(concept_data)
        
        return success_response(
            data=concept,
            message="Concept created successfully",
            metadata={"concept_id": concept['id']}
        )
        
    except ValueError as e:
        return error_response(
            message="Invalid concept data",
            code="INVALID_CONCEPT_DATA",
            details=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating concept: {e}")
        return error_response(
            message="Failed to create concept",
            code="CONCEPT_CREATE_ERROR",
            details=str(e)
        )

@router.put("/{concept_id}", response_model=BaseResponse)
async def update_concept(
    concept_data: Dict[str, Any],
    concept_id: str = Path(..., description="Concept ID"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Update an existing concept.
    
    All fields are optional for updates except the concept must exist.
    """
    try:
        # Check if concept exists
        existing_concept = service.get_concept(concept_id)
        if not existing_concept:
            return error_response(
                message="Concept not found",
                code="CONCEPT_NOT_FOUND",
                details=f"Concept with ID '{concept_id}' does not exist"
            )
        
        # Validate subject if being updated
        if 'subject_id' in concept_data:
            if not service.validate_subject_exists(concept_data['subject_id']):
                return error_response(
                    message="Invalid subject",
                    code="INVALID_SUBJECT",
                    details=f"Subject with ID '{concept_data['subject_id']}' does not exist"
                )
        
        # Update concept
        concept = service.update_concept(concept_id, concept_data)
        
        return success_response(
            data=concept,
            message="Concept updated successfully"
        )
        
    except ValueError as e:
        return error_response(
            message="Invalid concept data",
            code="INVALID_CONCEPT_DATA",
            details=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating concept {concept_id}: {e}")
        return error_response(
            message="Failed to update concept",
            code="CONCEPT_UPDATE_ERROR",
            details=str(e)
        )

@router.delete("/{concept_id}", response_model=BaseResponse)
async def delete_concept(
    concept_id: str = Path(..., description="Concept ID"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Delete a concept.
    
    Note: This will also delete associated relationships and may affect
    other concepts that depend on this concept.
    """
    try:
        # Check if concept exists
        existing_concept = service.get_concept(concept_id)
        if not existing_concept:
            return error_response(
                message="Concept not found",
                code="CONCEPT_NOT_FOUND",
                details=f"Concept with ID '{concept_id}' does not exist"
            )
        
        # Delete concept (this will cascade to relationships)
        success = service.delete_concept(concept_id)
        
        if success:
            return success_response(
                message="Concept deleted successfully",
                metadata={"deleted_concept_id": concept_id}
            )
        else:
            return error_response(
                message="Failed to delete concept",
                code="CONCEPT_DELETE_ERROR"
            )
        
    except Exception as e:
        logger.error(f"Error deleting concept {concept_id}: {e}")
        return error_response(
            message="Failed to delete concept",
            code="CONCEPT_DELETE_ERROR",
            details=str(e)
        )

@router.post("/{concept_id}/relationships", response_model=BaseResponse)
async def create_concept_relationship(
    relationship_data: Dict[str, Any],
    concept_id: str = Path(..., description="Source concept ID"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Create a relationship between concepts.
    
    Required fields:
    - target_concept_id: ID of the target concept
    - relationship_type: Type of relationship (prerequisite, related, builds_upon, etc.)
    
    Optional fields:
    - strength: Relationship strength (0.0 - 1.0)
    - description: Description of the relationship
    """
    try:
        # Validate required fields
        required_fields = ['target_concept_id', 'relationship_type']
        missing_fields = [field for field in required_fields if field not in relationship_data]
        
        if missing_fields:
            return error_response(
                message="Missing required fields",
                code="MISSING_REQUIRED_FIELDS",
                details=f"Required fields: {', '.join(missing_fields)}"
            )
        
        # Validate both concepts exist
        if not service.get_concept(concept_id):
            return error_response(
                message="Source concept not found",
                code="SOURCE_CONCEPT_NOT_FOUND"
            )
        
        target_id = relationship_data['target_concept_id']
        if not service.get_concept(target_id):
            return error_response(
                message="Target concept not found",
                code="TARGET_CONCEPT_NOT_FOUND",
                details=f"Concept with ID '{target_id}' does not exist"
            )
        
        # Create relationship
        relationship = service.create_relationship(
            source_concept_id=concept_id,
            target_concept_id=target_id,
            relationship_type=relationship_data['relationship_type'],
            strength=relationship_data.get('strength'),
            description=relationship_data.get('description')
        )
        
        return success_response(
            data=relationship,
            message="Concept relationship created successfully"
        )
        
    except ValueError as e:
        return error_response(
            message="Invalid relationship data",
            code="INVALID_RELATIONSHIP_DATA",
            details=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating concept relationship: {e}")
        return error_response(
            message="Failed to create concept relationship",
            code="RELATIONSHIP_CREATE_ERROR",
            details=str(e)
        )

@router.delete("/{concept_id}/relationships/{target_concept_id}", response_model=BaseResponse)
async def delete_concept_relationship(
    concept_id: str = Path(..., description="Source concept ID"),
    target_concept_id: str = Path(..., description="Target concept ID"),
    relationship_type: str = Query(..., description="Relationship type"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Delete a specific relationship between concepts.
    """
    try:
        success = service.delete_relationship(
            source_concept_id=concept_id,
            target_concept_id=target_concept_id,
            relationship_type=relationship_type
        )
        
        if success:
            return success_response(
                message="Concept relationship deleted successfully"
            )
        else:
            return error_response(
                message="Relationship not found",
                code="RELATIONSHIP_NOT_FOUND"
            )
        
    except Exception as e:
        logger.error(f"Error deleting concept relationship: {e}")
        return error_response(
            message="Failed to delete concept relationship",
            code="RELATIONSHIP_DELETE_ERROR",
            details=str(e)
        )

@router.get("/{concept_id}/dependencies", response_model=BaseResponse)
async def get_concept_dependencies(
    concept_id: str = Path(..., description="Concept ID"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Get all dependencies (prerequisites and relationships) for a concept.
    
    Returns both concepts that this concept depends on and concepts
    that depend on this concept.
    """
    try:
        dependencies = service.get_concept_dependencies(concept_id)
        
        return success_response(
            data=dependencies,
            message="Concept dependencies retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error getting concept dependencies: {e}")
        return error_response(
            message="Failed to retrieve concept dependencies",
            code="DEPENDENCIES_GET_ERROR",
            details=str(e)
        )

@router.post("/search", response_model=BaseResponse)
async def search_concepts(
    search_data: Dict[str, Any],
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency,
    search_service: SearchService = search_service_dependency
):
    """
    Advanced search for concepts with multiple criteria.
    
    Search parameters:
    - query: Text query for full-text search
    - subject_ids: List of subject IDs to filter by
    - difficulty_levels: List of difficulty levels (1-5)
    - tags: List of tags to filter by
    - has_content: Boolean to filter concepts with/without content
    - page: Page number
    - page_size: Items per page
    - sort_by: Sort field
    - sort_order: Sort order
    """
    try:
        result = service.advanced_search(
            query=search_data.get('query'),
            subject_ids=search_data.get('subject_ids'),
            difficulty_levels=search_data.get('difficulty_levels'),
            tags=search_data.get('tags'),
            has_content=search_data.get('has_content'),
            page=search_data.get('page', 1),
            page_size=search_data.get('page_size', 20),
            sort_by=search_data.get('sort_by', 'relevance'),
            sort_order=search_data.get('sort_order', 'desc')
        )
        
        return paginated_response(
            data=result['items'],
            page=search_data.get('page', 1),
            page_size=search_data.get('page_size', 20),
            total_items=result['total'],
            message=f"Found {len(result['items'])} concepts",
            metadata={
                "search_criteria": search_data,
                "search_time_ms": result.get('search_time_ms'),
                "facets": result.get('facets', {})
            }
        )
        
    except Exception as e:
        logger.error(f"Error searching concepts: {e}")
        return error_response(
            message="Failed to search concepts",
            code="SEARCH_ERROR",
            details=str(e)
        )

@router.get("/popular/learning-paths", response_model=BaseResponse)
async def get_popular_learning_paths(
    subject_id: Optional[str] = Query(None, description="Filter by subject ID"),
    limit: int = Query(10, ge=1, le=50, description="Number of learning paths to return"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Get popular learning paths based on completion rates and user engagement.
    """
    try:
        learning_paths = service.get_popular_learning_paths(
            subject_id=subject_id,
            limit=limit
        )
        
        return success_response(
            data=learning_paths,
            message=f"Retrieved {len(learning_paths)} popular learning paths",
            metadata={
                "subject_id": subject_id,
                "limit": limit
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting popular learning paths: {e}")
        return error_response(
            message="Failed to retrieve popular learning paths",
            code="POPULAR_PATHS_ERROR",
            details=str(e)
        )

@router.get("/{concept_id}/recommendations", response_model=BaseResponse)
async def get_concept_recommendations(
    concept_id: str = Path(..., description="Concept ID"),
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations to return"),
    db: Session = db_dependency,
    service: ConceptService = concept_service_dependency
):
    """
    Get recommended concepts based on relationships and user patterns.
    """
    try:
        recommendations = service.get_concept_recommendations(
            concept_id=concept_id,
            limit=limit
        )
        
        return success_response(
            data=recommendations,
            message=f"Retrieved {len(recommendations)} concept recommendations",
            metadata={
                "concept_id": concept_id,
                "limit": limit
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting concept recommendations: {e}")
        return error_response(
            message="Failed to retrieve concept recommendations",
            code="RECOMMENDATIONS_ERROR",
            details=str(e)
        )