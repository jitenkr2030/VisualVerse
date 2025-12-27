"""
Governance Services - Main Application Entry Point
Handles identity, access management, content moderation, analytics, and audit.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from collections import defaultdict

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.database import get_db, Base, engine
from shared.database.models import (
    User, Role, Institution, Content, AuditLog, ModerationQueue,
    UserProgress, AssessmentResult, ContentStatus
)
from shared.auth.jwt_handler import get_current_user, has_permission, ROLE_ADMIN, ROLE_MODERATOR
from shared.schemas.api_schemas import (
    UserResponse, UserUpdate, ModerationReview, ModerationResponse,
    AuditLogQuery, AuditLogResponse, AnalyticsQuery, AnalyticsResponse,
    ApiResponse, ErrorResponse, PaginatedResponse
)

# Create FastAPI application
app = FastAPI(
    title="VisualVerse Governance Services",
    description="Identity, Access Management, Moderation, Analytics, and Audit",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Database Initialization ==============

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    Base.metadata.create_all(bind=engine)


# ============== Identity & Access Management Endpoints ==============

@app.get("/api/v1/users", response_model=List[UserResponse], tags=["Identity"])
async def list_users(
    role: Optional[str] = None,
    institution_id: Optional[int] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List users with filtering and pagination (admin only).
    """
    if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can list all users"
        )
    
    query = db.query(User)
    
    if role:
        query = query.filter(User.role.has(name=role))
    if institution_id:
        query = query.filter(User.institution_id == institution_id)
    if status:
        query = query.filter(User.status == status)
    
    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            status=user.status.value,
            institution_id=user.institution_id,
            role=user.role.name if user.role else "unknown",
            created_at=user.created_at,
            is_creator=user.is_creator,
            is_instructor=user.is_instructor
        )
        for user in users
    ]


@app.get("/api/v1/users/{user_id}", response_model=UserResponse, tags=["Identity"])
async def get_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user details by ID.
    """
    # Users can view their own profile, admins can view any
    if current_user["user_id"] != user_id and not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        status=user.status.value,
        institution_id=user.institution_id,
        role=user.role.name if user.role else "unknown",
        created_at=user.created_at,
        is_creator=user.is_creator,
        is_instructor=user.is_instructor
    )


@app.put("/api/v1/users/{user_id}", response_model=UserResponse, tags=["Identity"])
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user information.
    """
    # Users can update their own profile, admins can update any
    if current_user["user_id"] != user_id and not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user_data.full_name:
        user.full_name = user_data.full_name
    if user_data.avatar_url:
        user.avatar_url = user_data.avatar_url
    if user_data.preferences:
        user.preferences = user_data.preferences
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        status=user.status.value,
        institution_id=user.institution_id,
        role=user.role.name if user.role else "unknown",
        created_at=user.created_at,
        is_creator=user.is_creator,
        is_instructor=user.is_instructor
    )


@app.post("/api/v1/users/{user_id}/suspend", tags=["Identity"])
async def suspend_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Suspend a user account (admin only).
    """
    if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can suspend users"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.status = "suspended"
    user.updated_at = datetime.utcnow()
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user["user_id"],
        action="user_suspended",
        resource_type="user",
        resource_id=str(user_id),
        details={"reason": "Administrative action"}
    )
    db.add(audit)
    db.commit()
    
    return ApiResponse(success=True, message=f"User {user_id} has been suspended")


@app.post("/api/v1/users/{user_id}/activate", tags=["Identity"])
async def activate_user(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activate a suspended user account (admin only).
    """
    if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can activate users"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.status = "active"
    user.updated_at = datetime.utcnow()
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user["user_id"],
        action="user_activated",
        resource_type="user",
        resource_id=str(user_id),
        details={"reason": "Administrative action"}
    )
    db.add(audit)
    db.commit()
    
    return ApiResponse(success=True, message=f"User {user_id} has been activated")


# ============== Content Moderation Endpoints ==============

