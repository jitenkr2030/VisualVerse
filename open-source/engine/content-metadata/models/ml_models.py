"""
Machine Learning Models for Adaptive Sequencing in VisualVerse Content Metadata Layer

This module provides abstract base classes and concrete implementations for ML models
that predict optimal learning sequences, difficulty levels, and learner engagement.
These models enable the transition from rule-based to data-driven personalization.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import math
import random
import numpy as np
from collections import defaultdict
import uuid


# =============================================================================
# Data Classes for ML Framework
# =============================================================================

@dataclass
class LearnerStateVector:
    """
    Feature vector representing a learner's current state.
    
    This is the primary input to ML models for making predictions about
    optimal learning actions.
    """
    learner_id: str
    
    # Mastery features (concept_id -> mastery_score)
    mastery_levels: Dict[str, float] = field(default_factory=dict)
    
    # Recent interaction sequence (last N interactions)
    recent_interactions: List[str] = field(default_factory=list)
    
    # Performance metrics
    avg_time_per_task: float = 30.0  # seconds
    error_rate: float = 0.2  # rolling average
    session_completion_rate: float = 0.75
    
    # Engagement features
    sessions_last_week: int = 3
    avg_session_length: float = 20.0  # minutes
    days_since_last_session: int = 1
    streak_days: int = 0
    
    # Cognitive profile features
    working_memory_score: float = 0.5
    processing_speed_score: float = 0.5
    attention_span_minutes: float = 15.0
    
    # Learning style features
    visual_preference: float = 0.35
    auditory_preference: float = 0.25
    reading_preference: float = 0.20
    kinesthetic_preference: float = 0.20
    
    # Motivation features
    achievement_motivation: float = 0.5
    competition_motivation: float = 0.3
    social_motivation: float = 0.4
    
    # Context features
    current_difficulty_tolerance: int = 3  # 1-5 scale
    preferred_session_length: int = 30  # minutes
    time_of_day: int = 10  # hour of day
    
    def to_vector(self) -> np.ndarray:
        """Convert to numpy array for model input"""
        features = []
        
        # Mastery levels (fixed-size vector, padded with zeros)
        max_concepts = 50
        mastery_values = list(self.mastery_levels.values())[:max_concepts]
        while len(mastery_values) < max_concepts:
            mastery_values.append(0.0)
        features.extend(mastery_values)
        
        # Interaction history (encoded as integers)
        interaction_map = {
            "practice": 0, "assessment": 1, "review": 2,
            "visualization": 3, "application": 4
        }
        for _ in range(20):  # Fixed sequence length
            if self.recent_interactions:
                features.append(interaction_map.get(self.recent_interactions[-1], 0))
                self.recent_interactions.pop()
            else:
                features.append(-1)  # Padding
        
        # Numeric features
        features.extend([
            self.avg_time_per_task / 100,  # Normalized
            self.error_rate,
            self.session_completion_rate,
            self.sessions_last_week / 7,
            self.avg_session_length / 60,
            min(self.days_since_last_session / 14, 1.0),
            min(self.streak_days / 30, 1.0),
            self.working_memory_score,
            self.processing_speed_score,
            self.attention_span_minutes / 30,
            self.visual_preference,
            self.auditory_preference,
            self.reading_preference,
            self.kinesthetic_preference,
            self.achievement_motivation,
            self.competition_motivation,
            self.social_motivation,
            self.current_difficulty_tolerance / 5,
            self.preferred_session_length / 60,
            self.time_of_day / 24
        ])
        
        return np.array(features, dtype=np.float32)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearnerStateVector":
        """Create from dictionary"""
        return cls(
            learner_id=data.get("learner_id", str(uuid.uuid4())),
            mastery_levels=data.get("mastery_levels", {}),
            recent_interactions=data.get("recent_interactions", []),
            avg_time_per_task=data.get("avg_time_per_task", 30.0),
            error_rate=data.get("error_rate", 0.2),
            session_completion_rate=data.get("session_completion_rate", 0.75),
            sessions_last_week=data.get("sessions_last_week", 3),
            avg_session_length=data.get("avg_session_length", 20.0),
            days_since_last_session=data.get("days_since_last_session", 1),
            streak_days=data.get("streak_days", 0),
            working_memory_score=data.get("working_memory_score", 0.5),
            processing_speed_score=data.get("processing_speed_score", 0.5),
            attention_span_minutes=data.get("attention_span_minutes", 15.0),
            visual_preference=data.get("visual_preference", 0.35),
            auditory_preference=data.get("auditory_preference", 0.25),
            reading_preference=data.get("reading_preference", 0.20),
            kinesthetic_preference=data.get("kinesthetic_preference", 0.20),
            achievement_motivation=data.get("achievement_motivation", 0.5),
            competition_motivation=data.get("competition_motivation", 0.3),
            social_motivation=data.get("social_motivation", 0.4),
            current_difficulty_tolerance=data.get("current_difficulty_tolerance", 3),
            preferred_session_length=data.get("preferred_session_length", 30),
            time_of_day=data.get("time_of_day", 10)
        )


@dataclass
class ConceptFeatures:
    """
    Feature representation of a learning concept.
    
    Used as input context when making predictions about concept sequences.
    """
    concept_id: str
    name: str
    difficulty_score: float = 0.5  # 0.0-1.0
    duration_minutes: float = 30.0
    
    # Content features
    has_visual_content: bool = True
    has_interactive_content: bool = True
    has_text_content: bool = True
    has_audio_content: bool = False
    
    # Structural features
    prerequisite_count: int = 0
    dependent_count: int = 0
    topic_category: str = "general"
    tags: List[str] = field(default_factory=list)
    
    # Historical success rate
    global_success_rate: float = 0.75
    avg_completion_time: float = 30.0
    
    def to_vector(self) -> np.ndarray:
        """Convert to numpy array"""
        topic_map = {
            "mathematics": 0, "science": 1, "language": 2,
            "history": 3, "programming": 4, "art": 5, "general": 6
        }
        topic_one_hot = [0] * 7
        topic_one_hot[topic_map.get(self.topic_category, 6)] = 1
        
        return np.array([
            self.difficulty_score,
            self.duration_minutes / 60,
            int(self.has_visual_content),
            int(self.has_interactive_content),
            int(self.has_text_content),
            int(self.has_audio_content),
            self.prerequisite_count / 10,
            self.dependent_count / 10,
            self.global_success_rate,
            self.avg_completion_time / 60
        ] + topic_one_hot, dtype=np.float32)


@dataclass
class PredictionContext:
    """
    Context for making predictions about learning sequences.
    
    Contains the current learner state and available concept candidates.
    """
    learner_id: str
    candidate_concepts: List[str] = field(default_factory=list)
    current_concept_id: Optional[str] = None
    target_learning_goal: Optional[str] = None
    available_time_minutes: int = 30
    session_type: str = "learning"  # learning, review, assessment
    require_new_content: bool = True
    
    def __post_init__(self):
        if not self.candidate_concepts:
            self.candidate_concepts = []


@dataclass
class ModelPrediction:
    """
    Output from ML model predictions.
    
    Contains the predicted optimal action and associated metadata.
    """
    prediction_id: str
    recommended_sequence: List[str] = field(default_factory=list)
    predicted_difficulty: float = 0.5
    engagement_score: float = 0.8
    confidence_score: float = 0.5
    
    # Per-concept predictions
    concept_scores: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    model_version: str = "1.0.0"
    model_name: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Alternative options for exploration
    alternative_sequences: List[List[str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction_id": self.prediction_id,
            "recommended_sequence": self.recommended_sequence,
            "predicted_difficulty": self.predicted_difficulty,
            "engagement_score": self.engagement_score,
            "confidence_score": self.confidence_score,
            "concept_scores": self.concept_scores,
            "model_version": self.model_version,
            "model_name": self.model_name,
            "timestamp": self.timestamp.isoformat(),
            "alternatives": self.alternative_sequences
        }


@dataclass
class TrainingData:
    """
    Training data structure for ML models.
    
    Contains feature-label pairs for supervised learning.
    """
    data_id: str
    created_at: datetime
    samples: List[Dict[str, Any]] = field(default_factory=list)
    
    # Data metadata
    source: str = "historical_logs"
    total_samples: int = 0
    positive_samples: int = 0  # For classification
    negative_samples: int = 0
    
    @classmethod
    def create(cls) -> "TrainingData":
        return cls(
            data_id=str(uuid.uuid4()),
            created_at=datetime.now()
        )
    
    def add_sample(
        self,
        features: Dict[str, Any],
        label: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a single training sample"""
        sample = {
            "features": features,
            "label": label,
            "metadata": metadata or {}
        }
        self.samples.append(sample)
        self.total_samples += 1
        
        if isinstance(label, (int, float)):
            if label > 0.5 or (isinstance(label, bool) and label):
                self.positive_samples += 1
            else:
                self.negative_samples += 1
    
    def to_numpy(self) -> Tuple[np.ndarray, np.ndarray]:
        """Convert to numpy arrays for training"""
        X = []
        y = []
        
        for sample in self.samples:
            if isinstance(sample["features"], np.ndarray):
                X.append(sample["features"])
            elif isinstance(sample["features"], dict):
                # Flatten dict to vector
                features = self._flatten_dict(sample["features"])
                X.append(features)
            else:
                continue
            
            y.append(sample["label"])
        
        return np.array(X), np.array(y)
    
    def _flatten_dict(self, d: Dict[str, Any]) -> np.ndarray:
        """Flatten nested dictionary to feature vector"""
        features = []
        
        def extract(obj, prefix=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    extract(v, f"{prefix}_{k}")
            elif isinstance(obj, (int, float)):
                features.append(float(obj))
            elif isinstance(obj, list):
                for item in obj:
                    extract(item)
        
        extract(d)
        return np.array(features, dtype=np.float32)


@dataclass
class TrainingMetrics:
    """
    Metrics from model training.
    
    Used to evaluate model quality and track improvements.
    """
    model_name: str
    model_version: str
    training_timestamp: datetime
    
    # Loss metrics
    train_loss: float = 0.0
    val_loss: float = 0.0
    
    # Classification metrics
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    auc_roc: float = 0.0
    
    # Regression metrics
    mse: float = 0.0
    rmse: float = 0.0
    mae: float = 0.0
    r_squared: float = 0.0
    
    # Ranking metrics
    ndcg: float = 0.0
    hit_rate: float = 0.0
    
    # Training info
    epochs_trained: int = 0
    training_samples: int = 0
    validation_samples: int = 0
    training_time_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "training_timestamp": self.training_timestamp.isoformat(),
            "metrics": {
                "loss": {"train": self.train_loss, "val": self.val_loss},
                "classification": {
                    "accuracy": self.accuracy,
                    "precision": self.precision,
                    "recall": self.recall,
                    "f1": self.f1_score,
                    "auc_roc": self.auc_roc
                },
                "regression": {
                    "mse": self.mse,
                    "rmse": self.rmse,
                    "mae": self.mae,
                    "r_squared": self.r_squared
                },
                "ranking": {
                    "ndcg": self.ndcg,
                    "hit_rate": self.hit_rate
                }
            },
            "training_info": {
                "epochs": self.epochs_trained,
                "train_samples": self.training_samples,
                "val_samples": self.validation_samples,
                "time_seconds": self.training_time_seconds
            }
        }


