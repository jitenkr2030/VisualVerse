"""
Subjects API Routes for VisualVerse Content Metadata Service

API endpoints for managing educational subjects with CRUD operations
and relationship management.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
import logging

from ..app.database import get_db_session
from ..models.subject import Subject
from ..models.concept import Concept
from ...common.schemas.base_response import (
    BaseResponse, success_response, error_response, paginated_response
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/subjects", tags=["subjects"])

# Dependency to get database session
db_dependency = Depends(get_db_session)

@router.get("", response_model=BaseResponse)
async def list_subjects(
    db: Session = db_dependency,
    # Filtering
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    include_stats: bool = Query(False, description="Include concept counts and statistics"),
    
    # Sorting
    sort_by: str = Query("sort_order", description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
):
    """
    List all subjects with optional filtering and statistics.
    
    Can include statistics like:
    - Total concept count
    - Published concept count
    - Average difficulty level
    - Recent activity
    """
    try:
        # Build query
        query = db.query(Subject)
        
        # Apply filters
        if is_active is not None:
            query = query.filter(Subject.is_active == is_active)
        
        # Apply sorting
        if sort_by == "name":
            sort_field = Subject.name
        elif sort_by == "concept_count" and include_stats:
            # This will be handled after the query with group by
            sort_field = None
        else:
            sort_field = Subject.sort_order
        
        if sort_field:
            if sort_order == "desc":
                query = query.order_by(desc(sort_field))
            else:
                query = query.order_by(asc(sort_field))
        
        subjects = query.all()
        
        # Add statistics if requested
        if include_stats:
            # Get concept counts per subject
            concept_stats = db.query(
                Concept.subject_id,
                func.count(Concept.id).label('total_concepts'),
                func.sum(func.cast(Concept.is_published, int)).label('published_concepts'),
                func.avg(Concept.difficulty_level).label('avg_difficulty')
            ).group_by(Concept.subject_id).all()
            
            stats_dict = {stat.subject_id: stat for stat in concept_stats}
            
            # Enhance subjects with statistics
            for subject in subjects:
                stats = stats_dict.get(subject.id)
                if stats:
                    subject.concept_count = stats.total_concepts
                    subject.published_concepts = stats.published_concepts
                    subject.avg_difficulty = float(stats.avg_difficulty) if stats.avg_difficulty else None
                else:
                    subject.concept_count = 0
                    subject.published_concepts = 0
                    subject.avg_difficulty = None
        
        # Convert to dictionaries for response
        subject_data = []
        for subject in subjects:
            subject_dict = {
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "icon_url": subject.icon_url,
                "color_code": subject.color_code,
                "is_active": subject.is_active,
                "sort_order": subject.sort_order,
                "created_at": subject.created_at.isoformat() if subject.created_at else None,
                "updated_at": subject.updated_at.isoformat() if subject.updated_at else None
            }
            
            # Add statistics if available
            if include_stats:
                subject_dict.update({
                    "concept_count": getattr(subject, 'concept_count', 0),
                    "published_concepts": getattr(subject, 'published_concepts', 0),
                    "avg_difficulty": getattr(subject, 'avg_difficulty', None)
                })
            
            subject_data.append(subject_dict)
        
        return success_response(
            data=subject_data,
            message=f"Retrieved {len(subject_data)} subjects",
            metadata={
                "include_stats": include_stats,
                "filters": {"is_active": is_active},
                "sorting": {"sort_by": sort_by, "sort_order": sort_order}
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing subjects: {e}")
        return error_response(
            message="Failed to retrieve subjects",
            code="SUBJECTS_LIST_ERROR",
            details=str(e)
        )

@router.get("/{subject_id}", response_model=BaseResponse)
async def get_subject(
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = db_dependency,
    include_stats: bool = Query(False, description="Include detailed statistics"),
    include_concepts: bool = Query(False, description="Include concept summary"),
    concept_limit: int = Query(10, ge=1, le=100, description="Max concepts to include if include_concepts=True")
):
    """
    Get a single subject by ID with optional statistics and concept overview.
    """
    try:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        
        if not subject:
            return error_response(
                message="Subject not found",
                code="SUBJECT_NOT_FOUND",
                details=f"Subject with ID '{subject_id}' does not exist"
            )
        
        # Build subject data
        subject_data = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "icon_url": subject.icon_url,
            "color_code": subject.color_code,
            "is_active": subject.is_active,
            "sort_order": subject.sort_order,
            "created_at": subject.created_at.isoformat() if subject.created_at else None,
            "updated_at": subject.updated_at.isoformat() if subject.updated_at else None
        }
        
        # Add statistics if requested
        if include_stats:
            # Get comprehensive statistics
            stats_query = db.query(
                func.count(Concept.id).label('total_concepts'),
                func.sum(func.cast(Concept.is_published, int)).label('published_concepts'),
                func.avg(Concept.difficulty_level).label('avg_difficulty'),
                func.min(Concept.difficulty_level).label('min_difficulty'),
                func.max(Concept.difficulty_level).label('max_difficulty'),
                func.count(func.distinct(Concept.created_by)).label('creator_count')
            ).filter(Concept.subject_id == subject_id).first()
            
            if stats_query:
                subject_data.update({
                    "statistics": {
                        "total_concepts": stats_query.total_concepts,
                        "published_concepts": stats_query.published_concepts,
                        "avg_difficulty": float(stats_query.avg_difficulty) if stats_query.avg_difficulty else None,
                        "min_difficulty": stats_query.min_difficulty,
                        "max_difficulty": stats_query.max_difficulty,
                        "creator_count": stats_query.creator_count,
                        "concept_publication_rate": (stats_query.published_concepts / stats_query.total_concepts * 100) if stats_query.total_concepts > 0 else 0
                    }
                })
        
        # Add concept overview if requested
        if include_concepts:
            concepts = db.query(Concept).filter(
                Concept.subject_id == subject_id
            ).order_by(Concept.difficulty_level, Concept.name).limit(concept_limit).all()
            
            concept_summary = []
            for concept in concepts:
                concept_summary.append({
                    "id": concept.id,
                    "name": concept.name,
                    "difficulty_level": concept.difficulty_level,
                    "is_published": concept.is_published,
                    "estimated_duration": concept.estimated_duration,
                    "tag_count": len(concept.tags) if concept.tags else 0
                })
            
            subject_data["concepts_preview"] = concept_summary
        
        return success_response(
            data=subject_data,
            message="Subject retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting subject {subject_id}: {e}")
        return error_response(
            message="Failed to retrieve subject",
            code="SUBJECT_GET_ERROR",
            details=str(e)
        )

@router.post("", response_model=BaseResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject_data: Dict[str, Any],
    db: Session = db_dependency
):
    """
    Create a new subject.
    
    Required fields:
    - id: Unique identifier
    - name: Subject name
    
    Optional fields:
    - description: Detailed description
    - icon_url: URL to subject icon
    - color_code: Hex color code for UI theming
    - sort_order: Display order (defaults to next available)
    """
    try:
        # Validate required fields
        if 'id' not in subject_data or 'name' not in subject_data:
            return error_response(
                message="Missing required fields",
                code="MISSING_REQUIRED_FIELDS",
                details="Both 'id' and 'name' are required"
            )
        
        # Check if subject ID already exists
        existing = db.query(Subject).filter(Subject.id == subject_data['id']).first()
        if existing:
            return error_response(
                message="Subject ID already exists",
                code="SUBJECT_ID_EXISTS",
                details=f"A subject with ID '{subject_data['id']}' already exists"
            )
        
        # Get next sort order if not provided
        if 'sort_order' not in subject_data:
            max_order = db.query(func.max(Subject.sort_order)).scalar()
            subject_data['sort_order'] = (max_order or 0) + 1
        
        # Create subject
        subject = Subject(**subject_data)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        
        return success_response(
            data={
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "icon_url": subject.icon_url,
                "color_code": subject.color_code,
                "is_active": subject.is_active,
                "sort_order": subject.sort_order,
                "created_at": subject.created_at.isoformat() if subject.created_at else None
            },
            message="Subject created successfully",
            metadata={"subject_id": subject.id}
        )
        
    except ValueError as e:
        return error_response(
            message="Invalid subject data",
            code="INVALID_SUBJECT_DATA",
            details=str(e)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating subject: {e}")
        return error_response(
            message="Failed to create subject",
            code="SUBJECT_CREATE_ERROR",
            details=str(e)
        )

@router.put("/{subject_id}", response_model=BaseResponse)
async def update_subject(
    subject_data: Dict[str, Any],
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = db_dependency
):
    """
    Update an existing subject.
    
    All fields are optional for updates except the subject must exist.
    """
    try:
        # Check if subject exists
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            return error_response(
                message="Subject not found",
                code="SUBJECT_NOT_FOUND",
                details=f"Subject with ID '{subject_id}' does not exist"
            )
        
        # Update fields
        for field, value in subject_data.items():
            if hasattr(subject, field) and field not in ['id', 'created_at']:
                setattr(subject, field, value)
        
        db.commit()
        db.refresh(subject)
        
        return success_response(
            data={
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "icon_url": subject.icon_url,
                "color_code": subject.color_code,
                "is_active": subject.is_active,
                "sort_order": subject.sort_order,
                "updated_at": subject.updated_at.isoformat() if subject.updated_at else None
            },
            message="Subject updated successfully"
        )
        
    except ValueError as e:
        return error_response(
            message="Invalid subject data",
            code="INVALID_SUBJECT_DATA",
            details=str(e)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating subject {subject_id}: {e}")
        return error_response(
            message="Failed to update subject",
            code="SUBJECT_UPDATE_ERROR",
            details=str(e)
        )

@router.delete("/{subject_id}", response_model=BaseResponse)
async def delete_subject(
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = db_dependency,
    force: bool = Query(False, description="Force deletion even with existing concepts")
):
    """
    Delete a subject.
    
    By default, prevents deletion if concepts exist for this subject.
    Set force=True to delete all associated concepts as well.
    """
    try:
        # Check if subject exists
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            return error_response(
                message="Subject not found",
                code="SUBJECT_NOT_FOUND",
                details=f"Subject with ID '{subject_id}' does not exist"
            )
        
        # Check for existing concepts
        concept_count = db.query(Concept).filter(Concept.subject_id == subject_id).count()
        
        if concept_count > 0 and not force:
            return error_response(
                message="Cannot delete subject with existing concepts",
                code="SUBJECT_HAS_CONCEPTS",
                details=f"Subject has {concept_count} concepts. Use force=true to delete all concepts."
            )
        
        # Delete subject (this will cascade to concepts if force=True)
        db.delete(subject)
        db.commit()
        
        return success_response(
            message="Subject deleted successfully",
            metadata={
                "deleted_subject_id": subject_id,
                "concepts_deleted": concept_count if force else 0
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting subject {subject_id}: {e}")
        return error_response(
            message="Failed to delete subject",
            code="SUBJECT_DELETE_ERROR",
            details=str(e)
        )

@router.post("/{subject_id}/reorder", response_model=BaseResponse)
async def reorder_subjects(
    order_data: Dict[str, Any],
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = db_dependency
):
    """
    Update the sort order of subjects.
    
    Request body should contain:
    - new_order: New sort order value for the subject
    """
    try:
        new_order = order_data.get('new_order')
        if new_order is None:
            return error_response(
                message="Missing new_order field",
                code="MISSING_ORDER_FIELD"
            )
        
        # Validate order is integer and positive
        try:
            new_order = int(new_order)
            if new_order < 0:
                raise ValueError("Order must be non-negative")
        except (ValueError, TypeError):
            return error_response(
                message="Invalid order value",
                code="INVALID_ORDER",
                details="Order must be a non-negative integer"
            )
        
        # Check if subject exists
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            return error_response(
                message="Subject not found",
                code="SUBJECT_NOT_FOUND"
            )
        
        # Update sort order (reordering logic)
        old_order = subject.sort_order
        
        if new_order != old_order:
            # Shift other subjects' orders
            if new_order > old_order:
                # Moving down: decrement orders of subjects between old and new position
                db.query(Subject).filter(
                    Subject.sort_order > old_order,
                    Subject.sort_order <= new_order,
                    Subject.id != subject_id
                ).update({Subject.sort_order: Subject.sort_order - 1})
            else:
                # Moving up: increment orders of subjects between new and old position
                db.query(Subject).filter(
                    Subject.sort_order >= new_order,
                    Subject.sort_order < old_order,
                    Subject.id != subject_id
                ).update({Subject.sort_order: Subject.sort_order + 1})
            
            # Update the subject's order
            subject.sort_order = new_order
            db.commit()
        
        return success_response(
            data={
                "subject_id": subject_id,
                "old_order": old_order,
                "new_order": new_order
            },
            message="Subject order updated successfully"
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error reordering subject {subject_id}: {e}")
        return error_response(
            message="Failed to update subject order",
            code="SUBJECT_REORDER_ERROR",
            details=str(e)
        )

@router.get("/{subject_id}/concepts", response_model=BaseResponse)
async def get_subject_concepts(
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = db_dependency,
    # Filtering
    difficulty_level: Optional[int] = Query(None, ge=1, le=5, description="Filter by difficulty level"),
    is_published: Optional[bool] = Query(None, description="Filter by publication status"),
    
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    
    # Sorting
    sort_by: str = Query("name", description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
):
    """
    Get all concepts for a specific subject with filtering and pagination.
    """
    try:
        # Check if subject exists
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            return error_response(
                message="Subject not found",
                code="SUBJECT_NOT_FOUND"
            )
        
        # Build query
        query = db.query(Concept).filter(Concept.subject_id == subject_id)
        
        # Apply filters
        if difficulty_level is not None:
            query = query.filter(Concept.difficulty_level == difficulty_level)
        if is_published is not None:
            query = query.filter(Concept.is_published == is_published)
        
        # Apply sorting
        if sort_by == "name":
            sort_field = Concept.name
        elif sort_by == "difficulty":
            sort_field = Concept.difficulty_level
        elif sort_by == "created":
            sort_field = Concept.created_at
        else:
            sort_field = Concept.name
        
        if sort_order == "desc":
            query = query.order_by(desc(sort_field))
        else:
            query = query.order_by(asc(sort_field))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        concepts = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # Convert to response format
        concept_data = []
        for concept in concepts:
            concept_data.append({
                "id": concept.id,
                "name": concept.name,
                "description": concept.description,
                "difficulty_level": concept.difficulty_level,
                "estimated_duration": concept.estimated_duration,
                "tags": concept.tags or [],
                "is_published": concept.is_published,
                "created_by": concept.created_by,
                "created_at": concept.created_at.isoformat() if concept.created_at else None
            })
        
        return paginated_response(
            data=concept_data,
            page=page,
            page_size=page_size,
            total_items=total,
            message=f"Retrieved {len(concept_data)} concepts for subject '{subject.name}'",
            metadata={
                "subject_id": subject_id,
                "subject_name": subject.name,
                "filters": {
                    "difficulty_level": difficulty_level,
                    "is_published": is_published
                },
                "sorting": {
                    "sort_by": sort_by,
                    "sort_order": sort_order
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting concepts for subject {subject_id}: {e}")
        return error_response(
            message="Failed to retrieve subject concepts",
            code="SUBJECT_CONCEPTS_ERROR",
            details=str(e)
        )

@router.get("/statistics/overview", response_model=BaseResponse)
async def get_subjects_statistics(
    db: Session = db_dependency
):
    """
    Get overall statistics for all subjects.
    
    Returns aggregated statistics across all subjects including
    concept counts, difficulty distributions, and activity metrics.
    """
    try:
        # Get basic subject count
        total_subjects = db.query(Subject).count()
        active_subjects = db.query(Subject).filter(Subject.is_active == True).count()
        
        # Get concept statistics per subject
        subject_stats = db.query(
            Subject.id,
            Subject.name,
            func.count(Concept.id).label('total_concepts'),
            func.sum(func.cast(Concept.is_published, int)).label('published_concepts'),
            func.avg(Concept.difficulty_level).label('avg_difficulty')
        ).outerjoin(Concept, Subject.id == Concept.subject_id).group_by(Subject.id, Subject.name).all()
        
        # Calculate overall statistics
        total_concepts = sum(stat.total_concepts or 0 for stat in subject_stats)
        total_published = sum(stat.published_concepts or 0 for stat in subject_stats)
        
        # Get difficulty distribution
        difficulty_dist = db.query(
            Concept.difficulty_level,
            func.count(Concept.id).label('count')
        ).group_by(Concept.difficulty_level).all()
        
        difficulty_distribution = {str(item.difficulty_level): item.count for item in difficulty_dist}
        
        # Get recent activity (concepts created in last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_concepts = db.query(Concept).filter(Concept.created_at >= thirty_days_ago).count()
        
        return success_response(
            data={
                "overview": {
                    "total_subjects": total_subjects,
                    "active_subjects": active_subjects,
                    "total_concepts": total_concepts,
                    "total_published_concepts": total_published,
                    "publication_rate": (total_published / total_concepts * 100) if total_concepts > 0 else 0,
                    "recent_concepts_30_days": recent_concepts
                },
                "subject_details": [
                    {
                        "subject_id": stat.id,
                        "subject_name": stat.name,
                        "total_concepts": stat.total_concepts or 0,
                        "published_concepts": stat.published_concepts or 0,
                        "avg_difficulty": float(stat.avg_difficulty) if stat.avg_difficulty else None,
                        "publication_rate": ((stat.published_concepts or 0) / (stat.total_concepts or 1) * 100)
                    }
                    for stat in subject_stats
                ],
                "difficulty_distribution": difficulty_distribution
            },
            message="Subject statistics retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error getting subjects statistics: {e}")
        return error_response(
            message="Failed to retrieve subjects statistics",
            code="SUBJECTS_STATS_ERROR",
            details=str(e)
        )