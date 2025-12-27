"""
Enhanced Learner Profile Models for VisualVerse Content Metadata Layer

This module provides comprehensive learner profile models that extend beyond basic
tracking to include cognitive profiles, learning preferences, motivation factors,
and adaptive behavior patterns. These models enable truly personalized learning
experiences based on individual learner characteristics.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from enum import Enum
from dataclasses import dataclass, field
import uuid


class LearningStyleDimension(str, Enum):
    """Learning style dimensions based on VARK model"""
    VISUAL = "visual"      # Prefers diagrams, charts, videos
    AUDITORY = "auditory"  # Prefers lectures, discussions
    READING = "reading"    # Prefers text, written explanations
    KINESTHETIC = "kinesthetic"  # Prefers hands-on, practice


class CognitiveStyle(str, Enum):
    """Cognitive processing styles"""
    GLOBAL = "global"      # Prefers big picture first
    SEQUENTIAL = "sequential"  # Prefers step-by-step
    ANALYTIC = "analytic"  # Prefers detailed analysis
    INTUITIVE = "intuitive"  # Prefers patterns and connections


class MotivationType(str, Enum):
    """Types of learner motivation"""
    ACHIEVEMENT = "achievement"  # Driven by mastery and competence
    COMPETITION = "competition"  # Driven by outperforming others
    SOCIAL = "social"  # Driven by collaboration and recognition
    INTEREST = "interest"  # Driven by curiosity and topics
    UTILITY = "utility"  # Driven by practical application
    ESCAPE = "escape"  # Driven by avoiding negative outcomes


class FeedbackPreference(str, Enum):
    """Feedback timing and style preferences"""
    IMMEDIATE = "immediate"     # Wants instant feedback
    DELAYED = "delayed"         # Prefers to complete before feedback
    DETAILED = "detailed"       # Wants thorough explanations
    CONCISE = "concise"         # Prefers brief summaries
    ENCOURAGING = "encouraging"  # Prefers positive reinforcement
    DIRECT = "direct"           # Prefers direct criticism


class DifficultyPacing(str, Enum):
    """Difficulty progression preferences"""
    GRADUAL = "gradual"         # Slow, steady progression
    MODERATE = "moderate"       # Balanced pace
    ACCELERATED = "accelerated" # Fast-paced learning
    SPIKE = "spike"             # Mix of easy and challenging


class SessionPattern(str, Enum):
    """Typical learning session patterns"""
    MORNING = "morning"         # Prefers early sessions
    AFTERNOON = "afternoon"     # Prefers midday
    EVENING = "evening"         # Prefers night sessions
    FRAGMENTED = "fragmented"   # Prefers short, frequent sessions
    EXTENDED = "extended"       # Prefers long, immersive sessions


@dataclass
class CognitiveProfile:
    """
    Cognitive characteristics that affect learning efficiency.
    
    These metrics are inferred from learning behavior and used to
    optimize content presentation and pacing.
    """
    # Working memory capacity (0.0-1.0)
    working_memory_capacity: float = 0.5
    
    # Processing speed relative to age norm (0.0-1.0)
    processing_speed: float = 0.5
    
    # Attention span in minutes
    attention_span_minutes: float = 15.0
    
    # Cognitive load tolerance (0.0-1.0)
    cognitive_load_tolerance: float = 0.5
    
    # Visual processing ability (0.0-1.0)
    visual_processing: float = 0.5
    
    # Verbal processing ability (0.0-1.0)
    verbal_processing: float = 0.5
    
    # Pattern recognition (0.0-1.0)
    pattern_recognition: float = 0.5
    
    # Abstract reasoning (0.0-1.0)
    abstract_reasoning: float = 0.5
    
    @classmethod
    def create(cls) -> "CognitiveProfile":
        """Factory method for default cognitive profile"""
        return cls()
    
    def get_optimal_content_chunk_size(self) -> int:
        """Get optimal content chunk size based on working memory"""
        if self.working_memory_capacity >= 0.8:
            return 7  # Can handle 7 items
        elif self.working_memory_capacity >= 0.6:
            return 5
        elif self.working_memory_capacity >= 0.4:
            return 3
        else:
            return 2  # Needs smaller chunks
    
    def get_recommended_session_length(self) -> int:
        """Get recommended session length in minutes"""
        return int(self.attention_span_minutes * 2)
    
    def needs_visual_support(self) -> bool:
        """Check if learner needs additional visual aids"""
        return self.visual_processing < 0.4
    
    def needs_verbose_explanation(self) -> bool:
        """Check if learner needs more detailed explanations"""
        return self.verbal_processing < 0.4


@dataclass
class LearningStyleProfile:
    """
    Comprehensive learning style preferences across multiple dimensions.
    
    This profile goes beyond simple style classification to capture
    nuanced preferences that affect content delivery.
    """
    # VARK dimensions (weights sum to 1.0)
    visual_weight: float = 0.35
    auditory_weight: float = 0.25
    reading_weight: float = 0.20
    kinesthetic_weight: float = 0.20
    
    # Cognitive style
    cognitive_style: CognitiveStyle = CognitiveStyle.SEQUENTIAL
    
    # Content structure preference
    prefers_prerequisites_first: bool = True
    prefers_overview_first: bool = False
    prefers_examples_first: bool = False
    
    # Interaction preferences
    prefers_discovery_learning: bool = False
    prefers_guided_instruction: bool = True
    prefers_social_learning: bool = False
    prefers_independent_study: bool = True
    
    # Pacing preferences
    difficulty_pacing: DifficultyPacing = DifficultyPacing.MODERATE
    preferred_content_length: str = "medium"  # short, medium, long
    prefers_mixed_difficulty: bool = True
    
    # Assessment preferences
    prefers_formative_assessment: bool = True
    prefers_summative_assessment: bool = True
    prefers_practice_over_test: bool = False
    
    @classmethod
    def create(cls) -> "LearningStyleProfile":
        """Factory method for default learning style profile"""
        return cls()
    
    def get_primary_modality(self) -> LearningStyleDimension:
        """Get the primary learning modality"""
        weights = {
            LearningStyleDimension.VISUAL: self.visual_weight,
            LearningStyleDimension.AUDITORY: self.auditory_weight,
            LearningStyleDimension.READING: self.reading_weight,
            LearningStyleDimension.KINESTHETIC: self.kinesthetic_weight
        }
        return max(weights, key=weights.get)
    
    def needs_prerequisites_shown(self) -> bool:
        """Check if learner should see prerequisite chain"""
        return self.prefers_prerequisites_first
    
    def prefers_visual_content(self) -> bool:
        """Check if visual content should be prioritized"""
        return self.visual_weight >= 0.4
    
    def needs_interactive_elements(self) -> bool:
        """Check if interactive elements are important"""
        return self.kinesthetic_weight >= 0.3 or self.prefers_discovery_learning
    
    def get_content_length_category(self) -> str:
        """Get content length category"""
        return self.preferred_content_length


@dataclass
class TemporalPreferences:
    """
    Temporal patterns and preferences for learning activities.
    
    This model captures when and how long learners prefer to study,
    enabling optimal scheduling of learning sessions.
    """
    # Typical session times
    preferred_session_pattern: SessionPattern = SessionPattern.AFTERNOON
    
    # Preferred start time (for scheduled sessions)
    preferred_start_time: Optional[time] = None
    
    # Maximum session length in minutes
    max_session_length_minutes: int = 60
    
    # Minimum session length in minutes
    min_session_length_minutes: int = 10
    
    # Preferred days of week (0=Monday, 6=Sunday)
    preferred_days: List[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5, 6])
    
    # Daily learning goal in minutes
    daily_learning_goal_minutes: int = 30
    
    # Weekly learning goal in minutes
    weekly_learning_goal_minutes: int = 210
    
    # Preferred break frequency in minutes
    break_frequency_minutes: int = 25
    
    # Preferred break duration in minutes
    break_duration_minutes: int = 5
    
    # Timezone offset from UTC
    timezone_offset: int = 0
    
    @classmethod
    def create(cls) -> "TemporalPreferences":
        """Factory method for default temporal preferences"""
        return cls(
            preferred_start_time=time(9, 0),  # 9:00 AM default
            preferred_days=[0, 1, 2, 3, 4],  # Weekdays
            daily_learning_goal_minutes=30,
            weekly_learning_goal_minutes=150
        )
    
    def is_available_now(self, current_time: datetime) -> bool:
        """Check if current time matches preferred learning time"""
        day_preferred = current_time.weekday() in self.preferred_days
        
        if not day_preferred:
            return False
        
        if self.preferred_session_pattern == SessionPattern.MORNING:
            hour = current_time.hour
            return 6 <= hour < 12
        elif self.preferred_session_pattern == SessionPattern.AFTERNOON:
            hour = current_time.hour
            return 12 <= hour < 18
        elif self.preferred_session_pattern == SessionPattern.EVENING:
            hour = current_time.hour
            return 18 <= hour < 23
        else:
            return True  # Fragmented/extended can learn anytime
    
    def get_optimal_session_length(self, available_minutes: int) -> int:
        """Get optimal session length within available time"""
        if available_minutes <= self.min_session_length_minutes:
            return self.min_session_length_minutes
        if available_minutes >= self.max_session_length_minutes:
            return self.max_session_length_minutes
        return available_minutes
    
    def calculate_session_breaks(self, session_minutes: int) -> int:
        """Calculate number of breaks needed for a session"""
        if session_minutes <= self.break_frequency_minutes:
            return 0
        return int(session_minutes / self.break_frequency_minutes)


@dataclass
class MotivationProfile:
    """
    Motivation factors and goals that drive learning behavior.
    
    Understanding motivation helps create engaging learning experiences
    and appropriate goal structures.
    """
    # Primary motivation type
    primary_motivation: MotivationType = MotivationType.INTEREST
    
    # Secondary motivation types
    secondary_motivations: List[MotivationType] = field(default_factory=list)
    
    # Short-term learning goals
    short_term_goals: List[str] = field(default_factory=list)
    
    # Long-term learning goals
    long_term_goals: List[str] = field(default_factory=list)
    
    # Target completion date for current learning path
    target_completion_date: Optional[datetime] = None
    
    # Desired competency level (0.0-1.0)
    target_competency: float = 0.8
    
    # Extrinsic rewards that motivate
    preferred_rewards: List[str] = field(default_factory=list)
    
    # Gamification preferences
    enjoys_badges: bool = True
    enjoys_leaderboards: bool = True
    enjoys_streaks: bool = True
    
    # Progress recognition
    needs_progress_celebration: bool = True
    preferred_recognition_frequency: str = "session"  # session, daily, weekly, milestone
    
    # Challenge comfort
    comfort_with_challenge: float = 0.5  # 0.0-1.0
    enjoys_difficulty_spikes: bool = False
    
    @classmethod
    def create(cls) -> "MotivationProfile":
        """Factory method for default motivation profile"""
        return cls(
            primary_motivation=MotivationType.INTEREST
        )
    
    def get_motivating_factors(self) -> List[str]:
        """Get list of factors that motivate this learner"""
        factors = []
        if self.primary_motivation == MotivationType.ACHIEVEMENT:
            factors.append("mastery_progress")
        elif self.primary_motivation == MotivationType.COMPETITION:
            factors.append("rankings")
        elif self.primary_motivation == MotivationType.SOCIAL:
            factors.append("collaboration")
        elif self.primary_motivation == MotivationType.INTEREST:
            factors.append("curiosity")
        elif self.primary_motivation == MotivationType.UTILITY:
            factors.append("practical_skills")
        return factors
    
    def should_celebrate_progress(self) -> bool:
        """Check if learner needs progress celebrations"""
        return self.needs_progress_celebration
    
    def get_optimal_goal_difficulty(self) -> float:
        """Get optimal challenge level based on comfort"""
        return 0.7 + (self.comfort_with_challenge * 0.2)  # Range 0.7-0.9


@dataclass
class EngagementPattern:
    """
    Observed patterns in learner engagement and behavior.
    
    These patterns are derived from historical data and used to
    predict and optimize future engagement.
    """
    # Average session length in minutes
    average_session_length: float = 20.0
    
    # Average sessions per week
    average_sessions_per_week: float = 3.5
    
    # Typical completion rate for started content
    completion_rate: float = 0.75
    
    # Likelihood to return after break
    return_likelihood: float = 0.8
    
    # Preferred content consumption rate (concepts per hour)
    content_consumption_rate: float = 2.0
    
    # Peak engagement hours (list of hours 0-23)
    peak_engagement_hours: List[int] = field(default_factory=lambda: [9, 10, 11, 14, 15, 16, 19, 20])
    
    # Days of week with highest engagement
    peak_engagement_days: List[int] = field(default_factory=lambda: [1, 2, 3, 4])  # Tue-Fri
    
    # Average time between sessions in hours
    average_gap_between_sessions: float = 24.0
    
    # Drop-off risk factors
    risk_factors: List[str] = field(default_factory=list)
    
    # Engagement resilience score (0.0-1.0)
    resilience_score: float = 0.5
    
    # Content abandonment patterns
    abandonment_triggers: List[str] = field(default_factory=list)
    
    @classmethod
    def create(cls) -> "EngagementPattern":
        """Factory method for default engagement pattern"""
        return cls(
            average_session_length=20.0,
            average_sessions_per_week=3.5,
            completion_rate=0.75,
            content_consumption_rate=2.0
        )
    
    def get_optimal_reminder_timing(self) -> float:
        """Get optimal reminder timing in hours"""
        return min(48, max(12, self.average_gap_between_sessions * 1.2))
    
    def is_high_risk_for_abandonment(self, days_inactive: int) -> bool:
        """Check if learner is at high risk of abandonment"""
        if days_inactive < 3:
            return False
        if days_inactive > 14:
            return True
        return self.return_likelihood < 0.5 and days_inactive > self.average_gap_between_sessions * 2
    
    def get_optimal_session_count_today(self, current_session_count: int) -> int:
        """Get optimal number of sessions for today"""
        weekly_target = self.average_sessions_per_week * 7
        daily_estimate = weekly_target / 7
        remaining = max(0, int(daily_estimate - current_session_count))
        return min(remaining, 3)  # Cap at 3 sessions per day


@dataclass
class AccessibilityNeeds:
    """
    Accessibility requirements and accommodations.
    
    This model ensures content is presented in ways that meet
    diverse learner needs.
    """
    # Visual accommodations
    needs_large_text: bool = False
    needs_high_contrast: bool = False
    needs_screen_reader: bool = False
    color_blind_mode: str = "none"  # none, protanopia, deuteranopia, tritanopia
    
    # Auditory accommodations
    needs_captions: bool = False
    needs_transcripts: bool = False
    needs_audio_description: bool = False
    
    # Motor accommodations
    needs_keyboard_navigation: bool = False
    needs_larger_click_targets: bool = False
    needs_longer_timeout: bool = False
    
    # Cognitive accommodations
    needs_simplified_language: bool = False
    needs_additional_processing_time: bool = False
    needs_chunked_content: bool = False
    
    # Preferred content speed
    preferred_playback_speed: float = 1.0
    
    # Reading assistance
    needs_reading_assistance: bool = False
    
    @classmethod
    def create(cls) -> "AccessibilityNeeds":
        """Factory method for default accessibility needs"""
        return cls()
    
    def requires_accessibility_optimization(self) -> bool:
        """Check if any accessibility accommodations are needed"""
        return (
            self.needs_large_text or self.needs_high_contrast or
            self.needs_screen_reader or self.needs_captions or
            self.needs_transcripts or self.needs_keyboard_navigation or
            self.needs_simplified_language or self.needs_chunked_content
        )
    
    def should_reduce_content_speed(self) -> bool:
        """Check if content playback should be slowed"""
        return self.needs_additional_processing_time


@dataclass
class EnhancedLearnerProfile:
    """
    Comprehensive learner profile combining all personalization dimensions.
    
    This is the main profile class that aggregates cognitive, style, temporal,
    motivational, engagement, and accessibility data to enable truly
    personalized learning experiences.
    """
    profile_id: str
    user_id: str
    created_at: datetime
    last_updated: datetime
    
    # Core components
    cognitive_profile: CognitiveProfile = field(default_factory=CognitiveProfile)
    learning_style: LearningStyleProfile = field(default_factory=LearningStyleProfile)
    temporal_preferences: TemporalPreferences = field(default_factory=TemporalPreferences)
    motivation: MotivationProfile = field(default_factory=MotivationProfile)
    engagement_pattern: EngagementPattern = field(default_factory=EngagementPattern)
    accessibility: AccessibilityNeeds = field(default_factory=AccessibilityNeeds)
    
    # Version tracking for profile updates
    profile_version: int = 1
    
    # Confidence in profile accuracy (0.0-1.0)
    profile_confidence: float = 0.0
    
    # Data sources used to build profile
    data_sources: List[str] = field(default_factory=list)
    
    # Explicit preferences (set by user)
    explicit_preferences: Dict[str, Any] = field(default_factory=dict)
    
    # Inferred preferences (derived from behavior)
    inferred_preferences: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def create(cls, user_id: str) -> "EnhancedLearnerProfile":
        """Factory method to create a new enhanced learner profile"""
        now = datetime.now()
        return cls(
            profile_id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=now,
            last_updated=now,
            cognitive_profile=CognitiveProfile.create(),
            learning_style=LearningStyleProfile.create(),
            temporal_preferences=TemporalPreferences.create(),
            motivation=MotivationProfile.create(),
            engagement_pattern=EngagementPattern.create(),
            accessibility=AccessibilityNeeds.create(),
            profile_version=1,
            profile_confidence=0.0
        )
    
    def update_timestamp(self) -> None:
        """Update the last modified timestamp"""
        self.last_updated = datetime.now()
        self.profile_version += 1
    
    def add_data_source(self, source: str) -> None:
        """Add a data source used for profiling"""
        if source not in self.data_sources:
            self.data_sources.append(source)
    
    def set_explicit_preference(self, key: str, value: Any) -> None:
        """Set an explicitly stated user preference"""
        self.explicit_preferences[key] = value
        self.update_timestamp()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a preference, checking explicit first, then inferred"""
        if key in self.explicit_preferences:
            return self.explicit_preferences[key]
        return self.inferred_preferences.get(key, default)
    
    def get_optimal_difficulty_level(self) -> str:
        """Get the optimal difficulty level for this learner"""
        base_difficulty = 0.5
        cognitive_factor = self.cognitive_profile.processing_speed * 0.3
        motivation_factor = self.motivation.get_optimal_goal_difficulty() * 0.3
        engagement_factor = self.engagement_pattern.completion_rate * 0.2
        style_factor = 0.3 if self.learning_style.difficulty_pacing == DifficultyPacing.ACCELERATED else 0.1
        
        difficulty_score = base_difficulty + cognitive_factor + motivation_factor + engagement_factor + style_factor
        difficulty_score = max(0.0, min(1.0, difficulty_score))
        
        if difficulty_score < 0.3:
            return "beginner"
        elif difficulty_score < 0.5:
            return "elementary"
        elif difficulty_score < 0.7:
            return "intermediate"
        elif difficulty_score < 0.85:
            return "advanced"
        else:
            return "expert"
    
    def get_recommended_content_types(self) -> List[str]:
        """Get recommended content types based on learning style"""
        content_types = []
        
        if self.learning_style.prefers_visual_content():
            content_types.extend(["animation", "diagram", "infographic", "video"])
        
        if self.learning_style.kinesthetic_weight >= 0.25:
            content_types.extend(["interactive", "simulation", "practice", "exercise"])
        
        if self.learning_style.auditory_weight >= 0.3:
            content_types.extend(["audio", "podcast", "discussion"])
        
        if self.learning_style.reading_weight >= 0.3:
            content_types.extend(["text", "article", "documentation"])
        
        if self.cognitive_profile.needs_visual_support():
            content_types.append("visual_aid")
        
        return list(set(content_types))
    
    def get_session_recommendations(self) -> Dict[str, Any]:
        """Get optimal session configuration for this learner"""
        return {
            "max_duration_minutes": self.temporal_preferences.max_session_length_minutes,
            "min_duration_minutes": self.temporal_preferences.min_session_length_minutes,
            "break_frequency_minutes": self.temporal_preferences.break_frequency_minutes,
            "break_duration_minutes": self.temporal_preferences.break_duration_minutes,
            "content_chunk_size": self.cognitive_profile.get_optimal_content_chunk_size(),
            "session_count_target": self.engagement_pattern.average_sessions_per_week / 7
        }
    
    def get_motivation_strategies(self) -> List[str]:
        """Get strategies to motivate this learner"""
        strategies = []
        
        # Based on motivation type
        if self.motivation.primary_motivation == MotivationType.ACHIEVEMENT:
            strategies.extend(["progress_milestones", "competency_badges", "mastery_levels"])
        elif self.motivation.primary_motivation == MotivationType.COMPETITION:
            strategies.extend(["leaderboards", "peer_comparison", "challenges"])
        elif self.motivation.primary_motivation == MotivationType.SOCIAL:
            strategies.extend(["collaborative_projects", "discussion_forums", "study_groups"])
        elif self.motivation.primary_motivation == MotivationType.INTEREST:
            strategies.extend(["exploration_paths", "curiosity_questions", "real_world_connections"])
        elif self.motivation.primary_motivation == MotivationType.UTILITY:
            strategies.extend(["practical_projects", "certification_paths", "career_goals"])
        
        # Based on engagement patterns
        if self.motivation.enjoys_badges:
            strategies.append("achievement_badges")
        if self.motivation.enjoys_streaks:
            strategies.append("learning_streaks")
        
        return strategies
    
    def needs_intervention(self, days_inactive: int) -> bool:
        """Check if learner needs engagement intervention"""
        return self.engagement_pattern.is_high_risk_for_abandonment(days_inactive)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary for storage"""
        return {
            "profile_id": self.profile_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "profile_version": self.profile_version,
            "profile_confidence": self.profile_confidence,
            "data_sources": self.data_sources,
            "explicit_preferences": self.explicit_preferences,
            "inferred_preferences": self.inferred_preferences,
            "cognitive": {
                "working_memory_capacity": self.cognitive_profile.working_memory_capacity,
                "processing_speed": self.cognitive_profile.processing_speed,
                "attention_span_minutes": self.cognitive_profile.attention_span_minutes,
                "cognitive_load_tolerance": self.cognitive_profile.cognitive_load_tolerance
            },
            "learning_style": {
                "visual_weight": self.learning_style.visual_weight,
                "auditory_weight": self.learning_style.auditory_weight,
                "reading_weight": self.learning_style.reading_weight,
                "kinesthetic_weight": self.learning_style.kinesthetic_weight,
                "cognitive_style": self.learning_style.cognitive_style.value,
                "difficulty_pacing": self.learning_style.difficulty_pacing.value
            },
            "temporal": {
                "preferred_session_pattern": self.temporal_preferences.preferred_session_pattern.value,
                "max_session_length_minutes": self.temporal_preferences.max_session_length_minutes,
                "daily_goal_minutes": self.temporal_preferences.daily_learning_goal_minutes
            },
            "motivation": {
                "primary_motivation": self.motivation.primary_motivation.value,
                "comfort_with_challenge": self.motivation.comfort_with_challenge
            },
            "accessibility": {
                "requires_accommodation": self.accessibility.requires_accessibility_optimization()
            }
        }


@dataclass
class ProfileSnapshot:
    """
    Point-in-time snapshot of learner profile state.
    
    Used for tracking profile evolution and analyzing changes over time.
    """
    snapshot_id: str
    learner_id: str
    captured_at: datetime
    
    # Profile state at snapshot time
    overall_mastery: float
    concepts_mastered: int
    current_streak: int
    total_learning_time: int
    
    # Engagement metrics
    average_session_length: float
    sessions_last_week: int
    
    # Top strengths and weaknesses
    top_strengths: List[str]
    top_weaknesses: List[str]
    
    # Recommendations that were effective
    effective_recommendations: List[str]
    
    @classmethod
    def create(
        cls,
        learner_id: str,
        overall_mastery: float,
        concepts_mastered: int,
        engagement_pattern: EngagementPattern
    ) -> "ProfileSnapshot":
        """Factory method to create a profile snapshot"""
        return cls(
            snapshot_id=str(uuid.uuid4()),
            learner_id=learner_id,
            captured_at=datetime.now(),
            overall_mastery=overall_mastery,
            concepts_mastered=concepts_mastered,
            current_streak=0,
            total_learning_time=0,
            average_session_length=engagement_pattern.average_session_length,
            sessions_last_week=int(engagement_pattern.average_sessions_per_week),
            top_strengths=[],
            top_weaknesses=[],
            effective_recommendations=[]
        )