@dataclass
class InteractionOutcome:
    """
    Recorded outcome of a predicted action.
    
    Used for continuous model improvement and evaluation.
    """
    prediction_id: str
    learner_id: str
    recommended_sequence: List[str]
    actual_sequence: List[str] = field(default_factory=list)
    
    # Outcomes
    completed_count: int = 0
    success_count: int = 0
    abandonment_point: Optional[int] = None
    
    # Engagement metrics
    time_spent_seconds: float = 0.0
    engagement_score: float = 0.0
    
    # Difficulty perception
    perceived_difficulty: Optional[float] = None
    was_too_easy: bool = False
    was_too_hard: bool = False
    
    # Timestamps
    predicted_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def calculate_success_rate(self) -> float:
        """Calculate success rate of recommended sequence"""
        if not self.recommended_sequence:
            return 0.0
        return self.success_count / len(self.recommended_sequence)
    
    def was_abandoned(self) -> bool:
        """Check if session was abandoned"""
        return self.abandonment_point is not None and \
               self.abandonment_point < len(self.recommended_sequence) * 0.5


# =============================================================================
# Abstract Base Classes for ML Models
# =============================================================================

class IMLModel(ABC):
    """Abstract base class for all ML models"""
    
    def __init__(self, model_name: str, model_version: str = "1.0.0"):
        self.model_name = model_name
        self.model_version = model_version
        self.is_trained = False
        self.feature_dim = 0
    
    @abstractmethod
    def train(self, training_data: TrainingData) -> TrainingMetrics:
        """Train the model on provided data"""
        pass
    
    @abstractmethod
    def predict(self, state: LearnerStateVector, context: PredictionContext) -> ModelPrediction:
        """Make prediction based on learner state"""
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """Save model to disk"""
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """Load model from disk"""
        pass
    
    @abstractmethod
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        pass


