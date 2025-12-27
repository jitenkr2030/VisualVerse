"""
Recommendation Services Package.

Provides personalized content recommendations, learning path generation,
and adaptive suggestions for the VisualVerse platform.
"""

from .recommendation_service import (
    RecommendationService,
    Recommendation,
    RecommendationSet,
    LearnerProfile,
    ContentFeatures,
    RecommendationType,
    create_recommendation_service
)

__all__ = [
    "RecommendationService",
    "Recommendation",
    "RecommendationSet",
    "LearnerProfile",
    "ContentFeatures",
    "RecommendationType",
    "create_recommendation_service"
]
