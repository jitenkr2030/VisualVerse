"""
User Profile Model for VisualVerse Recommendation Engine

SQLAlchemy model for storing computed user preferences and learning patterns
used by recommendation algorithms.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

class UserPreferenceProfile(Base):
    """Detailed user preference profile for personalization"""
    __tablename__ = "user_preference_profiles"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, unique=True, index=True)
    
    # Subject preferences (computed from interaction history)
    subject_preferences = Column(JSON, nullable=True)  # {subject_id: preference_score}
    subject_engagement_scores = Column(JSON, nullable=True)  # {subject_id: engagement_score}
    subject_mastery_levels = Column(JSON, nullable=True)  # {subject_id: mastery_level_1_5}
    
    # Content type preferences
    content_type_preferences = Column(JSON, nullable=True)  # {content_type: preference_score}
    duration_preferences = Column(JSON, nullable=True)  # {duration_range: preference_score}
    
    # Learning style preferences (computed from behavior)
    preferred_difficulty_levels = Column(JSON, nullable=True)  # List of preferred difficulty levels
    learning_pace_preference = Column(Float, nullable=True)  # Concepts per week preference
    session_duration_preference = Column(Float, nullable=True)  # Preferred session length in minutes
    
    # Temporal preferences
    active_time_patterns = Column(JSON, nullable=True)  # Hour-day patterns of activity
    learning_frequency_preference = Column(String(20), nullable=True)  # daily, weekly, flexible
    optimal_learning_times = Column(JSON, nullable=True)  # Best times for learning
    
    # Engagement patterns
    completion_rate_by_subject = Column(JSON, nullable=True)  # Completion rates per subject
    dropout_points = Column(JSON, nullable=True)  # Points where users typically drop off
    retry_patterns = Column(JSON, nullable=True)  # Content that users retry
    skipping_patterns = Column(JSON, nullable=True)  # Content that users typically skip
    
    # Social learning preferences
    collaboration_preference = Column(String(20), nullable=True)  # collaborative, independent, mixed
    peer_learning_engagement = Column(Float, nullable=True)  # Score 0-1
    discussion_participation = Column(Float, nullable=True)  # Score 0-1
    
    # Goal-oriented preferences
    learning_goal_orientation = Column(String(20), nullable=True)  # performance, mastery, enjoyment
    goal_specificity = Column(String(20), nullable=True)  # specific, general, exploratory
    progress_tracking_preference = Column(String(20), nullable=True)  # detailed, summary, minimal
    
    # Cognitive load preferences
    information_density_preference = Column(String(20), nullable=True)  # low, medium, high
    multimedia_preference = Column(String(20), nullable=True)  # text, visual, audio, mixed
    complexity_handling = Column(String(20), nullable=True)  # gradual, immediate, adaptive
    
    # Feedback preferences
    feedback_frequency_preference = Column(String(20), nullable=True)  # frequent, occasional, minimal
    feedback_type_preference = Column(JSON, nullable=True)  # {feedback_type: preference_score}
    motivation_feedback_preference = Column(String(20), nullable=True)  # encouragement, achievement, progress
    
    # A/B testing and experimentation
    experiment_groups = Column(JSON, nullable=True)  # Current experiment group assignments
    preference_stability_score = Column(Float, nullable=True)  # How stable preferences are over time
    
    # Confidence and uncertainty
    preference_confidence = Column(Float, nullable=True)  # Confidence in preference predictions 0-1
    last_preference_update = Column(DateTime, nullable=True)
    preference_version = Column(Integer, nullable=False, default=1)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_user_preference_user_id', 'user_id'),
        Index('ix_user_preference_last_update', 'last_preference_update'),
        Index('ix_user_preference_confidence', 'preference_confidence'),
    )
    
    def __repr__(self):
        return f"<UserPreferenceProfile(user_id='{self.user_id}', confidence={self.preference_confidence})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subject_preferences": self.subject_preferences,
            "subject_engagement_scores": self.subject_engagement_scores,
            "subject_mastery_levels": self.subject_mastery_levels,
            "content_type_preferences": self.content_type_preferences,
            "duration_preferences": self.duration_preferences,
            "preferred_difficulty_levels": self.preferred_difficulty_levels,
            "learning_pace_preference": self.learning_pace_preference,
            "session_duration_preference": self.session_duration_preference,
            "active_time_patterns": self.active_time_patterns,
            "learning_frequency_preference": self.learning_frequency_preference,
            "optimal_learning_times": self.optimal_learning_times,
            "completion_rate_by_subject": self.completion_rate_by_subject,
            "dropout_points": self.dropout_points,
            "retry_patterns": self.retry_patterns,
            "skipping_patterns": self.skipping_patterns,
            "collaboration_preference": self.collaboration_preference,
            "peer_learning_engagement": self.peer_learning_engagement,
            "discussion_participation": self.discussion_participation,
            "learning_goal_orientation": self.learning_goal_orientation,
            "goal_specificity": self.goal_specificity,
            "progress_tracking_preference": self.progress_tracking_preference,
            "information_density_preference": self.information_density_preference,
            "multimedia_preference": self.multimedia_preference,
            "complexity_handling": self.complexity_handling,
            "feedback_frequency_preference": self.feedback_frequency_preference,
            "feedback_type_preference": self.feedback_type_preference,
            "motivation_feedback_preference": self.motivation_feedback_preference,
            "experiment_groups": self.experiment_groups,
            "preference_stability_score": self.preference_stability_score,
            "preference_confidence": self.preference_confidence,
            "last_preference_update": self.last_preference_update.isoformat() if self.last_preference_update else None,
            "preference_version": self.preference_version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class LearningBehaviorPattern(Base):
    """Model for tracking detailed learning behavior patterns"""
    __tablename__ = "learning_behavior_patterns"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, index=True)
    
    # Pattern identification
    pattern_type = Column(String(50), nullable=False, index=True)  # session_pattern, learning_rhythm, difficulty_progression
    pattern_name = Column(String(100), nullable=True)  # Descriptive name for the pattern
    pattern_description = Column(Text, nullable=True)  # Detailed description
    
    # Pattern characteristics
    pattern_data = Column(JSON, nullable=False)  # Pattern-specific data structure
    pattern_frequency = Column(Float, nullable=True)  # How often this pattern occurs (0-1)
    pattern_strength = Column(Float, nullable=True)  # Strength of the pattern (0-1)
    
    # Temporal aspects
    pattern_start_date = Column(DateTime, nullable=True)
    pattern_end_date = Column(DateTime, nullable=True)
    last_observed = Column(DateTime, nullable=True, index=True)
    
    # Confidence and validation
    confidence_score = Column(Float, nullable=True)  # Confidence in pattern detection (0-1)
    validation_count = Column(Integer, nullable=False, default=0)  # Number of times pattern validated
    violation_count = Column(Integer, nullable=False, default=0)  # Number of times pattern violated
    
    # Pattern metadata
    algorithm_used = Column(String(50), nullable=True)  # Algorithm that detected this pattern
    features_used = Column(JSON, nullable=True)  # Features used to detect pattern
    pattern_version = Column(Integer, nullable=False, default=1)
    
    # Adaptability
    is_adaptive = Column(Boolean, nullable=False, default=False)  # Whether pattern can adapt
    adaptation_rate = Column(Float, nullable=True)  # Rate of adaptation (0-1)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('ix_learning_pattern_user_type', 'user_id', 'pattern_type'),
        Index('ix_learning_pattern_last_observed', 'last_observed'),
        Index('ix_learning_pattern_strength', 'pattern_strength'),
        Index('ix_learning_pattern_confidence', 'confidence_score'),
    )
    
    def __repr__(self):
        return f"<LearningBehaviorPattern(user_id='{self.user_id}', type='{self.pattern_type}', strength={self.pattern_strength})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for analysis"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pattern_type": self.pattern_type,
            "pattern_name": self.pattern_name,
            "pattern_description": self.pattern_description,
            "pattern_data": self.pattern_data,
            "pattern_frequency": self.pattern_frequency,
            "pattern_strength": self.pattern_strength,
            "pattern_start_date": self.pattern_start_date.isoformat() if self.pattern_start_date else None,
            "pattern_end_date": self.pattern_end_date.isoformat() if self.pattern_end_date else None,
            "last_observed": self.last_observed.isoformat() if self.last_observed else None,
            "confidence_score": self.confidence_score,
            "validation_count": self.validation_count,
            "violation_count": self.violation_count,
            "algorithm_used": self.algorithm_used,
            "features_used": self.features_used,
            "pattern_version": self.pattern_version,
            "is_adaptive": self.is_adaptive,
            "adaptation_rate": self.adaptation_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class UserSkillProfile(Base):
    """Model for tracking user skill levels and competency progression"""
    __tablename__ = "user_skill_profiles"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, index=True)
    
    # Skill identification
    skill_category = Column(String(50), nullable=False, index=True)  # subject, topic, concept, competency
    skill_identifier = Column(String(100), nullable=False)  # ID of the skill (subject_id, concept_id, etc.)
    skill_name = Column(String(255), nullable=True)  # Human-readable skill name
    
    # Skill metrics
    current_level = Column(Integer, nullable=False, default=1)  # Skill level 1-5
    proficiency_score = Column(Float, nullable=True)  # Detailed proficiency score 0-1
    confidence_level = Column(Float, nullable=True)  # User's confidence in this skill 0-1
    
    # Learning trajectory
    progression_rate = Column(Float, nullable=True)  # Rate of skill improvement per week
    mastery_velocity = Column(Float, nullable=True)  # How quickly user achieves mastery
    plateau_duration = Column(Integer, nullable=True)  # Days at current level before progression
    
    # Learning patterns
    preferred_difficulty_progression = Column(String(20), nullable=True)  # gradual, immediate, mixed
    skill_decay_rate = Column(Float, nullable=True)  # Rate of skill decay over time
    retention_score = Column(Float, nullable=True)  # How well user retains this skill
    
    # Learning strategies
    effective_strategies = Column(JSON, nullable=True)  # Strategies that work well for this skill
    ineffective_strategies = Column(JSON, nullable=True)  # Strategies that don't work
    strategy_adaptation = Column(Float, nullable=True)  # How well user adapts strategies
    
    # Context and conditions
    optimal_learning_conditions = Column(JSON, nullable=True)  # Best conditions for learning this skill
    challenging_factors = Column(JSON, nullable=True)  # Factors that make this skill challenging
    support_requirements = Column(JSON, nullable=True)  # Support needed for this skill
    
    # Performance metrics
    success_rate = Column(Float, nullable=True)  # Success rate on skill-related tasks
    error_patterns = Column(JSON, nullable=True)  # Common error patterns
    improvement_areas = Column(JSON, nullable=True)  # Areas needing improvement
    
    # Social learning aspects
    peer_comparison_level = Column(String(20), nullable=True)  # below_average, average, above_average, expert
    collaboration_effectiveness = Column(Float, nullable=True)  # How well user learns with others
    teaching_effectiveness = Column(Float, nullable=True)  # How well user can teach others
    
    # Timestamps
    first_assessed = Column(DateTime, nullable=True)
    last_assessed = Column(DateTime, nullable=True, index=True)
    last_practiced = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('ix_user_skill_user_category', 'user_id', 'skill_category'),
        Index('ix_user_skill_identifier', 'skill_identifier'),
        Index('ix_user_skill_level', 'current_level'),
        Index('ix_user_skill_proficiency', 'proficiency_score'),
        Index('ix_user_skill_last_assessed', 'last_assessed'),
        UniqueConstraint('user_id', 'skill_category', 'skill_identifier', name='uq_user_skill')
    )
    
    def __repr__(self):
        return f"<UserSkillProfile(user_id='{self.user_id}', skill='{self.skill_identifier}', level={self.current_level})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for skill tracking"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "skill_category": self.skill_category,
            "skill_identifier": self.skill_identifier,
            "skill_name": self.skill_name,
            "current_level": self.current_level,
            "proficiency_score": self.proficiency_score,
            "confidence_level": self.confidence_level,
            "progression_rate": self.progression_rate,
            "mastery_velocity": self.mastery_velocity,
            "plateau_duration": self.plateau_duration,
            "preferred_difficulty_progression": self.preferred_difficulty_progression,
            "skill_decay_rate": self.skill_decay_rate,
            "retention_score": self.retention_score,
            "effective_strategies": self.effective_strategies,
            "ineffective_strategies": self.ineffective_strategies,
            "strategy_adaptation": self.strategy_adaptation,
            "optimal_learning_conditions": self.optimal_learning_conditions,
            "challenging_factors": self.challenging_factors,
            "support_requirements": self.support_requirements,
            "success_rate": self.success_rate,
            "error_patterns": self.error_patterns,
            "improvement_areas": self.improvement_areas,
            "peer_comparison_level": self.peer_comparison_level,
            "collaboration_effectiveness": self.collaboration_effectiveness,
            "teaching_effectiveness": self.teaching_effectiveness,
            "first_assessed": self.first_assessed.isoformat() if self.first_assessed else None,
            "last_assessed": self.last_assessed.isoformat() if self.last_assessed else None,
            "last_practiced": self.last_practiced.isoformat() if self.last_practiced else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class LearningGoal(Base):
    """Model for tracking user learning goals and progress"""
    __tablename__ = "learning_goals"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, index=True)
    
    # Goal identification
    goal_type = Column(String(50), nullable=False, index=True)  # mastery, completion, skill_acquisition, certification
    goal_category = Column(String(50), nullable=True)  # subject, skill, competency
    goal_identifier = Column(String(100), nullable=True)  # ID of what the goal relates to
    
    # Goal details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal_scope = Column(String(20), nullable=False)  # specific, broad, exploratory
    
    # Target and metrics
    target_value = Column(Float, nullable=True)  # Target proficiency score, completion percentage, etc.
    current_value = Column(Float, nullable=True, default=0.0)  # Current progress
    measurement_unit = Column(String(50), nullable=True)  # percentage, score, level, hours
    
    # Timeline
    target_completion_date = Column(DateTime, nullable=True, index=True)
    estimated_completion_date = Column(DateTime, nullable=True)
    actual_completion_date = Column(DateTime, nullable=True)
    
    # Priority and importance
    priority_level = Column(Integer, nullable=False, default=3)  # 1=high, 5=low
    importance_score = Column(Float, nullable=True)  # 0-1 importance to user
    motivation_level = Column(Float, nullable=True)  # 0-1 current motivation
    
    # Progress tracking
    progress_percentage = Column(Float, nullable=False, default=0.0)  # 0-100
    milestones = Column(JSON, nullable=True)  # List of milestone definitions
    completed_milestones = Column(JSON, nullable=True)  # List of completed milestones
    
    # Strategy and approach
    learning_strategy = Column(String(50), nullable=True)  # Self-paced, guided, mixed
    resource_preferences = Column(JSON, nullable=True)  # Preferred types of learning resources
    support_requirements = Column(JSON, nullable=True)  # Support needed to achieve goal
    
    # Constraints and considerations
    time_constraints = Column(JSON, nullable=True)  # Available time windows
    difficulty_preferences = Column(String(20), nullable=True)  # preferred difficulty level
    learning_style_alignment = Column(Float, nullable=True)  # How well goal aligns with learning style
    
    # Outcome tracking
    success_criteria = Column(JSON, nullable=True)  # What constitutes goal achievement
    success_probability = Column(Float, nullable=True)  # Estimated probability of success
    risk_factors = Column(JSON, nullable=True)  # Factors that might prevent goal achievement
    
    # Status and state
    goal_status = Column(String(20), nullable=False, default='active', index=True)  # active, paused, completed, abandoned
    last_progress_update = Column(DateTime, nullable=True)
    progress_update_frequency = Column(String(20), nullable=True)  # daily, weekly, monthly
    
    # Feedback and reflection = Column(Text,
    reflection_notes nullable=True)  # User reflections on progress
    feedback_received = Column(JSON, nullable=True)  # Feedback from instructors/peers
    goal_satisfaction = Column(Float, nullable=True)  # User satisfaction with goal progress
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('ix_learning_goal_user_status', 'user_id', 'goal_status'),
        Index('ix_learning_goal_target_date', 'target_completion_date'),
        Index('ix_learning_goal_priority', 'priority_level'),
        Index('ix_learning_goal_progress', 'progress_percentage'),
        Index('ix_learning_goal_type', 'goal_type'),
    )
    
    def __repr__(self):
        return f"<LearningGoal(user_id='{self.user_id}', title='{self.title}', progress={self.progress_percentage}%)>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for goal tracking"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "goal_type": self.goal_type,
            "goal_category": self.goal_category,
            "goal_identifier": self.goal_identifier,
            "title": self.title,
            "description": self.description,
            "goal_scope": self.goal_scope,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "measurement_unit": self.measurement_unit,
            "target_completion_date": self.target_completion_date.isoformat() if self.target_completion_date else None,
            "estimated_completion_date": self.estimated_completion_date.isoformat() if self.estimated_completion_date else None,
            "actual_completion_date": self.actual_completion_date.isoformat() if self.actual_completion_date else None,
            "priority_level": self.priority_level,
            "importance_score": self.importance_score,
            "motivation_level": self.motivation_level,
            "progress_percentage": self.progress_percentage,
            "milestones": self.milestones,
            "completed_milestones": self.completed_milestones,
            "learning_strategy": self.learning_strategy,
            "resource_preferences": self.resource_preferences,
            "support_requirements": self.support_requirements,
            "time_constraints": self.time_constraints,
            "difficulty_preferences": self.difficulty_preferences,
            "learning_style_alignment": self.learning_style_alignment,
            "success_criteria": self.success_criteria,
            "success_probability": self.success_probability,
            "risk_factors": self.risk_factors,
            "goal_status": self.goal_status,
            "last_progress_update": self.last_progress_update.isoformat() if self.last_progress_update else None,
            "progress_update_frequency": self.progress_update_frequency,
            "reflection_notes": self.reflection_notes,
            "feedback_received": self.feedback_received,
            "goal_satisfaction": self.goal_satisfaction,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Utility functions for profile management
def calculate_learning_velocity(user_interactions: List, time_window_days: int = 30) -> float:
    """Calculate user's learning velocity (concepts mastered per week)"""
    try:
        if not user_interactions:
            return 0.0
        
        cutoff_date = datetime.utcnow() - timedelta(days=time_window_days)
        recent_interactions = [i for i in user_interactions if i.timestamp >= cutoff_date]
        
        # Count completed concepts
        completed_concepts = set()
        for interaction in recent_interactions:
            if interaction.interaction_type == 'complete':
                completed_concepts.add(interaction.content_id)
        
        # Calculate velocity per week
        weeks = time_window_days / 7.0
        velocity = len(completed_concepts) / weeks if weeks > 0 else 0.0
        
        return max(0.0, velocity)
        
    except Exception as e:
        logger.error(f"Error calculating learning velocity: {e}")
        return 0.0