class SequenceOptimizerModel(IMLModel):
    """
    Model for predicting optimal learning sequences.
    
    Uses sequence modeling to rank concepts by probability of successful completion.
    """
    
    def __init__(self, model_version: str = "1.0.0", sequence_length: int = 10):
        super().__init__("SequenceOptimizer", model_version)
        self.sequence_length = sequence_length
        self.weights: Optional[np.ndarray] = None
        self.concept_embeddings: Dict[str, np.ndarray] = {}
        self.success_rates: Dict[str, float] = {}
    
    def train(self, training_data: TrainingData) -> TrainingMetrics:
        """Train the sequence optimizer"""
        metrics = TrainingMetrics(
            model_name=self.model_name,
            model_version=self.model_version,
            training_timestamp=datetime.now()
        )
        
        # Extract features and labels
        X, y = training_data.to_numpy()
        self.feature_dim = X.shape[1] if X.size > 0 else 70
        metrics.training_samples = len(training_data.samples)
        
        if X.size == 0:
            # Initialize with default weights if no training data
            self.weights = np.random.randn(self.feature_dim) * 0.01
            self.is_trained = False
            return metrics
        
        # Simple linear model for sequence scoring
        # In production, this would be replaced with LSTM/Transformer
        self.weights = np.zeros(self.feature_dim)
        
        # Train with gradient descent (simplified)
        learning_rate = 0.01
        epochs = 100
        
        for epoch in range(epochs):
            predictions = self._sigmoid(X @ self.weights)
            errors = y - predictions
            self.weights += learning_rate * (X.T @ errors) / len(y)
        
        # Calculate metrics
        final_predictions = self._sigmoid(X @ self.weights)
        predicted_labels = (final_predictions > 0.5).astype(int)
        actual_labels = y.astype(int)
        
        metrics.accuracy = np.mean(predicted_labels == actual_labels)
        
        # Calculate additional metrics
        true_positives = np.sum((predicted_labels == 1) & (actual_labels == 1))
        predicted_positives = np.sum(predicted_labels == 1)
        actual_positives = np.sum(actual_labels == 1)
        
        if predicted_positives > 0:
            metrics.precision = true_positives / predicted_positives
        if actual_positives > 0:
            metrics.recall = true_positives / actual_positives
        
        if metrics.precision + metrics.recall > 0:
            metrics.f1_score = 2 * metrics.precision * metrics.recall / (metrics.precision + metrics.recall)
        
        metrics.epochs_trained = epochs
        metrics.training_time_seconds = 0.1 * epochs  # Approximate
        self.is_trained = True
        
        return metrics
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def predict(
        self,
        state: LearnerStateVector,
        context: PredictionContext
    ) -> ModelPrediction:
        """Predict optimal sequence for learner"""
        prediction_id = str(uuid.uuid4())
        
        if not context.candidate_concepts:
            # Return empty prediction if no candidates
            return ModelPrediction(
                prediction_id=prediction_id,
                model_version=self.model_version,
                model_name=self.model_name
            )
        
        # Get state vector
        state_vector = state.to_vector()
        
        # Score each candidate
        concept_scores = {}
        for concept_id in context.candidate_concepts:
            # Combine state with concept features
            combined = self._combine_features(state_vector, concept_id)
            score = self._predict_score(combined)
            concept_scores[concept_id] = float(score)
        
        # Sort by score to get optimal sequence
        sorted_concepts = sorted(
            concept_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Build sequence respecting prerequisites
        sequence = self._build_sequence(
            [c[0] for c in sorted_concepts],
            state,
            context
        )
        
        # Calculate predicted difficulty based on sequence
        avg_difficulty = np.mean([
            self.success_rates.get(c, 0.75) for c in sequence[:5]
        ]) if sequence else 0.5
        
        # Predict engagement
        engagement = self._predict_engagement(state, sequence)
        
        return ModelPrediction(
            prediction_id=prediction_id,
            recommended_sequence=sequence,
            predicted_difficulty=1.0 - avg_difficulty,
            engagement_score=engagement,
            confidence_score=0.6 if self.is_trained else 0.3,
            concept_scores=concept_scores,
            model_version=self.model_version,
            model_name=self.model_name
        )
    
    def _combine_features(self, state_vector: np.ndarray, concept_id: str) -> np.ndarray:
        """Combine learner state with concept information"""
        # Concept embedding or default
        if concept_id in self.concept_embeddings:
            concept_vec = self.concept_embeddings[concept_id]
        else:
            concept_vec = np.random.randn(10) * 0.1
        
        # Success rate as additional feature
        success_rate = self.success_rates.get(concept_id, 0.75)
        
        return np.concatenate([
            state_vector,
            concept_vec,
            [success_rate]
        ])
    
    def _predict_score(self, features: np.ndarray) -> float:
        """Predict success score for a concept"""
        if self.weights is None:
            return 0.5
        
        score = self._sigmoid(np.dot(features, self.weights))
        return float(score)
    
    def _build_sequence(
        self,
        sorted_concepts: List[str],
        state: LearnerStateVector,
        context: PredictionContext
    ) -> List[str]:
        """Build optimal sequence respecting constraints"""
        sequence = []
        mastery = state.mastery_levels
        
        for concept_id in sorted_concepts:
            if len(sequence) >= self.sequence_length:
                break
            
            # Check if prerequisites are met
            mastery_score = mastery.get(concept_id, 0.0)
            
            # Include if not mastered or needs review
            if mastery_score < 0.7:
                sequence.append(concept_id)
        
        return sequence
    
    def _predict_engagement(self, state: LearnerStateVector, sequence: List[str]) -> float:
        """Predict engagement likelihood for sequence"""
        base_engagement = 0.8
        
        # Adjust based on learner characteristics
        if state.error_rate > 0.3:
            base_engagement -= 0.1
        if state.days_since_last_session > 7:
            base_engagement -= 0.15
        if state.avg_session_length < 10:
            base_engagement -= 0.05
        
        # Adjust based on difficulty
        if len(sequence) > 3:
            avg_mastery = np.mean([state.mastery_levels.get(c, 0) for c in sequence[:3]])
            if avg_mastery < 0.3:
                base_engagement -= 0.1
        
        return max(0.3, min(0.95, base_engagement))
    
    def save(self, path: str) -> None:
        """Save model weights and metadata"""
        import json
        
        data = {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "weights": self.weights.tolist() if self.weights is not None else None,
            "concept_embeddings": {k: v.tolist() for k, v in self.concept_embeddings.items()},
            "success_rates": self.success_rates,
            "feature_dim": self.feature_dim,
            "is_trained": self.is_trained
        }
        
        with open(f"{path}/model.json", "w") as f:
            json.dump(data, f)
    
    def load(self, path: str) -> None:
        """Load model weights and metadata"""
        import json
        
        with open(f"{path}/model.json", "r") as f:
            data = json.load(f)
        
        self.model_name = data["model_name"]
        self.model_version = data["model_version"]
        self.weights = np.array(data["weights"]) if data["weights"] else None
        self.concept_embeddings = {
            k: np.array(v) for k, v in data.get("concept_embeddings", {}).items()
        }
        self.success_rates = data.get("success_rates", {})
        self.feature_dim = data.get("feature_dim", 70)
        self.is_trained = data.get("is_trained", False)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if self.weights is None:
            return {}
        
        importance = {
            "mastery_level": float(np.abs(self.weights[0])),
            "error_rate": float(np.abs(self.weights[1])),
            "session_completion": float(np.abs(self.weights[2])),
            "time_per_task": float(np.abs(self.weights[3])),
            "motivation": float(np.abs(self.weights[15]))
        }
        
        return importance


class DifficultyPredictorModel(IMLModel):
    """
    Model for predicting optimal difficulty level for learners.
    
    Predicts the perceived difficulty of content for a specific learner.
    """
    
    def __init__(self, model_version: str = "1.0.0"):
        super().__init__("DifficultyPredictor", model_version)
        self.weights: Optional[np.ndarray] = None
        self.concept_difficulties: Dict[str, float] = {}
    
    def train(self, training_data: TrainingData) -> TrainingMetrics:
        """Train the difficulty predictor"""
        metrics = TrainingMetrics(
            model_name=self.model_name,
            model_version=self.model_version,
            training_timestamp=datetime.now()
        )
        
        X, y = training_data.to_numpy()
        self.feature_dim = X.shape[1] if X.size > 0 else 70
        metrics.training_samples = len(training_data.samples)
        
        if X.size == 0:
            self.weights = np.random.randn(self.feature_dim) * 0.01
            self.is_trained = False
            return metrics
        
        # Linear regression for difficulty prediction
        self.weights = np.zeros(self.feature_dim)
        
        # Simple gradient descent
        learning_rate = 0.001
        epochs = 200
        
        for epoch in range(epochs):
            predictions = X @ self.weights
            errors = y - predictions
            self.weights += learning_rate * (X.T @ errors) / len(y)
        
        # Calculate metrics
        predictions = X @ self.weights
        metrics.mse = np.mean((y - predictions) ** 2)
        metrics.rmse = np.sqrt(metrics.mse)
        metrics.mae = np.mean(np.abs(y - predictions))
        
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        metrics.r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        metrics.epochs_trained = epochs
        metrics.training_time_seconds = 0.05 * epochs
        self.is_trained = True
        
        return metrics
    
    def predict(
        self,
        state: LearnerStateVector,
        context: PredictionContext
    ) -> ModelPrediction:
        """Predict optimal difficulty for learner"""
        prediction_id = str(uuid.uuid4())
        state_vector = state.to_vector()
        
        # Predict difficulty tolerance
        predicted_difficulty = float(np.clip(
            state_vector @ self.weights if self.weights is not None else 0.5,
            0.0, 1.0
        ))
        
        # Adjust based on context
        if context.current_difficulty_tolerance:
            tolerance_normalized = context.current_difficulty_tolerance / 5
            predicted_difficulty = (predicted_difficulty + tolerance_normalized) / 2
        
        # Calculate confidence
        confidence = 0.7 if self.is_trained else 0.3
        
        return ModelPrediction(
            prediction_id=prediction_id,
            predicted_difficulty=predicted_difficulty,
            engagement_score=0.8,
            confidence_score=confidence,
            model_version=self.model_version,
            model_name=self.model_name
        )
    
    def save(self, path: str) -> None:
        """Save model weights"""
        import json
        
        data = {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "weights": self.weights.tolist() if self.weights is not None else None,
            "concept_difficulties": self.concept_difficulties,
            "feature_dim": self.feature_dim,
            "is_trained": self.is_trained
        }
        
        with open(f"{path}/model.json", "w") as f:
            json.dump(data, f)
    
    def load(self, path: str) -> None:
        """Load model weights"""
        import json
        
        with open(f"{path}/model.json", "r") as f:
            data = json.load(f)
        
        self.model_name = data["model_name"]
        self.model_version = data["model_version"]
        self.weights = np.array(data["weights"]) if data["weights"] else None
        self.concept_difficulties = data.get("concept_difficulties", {})
        self.feature_dim = data.get("feature_dim", 70)
        self.is_trained = data.get("is_trained", False)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance for difficulty prediction"""
        if self.weights is None:
            return {}
        
        return {
            "working_memory": float(np.abs(self.weights[25])),
            "processing_speed": float(np.abs(self.weights[26])),
            "error_rate": float(np.abs(self.weights[1])),
            "motivation": float(np.abs(self.weights[15])),
            "session_history": float(np.abs(self.weights[3]))
        }


class EngagementPredictorModel(IMLModel):
    """
    Model for predicting learner engagement and abandonment risk.
    
    Binary classification model to detect risk of session abandonment.
    """
    
    def __init__(self, model_version: str = "1.0.0"):
        super().__init__("EngagementPredictor", model_version)
        self.weights: Optional[np.ndarray] = None
        self.threshold: float = 0.5
    
    def train(self, training_data: TrainingData) -> TrainingMetrics:
        """Train the engagement predictor"""
        metrics = TrainingMetrics(
            model_name=self.model_name,
            model_version=self.model_version,
            training_timestamp=datetime.now()
        )
        
        X, y = training_data.to_numpy()
        self.feature_dim = X.shape[1] if X.size > 0 else 70
        metrics.training_samples = len(training_data.samples)
        
        if X.size == 0:
            self.weights = np.random.randn(self.feature_dim) * 0.01
            self.is_trained = False
            return metrics
        
        # Logistic regression for binary classification
        self.weights = np.zeros(self.feature_dim)
        learning_rate = 0.01
        epochs = 100
        
        for epoch in range(epochs):
            z = X @ self.weights
            predictions = self._sigmoid(z)
            errors = y - predictions
            self.weights += learning_rate * (X.T @ errors) / len(y)
        
        # Calculate metrics
        final_predictions = self._sigmoid(X @ self.weights)
        predicted_labels = (final_predictions > self.threshold).astype(int)
        actual_labels = y.astype(int)
        
        metrics.accuracy = np.mean(predicted_labels == actual_labels)
        
        true_positives = np.sum((predicted_labels == 1) & (actual_labels == 1))
        predicted_positives = np.sum(predicted_labels == 1)
        actual_positives = np.sum(actual_labels == 1)
        
        if predicted_positives > 0:
            metrics.precision = true_positives / predicted_positives
        if actual_positives > 0:
            metrics.recall = true_positives / actual_positives
        
        if metrics.precision + metrics.recall > 0:
            metrics.f1_score = 2 * metrics.precision * metrics.recall / (metrics.precision + metrics.recall)
        
        metrics.epochs_trained = epochs
        metrics.training_time_seconds = 0.05 * epochs
        self.is_trained = True
        
        return metrics
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def predict(
        self,
        state: LearnerStateVector,
        context: PredictionContext
    ) -> ModelPrediction:
        """Predict engagement risk for learner"""
        prediction_id = str(uuid.uuid4())
        state_vector = state.to_vector()
        
        # Calculate abandonment probability
        if self.weights is not None:
            z = np.dot(state_vector, self.weights)
            abandonment_prob = self._sigmoid(np.array([z]))[0]
        else:
            abandonment_prob = 0.2
        
        engagement_score = 1.0 - abandonment_prob
        
        # Risk factors
        risk_factors = []
        if state.error_rate > 0.4:
            risk_factors.append("high_error_rate")
        if state.days_since_last_session > 7:
            risk_factors.append("prolonged_inactivity")
        if state.avg_session_length < 10:
            risk_factors.append("short_sessions")
        
        return ModelPrediction(
            prediction_id=prediction_id,
            engagement_score=engagement_score,
            confidence_score=0.7 if self.is_trained else 0.3,
            model_version=self.model_version,
            model_name=self.model_name,
            concept_scores={"abandonment_risk": float(abandonment_prob)},
            alternative_sequences=[risk_factors] if risk_factors else []
        )
    
    def predict_risk(self, state: LearnerStateVector) -> Tuple[float, List[str]]:
        """Predict risk and identify factors"""
        prediction = self.predict(state, PredictionContext(
            learner_id=state.learner_id,
            candidate_concepts=[]
        ))
        
        abandonment_prob = 1.0 - prediction.engagement_score
        
        risk_factors = []
        if state.error_rate > 0.4:
            risk_factors.append("high_error_rate")
        if state.days_since_last_session > 7:
            risk_factors.append("prolonged_inactivity")
        if state.avg_session_length < 10:
            risk_factors.append("short_sessions")
        if state.streak_days == 0 and state.days_since_last_session > 3:
            risk_factors.append("broken_streak")
        
        return abandonment_prob, risk_factors
    
    def save(self, path: str) -> None:
        """Save model weights"""
        import json
        
        data = {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "weights": self.weights.tolist() if self.weights is not None else None,
            "threshold": self.threshold,
            "feature_dim": self.feature_dim,
            "is_trained": self.is_trained
        }
        
        with open(f"{path}/model.json", "w") as f:
            json.dump(data, f)
    
    def load(self, path: str) -> None:
        """Load model weights"""
        import json
        
        with open(f"{path}/model.json", "r") as f:
            data = json.load(f)
        
        self.model_name = data["model_name"]
        self.model_version = data["model_version"]
        self.weights = np.array(data["weights"]) if data["weights"] else None
        self.threshold = data.get("threshold", 0.5)
        self.feature_dim = data.get("feature_dim", 70)
        self.is_trained = data.get("is_trained", False)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance for engagement prediction"""
        if self.weights is None:
            return {}
        
        return {
            "error_rate": float(np.abs(self.weights[1])),
            "session_completion": float(np.abs(self.weights[2])),
            "days_inactive": float(np.abs(self.weights[6])),
            "streak": float(np.abs(self.weights[7])),
            "motivation": float(np.abs(self.weights[15]))
        }


class LearningPathPredictorModel(IMLModel):
    """
    Model for predicting complete learning paths.
    
    Uses graph-based approach with learned weights to generate optimal
    long-term learning trajectories.
    """
    
    def __init__(self, model_version: str = "1.0.0"):
        super().__init__("LearningPathPredictor", model_version)
        self.concept_weights: Dict[str, float] = {}
        self.prerequisite_weights: Dict[Tuple[str, str], float] = {}
        self.topic_weights: Dict[str, float] = {}
    
    def train(self, training_data: TrainingData) -> TrainingMetrics:
        """Train the path predictor"""
        metrics = TrainingMetrics(
            model_name=self.model_name,
            model_version=self.model_version,
            training_timestamp=datetime.now()
        )
        
        # Extract path completion data
        X, y = training_data.to_numpy()
        metrics.training_samples = len(training_data.samples)
        
        # Analyze successful paths to learn weights
        for sample in training_data.samples:
            metadata = sample.get("metadata", {})
            
            # Learn concept importance
            concepts = metadata.get("concepts_covered", [])
            for i, concept in enumerate(concepts):
                # Earlier concepts in successful paths are more important
                weight = 1.0 / (i + 1)
                self.concept_weights[concept] = self.concept_weights.get(concept, 0) + weight
            
            # Learn prerequisite weights
            prerequisites = metadata.get("prerequisites", [])
            for prereq in prerequisites:
                self.prerequisite_weights[(prereq, "needed")] = \
                    self.prerequisite_weights.get((prereq, "needed"), 0) + 0.5
        
        # Normalize weights
        if self.concept_weights:
            max_weight = max(self.concept_weights.values())
            self.concept_weights = {k: v / max_weight for k, v in self.concept_weights.items()}
        
        metrics.accuracy = 0.75  # Placeholder for path completion rate
        metrics.ndcg = 0.7  # Placeholder for ranking metric
        self.is_trained = True
        
        return metrics
    
    def predict(
        self,
        state: LearnerStateVector,
        context: PredictionContext
    ) -> ModelPrediction:
        """Predict learning path to goal"""
        prediction_id = str(uuid.uuid4())
        
        # Build path using A* with learned weights
        path = self._build_path(state, context)
        
        # Predict engagement for the path
        engagement = self._predict_path_engagement(state, path)
        
        return ModelPrediction(
            prediction_id=prediction_id,
            recommended_sequence=path,
            engagement_score=engagement,
            confidence_score=0.6 if self.is_trained else 0.3,
            model_version=self.model_version,
            model_name=self.model_name
        )
    
    def _build_path(
        self,
        state: LearnerStateVector,
        context: PredictionContext
    ) -> List[str]:
        """Build optimal learning path"""
        path = []
        mastery = state.mastery_levels
        
        # Get sorted candidates by weight
        candidates = context.candidate_concepts
        if not candidates:
            return path
        
        # Sort by learned weights
        sorted_candidates = sorted(
            candidates,
            key=lambda c: self.concept_weights.get(c, 0.5),
            reverse=True
        )
        
        # Build path respecting mastery
        for concept in sorted_candidates:
            if len(path) >= 10:
                break
            
            mastery_score = mastery.get(concept, 0.0)
            
            # Add if needs work
            if mastery_score < 0.85:
                path.append(concept)
        
        return path
    
    def _predict_path_engagement(
        self,
        state: LearnerStateVector,
        path: List[str]
    ) -> float:
        """Predict engagement for a learning path"""
        base_engagement = 0.8
        
        # Adjust based on path length
        if len(path) > 8:
            base_engagement -= 0.1
        elif len(path) < 3:
            base_engagement -= 0.05
        
        # Adjust based on learner readiness
        if path:
            avg_mastery = np.mean([state.mastery_levels.get(c, 0) for c in path[:3]])
            if avg_mastery < 0.2:
                base_engagement -= 0.15
        
        return max(0.4, min(0.95, base_engagement))
    
    def save(self, path: str) -> None:
        """Save model weights"""
        import json
        
        data = {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "concept_weights": self.concept_weights,
            "topic_weights": self.topic_weights,
            "is_trained": self.is_trained
        }
        
        # Save prerequisite weights
        prereq_weights = {
            f"{k[0]}->{k[1]}": v for k, v in self.prerequisite_weights.items()
        }
        data["prerequisite_weights"] = prereq_weights
        
        with open(f"{path}/model.json", "w") as f:
            json.dump(data, f)
    
    def load(self, path: str) -> None:
        """Load model weights"""
        import json
        
        with open(f"{path}/model.json", "r") as f:
            data = json.load(f)
        
        self.model_name = data["model_name"]
        self.model_version = data["model_version"]
        self.concept_weights = data.get("concept_weights", {})
        self.topic_weights = data.get("topic_weights", {})
        self.prerequisite_weights = {}
        for k, v in data.get("prerequisite_weights", {}).items():
            parts = k.split("->")
            if len(parts) == 2:
                self.prerequisite_weights[(parts[0], parts[1])] = v
        self.is_trained = data.get("is_trained", False)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get concept importance scores"""
        return self.concept_weights