@app.get("/api/v1/moderation/queue", response_model=List[ModerationResponse], tags=["Moderation"])
async def get_moderation_queue(
    status: Optional[str] = "pending",
    platform: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get content pending moderation (moderators and admins only).
    """
    if not has_permission(current_user.get("role", ""), ROLE_MODERATOR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator access required"
        )
    
    query = db.query(ModerationQueue).filter(ModerationQueue.status == status)
    
    if platform:
        query = query.filter(ModerationQueue.content.has(platform=platform))
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for item in items:
        content_data = None
        if item.content:
            content_data = {
                "id": item.content.id,
                "title": item.content.title,
                "platform": item.content.platform,
                "creator_id": item.content.creator_id
            }
        
        result.append(ModerationResponse(
            id=item.id,
            content_id=item.content_id,
            status=item.status,
            reviewer_id=item.reviewer_id,
            review_notes=item.review_notes,
            created_at=item.created_at,
            reviewed_at=item.reviewed_at,
            content=content_data
        ))
    
    return result


@app.post("/api/v1/moderation/{moderation_id}/review", tags=["Moderation"])
async def review_content(
    moderation_id: int,
    review: ModerationReview,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve or reject content in moderation queue.
    """
    if not has_permission(current_user.get("role", ""), ROLE_MODERATOR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator access required"
        )
    
    moderation = db.query(ModerationQueue).filter(ModerationQueue.id == moderation_id).first()
    if not moderation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moderation item not found"
        )
    
    # Update moderation status
    moderation.status = review.status
    moderation.reviewer_id = current_user["user_id"]
    moderation.review_notes = review.review_notes
    moderation.reviewed_at = datetime.utcnow()
    
    # Update content status
    if moderation.content:
        if review.status == "approved":
            moderation.content.status = ContentStatus.APPROVED
        elif review.status == "rejected":
            moderation.content.status = ContentStatus.REJECTED
    
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user["user_id"],
        action=f"content_{review.status}",
        resource_type="content",
        resource_id=str(moderation.content_id),
        details={"notes": review.review_notes}
    )
    db.add(audit)
    db.commit()
    
    return ApiResponse(
        success=True,
        message=f"Content has been {review.status}",
        data={"moderation_id": moderation_id, "status": review.status}
    )


@app.post("/api/v1/moderation/content/{content_id}/submit", tags=["Moderation"])
async def submit_for_moderation(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit content for moderation review.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Check ownership
    if content.creator_id != current_user["user_id"]:
        if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to submit this content"
            )
    
    # Create moderation entry
    moderation = ModerationQueue(
        content_id=content_id,
        status="pending"
    )
    db.add(moderation)
    
    # Update content status
    content.status = ContentStatus.PENDING_REVIEW
    db.commit()
    
    return ApiResponse(
        success=True,
        message="Content submitted for moderation",
        data={"content_id": content_id, "moderation_id": moderation.id}
    )


# ============== Analytics Endpoints ==============

