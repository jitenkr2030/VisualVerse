"""
Learner Profile and Concept Mastery Models for VisualVerse Content Metadata Layer

This module provides data models for tracking learner progress, concept mastery levels,
learning sessions, and aggregated analytics. It implements the mathematical foundations
for spaced repetition systems and mastery-based learning.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import uuid


class MasteryLevel(str, Enum):
    """Mastery level classifications"""
    NOVICE = "novice"
    BEGINNER = "beginner"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    EXPERT = "expert"


class InteractionType(str, Enum):
    """Types of learning interactions"""
    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    REVIEW = "review"
    VISUALIZATION = "visualization"
    APPLICATION = "application"


@dataclass
class LearnerProfile:
    """
    Stores the persistent identity and meta-preferences of the learner.
    
    This profile tracks overall learning characteristics including cognitive load
    capacity, learning style preferences, and activity patterns that inform
    adaptive learning decisions.
    """
    profile_id: str
    user_id: str
    
    # Learning style preferences (weights sum to 1.0)
    learning_style_weights: Dict[str, float] = field(default_factory=lambda: {
        "visual": 0.4,
        "textual": 0.3,
        "interactive": 0.3
    })
    
    # Cognitive and scheduling preferences
    cognitive_load_capacity: float = 0.7  # 0.0-1.0, dynamic score
    daily_goal_minutes: int = 30
    preferred_session_duration: int = 15  # minutes
    
    # Activity tracking
    last_active_at: Optional[datetime] = None
    streak_days: int = 0
    total_learning_minutes: int = 0
    total_sessions: int = 0
    
    # Learning velocity tracking
    average_session_duration: float = 15.0
    concepts_per_hour: float = 2.0
    
    def __post_init__(self):
        """Validate and normalize learning style weights"""
        if self.learning_style_weights:
            total = sum(self.learning_style_weights.values())
            if total > 0:
                self.learning_style_weights = {
                    k: v / total for k, v in self.learning_style_weights.items()
                }
    
    @classmethod
    def create(cls, user_id: str) -> "LearnerProfile":
        """Factory method to create a new learner profile"""
        return cls(
            profile_id=str(uuid.uuid4()),
            user_id=user_id,
            learning_style_weights={"visual": 0.4, "textual": 0.3, "interactive": 0.3},
            cognitive_load_capacity=0.7,
            daily_goal_minutes=30,
            preferred_session_duration=15,
            last_active_at=datetime.now(),
            streak_days=0,
            total_learning_minutes=0,
            total_sessions=0
        )
    
    def get_primary_style(self) -> str:
        """Get the primary learning style preference"""
        if not self.learning_style_weights:
            return "visual"
        return max(self.learning_style_weights, key=self.learning_style_weights.get)
    
    def update_activity(self, session_minutes: int) -> None:
        """Update activity metrics after a learning session"""
        self.total_learning_minutes += session_minutes
        self.total_sessions += 1
        self.last_active_at = datetime.now()
        
        # Update rolling averages
        self.average_session_duration = (
            self.average_session_duration * 0.9 + session_minutes * 0.1
        )
    
    def get_retention_target_days(self) -> int:
        """Get the target number of days between reviews based on mastery level"""
        if self.cognitive_load_capacity >= 0.9:
            return 14  # Expert learners can go longer
        elif self.cognitive_load_capacity >= 0.7:
            return 7   # Proficient learners
        elif self.cognitive_load_capacity >= 0.5:
            return 4   # Developing learners
        else:
            return 2   # Novice learners need frequent review


@dataclass
class ConceptMastery:
    """
    The core atomic unit of tracking. One record per user per concept.
    
    This model implements a Spaced Repetition System (SRS) inspired approach
    where each concept has a mastery score, stability factor, and review history.
    The stability factor determines how quickly memory decays and thus when
    reviews should be scheduled.
    """
    mastery_id: str
    learner_id: str
    concept_id: str
    
    # Mastery metrics (0.0 to 1.0 scale)
    mastery_score: float = 0.0  # Current proficiency level
    confidence_score: float = 0.0  # System confidence in this rating
    
    # Spaced repetition parameters
    stability: float = 1.0  # Memory stability (higher = slower decay)
    difficulty_modifier: float = 1.0  # Concept-specific difficulty
    interval_days: int = 1  # Days until next recommended review
    
    # Temporal data
    first_exposure_at: datetime = field(default_factory=datetime.now)
    last_interaction_at: datetime = field(default_factory=datetime.now)
    next_review_at: datetime = field(default_factory=datetime.now)
    last_mastered_at: Optional[datetime] = None
    
    # Interaction history
    interaction_count: int = 0
    successful_interactions: int = 0
    total_session_time_minutes: int = 0
    
    # Mastery history for analytics
    peak_mastery_score: float = 0.0
    mastery_history: List[Dict[str, Any]] = field(default_factory=list)
    
    @classmethod
    def create(cls, learner_id: str, concept_id: str) -> "ConceptMastery":
        """Factory method to create a new concept mastery record"""
        now = datetime.now()
        return cls(
            mastery_id=str(uuid.uuid4()),
            learner_id=learner_id,
            concept_id=concept_id,
            mastery_score=0.0,
            confidence_score=0.0,
            stability=1.0,
            difficulty_modifier=1.0,
            interval_days=1,
            first_exposure_at=now,
            last_interaction_at=now,
            next_review_at=now,
            interaction_count=0,
            successful_interactions=0,
            total_session_time_minutes=0,
            peak_mastery_score=0.0
        )
    
    def get_mastery_level(self) -> MasteryLevel:
        """Determine the mastery level classification"""
        score = self.mastery_score
        
        if score >= 0.95:
            return MasteryLevel.EXPERT
        elif score >= 0.85:
            return MasteryLevel.ADVANCED
        elif score >= 0.70:
            return MasteryLevel.PROFICIENT
        elif score >= 0.50:
            return MasteryLevel.DEVELOPING
        elif score >= 0.25:
            return MasteryLevel.BEGINNER
        else:
            return MasteryLevel.NOVICE
    
    def is_overdue_for_review(self, current_time: Optional[datetime] = None) -> bool:
        """Check if this concept is overdue for review"""
        if current_time is None:
            current_time = datetime.now()
        return current_time >= self.next_review_at
    
    def is_considered_known(self, threshold: float = 0.7) -> bool:
        """Check if this concept is considered known"""
        return self.mastery_score >= threshold
    
    def record_interaction(
        self,
        success: bool,
        interaction_type: InteractionType,
        time_spent_minutes: int,
        difficulty_rating: float = 1.0
    ) -> None:
        """
        Record a new interaction with this concept.
        
        Args:
            success: Whether the interaction was successful
            interaction_type: Type of learning interaction
            time_spent_minutes: Time spent on this interaction
            difficulty_rating: Perceived difficulty (0.5-2.0)
        """
        self.interaction_count += 1
        self.total_session_time_minutes += time_spent_minutes
        self.last_interaction_at = datetime.now()
        
        if success:
            self.successful_interactions += 1
        
        # Record history point
        history_entry = {
            "timestamp": self.last_interaction_at.isoformat(),
            "success": success,
            "type": interaction_type.value,
            "time_spent": time_spent_minutes,
            "score_before": self.mastery_score,
            "difficulty": difficulty_rating
        }
        self.mastery_history.append(history_entry)
        
        # Keep only last 100 entries
        if len(self.mastery_history) > 100:
            self.mastery_history = self.mastery_history[-100:]
        
        # Update peak mastery
        if self.mastery_score > self.peak_mastery_score:
            self.peak_mastery_score = self.mastery_score
        
        # Mark mastered if threshold reached
        if self.mastery_score >= 0.85 and self.last_mastered_at is None:
            self.last_mastered_at = datetime.now()
    
    def get_retention_prediction(
        self,
        days_ahead: int,
        current_time: Optional[datetime] = None
    ) -> float:
        """
        Predict retention probability after a given number of days.
        
        Uses the Ebbinghaus forgetting curve: R = e^(-t/S)
        Where R is retention, t is time elapsed, and S is stability.
        
        Args:
            days_ahead: Number of days in the future
            current_time: Current reference time
            
        Returns:
            Predicted retention probability (0.0-1.0)
        """
        if current_time is None:
            current_time = datetime.now()
        
        # Calculate effective stability considering difficulty
        effective_stability = self.stability * self.difficulty_modifier
        
        # Time since last review in days
        time_since_review = (current_time - self.last_interaction_at).total_seconds() / 86400
        total_days = time_since_review + days_ahead
        
        # Ebbinghaus forgetting curve
        retention = 1.0 if total_days == 0 else pow(2.71828, -total_days / effective_stability)
        
        return max(0.0, min(1.0, retention))


@dataclass
class LearningSession:
    """
    Transient data capturing a specific study block to calculate velocity.
    
    Each session represents a period of focused learning activity and contains
    metrics about performance, focus, and concepts covered.
    """
    session_id: str
    learner_id: str
    start_time: datetime
    end_time: datetime
    
    # Session content
    concepts_covered: List[str] = field(default_factory=list)
    interactions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Session metrics
    accuracy_rate: float = 0.0  # 0.0-1.0, percentage correct
    focus_score: float = 0.8  # Inferred from interaction timing
    completion_rate: float = 1.0  # How much of planned content was completed
    
    # Time metrics
    total_pause_duration_minutes: int = 0
    active_learning_time_minutes: int = 0
    
    # Derived metrics
    concepts_learned: int = 0
    concepts_reviewed: int = 0
    
    @classmethod
    def create(cls, learner_id: str) -> "LearningSession":
        """Factory method to create a new learning session"""
        now = datetime.now()
        return cls(
            session_id=str(uuid.uuid4()),
            learner_id=learner_id,
            start_time=now,
            end_time=now,
            concepts_covered=[],
            interactions=[],
            accuracy_rate=0.0,
            focus_score=0.8,
            completion_rate=1.0
        )
    
    def complete_session(self) -> None:
        """Finalize the session and calculate metrics"""
        self.end_time = datetime.now()
        
        # Calculate active learning time
        duration = (self.end_time - self.start_time).total_seconds() / 60
        self.active_learning_time_minutes = max(1, int(duration - self.total_pause_duration_minutes))
        
        # Calculate accuracy rate
        if self.interactions:
            successful = sum(1 for i in self.interactions if i.get("success", False))
            self.accuracy_rate = successful / len(self.interactions)
        
        # Count concepts learned vs reviewed
        self.concepts_learned = len([c for c in self.concepts_covered if c not in 
                                     [i.get("concept_id") for i in self.interactions 
                                      if i.get("type") == "review"]])
        self.concepts_reviewed = len([c for c in self.concepts_covered if c in 
                                      [i.get("concept_id") for i in self.interactions 
                                       if i.get("type") == "review"]])
    
    def add_interaction(
        self,
        concept_id: str,
        interaction_type: InteractionType,
        success: bool,
        time_spent_seconds: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an interaction record to this session"""
        self.interactions.append({
            "concept_id": concept_id,
            "type": interaction_type.value,
            "success": success,
            "time_spent_seconds": time_spent_seconds,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        if concept_id not in self.concepts_covered:
            self.concepts_covered.append(concept_id)
    
    def get_duration_minutes(self) -> int:
        """Get session duration in minutes"""
        duration = (self.end_time - self.start_time).total_seconds() / 60
        return max(1, int(duration))


@dataclass
class MasteryMetrics:
    """
    Aggregated analytics for reporting and high-level adjustments.
    
    These metrics provide an overview of a learner's progress across all concepts
    and are used for course-level adjustments and progress reporting.
    """
    learner_id: str
    calculated_at: datetime
    
    # Global averages
    global_mastery_average: float = 0.0
    global_confidence_average: float = 0.0
    
    # Velocity metrics
    learning_velocity: float = 0.0  # Mastery points gained per hour
    concepts_learned_per_week: float = 0.0
    average_session_score: float = 0.0
    
    # Retention metrics
    retention_rate_7day: float = 0.0  # 7-day rolling average
    retention_rate_30day: float = 0.0  # 30-day rolling average
    average_stability: float = 1.0
    
    # Progress metrics
    total_concepts_started: int = 0
    total_concepts_mastered: int = 0
    concepts_in_progress: int = 0
    concepts_due_for_review: int = 0
    
    # Weakness analysis
    weakest_domain: Optional[str] = None
    strongest_domain: Optional[str] = None
    struggling_concepts: List[str] = field(default_factory=list)
    
    # Streak and engagement
    current_streak_days: int = 0
    average_weekly_sessions: float = 0.0
    average_weekly_minutes: float = 0.0
    
    @classmethod
    def create(cls, learner_id: str) -> "MasteryMetrics":
        """Factory method to create initial metrics record"""
        return cls(
            learner_id=learner_id,
            calculated_at=datetime.now()
        )
    
    def update_from_mastery_records(
        self,
        mastery_records: List[ConceptMastery],
        domain_map: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Update metrics from a list of concept mastery records.
        
        Args:
            mastery_records: List of ConceptMastery records
            domain_map: Optional mapping of concept_id to domain/category
        """
        if not mastery_records:
            return
        
        # Calculate global averages
        self.global_mastery_average = sum(m.mastery_score for m in mastery_records) / len(mastery_records)
        self.global_confidence_average = sum(m.confidence_score for m in mastery_records) / len(mastery_records)
        self.average_stability = sum(m.stability for m in mastery_records) / len(mastery_records)
        
        # Count concepts by status
        mastered = [m for m in mastery_records if m.is_considered_known()]
        self.total_concepts_mastered = len(mastered)
        self.total_concepts_started = len(mastery_records)
        self.concepts_in_progress = len(mastery_records) - self.total_concepts_mastered
        
        # Count concepts due for review
        now = datetime.now()
        due = [m for m in mastery_records if m.is_overdue_for_review(now)]
        self.concepts_due_for_review = len(due)
        
        # Identify struggling concepts (low mastery but high interaction count)
        struggling = [
            m.concept_id for m in mastery_records
            if m.mastery_score < 0.5 and m.interaction_count >= 3
        ]
        self.struggling_concepts = struggling[:10]  # Top 10
        
        # Calculate domain-level averages
        if domain_map:
            domain_scores: Dict[str, List[float]] = {}
            for m in mastery_records:
                domain = domain_map.get(m.concept_id, "uncategorized")
                if domain not in domain_scores:
                    domain_scores[domain] = []
                domain_scores[domain].append(m.mastery_score)
            
            if domain_scores:
                domain_averages = {
                    d: sum(scores) / len(scores) 
                    for d, scores in domain_scores.items()
                }
                self.weakest_domain = min(domain_averages, key=domain_averages.get) if domain_averages else None
                self.strongest_domain = max(domain_averages, key=domain_averages.get) if domain_averages else None
        
        self.calculated_at = datetime.now()
    
    def get_mastery_distribution(self) -> Dict[str, int]:
        """Get count of concepts at each mastery level"""
        return {
            "novice": 0,
            "beginner": 0,
            "developing": 0,
            "proficient": 0,
            "advanced": 0,
            "expert": 0
        }
    
    def get_progress_percentage(self) -> float:
        """Get overall progress as a percentage (0.0-1.0)"""
        if self.total_concepts_started == 0:
            return 0.0
        return self.total_concepts_mastered / self.total_concepts_started


@dataclass
class InteractionResult:
    """
    Result of a learning interaction for mastery calculation.
    
    This is a data transfer object passed to the mastery update algorithm
    containing all relevant information about the learner's performance.
    """
    concept_id: str
    interaction_type: InteractionType
    success: bool
    score: float  # 0.0-1.0, raw score on the assessment
    time_spent_seconds: int
    difficulty_rating: float = 1.0  # Perceived difficulty 0.5-2.0
    attempt_number: int = 1
    
    # Context
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate and normalize values"""
        self.score = max(0.0, min(1.0, self.score))
        self.difficulty_rating = max(0.5, min(2.0, self.difficulty_rating))


@dataclass
class ReviewSchedule:
    """
    A scheduled review item for spaced repetition.
    
    This model represents a single scheduled review with its priority
    and optimal timing information.
    """
    concept_id: str
    concept_name: str
    scheduled_date: datetime
    priority_score: float  # 0.0-1.0, higher = more urgent
    current_mastery: float
    predicted_decay: float  # Expected retention drop by scheduled date
    domain: str
    has_visual_aid: bool = False
    asset_id: Optional[str] = None
    
    @classmethod
    def create(
        cls,
        concept_id: str,
        concept_name: str,
        mastery_record: ConceptMastery,
        priority_score: float,
        domain: str = "general",
        has_visual_aid: bool = False,
        asset_id: Optional[str] = None
    ) -> "ReviewSchedule":
        """Factory method to create a review schedule from mastery record"""
        return cls(
            concept_id=concept_id,
            concept_name=concept_name,
            scheduled_date=mastery_record.next_review_at,
            priority_score=priority_score,
            current_mastery=mastery_record.mastery_score,
            predicted_decay=1.0 - mastery_record.get_retention_prediction(
                (mastery_record.next_review_at - datetime.now()).days
            ),
            domain=domain,
            has_visual_aid=has_visual_aid,
            asset_id=asset_id
        )
