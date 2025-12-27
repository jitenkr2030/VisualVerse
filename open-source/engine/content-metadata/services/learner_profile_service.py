"""
Learner Profile Service for VisualVerse Content Metadata Layer

This service manages enhanced learner profiles, providing functionality for profile
creation, updates, analysis, and profile-driven recommendation strategies. It enables
differentiated learning experiences based on comprehensive learner characteristics.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from enum import Enum
from collections import defaultdict
import logging
import random
import math

from ..models.enhanced_learner_profile import (
    EnhancedLearnerProfile,
    CognitiveProfile,
    LearningStyleProfile,
    TemporalPreferences,
    MotivationProfile,
    EngagementPattern,
    AccessibilityNeeds,
    ProfileSnapshot,
    LearningStyleDimension,
    CognitiveStyle,
    MotivationType,
    FeedbackPreference,
    DifficultyPacing,
    SessionPattern
)
from ..models.learner_profile import (
    ConceptMastery,
    MasteryMetrics
)
from .mastery_service import MasteryService
from .reasoning_engine import ReasoningEngine


logger = logging.getLogger(__name__)


class ProfileInferenceStatus(str, Enum):
    """Status of profile inference from behavior"""
    INSUFFICIENT_DATA = "insufficient_data"
    PARTIAL_INFERENCE = "partial_inference"
    HIGH_CONFIDENCE = "high_confidence"


@dataclass
class ProfileAnalysisResult:
    """Result of profile analysis"""
    status: ProfileInferenceStatus
    confidence: float
    inferred_dimensions: List[str]
    recommendations: List[str]
    data_needed: List[str]


@dataclass
class ProfileServiceStats:
    """Statistics for the profile service"""
    total_profiles: int = 0
    profiles_analyzed: int = 0
    inference_updates: int = 0
    average_confidence: float = 0.0


class LearnerProfileService:
    """
    Service for managing comprehensive learner profiles.
    
    This service handles profile creation, updates, inference from behavior,
    and provides analysis capabilities for personalizing learning experiences.
    """
    
    def __init__(
        self,
        mastery_service: Optional[MasteryService] = None,
        reasoning_engine: Optional[ReasoningEngine] = None
    ):
        """
        Initialize the learner profile service.
        
        Args:
            mastery_service: Optional mastery service for concept tracking data
            reasoning_engine: Optional reasoning engine for knowledge analysis
        """
        self.mastery = mastery_service or MasteryService()
        self.reasoning = reasoning_engine or ReasoningEngine()
        
        # In-memory storage (would be replaced with database in production)
        self._profiles: Dict[str, EnhancedLearnerProfile] = {}
        self._snapshots: Dict[str, List[ProfileSnapshot]] = defaultdict(list)
        
        # Statistics
        self._stats = ProfileServiceStats()
    
    # =========================================================================
    # Profile Management
    # =========================================================================
    
    def get_or_create_profile(self, user_id: str) -> EnhancedLearnerProfile:
        """Get or create a learner profile for a user"""
        if user_id in self._profiles:
            profile = self._profiles[user_id]
            profile.update_timestamp()
            return profile
        
        profile = EnhancedLearnerProfile.create(user_id)
        self._profiles[user_id] = profile
        self._stats.total_profiles += 1
        
        logger.info(f"Created enhanced profile for user {user_id}")
        return profile
    
    def get_profile(self, user_id: str) -> Optional[EnhancedLearnerProfile]:
        """Get a learner profile if it exists"""
        return self._profiles.get(user_id)
    
    def update_profile_from_interaction(
        self,
        user_id: str,
        interaction_data: Dict[str, Any]
    ) -> EnhancedLearnerProfile:
        """
        Update learner profile based on learning interaction data.
        
        This method analyzes interaction patterns and updates profile
        dimensions accordingly.
        
        Args:
            user_id: User identifier
            interaction_data: Data from the interaction including
                - session_duration: int (minutes)
                - concepts_covered: List[str]
                - completion_rate: float (0-1)
                - accuracy_rate: float (0-1)
                - time_spent_per_concept: Dict[str, int]
                - interaction_types: List[str]
                - content_types: List[str]
                - difficulty_levels: List[str]
                
        Returns:
            Updated learner profile
        """
        profile = self.get_or_create_profile(user_id)
        
        # Update engagement pattern
        self._update_engagement_from_interaction(profile, interaction_data)
        
        # Update cognitive profile
        self._update_cognitive_from_interaction(profile, interaction_data)
        
        # Update learning style inference
        self._update_style_from_interaction(profile, interaction_data)
        
        # Update temporal preferences
        self._update_temporal_from_interaction(profile, interaction_data)
        
        profile.add_data_source("interaction_analysis")
        self._stats.inference_updates += 1
        
        return profile
    
    def _update_engagement_from_interaction(
        self,
        profile: EnhancedLearnerProfile,
        data: Dict[str, Any]
    ) -> None:
        """Update engagement pattern from interaction data"""
        engagement = profile.engagement_pattern
        
        session_duration = data.get("session_duration", 20)
        completion_rate = data.get("completion_rate", 0.8)
        
        # Update averages with exponential moving average
        alpha = 0.2
        engagement.average_session_length = (
            engagement.average_session_length * (1 - alpha) + session_duration * alpha
        )
        engagement.completion_rate = (
            engagement.completion_rate * (1 - alpha) + completion_rate * alpha
        )
        
        # Update content consumption rate
        concepts = data.get("concepts_covered", [])
        if concepts and session_duration > 0:
            new_rate = len(concepts) / (session_duration / 60)
            engagement.content_consumption_rate = (
                engagement.content_consumption_rate * 0.8 + new_rate * 0.2
            )
        
        profile.update_timestamp()
    
    def _update_cognitive_from_interaction(
        self,
        profile: EnhancedLearnerProfile,
        data: Dict[str, Any]
    ) -> None:
        """Update cognitive profile from interaction data"""
        cognitive = profile.cognitive_profile
        
        accuracy = data.get("accuracy_rate", 0.7)
        time_per_concept = data.get("time_spent_per_concept", {})
        
        # Infer working memory from completion with time pressure
        if accuracy > 0.8 and len(time_per_concept) > 3:
            cognitive.working_memory_capacity = min(
                1.0,
                cognitive.working_memory_capacity + 0.05
            )
        elif accuracy < 0.5:
            cognitive.working_memory_capacity = max(
                0.2,
                cognitive.working_memory_capacity - 0.05
            )
        
        # Infer processing speed from average time
        if time_per_concept:
            avg_time = sum(time_per_concept.values()) / len(time_per_concept)
            if avg_time < 5:  # Fast processing
                cognitive.processing_speed = min(
                    1.0,
                    cognitive.processing_speed + 0.03
                )
            elif avg_time > 15:  # Slower processing
                cognitive.processing_speed = max(
                    0.3,
                    cognitive.processing_speed - 0.03
                )
        
        # Update attention span
        session_duration = data.get("session_duration", 20)
        if data.get("completed_session", True):
            cognitive.attention_span_minutes = (
                cognitive.attention_span_minutes * 0.9 +
                session_duration * 0.1
            )
        
        profile.update_timestamp()
    
    def _update_style_from_interaction(
        self,
        profile: EnhancedLearnerProfile,
        data: Dict[str, Any]
    ) -> None:
        """Update learning style from interaction data"""
        style = profile.learning_style
        
        content_types = data.get("content_types", [])
        interaction_types = data.get("interaction_types", [])
        completion_rates = data.get("completion_by_type", {})
        
        # Update VARK weights
        if "video" in content_types or "animation" in content_types:
            style.visual_weight = min(0.9, style.visual_weight + 0.02)
        if "text" in content_types or "article" in content_types:
            style.reading_weight = min(0.9, style.reading_weight + 0.02)
        if "audio" in content_types or "podcast" in content_types:
            style.auditory_weight = min(0.9, style.auditory_weight + 0.02)
        if "interactive" in content_types or "exercise" in content_types:
            style.kinesthetic_weight = min(0.9, style.kinesthetic_weight + 0.02)
        
        # Normalize weights
        total = (style.visual_weight + style.auditory_weight +
                style.reading_weight + style.kinesthetic_weight)
        if total > 0:
            style.visual_weight /= total
            style.auditory_weight /= total
            style.reading_weight /= total
            style.kinesthetic_weight /= total
        
        # Check for discovery vs guided preference
        if "discovery" in interaction_types:
            style.prefers_discovery_learning = True
            style.prefers_guided_instruction = False
        if "guided" in interaction_types:
            style.prefers_guided_instruction = True
            style.prefers_discovery_learning = False
        
        # Infer pacing preference from completion rates
        if completion_rates:
            avg_completion = sum(completion_rates.values()) / len(completion_rates)
            if avg_completion > 0.9:
                style.difficulty_pacing = DifficultyPacing.ACCELERATED
            elif avg_completion > 0.7:
                style.difficulty_pacing = DifficultyPacing.MODERATE
            else:
                style.difficulty_pacing = DifficultyPacing.GRADUAL
        
        profile.update_timestamp()
    
    def _update_temporal_from_interaction(
        self,
        profile: EnhancedLearnerProfile,
        data: Dict[str, Any]
    ) -> None:
        """Update temporal preferences from interaction data"""
        temporal = profile.temporal_preferences
        
        session_time = data.get("session_time")  # datetime of session
        session_duration = data.get("session_duration", 20)
        completed = data.get("completed_session", True)
        
        if session_time and completed:
            hour = session_time.hour
            
            # Infer preferred time pattern
            if 6 <= hour < 12:
                temporal.preferred_session_pattern = SessionPattern.MORNING
            elif 12 <= hour < 18:
                temporal.preferred_session_pattern = SessionPattern.AFTERNOON
            elif 18 <= hour < 23:
                temporal.preferred_session_pattern = SessionPattern.EVENING
            
            # Track peak hours
            if hour not in temporal.preferred_start_time:
                pass  # Would update peak engagement hours
        
        # Update session length preferences
        if completed:
            temporal.max_session_length_minutes = int(
                temporal.max_session_length_minutes * 0.9 +
                session_duration * 0.1
            )
        
        profile.update_timestamp()
    
    # =========================================================================
    # Profile Analysis and Inference
    # =========================================================================
    
    def analyze_profile(self, user_id: str) -> ProfileAnalysisResult:
        """
        Analyze a learner profile and generate insights.
        
        Args:
            user_id: User identifier
            
        Returns:
            ProfileAnalysisResult with status, confidence, and recommendations
        """
        profile = self.get_or_create_profile(user_id)
        
        inferred_dimensions = []
        recommendations = []
        data_needed = []
        
        # Check which dimensions have sufficient data
        data_sources = set(profile.data_sources)
        
        if "interaction_analysis" in data_sources:
            inferred_dimensions.append("engagement")
            inferred_dimensions.append("cognitive")
            inferred_dimensions.append("learning_style")
        
        if "assessment_results" in data_sources:
            inferred_dimensions.append("cognitive")
        
        if "explicit_preference" in data_sources:
            inferred_dimensions.append("explicit_preferences")
        
        # Calculate confidence based on data sources and profile version
        confidence = min(1.0, len(inferred_dimensions) * 0.2 + profile.profile_version * 0.05)
        
        # Determine status
        if len(inferred_dimensions) < 2:
            status = ProfileInferenceStatus.INSUFFICIENT_DATA
            data_needed = ["interaction_data", "preference_survey"]
        elif confidence < 0.6:
            status = ProfileInferenceStatus.PARTIAL_INFERENCE
        else:
            status = ProfileInferenceStatus.HIGH_CONFIDENCE
        
        # Generate recommendations
        recommendations = self._generate_profile_recommendations(profile)
        
        # Update stats
        self._stats.profiles_analyzed += 1
        self._stats.average_confidence = (
            self._stats.average_confidence * 0.9 + confidence * 0.1
        )
        
        return ProfileAnalysisResult(
            status=status,
            confidence=confidence,
            inferred_dimensions=inferred_dimensions,
            recommendations=recommendations,
            data_needed=data_needed
        )
    
    def _generate_profile_recommendations(self, profile: EnhancedLearnerProfile) -> List[str]:
        """Generate recommendations based on profile analysis"""
        recommendations = []
        
        # Cognitive recommendations
        cognitive = profile.cognitive_profile
        if cognitive.working_memory_capacity < 0.4:
            recommendations.append("Use smaller content chunks (2-3 items)")
        if cognitive.processing_speed < 0.4:
            recommendations.append("Provide extended time for assessments")
        if cognitive.attention_span_minutes < 15:
            recommendations.append("Break content into shorter sessions (10-15 min)")
        
        # Learning style recommendations
        style = profile.learning_style
        if style.prefers_visual_content():
            recommendations.append("Prioritize visual content (diagrams, animations)")
        if style.needs_interactive_elements():
            recommendations.append("Include interactive exercises and simulations")
        if style.difficulty_pacing == DifficultyPacing.GRADUAL:
            recommendations.append("Use gradual difficulty progression")
        
        # Motivation recommendations
        motivation = profile.motivation
        strategies = profile.get_motivation_strategies()
        if strategies:
            recommendations.append(f"Apply motivation strategies: {', '.join(strategies[:3])}")
        
        # Engagement recommendations
        engagement = profile.engagement_pattern
        if engagement.completion_rate < 0.6:
            recommendations.append("Reduce content difficulty or provide more support")
        if engagement.return_likelihood < 0.6:
            recommendations.append("Implement re-engagement reminders")
        
        return recommendations
    
    def infer_learning_style_from_history(
        self,
        user_id: str,
        history: List[Dict[str, Any]]
    ) -> LearningStyleProfile:
        """
        Infer learning style from interaction history.
        
        Args:
            user_id: User identifier
            history: List of interaction records with content types and outcomes
            
        Returns:
            Inferred LearningStyleProfile
        """
        profile = self.get_or_create_profile(user_id)
        style = profile.learning_style
        
        # Count successful interactions by content type
        type_success: Dict[str, Tuple[int, int]] = defaultdict(lambda: (0, 0))
        
        for interaction in history:
            content_types = interaction.get("content_types", [])
            success = interaction.get("success", True)
            
            for content_type in content_types:
                successes, total = type_success[content_type]
                type_success[content_type] = (successes + (1 if success else 0), total + 1)
        
        # Update weights based on success rates
        for content_type, (successes, total) in type_success.items():
            if total < 3:
                continue
            
            success_rate = successes / total
            if success_rate > 0.8:
                if content_type in ["video", "animation", "diagram"]:
                    style.visual_weight = min(0.9, style.visual_weight + 0.05)
                elif content_type in ["text", "article", "documentation"]:
                    style.reading_weight = min(0.9, style.reading_weight + 0.05)
                elif content_type in ["audio", "podcast"]:
                    style.auditory_weight = min(0.9, style.auditory_weight + 0.05)
                elif content_type in ["interactive", "exercise", "simulation"]:
                    style.kinesthetic_weight = min(0.9, style.kinesthetic_weight + 0.05)
        
        # Normalize
        total_weight = (style.visual_weight + style.auditory_weight +
                       style.reading_weight + style.kinesthetic_weight)
        if total_weight > 0:
            style.visual_weight /= total_weight
            style.auditory_weight /= total_weight
            style.reading_weight /= total_weight
            style.kinesthetic_weight /= total_weight
        
        profile.add_data_source("history_analysis")
        profile.update_timestamp()
        
        return style
    
    def update_explicit_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> EnhancedLearnerProfile:
        """
        Update profile with explicitly stated user preferences.
        
        Args:
            user_id: User identifier
            preferences: Dictionary of explicit preferences
            
        Returns:
            Updated profile
        """
        profile = self.get_or_create_profile(user_id)
        
        for key, value in preferences.items():
            profile.set_explicit_preference(key, value)
            
            # Apply to appropriate profile component
            if key == "preferred_difficulty":
                if value == "challenging":
                    profile.motivation.comfort_with_challenge = 0.8
                    profile.learning_style.difficulty_pacing = DifficultyPacing.ACCELERATED
                elif value == "steady":
                    profile.motivation.comfort_with_challenge = 0.5
                    profile.learning_style.difficulty_pacing = DifficultyPacing.MODERATE
                elif value == "gentle":
                    profile.motivation.comfort_with_challenge = 0.3
                    profile.learning_style.difficulty_pacing = DifficultyPacing.GRADUAL
            
            elif key == "session_length":
                profile.temporal_preferences.max_session_length_minutes = value
                profile.cognitive_profile.attention_span_minutes = value * 0.8
            
            elif key == "learning_time":
                if "morning" in value.lower():
                    profile.temporal_preferences.preferred_session_pattern = SessionPattern.MORNING
                elif "evening" in value.lower():
                    profile.temporal_preferences.preferred_session_pattern = SessionPattern.EVENING
                else:
                    profile.temporal_preferences.preferred_session_pattern = SessionPattern.AFTERNOON
            
            elif key == "content_format":
                if "visual" in value.lower():
                    profile.learning_style.visual_weight = 0.5
                if "hands-on" in value.lower():
                    profile.learning_style.kinesthetic_weight = 0.5
        
        profile.add_data_source("explicit_preference")
        return profile
    
    # =========================================================================
    # Profile-Driven Strategy Adjustment
    # =========================================================================
    
    def get_recommendation_strategy(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get the recommendation strategy optimized for a learner.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing strategy parameters for recommendations
        """
        profile = self.get_or_create_profile(user_id)
        
        strategy = {
            "difficulty_adjustment": self._calculate_difficulty_adjustment(profile),
            "content_preferences": profile.get_recommended_content_types(),
            "session_config": profile.get_session_recommendations(),
            "motivation_strategies": profile.get_motivation_strategies(),
            "feedback_style": self._determine_feedback_style(profile),
            "review_frequency": self._calculate_review_frequency(profile),
            "intervention_triggers": self._get_intervention_triggers(profile)
        }
        
        return strategy
    
    def _calculate_difficulty_adjustment(self, profile: EnhancedLearnerProfile) -> Dict[str, float]:
        """Calculate difficulty adjustment factors based on profile"""
        cognitive = profile.cognitive_profile
        motivation = profile.motivation
        
        # Base difficulty from cognitive profile
        cognitive_factor = cognitive.processing_speed * 0.4 + cognitive.working_memory_capacity * 0.3
        
        # Motivation factor
        motivation_factor = motivation.get_optimal_goal_difficulty()
        
        # Engagement factor
        engagement_factor = profile.engagement_pattern.completion_rate * 0.3 + 0.5
        
        # Calculate overall adjustment
        adjustment = (cognitive_factor + motivation_factor + engagement_factor) / 3
        
        return {
            "base_difficulty": adjustment,
            "step_size": 0.15 if cognitive.working_memory_capacity < 0.5 else 0.2,
            "max_difficulty": min(1.0, adjustment + 0.3),
            "min_difficulty": max(0.1, adjustment - 0.2),
            "difficulty_boost_for_challenge": 0.1 if motivation.comfort_with_challenge > 0.6 else 0.0
        }
    
    def _determine_feedback_style(self, profile: EnhancedLearnerProfile) -> Dict[str, Any]:
        """Determine optimal feedback style based on profile"""
        cognitive = profile.cognitive_profile
        motivation = profile.motivation
        
        # Determine feedback timing
        if cognitive.processing_speed < 0.4:
            timing = "delayed"
        elif cognitive.working_memory_capacity < 0.4:
            timing = "delayed"
        else:
            timing = "immediate"
        
        # Determine feedback detail level
        if cognitive.abstract_reasoning > 0.6:
            detail = "concise"
        else:
            detail = "detailed"
        
        # Determine feedback tone
        if motivation.primary_motivation == MotivationType.COMPETITION:
            tone = "competitive"
        elif motivation.primary_motivation == MotivationType.ACHIEVEMENT:
            tone = "encouraging"
        else:
            tone = "supportive"
        
        return {
            "timing": timing,
            "detail_level": detail,
            "tone": tone,
            "show_correct_answers": cognitive.processing_speed > 0.4,
            "highlight_errors": True,
            "provide_hints": cognitive.working_memory_capacity < 0.6
        }
    
    def _calculate_review_frequency(self, profile: EnhancedLearnerProfile) -> Dict[str, Any]:
        """Calculate optimal review frequency based on profile"""
        temporal = profile.temporal_preferences
        cognitive = profile.cognitive_profile
        engagement = profile.engagement_pattern
        
        # Base review interval from cognitive stability
        base_interval = max(1, int(cognitive.attention_span_minutes / 10))
        
        # Adjust for engagement patterns
        if engagement.completion_rate > 0.8:
            interval_multiplier = 1.2
        elif engagement.completion_rate < 0.5:
            interval_multiplier = 0.8
        else:
            interval_multiplier = 1.0
        
        # Adjust for temporal preferences
        if temporal.preferred_session_pattern == SessionPattern.FRAGMENTED:
            more_frequent = True
        else:
            more_frequent = False
        
        interval = int(base_interval * interval_multiplier)
        if more_frequent:
            interval = max(1, interval - 1)
        
        return {
            "initial_review_interval_days": interval,
            "subsequent_multiplier": 1.5 if cognitive.working_memory_capacity > 0.5 else 1.2,
            "max_interval_days": min(30, interval * 4),
            "spaced_repetition_enabled": True,
            "mini_reviews_enabled": more_frequent
        }
    
    def _get_intervention_triggers(self, profile: EnhancedLearnerProfile) -> Dict[str, Any]:
        """Get triggers for engagement intervention"""
        engagement = profile.engagement_pattern
        
        return {
            "inactive_days_warning": int(engagement.average_gap_between_sessions * 1.5),
            "inactive_days_critical": int(engagement.average_gap_between_sessions * 2.5),
            "low_session_quality_threshold": 0.5,
            "streak_broken_warning": True,
            "progress_plateau_threshold": 5,  # sessions without mastery gain
            "intervention_messages": self._get_intervention_messages(profile)
        }
    
    def _get_intervention_messages(self, profile: EnhancedLearnerProfile) -> Dict[str, List[str]]:
        """Get appropriate intervention messages based on profile"""
        motivation = profile.motivation
        
        messages = {
            "return_encouragement": [
                "We miss you! Ready to continue your learning journey?",
                "Your next milestone is waiting. Let's reach it together!",
                "A little progress each day adds up. Back at it?"
            ],
            "streak_motivation": [
                "Keep your streak alive! Just one session today.",
                f"You're on a {profile.engagement_pattern.current_streak}-day streak!"
            ],
            "progress_acknowledgment": [
                "Great progress! You've mastered X new concepts this week.",
                "Your dedication is paying off!"
            ]
        }
        
        # Customize based on motivation
        if motivation.primary_motivation == MotivationType.COMPETITION:
            messages["return_encouragement"].append(
                "Your ranking is at risk! Log in to maintain your position."
            )
        elif motivation.primary_motivation == MotivationType.SOCIAL:
            messages["return_encouragement"].append(
                "Your study group is waiting for you!"
            )
        
        return messages
    
    # =========================================================================
    # Profile Analytics and Snapshots
    # =========================================================================
    
    def create_profile_snapshot(
        self,
        user_id: str,
        mastery_metrics: MasteryMetrics
    ) -> ProfileSnapshot:
        """
        Create a point-in-time snapshot of learner profile.
        
        Args:
            user_id: User identifier
            mastery_metrics: Current mastery metrics
            
        Returns:
            ProfileSnapshot
        """
        profile = self.get_or_create_profile(user_id)
        
        snapshot = ProfileSnapshot.create(
            learner_id=user_id,
            overall_mastery=mastery_metrics.global_mastery_average,
            concepts_mastered=mastery_metrics.total_concepts_mastered,
            engagement_pattern=profile.engagement_pattern
        )
        
        self._snapshots[user_id].append(snapshot)
        
        # Keep only last 30 snapshots
        if len(self._snapshots[user_id]) > 30:
            self._snapshots[user_id] = self._snapshots[user_id][-30:]
        
        return snapshot
    
    def get_profile_evolution(
        self,
        user_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get profile evolution over time.
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Dictionary with evolution data
        """
        snapshots = self._snapshots.get(user_id, [])
        cutoff = datetime.now() - timedelta(days=days)
        
        relevant_snapshots = [
            s for s in snapshots if s.captured_at >= cutoff
        ]
        
        if len(relevant_snapshots) < 2:
            return {"evolution": "insufficient_data", "snapshots": len(relevant_snapshots)}
        
        # Calculate trends
        mastery_trend = []
        engagement_trend = []
        
        for snapshot in relevant_snapshots:
            mastery_trend.append(snapshot.overall_mastery)
            engagement_trend.append(snapshot.average_session_length)
        
        return {
            "mastery_trend": mastery_trend,
            "mastery_change": mastery_trend[-1] - mastery_trend[0] if mastery_trend else 0,
            "engagement_trend": engagement_trend,
            "engagement_change": engagement_trend[-1] - engagement_trend[0] if engagement_trend else 0,
            "snapshot_count": len(relevant_snapshots),
            "period_days": days
        }
    
    def compare_profiles(
        self,
        user_id_1: str,
        user_id_2: str
    ) -> Dict[str, Any]:
        """
        Compare two learner profiles.
        
        Args:
            user_id_1: First user ID
            user_id_2: Second user ID
            
        Returns:
            Comparison results
        """
        profile1 = self.get_profile(user_id_1)
        profile2 = self.get_profile(user_id_2)
        
        if not profile1 or not profile2:
            return {"error": "One or both profiles not found"}
        
        return {
            "user_1": {
                "cognitive_score": profile1.cognitive_profile.processing_speed,
                "learning_style": profile1.learning_style.get_primary_modality().value,
                "motivation": profile1.motivation.primary_motivation.value
            },
            "user_2": {
                "cognitive_score": profile2.cognitive_profile.processing_speed,
                "learning_style": profile2.learning_style.get_primary_modality().value,
                "motivation": profile2.motivation.primary_motivation.value
            },
            "similarity": self._calculate_profile_similarity(profile1, profile2)
        }
    
    def _calculate_profile_similarity(
        self,
        profile1: EnhancedLearnerProfile,
        profile2: EnhancedLearnerProfile
    ) -> float:
        """Calculate similarity between two profiles (0.0-1.0)"""
        similarity_factors = []
        
        # Learning style similarity
        style1 = profile1.learning_style
        style2 = profile2.learning_style
        style_diff = (
            abs(style1.visual_weight - style2.visual_weight) +
            abs(style1.auditory_weight - style2.auditory_weight) +
            abs(style1.reading_weight - style2.reading_weight) +
            abs(style1.kinesthetic_weight - style2.kinesthetic_weight)
        ) / 4
        similarity_factors.append(1.0 - style_diff)
        
        # Cognitive profile similarity
        cog1 = profile1.cognitive_profile
        cog2 = profile2.cognitive_profile
        cog_diff = (
            abs(cog1.processing_speed - cog2.processing_speed) +
            abs(cog1.working_memory_capacity - cog2.working_memory_capacity)
        ) / 2
        similarity_factors.append(1.0 - cog_diff)
        
        # Motivation similarity
        if profile1.motivation.primary_motivation == profile2.motivation.primary_motivation:
            similarity_factors.append(1.0)
        else:
            similarity_factors.append(0.5)
        
        return sum(similarity_factors) / len(similarity_factors)
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            "total_profiles": self._stats.total_profiles,
            "profiles_analyzed": self._stats.profiles_analyzed,
            "inference_updates": self._stats.inference_updates,
            "average_confidence": round(self._stats.average_confidence, 2),
            "total_snapshots": sum(len(s) for s in self._snapshots.values())
        }
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._profiles.clear()
        self._snapshots.clear()
        self._stats = ProfileServiceStats()
        logger.info("Cleared learner profile service cache")