@app.get("/api/v1/analytics/overview", response_model=AnalyticsResponse, tags=["Analytics"])
async def get_overview_analytics(
    start_date: datetime,
    end_date: datetime,
    institution_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get platform analytics overview.
    """
    if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required for analytics"
        )
    
    # Calculate metrics
    user_query = db.query(User)
    if institution_id:
        user_query = user_query.filter(User.institution_id == institution_id)
    
    total_users = user_query.count()
    active_users = user_query.filter(User.status == "active").count()
    
    content_query = db.query(Content)
    total_content = content_query.count()
    
    # Get progress data
    progress_query = db.query(UserProgress).filter(
        UserProgress.updated_at >= start_date,
        UserProgress.updated_at <= end_date
    )
    
    total_views = progress_query.count()
    total_completions = progress_query.filter(
        UserProgress.status == "completed"
    ).count()
    
    # Get assessment results
    assessment_query = db.query(AssessmentResult).filter(
        AssessmentResult.completed_at >= start_date,
        AssessmentResult.completed_at <= end_date
    )
    
    avg_score = 0.0
    if assessment_query.count() > 0:
        avg_score = db.query(func.avg(AssessmentResult.score)).filter(
            AssessmentResult.completed_at >= start_date,
            AssessmentResult.completed_at <= end_date
        ).scalar() or 0.0
    
    # Platform breakdown
    platform_breakdown = {}
    for platform in ["mathverse", "physicsverse", "chemverse", "algverse", "finverse"]:
        count = db.query(Content).filter(Content.platform == platform).count()
        platform_breakdown[platform] = count
    
    # Generate time series data
    time_series_data = []
    current = start_date
    while current <= end_date:
        day_end = min(current + timedelta(days=1), end_date)
        
        daily_progress = db.query(UserProgress).filter(
            UserProgress.updated_at >= current,
            UserProgress.updated_at < day_end
        ).count()
        
        time_series_data.append({
            "date": current.isoformat(),
            "views": daily_progress,
            "completions": daily_progress // 3  # Estimate
        })
        current += timedelta(days=1)
    
    # Top content
    top_content = db.query(Content).order_by(
        Content.id.desc()
    ).limit(10).all()
    
    top_content_data = [
        {
            "id": c.id,
            "title": c.title,
            "platform": c.platform,
            "views": 0
        }
        for c in top_content
    ]
    
    return AnalyticsResponse(
        total_users=total_users,
        active_users=active_users,
        total_content=total_content,
        total_views=total_views,
        total_completions=total_completions,
        average_score=round(avg_score, 2),
        time_series_data=time_series_data,
        top_content=top_content_data,
        platform_breakdown=platform_breakdown
    )


@app.get("/api/v1/analytics/content/{content_id}", tags=["Analytics"])
async def get_content_analytics(
    content_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analytics for specific content.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Check access
    if content.creator_id != current_user["user_id"]:
        if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this content's analytics"
            )
    
    # Get progress statistics
    progress_items = db.query(UserProgress).filter(
        UserProgress.content_id == content_id
    )
    
    total_starts = progress_items.count()
    total_completions = progress_items.filter(
        UserProgress.status == "completed"
    ).count()
    avg_progress = db.query(func.avg(UserProgress.progress_percentage)).filter(
        UserProgress.content_id == content_id
    ).scalar() or 0.0
    
    avg_time = db.query(func.avg(UserProgress.time_spent_seconds)).filter(
        UserProgress.content_id == content_id
    ).scalar() or 0
    
    return {
        "content_id": content_id,
        "total_starts": total_starts,
        "total_completions": total_completions,
        "completion_rate": round(total_completions / total_starts * 100, 2) if total_starts > 0 else 0,
        "average_progress": round(avg_progress, 2),
        "average_time_seconds": round(avg_time, 2)
    }


# ============== Audit Log Endpoints ==============

@app.get("/api/v1/audit/logs", response_model=List[AuditLogResponse], tags=["Audit"])
async def get_audit_logs(
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs (admin only).
    """
    if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required for audit logs"
        )
    
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if start_date:
        query = query.filter(AuditLog.created_at >= start_date)
    if end_date:
        query = query.filter(AuditLog.created_at <= end_date)
    
    logs = query.order_by(AuditLog.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    
    return [
        AuditLogResponse(
            id=log.id,
            user_id=log.user_id,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            details=log.details,
            ip_address=log.ip_address,
            created_at=log.created_at
        )
        for log in logs
    ]


@app.post("/api/v1/audit/log", tags=["Audit"])
async def create_audit_log(
    user_id: Optional[int],
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Create an audit log entry (internal endpoint for other services).
    """
    audit = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )
    db.add(audit)
    db.commit()
    
    return ApiResponse(success=True, message="Audit log created")


# ============== Health Check ==============

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for service monitoring.
    """
    return {"status": "healthy", "service": "governance"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
