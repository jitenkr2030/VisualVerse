"""
Mastery Service for VisualVerse Content Metadata Layer

This service implements the concept-mastery tracking functionality including
mastery score calculation algorithms, spaced repetition scheduling, weakness
detection, and retention prediction. It integrates with the learning path and
recommendation services to provide personalized learning experiences.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import math

from .learning_path_service import DependencyGraph
from .reasoning_engine import ReasoningEngine
from .animation_service import AnimationMetadataService
from ..models.learner_profile import (
    LearnerProfile,
    ConceptMastery,
    LearningSession,
    MasteryMetrics,
    InteractionResult,
    ReviewSchedule,
    MasteryLevel,
    InteractionType
)
from ..models.concept import Concept


logger = logging.getLogger(__name__)


@dataclass
class MasteryServiceStats:
    """Statistics for the mastery service"""
    total_mastery_updates: int = 0
    total_concepts_tracked: int = 0
    average_calculation_time_ms: float = 0.0
    weak_concepts_detected: int = 0
    reviews_scheduled: int = 0


class MasteryService:
    """
    Service for tracking and calculating concept mastery levels.
    
    This service implements the mathematical algorithms for:
    - Bayesian-inspired mastery score updates
    - Ebbinghaus forgetting curve retention prediction
    - Spaced repetition scheduling
    - Weak concept detection
    - Integration with learning path generation
    """
    
    # Algorithm constants
    INITIAL_MASTERY = 0.0
    INITIAL_CONFIDENCE = 0.0
    MIN_CONFIDENCE_THRESHOLD = 0.3  # Below this, system is uncertain
    
    # Learning rate parameters
    BASE_LEARNING_RATE = 0.3
    SUCCESS_BOOST = 0.1
    FAIL_PENALTY = 0.2
    
    # Spaced repetition parameters
    MIN_INTERVAL_DAYS = 1
    MAX_INTERVAL_DAYS = 365
    EASY_MULTIPLIER = 2.5
    HARD_MULTIPLIER = 1.5
    NORMAL_MULTIPLIER = 2.0
    
    # Decay parameters
    DEFAULT_STABILITY = 10.0  # Days until retention drops to ~37%
    STABILITY_GAIN_ON_SUCCESS = 1.2
    STABILITY_LOSS_ON_FAIL = 0.8
    MIN_STABILITY = 1.0
    
    def __init__(
        self,
        graph_engine: Optional[DependencyGraph] = None,
        reasoning_engine: Optional[ReasoningEngine] = None,
        animation_service: Optional[AnimationMetadataService] = None
    ):
        """
        Initialize the mastery service.
        
        Args:
            graph_engine: Optional dependency graph engine for path integration
            reasoning_engine: Optional reasoning engine for gap detection
            animation_service: Optional animation service for visual aids
        """
        self.graph = graph_engine
        self.reasoning = reasoning_engine or ReasoningEngine()
        self.animation = animation_service or AnimationMetadataService()
        
        # In-memory storage (would be replaced with database in production)
        self._learner_profiles: Dict[str, LearnerProfile] = {}
        self._concept_mastery: Dict[str, Dict[str, ConceptMastery]] = defaultdict(dict)  # learner_id -> concept_id -> record
        self._sessions: Dict[str, LearningSession] = {}
        
        # Statistics
        self._stats = MasteryServiceStats()
    
    # =========================================================================
    # Profile Management
    # =========================================================================
    
    def get_or_create_learner_profile(self, user_id: str) -> LearnerProfile:
        """Get or create a learner profile"""
        if user_id in self._learner_profiles:
            profile = self._learner_profiles[user_id]
            profile.last_active = datetime.now()
            return profile
        
        profile = LearnerProfile.create(user_id)
        self._learner_profiles[user_id] = profile
        
        logger.info(f"Created learner profile for user {user_id}")
        return profile
    
    def get_learner_profile(self, user_id: str) -> Optional[LearnerProfile]:
        """Get a learner profile if it exists"""
        return self._learner_profiles.get(user_id)
    
    def update_learner_profile(
        self,
        user_id: str,
        learning_styles: Optional[Dict[str, float]] = None,
        daily_goal_minutes: Optional[int] = None,
        session_duration: Optional[int] = None
    ) -> Optional[LearnerProfile]:
        """Update learner profile preferences"""
        profile = self.get_or_create_learner_profile(user_id)
        
        if learning_styles is not None:
            profile.learning_style_weights = learning_styles
        
        if daily_goal_minutes is not None:
            profile.daily_goal_minutes = daily_goal_minutes
        
        if session_duration is not None:
            profile.preferred_session_duration = session_duration
        
        return profile
    
    # =========================================================================
    # Concept Mastery Management
    # =========================================================================
    
    def get_concept_mastery(
        self,
        learner_id: str,
        concept_id: str
    ) -> Optional[ConceptMastery]:
        """Get mastery record for a specific concept"""
        learner_mastery = self._concept_mastery.get(learner_id, {})
        return learner_mastery.get(concept_id)
    
    def get_all_mastery(
        self,
        learner_id: str,
        include_overdue: bool = True
    ) -> List[ConceptMastery]:
        """Get all mastery records for a learner"""
        records = list(self._concept_mastery.get(learner_id, {}).values())
        
        if not include_overdue:
            now = datetime.now()
            records = [r for r in records if not r.is_overdue_for_review(now)]
        
        return records
    
    def get_mastery_for_concepts(
        self,
        learner_id: str,
        concept_ids: List[str]
    ) -> Dict[str, ConceptMastery]:
        """Get mastery records for multiple concepts"""
        result = {}
        learner_mastery = self._concept_mastery.get(learner_id, {})
        
        for concept_id in concept_ids:
            if concept_id in learner_mastery:
                result[concept_id] = learner_mastery[concept_id]
        
        return result
    
    def ensure_concept_mastery(
        self,
        learner_id: str,
        concept_id: str
    ) -> ConceptMastery:
        """Ensure a mastery record exists for a concept, creating if needed"""
        existing = self.get_concept_mastery(learner_id, concept_id)
        if existing:
            return existing
        
        record = ConceptMastery.create(learner_id, concept_id)
        self._concept_mastery[learner_id][concept_id] = record
        self._stats.total_concepts_tracked += 1
        
        return record
    
    # =========================================================================
    # Mastery Update Algorithm
    # =========================================================================
    
    def update_mastery(
        self,
        learner_id: str,
        interaction_result: InteractionResult
    ) -> ConceptMastery:
        """
        Update mastery score based on a learning interaction.
        
        This implements the core mastery calculation algorithm:
        1. Apply retention decay based on time since last interaction
        2. Calculate performance-based update using Bayesian approach
        3. Update stability for spaced repetition scheduling
        
        Args:
            learner_id: Learner identifier
            interaction_result: Details of the interaction
            
        Returns:
            Updated ConceptMastery record
        """
        # Ensure mastery record exists
        mastery = self.ensure_concept_mastery(
            learner_id,
            interaction_result.concept_id
        )
        
        # Step 1: Apply retention decay based on time since last interaction
        time_since_last = (
            datetime.now() - mastery.last_interaction_at
        ).total_seconds() / 86400  # Convert to days
        
        if time_since_last > 0.1:  # Only apply if more than ~2.4 hours have passed
            # Ebbinghaus decay: R = e^(-t/S)
            decay_factor = math.exp(-time_since_last / mastery.stability)
            mastery.mastery_score = mastery.mastery_score * decay_factor
        
        # Step 2: Calculate performance-based update
        # Bayesian update: M_new = M_old + alpha * (P - M_old) * C
        # where P is performance, C is confidence factor
        
        # Calculate learning rate based on difficulty
        difficulty_factor = 1.0 / interaction_result.difficulty_rating
        alpha = self.BASE_LEARNING_RATE * difficulty_factor
        
        # Confidence increases with interaction count, capped at 1.0
        confidence_boost = min(0.3, mastery.interaction_count * 0.02)
        confidence_factor = mastery.confidence_score + confidence_boost + 0.2
        
        # Calculate update
        if interaction_result.success:
            # Successful interaction increases mastery
            update = alpha * (interaction_result.score - mastery.mastery_score) * confidence_factor
            update += self.SUCCESS_BOOST * (1 - mastery.difficulty_modifier) * 0.1
            mastery.mastery_score = min(1.0, mastery.mastery_score + update)
        else:
            # Failed interaction decreases mastery
            update = -self.FAIL_PENALTY * mastery.mastery_score * confidence_factor
            mastery.mastery_score = max(0.0, mastery.mastery_score + update)
        
        # Step 3: Update confidence
        # Confidence grows faster with consistent results
        if interaction_result.success:
            mastery.confidence_score = min(
                1.0,
                mastery.confidence_score + 0.05 * confidence_factor
            )
        else:
            # Confidence decreases slightly on failure
            mastery.confidence_score = max(
                0.1,
                mastery.confidence_score - 0.02
            )
        
        # Step 4: Update stability for spaced repetition
        self._update_stability(mastery, interaction_result)
        
        # Step 5: Calculate next review date
        self._calculate_next_review(mastery)
        
        # Step 6: Record the interaction
        mastery.record_interaction(
            success=interaction_result.success,
            interaction_type=interaction_result.interaction_type,
            time_spent_minutes=int(interaction_result.time_spent_seconds / 60),
            difficulty_rating=interaction_result.difficulty_rating
        )
        
        self._stats.total_mastery_updates += 1
        
        return mastery
    
    def _update_stability(
        self,
        mastery: ConceptMastery,
        result: InteractionResult
    ) -> None:
        """Update stability factor based on performance"""
        if result.success:
            # Stability increases with successful reviews
            multiplier = self.EASY_MULTIPLIER if result.score > 0.9 else (
                self.HARD_MULTIPLIER if result.score < 0.6 else self.NORMAL_MULTIPLIER
            )
            mastery.stability = min(
                mastery.stability * multiplier,
                self.MAX_INTERVAL_DAYS
            )
        else:
            # Stability decreases on failure
            mastery.stability = max(
                mastery.stability * self.STABILITY_LOSS_ON_FAIL,
                self.MIN_STABILITY
            )
        
        # Adjust interval based on difficulty
        mastery.interval_days = max(
            self.MIN_INTERVAL_DAYS,
            int(mastery.stability / mastery.difficulty_modifier)
        )
    
    def _calculate_next_review(self, mastery: ConceptMastery) -> None:
        """Calculate the next review date based on current state"""
        # Base interval on stability
        base_interval = mastery.interval_days
        
        # Adjust for confidence (higher confidence = longer interval)
        confidence_multiplier = 0.5 + (mastery.confidence_score * 1.5)
        
        # Adjust for mastery level
        if mastery.mastery_score >= 0.95:
            interval_multiplier = 2.0  # Expert level, reviews can be sparse
        elif mastery.mastery_score >= 0.85:
            interval_multiplier = 1.5  # Advanced level
        elif mastery.mastery_score >= 0.70:
            interval_multiplier = 1.2  # Proficient level
        else:
            interval_multiplier = 1.0  # Still learning
        
        # Calculate next review date
        next_interval = int(base_interval * confidence_multiplier * interval_multiplier)
        next_interval = min(max(next_interval, 1), self.MAX_INTERVAL_DAYS)
        
        mastery.next_review_at = datetime.now() + timedelta(days=next_interval)
    
    # =========================================================================
    # Mastery Calculation Utilities
    # =========================================================================
    
    def calculate_mastery_level(
        self,
        mastery_records: List[Dict[str, Any]]
    ) -> float:
        """
        Recompute mastery level from historical interaction data.
        
        This is used for data repair or calibration, computing mastery
        from scratch using a time-weighted moving average.
        
        Args:
            mastery_records: List of historical interaction records
            
        Returns:
            Computed mastery score (0.0-1.0)
        """
        if not mastery_records:
            return 0.0
        
        # Sort by timestamp
        sorted_records = sorted(
            mastery_records,
            key=lambda r: r.get("timestamp", ""),
            reverse=True
        )
        
        # Time-weighted moving average (recent events = 70% weight)
        weighted_sum = 0.0
        total_weight = 0.0
        decay_weight = 0.7  # Weight decay per step
        
        for i, record in enumerate(sorted_records):
            weight = pow(decay_weight, i)
            score = record.get("score", 0.5) if record.get("success", True) else record.get("score", 0.0)
            
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def calculate_retention_curve(
        self,
        learner_id: str,
        concept_id: str,
        days_ahead: int = 30
    ) -> Dict[int, float]:
        """
        Calculate predicted retention over a time period.
        
        Returns a dictionary mapping days ahead to predicted retention.
        
        Args:
            learner_id: Learner identifier
            concept_id: Concept identifier
            days_ahead: Number of days to predict
            
        Returns:
            Dictionary of day -> retention probability
        """
        mastery = self.get_concept_mastery(learner_id, concept_id)
        
        if not mastery:
            # No data, assume rapid decay
            return {d: max(0.0, 1.0 - (d * 0.1)) for d in range(days_ahead + 1)}
        
        predictions = {}
        current_time = datetime.now()
        
        for day in range(days_ahead + 1):
            retention = mastery.get_retention_prediction(day, current_time)
            predictions[day] = retention
        
        return predictions
    
    def calculate_review_priority(
        self,
        learner_id: str,
        concept_id: str,
        current_mastery: float
    ) -> float:
        """
        Calculate priority score for a review recommendation.
        
        Higher priority = more urgent to review.
        
        Args:
            learner_id: Learner identifier
            concept_id: Concept identifier
            current_mastery: Current mastery level
            
        Returns:
            Priority score (0.0-1.0)
        """
        mastery = self.get_concept_mastery(learner_id, concept_id)
        
        if not mastery:
            return 0.5  # Neutral priority for unstarted concepts
        
        # Factors:
        # 1. Time overdue (0-0.3)
        # 2. Decay rate (0-0.3)
        # 3. Concept importance (0-0.2)
        # 4. Current mastery level (0-0.2)
        
        priority = 0.0
        
        # Time overdue factor
        now = datetime.now()
        if mastery.is_overdue_for_review(now):
            days_overdue = (now - mastery.next_review_at).days
            priority += min(0.3, days_overdue * 0.05)
        
        # Decay prediction
        decay_7day = mastery.get_retention_prediction(7, now)
        if decay_7day < 0.5:
            priority += 0.3
        elif decay_7day < 0.7:
            priority += 0.15
        
        # Current mastery - higher mastery means less urgent
        if current_mastery < 0.3:
            priority += 0.2  # Struggling concepts need review
        elif current_mastery < 0.5:
            priority += 0.1
        
        return min(1.0, priority)
    
    # =========================================================================
    # Weak Concept Detection
    # =========================================================================
    
    def detect_weak_concepts(
        self,
        learner_id: str,
        mastery_threshold: float = 0.4,
        inactivity_days: int = 7
    ) -> List[ConceptMastery]:
        """
        Identify concepts that need attention.
        
        A concept is considered weak if:
        - Mastery score is below threshold
        - AND either: recently interacted but struggling, or overdue for review
        
        Args:
            learner_id: Learner identifier
            mastery_threshold: Maximum mastery to be considered weak
            inactivity_days: Days since last interaction to flag
            
        Returns:
            List of weak ConceptMastery records, sorted by urgency
        """
        mastery_records = self.get_all_mastery(learner_id, include_overdue=False)
        weak_concepts = []
        now = datetime.now()
        
        for record in mastery_records:
            if record.mastery_score >= mastery_threshold:
                continue
            
            # Check if overdue or recently struggling
            if record.is_overdue_for_review(now):
                weak_concepts.append(record)
            elif record.interaction_count >= 3 and record.mastery_score < 0.3:
                # Multiple attempts but still low mastery
                weak_concepts.append(record)
            elif (now - record.last_interaction_at).days <= inactivity_days:
                # Recently interacted, check if struggling
                if record.mastery_score < 0.5:
                    weak_concepts.append(record)
        
        # Sort by urgency (combination of low mastery and time factors)
        weak_concepts.sort(key=lambda r: (
            r.mastery_score,  # Lower mastery = higher priority
            -(r.interaction_count),  # More attempts = needs help
            -(now - r.last_interaction_at).days  # More recent = more urgent
        ))
        
        self._stats.weak_concepts_detected += len(weak_concepts)
        
        return weak_concepts
    
    def detect_knowledge_gaps(
        self,
        learner_id: str,
        concepts: Dict[str, Concept],
        relationships: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect knowledge gaps based on incomplete prerequisite chains.
        
        Uses the reasoning engine to identify critical gaps.
        
        Args:
            learner_id: Learner identifier
            concepts: Available concepts
            relationships: Concept relationships
            
        Returns:
            List of detected knowledge gaps
        """
        # Get completed concepts
        mastery_records = self.get_all_mastery(learner_id)
        completed = {
            m.concept_id for m in mastery_records
            if m.mastery_score >= 0.7
        }
        
        # Build graph and detect gaps
        graph = self.reasoning.build_concept_graph(concepts, relationships)
        gaps = self.reasoning.detect_knowledge_gaps(
            graph,
            completed,
            include_minor_gaps=False
        )
        
        return [
            {
                "gap_id": gap.gap_id,
                "target_concept": gap.target_concept_name,
                "missing_prerequisites": [
                    m["id"] for m in gap.missing_concepts
                ],
                "severity": gap.severity.value,
                "recommendation": f"Learn {', '.join(m['name'] for m in gap.missing_concepts[:3])}"
            }
            for gap in gaps
        ]
    
    # =========================================================================
    # Review Scheduling
    # =========================================================================
    
    def get_review_schedule(
        self,
        learner_id: str,
        concepts: Dict[str, Concept],
        max_items: int = 10
    ) -> List[ReviewSchedule]:
        """
        Generate a review schedule for the learner.
        
        Args:
            learner_id: Learner identifier
            concepts: Available concepts with metadata
            max_items: Maximum items to return
            
        Returns:
            List of scheduled reviews sorted by priority
        """
        mastery_records = self.get_all_mastery(learner_id, include_overdue=True)
        schedules = []
        
        now = datetime.now()
        
        for record in mastery_records:
            if not record.is_overdue_for_review(now):
                continue
            
            # Calculate priority
            priority = self.calculate_review_priority(
                learner_id,
                record.concept_id,
                record.mastery_score
            )
            
            # Get concept name
            concept = concepts.get(record.concept_id)
            concept_name = concept.name if concept else record.concept_id
            
            # Check for visual aids
            visual_mappings = self.animation.get_mappings_for_concept(record.concept_id)
            has_visual = len(visual_mappings) > 0
            asset_id = visual_mappings[0].asset_id if visual_mappings else None
            
            # Get domain
            domain = concept.domain if concept else "general"
            
            schedule = ReviewSchedule.create(
                concept_id=record.concept_id,
                concept_name=concept_name,
                mastery_record=record,
                priority_score=priority,
                domain=domain,
                has_visual_aid=has_visual,
                asset_id=asset_id
            )
            schedules.append(schedule)
        
        # Sort by priority (highest first)
        schedules.sort(key=lambda s: s.priority_score, reverse=True)
        
        self._stats.reviews_scheduled = len(schedules)
        
        return schedules[:max_items]
    
    # =========================================================================
    # Integration with Learning Path Service
    # =========================================================================
    
    def get_ready_concepts(
        self,
        learner_id: str,
        graph: DependencyGraph
    ) -> List[str]:
        """
        Get concepts that are ready to learn based on mastery.
        
        A concept is ready if:
        - All prerequisites have mastery >= threshold
        - OR no mastery record exists and no prerequisites
        
        Args:
            learner_id: Learner identifier
            graph: Dependency graph
            
        Returns:
            List of ready concept IDs
        """
        MASTERY_THRESHOLD = 0.7
        ready = []
        
        # Get all concept IDs from graph
        all_concepts = [
            node.id for node in graph.get_all_nodes()
        ]
        
        for concept_id in all_concepts:
            # Check if already mastered
            mastery = self.get_concept_mastery(learner_id, concept_id)
            if mastery and mastery.is_considered_known(MASTERY_THRESHOLD):
                continue
            
            # Get prerequisites
            node = graph.get_node(concept_id)
            if not node:
                continue
            
            prereqs = node.prerequisites
            
            # Check if all prerequisites are mastered
            all_mastered = True
            for prereq_id in prereqs:
                prereq_mastery = self.get_concept_mastery(learner_id, prereq_id)
                if not prereq_mastery or not prereq_mastery.is_considered_known(MASTERY_THRESHOLD):
                    all_mastered = False
                    break
            
            if all_mastered:
                ready.append(concept_id)
        
        return ready
    
    def get_remedial_concepts(
        self,
        learner_id: str,
        target_concept_id: str,
        graph: DependencyGraph
    ) -> List[str]:
        """
        Get concepts that need remediation before target concept.
        
        Args:
            learner_id: Learner identifier
            target_concept_id: Concept to eventually learn
            graph: Dependency graph
            
        Returns:
            List of prerequisite concepts that need work
        """
        MASTERY_THRESHOLD = 0.7
        
        # Get all prerequisites recursively
        all_prereqs = graph.get_all_prerequisites(target_concept_id)
        
        # Filter to those not yet mastered
        remedial = []
        for prereq_id in all_prereqs:
            mastery = self.get_concept_mastery(learner_id, prereq_id)
            if not mastery or not mastery.is_considered_known(MASTERY_THRESHOLD):
                remedial.append(prereq_id)
        
        return remedial
    
    def adjust_path_for_mastery(
        self,
        learner_id: str,
        path_concepts: List[str],
        graph: DependencyGraph
    ) -> Tuple[List[str], List[str]]:
        """
        Adjust a learning path based on current mastery levels.
        
        Returns:
            Tuple of (adjusted_path, concepts_to_review)
        """
        MASTERY_THRESHOLD = 0.7
        
        adjusted_path = []
        review_concepts = []
        
        for concept_id in path_concepts:
            mastery = self.get_concept_mastery(learner_id, concept_id)
            
            if mastery and mastery.is_considered_known(MASTERY_THRESHOLD):
                # Already known, skip or add to review
                if mastery.is_overdue_for_review(datetime.now()):
                    review_concepts.append(concept_id)
            else:
                # Not known, add to path
                adjusted_path.append(concept_id)
        
        return adjusted_path, review_concepts
    
    # =========================================================================
    # Session Management
    # =========================================================================
    
    def start_session(self, learner_id: str) -> LearningSession:
        """Start a new learning session"""
        session = LearningSession.create(learner_id)
        self._sessions[session.session_id] = session
        return session
    
    def end_session(self, session_id: str) -> LearningSession:
        """End a learning session and update metrics"""
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.complete_session()
        
        # Update learner profile
        profile = self.get_or_create_learner_profile(session.learner_id)
        profile.update_activity(session.get_duration_minutes())
        
        return session
    
    def record_session_interaction(
        self,
        session_id: str,
        concept_id: str,
        interaction_type: InteractionType,
        success: bool,
        time_spent_seconds: int,
        score: float = 1.0
    ) -> None:
        """Record an interaction within a session"""
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        session.add_interaction(
            concept_id=concept_id,
            interaction_type=interaction_type,
            success=success,
            time_spent_seconds=time_spent_seconds
        )
        
        # Also update mastery
        result = InteractionResult(
            concept_id=concept_id,
            interaction_type=interaction_type,
            success=success,
            score=score,
            time_spent_seconds=time_spent_seconds,
            session_id=session_id
        )
        self.update_mastery(session.learner_id, result)
    
    # =========================================================================
    # Metrics and Analytics
    # =========================================================================
    
    def calculate_metrics(
        self,
        learner_id: str,
        domain_map: Optional[Dict[str, str]] = None
    ) -> MasteryMetrics:
        """
        Calculate aggregated metrics for a learner.
        
        Args:
            learner_id: Learner identifier
            domain_map: Optional mapping of concept_id to domain
            
        Returns:
            MasteryMetrics with all calculated values
        """
        mastery_records = self.get_all_mastery(learner_id)
        
        metrics = MasteryMetrics.create(learner_id)
        metrics.update_from_mastery_records(mastery_records, domain_map)
        
        return metrics
    
    def get_learning_velocity(
        self,
        learner_id: str,
        days: int = 7
    ) -> float:
        """
        Calculate learning velocity (mastery points per hour).
        
        Args:
            learner_id: Learner identifier
            days: Number of days to analyze
            
        Returns:
            Mastery points gained per hour of study
        """
        mastery_records = self.get_all_mastery(learner_id)
        
        if not mastery_records:
            return 0.0
        
        # Calculate total mastery gained in period
        total_gained = 0.0
        total_time = 0
        
        for record in mastery_records:
            # Consider only recent interactions
            cutoff = datetime.now() - timedelta(days=days)
            recent_history = [
                h for h in record.mastery_history
                if datetime.fromisoformat(h["timestamp"]) > cutoff
            ]
            
            for i, entry in enumerate(recent_history):
                if i == 0:
                    continue  # Skip first entry (baseline)
                if entry["success"]:
                    total_gained += 0.01  # Approximate gain per success
            total_time += record.total_session_time_minutes
        
        if total_time == 0:
            return 0.0
        
        # Convert to per-hour rate
        hours = total_time / 60
        return total_gained / hours if hours > 0 else 0.0
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            "total_mastery_updates": self._stats.total_mastery_updates,
            "total_concepts_tracked": self._stats.total_concepts_tracked,
            "average_calculation_time_ms": self._stats.average_calculation_time_ms,
            "weak_concepts_detected": self._stats.weak_concepts_detected,
            "reviews_scheduled": self._stats.reviews_scheduled,
            "active_learners": len(self._learner_profiles),
            "active_sessions": len(self._sessions)
        }
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._learner_profiles.clear()
        self._concept_mastery.clear()
        self._sessions.clear()
        self._stats = MasteryServiceStats()
        logger.info("Cleared mastery service cache")
