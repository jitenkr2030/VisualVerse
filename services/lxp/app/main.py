"""
Learning Experience Platform (LXP) - Main Application Entry Point
Handles progress tracking, adaptive assessments, and recommendations.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import random

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.database import get_db, Base, engine
from shared.database.models import (
    User, Content, Concept, Lesson, UserProgress, Assessment,
    AssessmentResult, Syllabus, ContentConcept
)
from shared.auth.jwt_handler import get_current_user
from shared.schemas.api_schemas import (
    ProgressUpdate, ProgressResponse, AssessmentCreate, AssessmentResponse,
    AssessmentSubmission, AssessmentResultResponse, RecommendationRequest,
    RecommendationResponse, ApiResponse
)

# Create FastAPI application
app = FastAPI(
    title="VisualVerse Learning Experience Platform",
    description="Progress Tracking, Adaptive Assessments, and Recommendations",
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


# ============== Progress Tracking Endpoints ==============

@app.get("/api/v1/progress", response_model=List[ProgressResponse], tags=["Progress"])
async def get_user_progress(
    content_id: Optional[int] = None,
    concept_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress for current user with optional filtering.
    """
    query = db.query(UserProgress).filter(
        UserProgress.user_id == current_user["user_id"]
    )
    
    if content_id:
        query = query.filter(UserProgress.content_id == content_id)
    if concept_id:
        query = query.filter(UserProgress.concept_id == concept_id)
    if status:
        query = query.filter(UserProgress.status == status)
    
    progress_items = query.order_by(UserProgress.updated_at.desc()).all()
    
    return [
        ProgressResponse(
            id=p.id,
            user_id=p.user_id,
            content_id=p.content_id,
            lesson_id=p.lesson_id,
            concept_id=p.concept_id,
            status=p.status,
            progress_percentage=p.progress_percentage,
            score=p.score,
            time_spent_seconds=p.time_spent_seconds,
            attempts=p.attempts,
            completed_at=p.completed_at,
            updated_at=p.updated_at
        )
        for p in progress_items
    ]


@app.get("/api/v1/progress/{content_id}", response_model=ProgressResponse, tags=["Progress"])
async def get_content_progress(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's progress for specific content.
    """
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user["user_id"],
        UserProgress.content_id == content_id
    ).first()
    
    if not progress:
        return ProgressResponse(
            id=0,
            user_id=current_user["user_id"],
            content_id=content_id,
            lesson_id=None,
            concept_id=None,
            status="not_started",
            progress_percentage=0.0,
            score=None,
            time_spent_seconds=0,
            attempts=0,
            completed_at=None,
            updated_at=datetime.utcnow()
        )
    
    return ProgressResponse(
        id=progress.id,
        user_id=progress.user_id,
        content_id=progress.content_id,
        lesson_id=progress.lesson_id,
        concept_id=progress.concept_id,
        status=progress.status,
        progress_percentage=progress.progress_percentage,
        score=progress.score,
        time_spent_seconds=progress.time_spent_seconds,
        attempts=progress.attempts,
        completed_at=progress.completed_at,
        updated_at=progress.updated_at
    )


@app.put("/api/v1/progress/{content_id}", response_model=ProgressResponse, tags=["Progress"])
async def update_progress(
    content_id: int,
    progress_data: ProgressUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's progress for specific content.
    """
    # Check if content exists
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Find or create progress record
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user["user_id"],
        UserProgress.content_id == content_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user["user_id"],
            content_id=content_id,
            status="in_progress"
        )
        db.add(progress)
    
    # Update fields
    if progress_data.progress_percentage is not None:
        progress.progress_percentage = min(100, max(0, progress_data.progress_percentage))
        
        if progress.progress_percentage >= 100:
            progress.status = "completed"
            progress.completed_at = datetime.utcnow()
    
    if progress_data.score is not None:
        progress.score = progress_data.score
    
    if progress_data.time_spent_seconds is not None:
        progress.time_spent_seconds += progress_data.time_spent_seconds
    
    if progress_data.last_position_seconds is not None:
        progress.last_position_seconds = progress_data.last_position_seconds
    
    progress.attempts += 1
    progress.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    
    return ProgressResponse(
        id=progress.id,
        user_id=progress.user_id,
        content_id=progress.content_id,
        lesson_id=progress.lesson_id,
        concept_id=progress.concept_id,
        status=progress.status,
        progress_percentage=progress.progress_percentage,
        score=progress.score,
        time_spent_seconds=progress.time_spent_seconds,
        attempts=progress.attempts,
        completed_at=progress.completed_at,
        updated_at=progress.updated_at
    )


