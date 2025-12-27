"""
Assessment Services Package.

Provides assessment creation, delivery, scoring, and analytics
for the VisualVerse Learner Experience Platform.
"""

from .assessment_service import (
    AssessmentService,
    Question,
    Answer,
    AssessmentConfig,
    AssessmentAttempt,
    AssessmentAnalytics,
    QuestionAnalytics,
    QuestionType,
    AssessmentType,
    Difficulty,
    AssessmentStatus,
    create_assessment_service
)

__all__ = [
    "AssessmentService",
    "Question",
    "Answer",
    "AssessmentConfig",
    "AssessmentAttempt",
    "AssessmentAnalytics",
    "QuestionAnalytics",
    "QuestionType",
    "AssessmentType",
    "Difficulty",
    "AssessmentStatus",
    "create_assessment_service"
]
