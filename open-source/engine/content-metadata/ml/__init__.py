"""
Machine Learning Module for Adaptive Learning

This module provides ML-driven adaptive sequencing capabilities for the VisualVerse
learning platform. It includes model interfaces, feature engineering, and the
orchestrating ML service for intelligent content recommendations.
"""

from .models.ml_models import (
    IMLModel,
    SequenceOptimizerModel,
    DifficultyPredictorModel,
    EngagementPredictorModel,
    LearningPathPredictorModel,
    ModelOutput,
    PredictionContext
)

__all__ = [
    'IMLModel',
    'SequenceOptimizerModel',
    'DifficultyPredictorModel',
    'EngagementPredictorModel',
    'LearningPathPredictorModel',
    'ModelOutput',
    'PredictionContext'
]