@app.post("/api/v1/progress/{content_id}/complete", response_model=ProgressResponse, tags=["Progress"])
async def mark_content_complete(
    content_id: int,
    score: Optional[float] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark content as completed.
    """
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user["user_id"],
        UserProgress.content_id == content_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user["user_id"],
            content_id=content_id,
            status="in_progress"
        )
        db.add(progress)
    
    progress.status = "completed"
    progress.progress_percentage = 100.0
    progress.score = score
    progress.completed_at = datetime.utcnow()
    progress.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(progress)
    
    return ProgressResponse(
        id=progress.id,
        user_id=progress.user_id,
        content_id=progress.content_id,
        lesson_id=progress.lesson_id,
        concept_id=progress.concept_id,
        status=progress.status,
        progress_percentage=progress.progress_percentage,
        score=progress.score,
        time_spent_seconds=progress.time_spent_seconds,
        attempts=progress.attempts,
        completed_at=progress.completed_at,
        updated_at=progress.updated_at
    )


@app.get("/api/v1/progress/stats", tags=["Progress"])
async def get_progress_stats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get progress statistics for current user.
    """
    user_id = current_user["user_id"]
    
    # Total content started
    total_started = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).count()
    
    # Total content completed
    total_completed = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.status == "completed"
    ).count()
    
    # Average progress
    avg_progress = db.query(func.avg(UserProgress.progress_percentage)).filter(
        UserProgress.user_id == user_id
    ).scalar() or 0.0
    
    # Total time spent
    total_time = db.query(func.sum(UserProgress.time_spent_seconds)).filter(
        UserProgress.user_id == user_id
    ).scalar() or 0
    
    # Platform breakdown
    platform_stats = {}
    user_progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()
    
    for p in user_progress:
        if p.content:
            platform = p.content.platform
            if platform not in platform_stats:
                platform_stats[platform] = {"started": 0, "completed": 0}
            platform_stats[platform]["started"] += 1
            if p.status == "completed":
                platform_stats[platform]["completed"] += 1
    
    # Streak calculation (simplified)
    streak = 0
    today = datetime.utcnow().date()
    for i in range(30):
        check_date = today - timedelta(days=i)
        day_start = datetime.combine(check_date, datetime.min.time())
        day_end = datetime.combine(check_date, datetime.max.time())
        
        has_progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.updated_at >= day_start,
            UserProgress.updated_at <= day_end
        ).first()
        
        if has_progress:
            streak += 1
        else:
            break
    
    return {
        "total_started": total_started,
        "total_completed": total_completed,
        "completion_rate": round(total_completed / total_started * 100, 2) if total_started > 0 else 0,
        "average_progress": round(avg_progress, 2),
        "total_time_seconds": total_time,
        "platform_breakdown": platform_stats,
        "learning_streak": streak,
        "last_activity": user_progress[0].updated_at.isoformat() if user_progress else None
    }


# ============== Assessment Endpoints ==============

@app.post("/api/v1/assessments", response_model=AssessmentResponse, tags=["Assessments"])
async def create_assessment(
    assessment_data: AssessmentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new assessment for content.
    """
    # Check if content exists
    content = db.query(Content).filter(Content.id == assessment_data.content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Check permission
    if content.creator_id != current_user["user_id"]:
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create assessments for this content"
            )
    
    assessment = Assessment(
        content_id=assessment_data.content_id,
        title=assessment_data.title,
        questions=[q.model_dump() for q in assessment_data.questions],
        passing_score=assessment_data.passing_score,
        time_limit_minutes=assessment_data.time_limit_minutes,
        difficulty_weight=assessment_data.difficulty_weight
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return AssessmentResponse(
        id=assessment.id,
        content_id=assessment.content_id,
        title=assessment.title,
        questions=assessment.questions,
        passing_score=assessment.passing_score,
        time_limit_minutes=assessment.time_limit_minutes,
        difficulty_weight=assessment.difficulty_weight,
        created_at=assessment.created_at
    )


@app.get("/api/v1/assessments/{content_id}", response_model=AssessmentResponse, tags=["Assessments"])
async def get_assessment(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get assessment for content (without correct answers).
    """
    assessment = db.query(Assessment).filter(
        Assessment.content_id == content_id
    ).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found for this content"
        )
    
    # Remove correct answers before sending to user
    questions_without_answers = []
    for q in assessment.questions:
        q_copy = q.copy()
        q_copy.pop("correct_answer", None)
        questions_without_answers.append(q_copy)
    
    return AssessmentResponse(
        id=assessment.id,
        content_id=assessment.content_id,
        title=assessment.title,
        questions=questions_without_answers,
        passing_score=assessment.passing_score,
        time_limit_minutes=assessment.time_limit_minutes,
        difficulty_weight=assessment.difficulty_weight,
        created_at=assessment.created_at
    )


