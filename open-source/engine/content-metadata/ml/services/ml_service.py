"""
ML Service Orchestrator

This module provides the MLService class that orchestrates all machine learning
models in the adaptive learning system. It handles model lifecycle management,
prediction requests, and serves as the primary interface between the application
and the ML layer.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging

from ..models.ml_models import (
    IMLModel,
    SequenceOptimizerModel,
    DifficultyPredictorModel,
    EngagementPredictorModel,
    LearningPathPredictorModel,
    ModelOutput,
    PredictionContext
)

logger = logging.getLogger(__name__)


class MLService:
    """
    Orchestrator for all ML models in the adaptive learning system.
    
    The MLService is responsible for:
    - Managing the lifecycle of all ML models (loading, initialization, saving)
    - Coordinating predictions across multiple models
    - Providing a unified interface for adaptive sequencing requests
    - Handling model versioning and hot-swapping for A/B testing
    
    Attributes:
        models (Dict[str, IMLModel]): Dictionary of loaded ML models
        model_versions (Dict[str, str]): Version information for each model
        is_initialized (bool): Whether all models have been loaded
    """
    
    def __init__(self):
        """Initialize the ML service with empty model registry."""
        self.models: Dict[str, IMLModel] = {}
        self.model_versions: Dict[str, str] = {}
        self.is_initialized: bool = False
        self._model_registry = self._initialize_model_registry()
    
    def _initialize_model_registry(self) -> Dict[str, type]:
        """
        Initialize the registry of available model types.
        
        Returns:
            Dictionary mapping model names to their class types
        """
        return {
            'sequence_optimizer': SequenceOptimizerModel,
            'difficulty_predictor': DifficultyPredictorModel,
            'engagement_predictor': EngagementPredictorModel,
            'learning_path_predictor': LearningPathPredictorModel
        }
    
    def initialize_models(self, model_config: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """
        Initialize all ML models from the registry.
        
        This method loads all registered models into memory. For production
        environments, models would be loaded from trained weights files.
        Currently, it initializes dummy models for demonstration purposes.
        
        Args:
            model_config: Optional configuration dictionary for model initialization.
                         Can include model paths, hyperparameters, or toggle
                         specific models on/off.
        
        Returns:
            Dictionary mapping model names to initialization success status
        """
        if model_config is None:
            model_config = {}
        
        initialization_results = {}
        
        for model_name, model_class in self._model_registry.items():
            try:
                # Check if model is disabled in config
                if model_config.get(f'disable_{model_name}', False):
                    logger.info(f"Model {model_name} is disabled in configuration")
                    initialization_results[model_name] = False
                    continue
                
                # Initialize the model with config if provided
                model_kwargs = model_config.get(model_name, {})
                model = model_class(**model_kwargs)
                
                # Store model and version
                self.models[model_name] = model
                self.model_versions[model_name] = model.model_version
                
                logger.info(f"Successfully initialized {model_name} (version: {model.model_version})")
                initialization_results[model_name] = True
                
            except Exception as e:
                logger.error(f"Failed to initialize {model_name}: {str(e)}")
                initialization_results[model_name] = False
        
        self.is_initialized = all(initialization_results.values())
        logger.info(f"ML Service initialization complete. Models loaded: {sum(initialization_results.values())}/{len(self._model_registry)}")
        
        return initialization_results
    
    def get_model(self, model_name: str) -> Optional[IMLModel]:
        """
        Retrieve a specific model from the registry.
        
        Args:
            model_name: The name of the model to retrieve
        
        Returns:
            The requested IMLModel instance, or None if not found
        """
        return self.models.get(model_name)
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Get the current status of all registered models.
        
        Returns:
            Dictionary containing model status information including:
            - initialization status
            - version information
            - model availability
        """
        return {
            'is_initialized': self.is_initialized,
            'models_loaded': len(self.models),
            'models': {
                name: {
                    'loaded': name in self.models,
                    'version': self.model_versions.get(name, 'unknown'),
                    'type': type(model).__name__ if (model := self.models.get(name)) else None
                }
                for name in self._model_registry.keys()
            }
        }
    
    def predict_difficulty(
        self,
        content_id: str,
        learner_profile: Dict[str, Any],
        context: Optional[PredictionContext] = None
    ) -> Optional[ModelOutput]:
        """
        Predict the difficulty level of content for a specific learner.
        
        Args:
            content_id: The identifier of the content to evaluate
            learner_profile: Dictionary containing learner characteristics
            context: Optional prediction context with additional metadata
        
        Returns:
            ModelOutput containing difficulty prediction and confidence score
        """
        model = self.models.get('difficulty_predictor')
        
        if model is None:
            logger.warning("Difficulty predictor model not available")
            return None
        
        try:
            # Build context if not provided
            if context is None:
                context = PredictionContext(
                    timestamp=datetime.now().isoformat(),
                    user_id=learner_profile.get('user_id', 'anonymous'),
                    session_id=learner_profile.get('session_id', 'unknown')
                )
            
            # Create input features from learner profile
            input_features = self._extract_difficulty_features(content_id, learner_profile)
            
            return model.predict(input_features, context)
            
        except Exception as e:
            logger.error(f"Difficulty prediction failed: {str(e)}")
            return None
    
    def predict_engagement(
        self,
        content_id: str,
        learner_profile: Dict[str, Any],
        context: Optional[PredictionContext] = None
    ) -> Optional[ModelOutput]:
        """
        Predict learner engagement for specific content.
        
        Args:
            content_id: The identifier of the content to evaluate
            learner_profile: Dictionary containing learner characteristics
            context: Optional prediction context with additional metadata
        
        Returns:
            ModelOutput containing engagement prediction and confidence score
        """
        model = self.models.get('engagement_predictor')
        
        if model is None:
            logger.warning("Engagement predictor model not available")
            return None
        
        try:
            if context is None:
                context = PredictionContext(
                    timestamp=datetime.now().isoformat(),
                    user_id=learner_profile.get('user_id', 'anonymous'),
                    session_id=learner_profile.get('session_id', 'unknown')
                )
            
            input_features = self._extract_engagement_features(content_id, learner_profile)
            
            return model.predict(input_features, context)
            
        except Exception as e:
            logger.error(f"Engagement prediction failed: {str(e)}")
            return None
    
    def get_adaptive_sequence(
        self,
        concept_ids: List[str],
        learner_profile: Dict[str, Any],
        learning_goals: Optional[List[str]] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate an optimized learning sequence for a learner.
        
        This is the primary method for adaptive sequencing. It coordinates
        multiple models to produce a personalized learning path that
        optimizes for retention, engagement, and learning efficiency.
        
        Args:
            concept_ids: List of concept identifiers to sequence
            learner_profile: Dictionary containing learner characteristics
            learning_goals: Optional list of learning goal identifiers
            constraints: Optional constraints (e.g., time_limit, max_concepts)
        
        Returns:
            Dictionary containing:
            - sequence: Ordered list of concept IDs
            - reasoning: Explanation of sequencing decisions
            - metadata: Additional information about the sequence
        """
        # Ensure models are initialized
        if not self.is_initialized:
            self.initialize_models()
        
        context = PredictionContext(
            timestamp=datetime.now().isoformat(),
            user_id=learner_profile.get('user_id', 'anonymous'),
            session_id=learner_profile.get('session_id', 'unknown'),
            metadata={
                'learning_goals': learning_goals or [],
                'constraints': constraints or {}
            }
        )
        
        # Use the sequence optimizer model if available
        optimizer = self.models.get('sequence_optimizer')
        path_predictor = self.models.get('learning_path_predictor')
        
        if optimizer is None and path_predictor is None:
            # Fallback to simple heuristic sequencing
            logger.warning("No ML model available for sequencing, using fallback")
            return self._fallback_sequence(concept_ids, learner_profile, constraints)
        
        try:
            if path_predictor is not None:
                # Use the learning path predictor for sequence generation
                input_features = self._extract_sequence_features(concept_ids, learner_profile)
                result = path_predictor.predict(input_features, context)
                
                return {
                    'sequence': result.predictions,
                    'reasoning': result.explanation,
                    'confidence': result.confidence,
                    'model_used': 'learning_path_predictor',
                    'model_version': self.model_versions.get('learning_path_predictor', 'unknown')
                }
            
            elif optimizer is not None:
                # Use the sequence optimizer
                input_features = self._extract_sequence_features(concept_ids, learner_profile)
                result = optimizer.predict(input_features, context)
                
                return {
                    'sequence': result.predictions,
                    'reasoning': result.explanation,
                    'confidence': result.confidence,
                    'model_used': 'sequence_optimizer',
                    'model_version': self.model_versions.get('sequence_optimizer', 'unknown')
                }
                
        except Exception as e:
            logger.error(f"Adaptive sequence generation failed: {str(e)}")
            return self._fallback_sequence(concept_ids, learner_profile, constraints)
    
    def _extract_difficulty_features(
        self,
        content_id: str,
        learner_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract features for difficulty prediction.
        
        Args:
            content_id: The content identifier
            learner_profile: Learner characteristics
        
        Returns:
            Dictionary of features for the difficulty model
        """
        return {
            'content_id': content_id,
            'learner_level': learner_profile.get('overall_mastery', 0.5),
            'concept_familiarity': learner_profile.get('concept_mastery', {}).get(content_id, 0.0),
            'learning_style': learner_profile.get('cognitive_profile', {}).get('learning_style', 'visual'),
            'time_since_last_review': learner_profile.get('temporal_preferences', {}).get('avg_session_duration', 30)
        }
    
    def _extract_engagement_features(
        self,
        content_id: str,
        learner_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract features for engagement prediction.
        
        Args:
            content_id: The content identifier
            learner_profile: Learner characteristics
        
        Returns:
            Dictionary of features for the engagement model
        """
        return {
            'content_id': content_id,
            'engagement_history': learner_profile.get('engagement_pattern', {}).get('avg_session_engagement', 0.7),
            'motivation_type': learner_profile.get('motivation_profile', {}).get('motivation_type', 'achievement'),
            'preferred_difficulty': learner_profile.get('motivation_profile', {}).get('preferred_difficulty_level', 'challenging'),
            'session_time': learner_profile.get('temporal_preferences', {}).get('preferred_session_time', 'morning')
        }
    
    def _extract_sequence_features(
        self,
        concept_ids: List[str],
        learner_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract features for sequence optimization.
        
        Args:
            concept_ids: List of concept identifiers to sequence
            learner_profile: Learner characteristics
        
        Returns:
            Dictionary of features for the sequence optimization model
        """
        return {
            'concept_ids': concept_ids,
            'learner_mastery': learner_profile.get('concept_mastery', {}),
            'cognitive_profile': learner_profile.get('cognitive_profile', {}),
            'motivation_profile': learner_profile.get('motivation_profile', {}),
            'temporal_preferences': learner_profile.get('temporal_preferences', {})
        }
    
    def _fallback_sequence(
        self,
        concept_ids: List[str],
        learner_profile: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a simple sequence using heuristic rules.
        
        This fallback is used when ML models are unavailable or fail.
        It provides a basic ordering based on mastery gaps.
        
        Args:
            concept_ids: List of concept identifiers to sequence
            learner_profile: Learner characteristics
            constraints: Optional constraints for the sequence
        
        Returns:
            Dictionary containing the fallback sequence
        """
        mastery = learner_profile.get('concept_mastery', {})
        
        # Sort by mastery level (lowest first) to prioritize weak concepts
        sorted_concepts = sorted(
            concept_ids,
            key=lambda c: mastery.get(c, 0.0)
        )
        
        # Apply constraints if provided
        max_concepts = constraints.get('max_concepts', len(concept_ids)) if constraints else len(concept_ids)
        final_sequence = sorted_concepts[:max_concepts]
        
        return {
            'sequence': final_sequence,
            'reasoning': 'Fallback heuristic sequencing: concepts ordered by ascending mastery level',
            'confidence': 0.3,
            'model_used': 'fallback_heuristic',
            'model_version': '1.0'
        }
    
    def save_model_state(self, model_name: str, filepath: str) -> bool:
        """
        Save the state of a specific model to a file.
        
        Args:
            model_name: The name of the model to save
            filepath: The path where the model state will be saved
        
        Returns:
            True if save was successful, False otherwise
        """
        model = self.models.get(model_name)
        
        if model is None:
            logger.error(f"Cannot save {model_name}: model not found")
            return False
        
        try:
            model.save(filepath)
            logger.info(f"Successfully saved {model_name} to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save {model_name}: {str(e)}")
            return False
    
    def load_model_state(self, model_name: str, filepath: str) -> bool:
        """
        Load the state of a specific model from a file.
        
        Args:
            model_name: The name of the model to load
            filepath: The path from which the model state will be loaded
        
        Returns:
            True if load was successful, False otherwise
        """
        model_class = self._model_registry.get(model_name)
        
        if model_class is None:
            logger.error(f"Cannot load {model_name}: model type not registered")
            return False
        
        try:
            model = model_class()
            model.load(filepath)
            self.models[model_name] = model
            logger.info(f"Successfully loaded {model_name} from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to load {model_name}: {str(e)}")
            return False


# Singleton instance for application-wide access
_ml_service_instance: Optional[MLService] = None


def get_ml_service() -> MLService:
    """
    Get the singleton MLService instance.
    
    Returns:
        The global MLService instance
    """
    global _ml_service_instance
    
    if _ml_service_instance is None:
        _ml_service_instance = MLService()
    
    return _ml_service_instance