def calculate_engagement_score(interactions: List, content_item) -> float:
    """Calculate engagement score for content based on user interactions"""
    try:
        if not interactions:
            return 0.0
        
        # Interaction weights
        weights = {
            'view': 1.0,
            'like': 3.0,
            'complete': 5.0,
            'share': 2.0,
            'rate': 4.0
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for interaction in interactions:
            weight = weights.get(interaction.interaction_type, 1.0)
            total_score += interaction.value * weight
            total_weight += weight
        
        # Add time factor (recent interactions weigh more)
        recent_interactions = [i for i in interactions if i.timestamp >= datetime.utcnow() - timedelta(days=7)]
        time_bonus = len(recent_interactions) / len(interactions) if interactions else 0.0
        
        # Normalize score
        base_score = total_score / total_weight if total_weight > 0 else 0.0
        final_score = base_score * (1.0 + time_bonus)
        
        return max(0.0, final_score)
        
    except Exception as e:
        logger.error(f"Error calculating engagement score: {e}")
        return 0.0

def update_subject_preferences(user_profile, interactions: List, content_items: Dict):
    """Update subject preferences based on interaction history"""
    try:
        subject_engagement = {}
        subject_completion = {}
        
        for interaction in interactions:
            if interaction.content_id not in content_items:
                continue
            
            content = content_items[interaction.content_id]
            subject_id = content.subject_id
            
            if subject_id not in subject_engagement:
                subject_engagement[subject_id] = []
                subject_completion[subject_id] = []
            
            # Calculate engagement for this interaction
            engagement = calculate_engagement_score([interaction], content)
            subject_engagement[subject_id].append(engagement)
            
            if interaction.interaction_type == 'complete':
                subject_completion[subject_id].append(1.0)
            else:
                subject_completion[subject_id].append(0.0)
        
        # Calculate preference scores
        subject_preferences = {}
        for subject_id, engagements in subject_engagement.items():
            avg_engagement = sum(engagements) / len(engagements)
            completion_rate = sum(subject_completion.get(subject_id, [0])) / len(engagements)
            
            # Combined preference score
            preference_score = (avg_engagement * 0.7) + (completion_rate * 0.3)
            subject_preferences[subject_id] = preference_score
        
        user_profile.subject_preferences = subject_preferences
        
    except Exception as e:
        logger.error(f"Error updating subject preferences: {e}")

def detect_learning_patterns(user_interactions: List) -> List[Dict[str, Any]]:
    """Detect learning behavior patterns from user interactions"""
    try:
        patterns = []
        
        # Session pattern detection
        sessions = {}
        for interaction in user_interactions:
            session_id = interaction.session_id or f"session_{interaction.user_id}_{interaction.timestamp.date()}"
            if session_id not in sessions:
                sessions[session_id] = []
            sessions[session_id].append(interaction)
        
        # Analyze session patterns
        session_durations = []
        session_sizes = []
        
        for session_id, session_interactions in sessions.items():
            if len(session_interactions) > 1:
                session_interactions.sort(key=lambda x: x.timestamp)
                duration = (session_interactions[-1].timestamp - session_interactions[0].timestamp).total_seconds() / 60
                session_durations.append(duration)
                session_sizes.append(len(session_interactions))
        
        if session_durations:
            patterns.append({
                "pattern_type": "session_pattern",
                "pattern_data": {
                    "avg_session_duration": sum(session_durations) / len(session_durations),
                    "avg_session_size": sum(session_sizes) / len(session_sizes),
                    "session_count": len(session_durations)
                },
                "pattern_strength": min(1.0, len(session_durations) / 10.0)  # More sessions = stronger pattern
            })
        
        # Temporal pattern detection
        hour_activity = {}
        for interaction in user_interactions:
            hour = interaction.timestamp.hour
            hour_activity[hour] = hour_activity.get(hour, 0) + 1
        
        if hour_activity:
            most_active_hour = max(hour_activity.items(), key=lambda x: x[1])
            patterns.append({
                "pattern_type": "temporal_pattern",
                "pattern_data": {
                    "most_active_hour": most_active_hour[0],
                    "activity_distribution": hour_activity
                },
                "pattern_strength": most_active_hour[1] / len(user_interactions)
            })
        
        return patterns
        
    except Exception as e:
        logger.error(f"Error detecting learning patterns: {e}")
        return []