@app.post("/api/v1/assessments/{assessment_id}/submit", response_model=AssessmentResultResponse, tags=["Assessments"])
async def submit_assessment(
    assessment_id: int,
    submission: AssessmentSubmission,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit assessment answers and get results.
    """
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Calculate score
    questions_dict = {i: q for i, q in enumerate(assessment.questions)}
    correct_count = 0
    total_questions = len(questions_dict)
    
    for q_idx, user_answer in submission.answers.items():
        if q_idx in questions_dict:
            correct_answer = questions_dict[q_idx].get("correct_answer", "")
            if user_answer.strip().lower() == correct_answer.strip().lower():
                correct_count += 1
    
    score = (correct_count / total_questions * 100) if total_questions > 0 else 0
    passed = score >= assessment.passing_score
    
    # Get previous attempts
    previous_attempts = db.query(AssessmentResult).filter(
        AssessmentResult.user_id == current_user["user_id"],
        AssessmentResult.assessment_id == assessment_id
    ).count()
    
    # Create result
    result = AssessmentResult(
        user_id=current_user["user_id"],
        assessment_id=assessment_id,
        score=score,
        passed=passed,
        answers=submission.answers,
        attempt_number=previous_attempts + 1
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    
    return AssessmentResultResponse(
        assessment_id=assessment_id,
        score=round(score, 2),
        passed=passed,
        correct_answers=correct_count,
        total_questions=total_questions,
        time_taken_seconds=0,  # Could be calculated from timestamps
        attempt_number=result.attempt_number,
        completed_at=result.completed_at
    )


# ============== Recommendation Endpoints ==============

@app.post("/api/v1/recommendations", response_model=RecommendationResponse, tags=["Recommendations"])
async def get_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized content recommendations for user.
    """
    user_id = current_user["user_id"]
    limit = request.limit or 10
    platform_filter = request.platform
    
    # Get user's completed content
    completed_content = db.query(UserProgress.content_id).filter(
        UserProgress.user_id == user_id,
        UserProgress.status == "completed"
    ).all()
    completed_ids = [c[0] for c in completed_content]
    
    # Get user's in-progress content
    in_progress = db.query(UserProgress.content_id).filter(
        UserProgress.user_id == user_id,
        UserProgress.status == "in_progress"
    ).all()
    in_progress_ids = [c[0] for c in in_progress]
    
    # Get concepts the user has engaged with
    user_concepts = db.query(ContentConcept.concept_id).filter(
        ContentConcept.content_id.in_(completed_ids + in_progress_ids)
    ).all()
    concept_ids = [c[0] for c in user_concepts]
    
    # Query for recommended content
    query = db.query(Content).filter(
        Content.status == "approved",
        Content.id.notin_(completed_ids)
    )
    
    if platform_filter:
        query = query.filter(Content.platform == platform_filter)
    
    # Filter out content that's already in progress
    if in_progress_ids:
        query = query.filter(Content.id.notin_(in_progress_ids))
    
    # Order by various factors
    recommended = query.order_by(
        Content.created_at.desc()
    ).limit(limit * 2).all()  # Get extra for diversity
    
    # If we have concept data, prioritize related content
    if concept_ids:
        concept_filter = db.query(ContentConcept.content_id).filter(
            ContentConcept.concept_id.in_(concept_ids)
        ).subquery()
        related = db.query(Content).filter(
            Content.id.in_(concept_filter),
            Content.status == "approved",
            Content.id.notin_(completed_ids),
            Content.id.notin_(in_progress_ids)
        )
        if platform_filter:
            related = related.filter(Content.platform == platform_filter)
        related = related.order_by(Content.created_at.desc()).limit(limit).all()
        
        # Merge results with priority to related content
        related_ids = set(c.id for c in related)
        other = [c for c in recommended if c.id not in related_ids]
        recommended = related + other[:limit - len(related)]
    else:
        recommended = recommended[:limit]
    
    # Build recommendations response
    recommendations = []
    for content in recommended:
        # Get concept info
        content_concepts = db.query(Concept).join(ContentConcept).filter(
            ContentConcept.content_id == content.id
        ).all()
        
        recommendations.append({
            "id": content.id,
            "title": content.title,
            "description": content.description,
            "platform": content.platform,
            "difficulty": content.difficulty.value,
            "thumbnail_url": content.thumbnail_url,
            "duration_seconds": content.duration_seconds,
            "concepts": [{"id": c.id, "name": c.name} for c in content_concepts],
            "reason": "based_on_your_progress" if content.id in [c[0] for c in in_progress] else "trending"
        })
    
    return RecommendationResponse(
        recommendations=recommendations,
        based_on="progress_and_similar_content",
        generated_at=datetime.utcnow()
    )


@app.get("/api/v1/recommendations/next-lesson", tags=["Recommendations"])
async def get_next_lesson(
    platform: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the next recommended lesson for the user.
    """
    user_id = current_user["user_id"]
    
    # Get in-progress content
    in_progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.status == "in_progress",
        UserProgress.progress_percentage < 100
    ).order_by(UserProgress.updated_at.asc()).first()
    
    if in_progress:
        content = db.query(Content).filter(Content.id == in_progress.content_id).first()
        if content:
            return {
                "type": "continue",
                "content": {
                    "id": content.id,
                    "title": content.title,
                    "platform": content.platform,
                    "progress": in_progress.progress_percentage
                },
                "message": "Continue where you left off"
            }
    
    # Get first incomplete lesson from popular content
    query = db.query(Content).filter(
        Content.status == "approved",
        Content.is_sample == True
    )
    
    if platform:
        query = query.filter(Content.platform == platform)
    
    # Exclude completed content
    completed = db.query(UserProgress.content_id).filter(
        UserProgress.user_id == user_id,
        UserProgress.status == "completed"
    ).all()
    completed_ids = [c[0] for c in completed]
    
    query = query.filter(Content.id.notin_(completed_ids))
    
    next_content = query.order_by(Content.created_at.desc()).first()
    
    if next_content:
        return {
            "type": "new",
            "content": {
                "id": next_content.id,
                "title": next_content.title,
                "platform": next_content.platform,
                "difficulty": next_content.difficulty.value
            },
            "message": "Start a new lesson"
        }
    
    return {
        "type": "none",
        "message": "All content completed! Check back for new lessons.",
        "content": None
    }


# ============== Learning Path Endpoints ==============

@app.get("/api/v1/learning-path/{concept_id}", tags=["Learning Path"])
async def get_learning_path(
    concept_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get recommended learning path for a concept.
    """
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concept not found"
        )
    
    # Get prerequisites
    prerequisites = []
    if concept.prerequisites:
        for prereq_id in concept.prerequisites:
            prereq = db.query(Concept).filter(Concept.id == prereq_id).first()
            if prereq:
                # Check if user has completed this prerequisite
                progress = db.query(UserProgress).filter(
                    UserProgress.user_id == current_user["user_id"],
                    UserProgress.concept_id == prereq_id,
                    UserProgress.status == "completed"
                ).first()
                
                prerequisites.append({
                    "id": prereq.id,
                    "name": prereq.name,
                    "completed": progress is not None
                })
    
    # Get content for this concept
    content = db.query(Content).join(ContentConcept).filter(
        ContentConcept.concept_id == concept_id,
        Content.status == "approved"
    ).all()
    
    content_list = []
    for c in content:
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user["user_id"],
            UserProgress.content_id == c.id
        ).first()
        
        content_list.append({
            "id": c.id,
            "title": c.title,
            "type": c.content_type.value,
            "duration": c.duration_seconds,
            "status": progress.status if progress else "not_started",
            "progress": progress.progress_percentage if progress else 0
        })
    
    return {
        "concept": {
            "id": concept.id,
            "name": concept.name,
            "description": concept.description,
            "difficulty": concept.difficulty.value,
            "estimated_duration": concept.estimated_duration
        },
        "prerequisites": prerequisites,
        "content": content_list,
        "estimated_total_duration": sum(
            (c.duration_seconds or 0) for c in content
        ) + (concept.estimated_duration or 0) * 60
    }


# ============== Health Check ==============

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for service monitoring.
    """
    return {"status": "healthy", "service": "lxp"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
