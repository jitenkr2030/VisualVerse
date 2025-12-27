"""
Content Recommendation Service for VisualVerse Content Metadata Layer

This service provides intelligent content recommendations based on knowledge
gaps, learner profiles, concept relationships, and concept mastery tracking.
It integrates the reasoning engine with animation metadata and the mastery
service to suggest optimal learning paths.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
import random
from collections import defaultdict

from ..models.reasoning import (
    InferenceRule,
    KnowledgeGap,
    GapSeverity,
    ConceptSimilarity,
    get_default_inference_rules
)
from ..models.visual_meta import (
    AnimationAsset,
    ConceptVisualMapping,
    VisualLearningPath,
    RelevanceType
)
from ..models.concept import Concept, DifficultyLevel
from ..models.learner_profile import (
    LearnerProfile as MasteryLearnerProfile,
    ConceptMastery,
    MasteryMetrics,
    InteractionResult,
    MasteryLevel,
    InteractionType
)
from .reasoning_engine import ReasoningEngine, SimpleGraph
from .animation_service import AnimationMetadataService
from .mastery_service import MasteryService


logger = logging.getLogger(__name__)


class RecommendationType(str, Enum):
    """Types of recommendations"""
    NEXT_LESSON = "next_lesson"
    REMEDIAL = "remedial"
    REINFORCEMENT = "reinforcement"
    CHALLENGE = "challenge"
    INTERDISCIPLINARY = "interdisciplinary"
    VISUAL_AID = "visual_aid"
    ASSESSMENT = "assessment"


class LearnerLevel(str, Enum):
    """Learner proficiency levels"""
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class LearnerProfile:
    """Profile of a learner for personalization (deprecated, use MasteryService)"""
    learner_id: str
    completed_concepts: Set[str] = field(default_factory=set)
    struggling_concepts: Set[str] = field(default_factory=set)
    preferred_difficulty: str = "intermediate"
    preferred_styles: List[str] = field(default_factory=list)
    learning_rate: float = 1.0  # 0.5 = slow, 1.0 = normal, 1.5 = fast
    daily_goal_minutes: int = 30
    streak_days: int = 0
    total_learning_minutes: int = 0
    last_active: Optional[datetime] = None
    
    def get_level(self) -> LearnerLevel:
        """Determine learner level from completed concepts and history"""
        concept_count = len(self.completed_concepts)
        
        if concept_count < 10:
            return LearnerLevel.BEGINNER
        elif concept_count < 30:
            return LearnerLevel.ELEMENTARY
        elif concept_count < 60:
            return LearnerLevel.INTERMEDIATE
        elif concept_count < 100:
            return LearnerLevel.ADVANCED
        else:
            return LearnerLevel.EXPERT
    
    def get_adjusted_difficulty(self) -> str:
        """Get difficulty adjusted for learning rate"""
        level = self.get_level()
        
        if self.learning_rate < 0.7:
            # Slower learner - suggest easier content
            level_map = {
                LearnerLevel.BEGINNER: 'beginner',
                LearnerLevel.ELEMENTARY: 'beginner',
                LearnerLevel.INTERMEDIATE: 'elementary',
                LearnerLevel.ADVANCED: 'intermediate',
                LearnerLevel.EXPERT: 'advanced'
            }
            return level_map.get(level, 'intermediate')
        elif self.learning_rate > 1.3:
            # Fast learner - suggest harder content
            level_map = {
                LearnerLevel.BEGINNER: 'elementary',
                LearnerLevel.ELEMENTARY: 'intermediate',
                LearnerLevel.INTERMEDIATE: 'advanced',
                LearnerLevel.ADVANCED: 'expert',
                LearnerLevel.EXPERT: 'expert'
            }
            return level_map.get(level, 'intermediate')
        
        return self.preferred_difficulty


@dataclass
class ContentRecommendation:
    """A single content recommendation"""
    recommendation_id: str
    recommendation_type: RecommendationType
    concept_id: str
    concept_name: str
    subject_id: str
    difficulty: str
    
    # Priority and rationale
    priority_score: float
    rationale: str
    
    # Content
    has_visual_aid: bool = False
    visual_asset_id: Optional[str] = None
    visual_asset_url: Optional[str] = None
    estimated_minutes: int = 30
    
    # Learning context
    prerequisites_needed: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    
    # Mastery context
    current_mastery_score: float = 0.0
    predicted_mastery_gain: float = 0.0
    is_review: bool = False
    
    # Action URL
    action_url: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'recommendation_id': self.recommendation_id,
            'recommendation_type': self.recommendation_type.value,
            'concept': {
                'id': self.concept_id,
                'name': self.concept_name,
                'subject_id': self.subject_id,
                'difficulty': self.difficulty
            },
            'priority_score': self.priority_score,
            'rationale': self.rationale,
            'has_visual_aid': self.has_visual_aid,
            'visual_asset_url': self.visual_asset_url,
            'estimated_minutes': self.estimated_minutes,
            'prerequisites_needed': self.prerequisites_needed,
            'related_concepts': self.related_concepts,
            'current_mastery_score': self.current_mastery_score,
            'predicted_mastery_gain': self.predicted_mastery_gain,
            'is_review': self.is_review,
            'action_url': self.action_url
        }


@dataclass
class LearningSession:
    """A planned learning session"""
    session_id: str
    learner_id: str
    recommendations: List[ContentRecommendation]
    total_duration_minutes: int
    difficulty_progression: List[str]
    subject_focus: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'session_id': self.session_id,
            'learner_id': self.learner_id,
            'recommendations': [r.to_dict() for r in self.recommendations],
            'total_duration_minutes': self.total_duration_minutes,
            'difficulty_progression': self.difficulty_progression,
            'subject_focus': self.subject_focus
        }


class RecommendationService:
    """
    Service for generating intelligent content recommendations.
    
    This service combines knowledge gap detection, concept similarity,
    learner profiling, and concept mastery tracking to provide
    personalized learning recommendations.
    """
    
    def __init__(
        self,
        reasoning_engine: Optional[ReasoningEngine] = None,
        animation_service: Optional[AnimationMetadataService] = None,
        mastery_service: Optional[MasteryService] = None
    ):
        """
        Initialize the recommendation service.
        
        Args:
            reasoning_engine: Optional reasoning engine instance
            animation_service: Optional animation metadata service
            mastery_service: Optional mastery service for concept tracking
        """
        self.reasoning = reasoning_engine or ReasoningEngine()
        self.animation = animation_service or AnimationMetadataService()
        self.mastery = mastery_service or MasteryService()
        
        # Legacy learner profiles cache (for backward compatibility)
        self._profiles: Dict[str, LearnerProfile] = {}
        
        # Statistics
        self._stats = {
            'total_recommendations': 0,
            'recommendations_by_type': defaultdict(int),
            'average_priority_score': 0.0,
            'sessions_generated': 0
        }
    
    # =========================================================================
    # Learner Profile Management (Legacy - prefer MasteryService)
    # =========================================================================
    
    def get_or_create_profile(self, learner_id: str) -> LearnerProfile:
        """Get or create a learner profile (legacy method)"""
        if learner_id in self._profiles:
            profile = self._profiles[learner_id]
            profile.last_active = datetime.now()
            return profile
        
        profile = LearnerProfile(learner_id=learner_id)
        self._profiles[learner_id] = profile
        
        logger.info(f"Created legacy profile for learner {learner_id}")
        
        return profile
    
    def update_profile(
        self,
        learner_id: str,
        completed_concepts: Optional[Set[str]] = None,
        struggling_concepts: Optional[Set[str]] = None,
        learning_minutes: Optional[int] = None
    ) -> LearnerProfile:
        """
        Update a learner's profile with new activity (legacy method).
        
        Args:
            learner_id: Learner ID
            completed_concepts: Newly completed concepts
            struggling_concepts: Concepts learner struggled with
            learning_minutes: Minutes spent learning
            
        Returns:
            Updated profile
        """
        profile = self.get_or_create_profile(learner_id)
        
        if completed_concepts:
            profile.completed_concepts.update(completed_concepts)
        
        if struggling_concepts:
            profile.struggling_concepts.update(struggling_concepts)
        
        if learning_minutes:
            profile.total_learning_minutes += learning_minutes
            profile.last_active = datetime.now()
            
            # Update learning rate
            if profile.total_learning_minutes > 0:
                # Simple rate calculation based on recent activity
                recent_completed = len(completed_concepts) if completed_concepts else 0
                if recent_completed > 0:
                    rate = learning_minutes / (recent_completed * 30)  # 30 min per concept baseline
                    profile.learning_rate = profile.learning_rate * 0.7 + rate * 0.3
        
        return profile
    
    # =========================================================================
    # Mastery-Aware Recommendation Generation
    # =========================================================================
    
    def generate_mastery_aware_recommendations(
        self,
        learner_id: str,
        concepts: Dict[str, Concept],
        relationships: List[Dict[str, Any]],
        max_recommendations: int = 10
    ) -> List[ContentRecommendation]:
        """
        Generate recommendations using mastery data for personalization.
        
        This is the preferred method for generating recommendations as it
        takes into account the learner's current mastery levels and
        schedules reviews based on spaced repetition principles.
        
        Args:
            learner_id: Learner ID
            concepts: Dictionary of concept data
            relationships: List of relationships
            max_recommendations: Maximum recommendations to return
            
        Returns:
            List of content recommendations
        """
        recommendations = []
        
        # Get mastery data
        mastery_records = self.mastery.get_all_mastery(learner_id)
        mastery_map = {m.concept_id: m for m in mastery_records}
        weak_concepts = self.mastery.detect_weak_concepts(learner_id)
        
        # Build graph
        concept_dict = {
            cid: {
                'id': cid,
                'name': c.name,
                'difficulty_level': c.difficulty_level.value if hasattr(c.difficulty_level, 'value') else str(c.difficulty_level),
                'subject_id': c.subject_id,
                'tags': getattr(c, 'tags', [])
            }
            for cid, c in concepts.items()
        }
        graph = self.reasoning.build_concept_graph(concept_dict, relationships)
        
        # Get review schedule
        review_schedule = self.mastery.get_review_schedule(
            learner_id, concept_dict, max_items=max_recommendations // 2
        )
        
        # Add review recommendations
        for review in review_schedule:
            concept = concepts.get(review.concept_id)
            if not concept:
                continue
            
            rec = self._build_mastery_recommendation(
                concept_id=review.concept_id,
                concept_data=concept_dict.get(review.concept_id, {}),
                rec_type=RecommendationType.REINFORCEMENT,
                priority=review.priority_score,
                rationale=f"Review needed: {review.concept_name} retention at {review.current_mastery:.0%}",
                current_mastery=review.current_mastery,
                is_review=True,
                has_visual_aid=review.has_visual_aid,
                asset_id=review.asset_id,
                graph=graph
            )
            recommendations.append(rec)
        
        # Add next lesson recommendations
        next_recommendations = self._get_next_lesson_recommendations_mastery(
            learner_id, concept_dict, mastery_map, graph
        )
        recommendations.extend(next_recommendations)
        
        # Add challenge recommendations
        challenge_recommendations = self._get_challenge_recommendations_mastery(
            learner_id, concept_dict, mastery_map, graph
        )
        recommendations.extend(challenge_recommendations)
        
        # Add weak concept remedial recommendations
        for weak in weak_concepts[:3]:
            concept = concepts.get(weak.concept_id)
            if not concept:
                continue
            
            rec = self._build_mastery_recommendation(
                concept_id=weak.concept_id,
                concept_data=concept_dict.get(weak.concept_id, {}),
                rec_type=RecommendationType.REMEDIAL,
                priority=0.9 - weak.mastery_score,  # Lower mastery = higher priority
                rationale=f"Strengthen your understanding of {weak.concept_id}",
                current_mastery=weak.mastery_score,
                is_review=False,
                graph=graph
            )
            recommendations.append(rec)
        
        # Sort by priority score and limit
        recommendations.sort(key=lambda r: r.priority_score, reverse=True)
        recommendations = recommendations[:max_recommendations]
        
        # Update statistics
        self._stats['total_recommendations'] += len(recommendations)
        for rec in recommendations:
            self._stats['recommendations_by_type'][rec.recommendation_type.value] += 1
        
        return recommendations
    
    def _build_mastery_recommendation(
        self,
        concept_id: str,
        concept_data: Dict[str, Any],
        rec_type: RecommendationType,
        priority: float,
        rationale: str,
        current_mastery: float,
        is_review: bool,
        has_visual_aid: bool = False,
        asset_id: Optional[str] = None,
        graph: Optional[SimpleGraph] = None
    ) -> ContentRecommendation:
        """Build a recommendation with mastery context"""
        # Get visual aid info
        visual_url = None
        if has_visual_aid and asset_id:
            visual_url = f"/api/v1/animations/{asset_id}/view"
        
        # Get related concepts
        related = self._get_related_concepts(concept_id, graph) if graph else []
        
        return ContentRecommendation(
            recommendation_id=f"rec-{concept_id}-{datetime.now().timestamp()}",
            recommendation_type=rec_type,
            concept_id=concept_id,
            concept_name=concept_data.get('name', concept_id),
            subject_id=concept_data.get('subject_id', ''),
            difficulty=concept_data.get('difficulty_level', 'intermediate'),
            priority_score=priority,
            rationale=rationale,
            has_visual_aid=has_visual_aid,
            visual_asset_id=asset_id,
            visual_asset_url=visual_url,
            estimated_minutes=concept_data.get('estimated_duration', 30),
            related_concepts=related,
            current_mastery_score=current_mastery,
            predicted_mastery_gain=0.15 if not is_review else 0.05,
            is_review=is_review,
            action_url=f"/learn/{concept_data.get('subject_id', 'general')}/{concept_id}"
        )
    
    def _get_next_lesson_recommendations_mastery(
        self,
        learner_id: str,
        concepts: Dict[str, Dict[str, Any]],
        mastery_map: Dict[str, ConceptMastery],
        graph: SimpleGraph
    ) -> List[ContentRecommendation]:
        """Get recommendations for what to learn next based on mastery"""
        recommendations = []
        
        for concept_id, data in concepts.items():
            # Skip if already mastered
            mastery = mastery_map.get(concept_id)
            if mastery and mastery.is_considered_known(0.7):
                continue
            
            # Get prerequisites
            prereqs = graph.get_prerequisites(concept_id, recursive=False)
            
            # Check if all prerequisites are mastered
            all_mastered = True
            for prereq_id in prereqs:
                prereq_mastery = mastery_map.get(prereq_id)
                if not prereq_mastery or not prereq_mastery.is_considered_known(0.7):
                    all_mastered = False
                    break
            
            if all_mastered:
                # Calculate priority based on concept importance and mastery gap
                priority = self._calculate_mastery_priority(concept_id, mastery, concepts)
                
                if priority > 0:
                    rec = self._build_mastery_recommendation(
                        concept_id=concept_id,
                        concept_data=data,
                        rec_type=RecommendationType.NEXT_LESSON,
                        priority=priority,
                        rationale=f"You're ready to learn {data.get('name', concept_id)}!",
                        current_mastery=mastery.mastery_score if mastery else 0.0,
                        is_review=False,
                        graph=graph
                    )
                    recommendations.append(rec)
        
        # Sort and limit
        recommendations.sort(key=lambda r: r.priority_score, reverse=True)
        return recommendations[:5]
    
    def _calculate_mastery_priority(
        self,
        concept_id: str,
        mastery: Optional[ConceptMastery],
        concepts: Dict[str, Dict[str, Any]]
    ) -> float:
        """Calculate priority score for a recommendation based on mastery"""
        priority = 0.5
        
        # Boost for new concepts (no mastery record)
        if mastery is None:
            priority += 0.2
        
        # Adjust for current mastery level
        if mastery:
            if mastery.mastery_score < 0.2:
                priority += 0.2  # High priority for very low mastery
            elif mastery.mastery_score < 0.4:
                priority += 0.1
        
        # Boost for concepts with visual aids
        if concept_id in self.animation._concept_to_assets:
            priority += 0.1
        
        return min(1.0, priority)
    
    def _get_challenge_recommendations_mastery(
        self,
        learner_id: str,
        concepts: Dict[str, Dict[str, Any]],
        mastery_map: Dict[str, ConceptMastery],
        graph: SimpleGraph
    ) -> List[ContentRecommendation]:
        """Get challenging recommendations based on current mastery level"""
        # Calculate average mastery
        if not mastery_map:
            return []
        
        avg_mastery = sum(m.mastery_score for m in mastery_map.values()) / len(mastery_map)
        
        # Target difficulty based on mastery
        if avg_mastery >= 0.85:
            target_difficulty = 'expert'
        elif avg_mastery >= 0.70:
            target_difficulty = 'advanced'
        elif avg_mastery >= 0.50:
            target_difficulty = 'intermediate'
        else:
            return []  # Not ready for challenges yet
        
        recommendations = []
        
        difficulty_order = ['beginner', 'elementary', 'intermediate', 'advanced', 'expert']
        target_idx = difficulty_order.index(target_difficulty)
        
        for concept_id, data in concepts.items():
            # Skip mastered concepts
            mastery = mastery_map.get(concept_id)
            if mastery and mastery.is_considered_known(0.7):
                continue
            
            difficulty = data.get('difficulty_level', 'intermediate')
            
            # Look for concepts at target difficulty
            if difficulty == target_difficulty:
                # Check prerequisites
                prereqs = graph.get_prerequisites(concept_id, recursive=False)
                
                # Allow if most prerequisites are mastered
                mastered_prereqs = [
                    p for p in prereqs
                    if mastery_map.get(p) and mastery_map[p].is_considered_known(0.7)
                ]
                
                if len(prereqs) == 0 or len(mastered_prereqs) >= len(prereqs) * 0.7:
                    rec = self._build_mastery_recommendation(
                        concept_id=concept_id,
                        concept_data=data,
                        rec_type=RecommendationType.CHALLENGE,
                        priority=0.5,
                        rationale=f"Challenge yourself with {data.get('name', concept_id)}!",
                        current_mastery=mastery.mastery_score if mastery else 0.0,
                        is_review=False,
                        graph=graph
                    )
                    recommendations.append(rec)
        
        return recommendations[:3]
    
    # =========================================================================
    # Legacy Recommendation Methods (for backward compatibility)
    # =========================================================================
    
    def generate_recommendations(
        self,
        learner_id: str,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        max_recommendations: int = 10,
        include_types: Optional[List[RecommendationType]] = None
    ) -> List[ContentRecommendation]:
        """
        Generate personalized recommendations for a learner.
        
        This is the legacy method. For new implementations, use
        generate_mastery_aware_recommendations instead.
        
        Args:
            learner_id: Learner ID
            concepts: Dictionary of concept data
            relationships: List of relationships
            max_recommendations: Maximum recommendations to return
            include_types: Types of recommendations to include
            
        Returns:
            List of content recommendations
        """
        profile = self.get_or_create_profile(learner_id)
        
        # Build graph
        graph = self.reasoning.build_concept_graph(concepts, relationships)
        
        # Run inference
        self.reasoning.run_inference(graph)
        
        # Get completed set
        completed = profile.completed_concepts
        
        # Determine next concepts
        recommendations = []
        
        # 1. Next lesson recommendations (what can be learned now)
        next_recommendations = self._get_next_lesson_recommendations(
            graph, concepts, completed, profile
        )
        recommendations.extend(next_recommendations)
        
        # 2. Remedial recommendations (fill gaps)
        if include_types is None or RecommendationType.REMEDIAL in include_types:
            remedial = self._get_remedial_recommendations(
                graph, concepts, relationships, profile
            )
            recommendations.extend(remedial)
        
        # 3. Reinforcement recommendations (review completed)
        if include_types is None or RecommendationType.REINFORCEMENT in include_types:
            reinforcement = self._get_reinforcement_recommendations(
                graph, concepts, relationships, profile
            )
            recommendations.extend(reinforcement)
        
        # 4. Challenge recommendations (push boundaries)
        if include_types is None or RecommendationType.CHALLENGE in include_types:
            challenges = self._get_challenge_recommendations(
                graph, concepts, completed, profile
            )
            recommendations.extend(challenges)
        
        # 5. Visual aid recommendations
        if include_types is None or RecommendationType.VISUAL_AID in include_types:
            visual = self._get_visual_recommendations(
                graph, concepts, profile
            )
            recommendations.extend(visual)
        
        # Sort by priority score and limit
        recommendations.sort(key=lambda r: r.priority_score, reverse=True)
        recommendations = recommendations[:max_recommendations]
        
        # Update statistics
        self._stats['total_recommendations'] += len(recommendations)
        for rec in recommendations:
            self._stats['recommendations_by_type'][rec.recommendation_type.value] += 1
        
        return recommendations
    
    def _get_next_lesson_recommendations(
        self,
        graph: SimpleGraph,
        concepts: Dict[str, Dict[str, Any]],
        completed: Set[str],
        profile: LearnerProfile
    ) -> List[ContentRecommendation]:
        """Get recommendations for what to learn next"""
        recommendations = []
        adjusted_difficulty = profile.get_adjusted_difficulty()
        
        # Find concepts with all prerequisites completed
        for concept_id, data in concepts.items():
            if concept_id in completed:
                continue
            
            # Get direct prerequisites
            prereqs = graph.get_prerequisites(concept_id, recursive=False)
            
            # Check if all prerequisites are completed
            if all(p in completed for p in prereqs):
                # Check difficulty match
                difficulty = data.get('difficulty_level', 'intermediate')
                
                # Calculate priority
                priority = self._calculate_priority(concept_id, data, prereqs, profile)
                
                if priority > 0:
                    recommendation = self._build_recommendation(
                        concept_id, data,
                        RecommendationType.NEXT_LESSON,
                        priority,
                        f"You're ready to learn {data.get('name', concept_id)}!",
                        prereqs_needed=[],
                        graph=graph
                    )
                    recommendations.append(recommendation)
        
        # Sort and limit
        recommendations.sort(key=lambda r: r.priority_score, reverse=True)
        
        return recommendations[:5]
    
    def _get_remedial_recommendations(
        self,
        graph: SimpleGraph,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        profile: LearnerProfile
    ) -> List[ContentRecommendation]:
        """Get recommendations for filling knowledge gaps"""
        if not profile.struggling_concepts:
            return []
        
        recommendations = []
        
        # Detect knowledge gaps based on struggling concepts
        completed = profile.completed_concepts | profile.struggling_concepts
        
        gaps = self.reasoning.detect_knowledge_gaps(
            graph,
            completed,
            include_minor_gaps=True
        )
        
        for gap in gaps[:3]:
            for missing in gap.missing_concepts[:2]:
                concept_id = missing['id']
                if concept_id in completed:
                    continue
                
                data = concepts.get(concept_id)
                if not data:
                    continue
                
                priority = 0.9 if gap.severity == GapSeverity.CRITICAL else 0.7
                
                recommendation = self._build_recommendation(
                    concept_id, data,
                    RecommendationType.REMEDIAL,
                    priority,
                    f"Fill the gap: {missing['name']} will help with {gap.target_concept_name}",
                    prerequisites_needed=[],
                    graph=graph
                )
                recommendations.append(recommendation)
        
        return recommendations
    
    def _get_reinforcement_recommendations(
        self,
        graph: SimpleGraph,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        profile: LearnerProfile
    ) -> List[ContentRecommendation]:
        """Get recommendations for reviewing completed concepts"""
        if not profile.completed_concepts:
            return []
        
        recommendations = []
        
        # Find completed concepts that could use review
        struggling = profile.struggling_concepts
        
        for concept_id in struggling:
            data = concepts.get(concept_id)
            if not data:
                continue
            
            # Check for visual aids
            mappings = self.animation.get_mappings_for_concept(concept_id)
            has_visual = len(mappings) > 0
            
            priority = 0.6
            
            recommendation = self._build_recommendation(
                concept_id, data,
                RecommendationType.REINFORCEMENT,
                priority,
                f"Review: {data.get('name', concept_id)} to strengthen your understanding",
                has_visual_aid=has_visual,
                graph=graph
            )
            recommendations.append(recommendation)
        
        # Add some random completed concepts for variety
        completed_list = list(profile.completed_concepts - struggling)
        random.shuffle(completed_list)
        
        for concept_id in completed_list[:2]:
            if len(recommendations) >= 3:
                break
            
            data = concepts.get(concept_id)
            if not data:
                continue
            
            recommendation = self._build_recommendation(
                concept_id, data,
                RecommendationType.REINFORCEMENT,
                0.4,
                f"Quick review: {data.get('name', concept_id)}",
                graph=graph
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_challenge_recommendations(
        self,
        graph: SimpleGraph,
        concepts: Dict[str, Dict[str, Any]],
        completed: Set[str],
        profile: LearnerProfile
    ) -> List[ContentRecommendation]:
        """Get challenging recommendations for advancement"""
        level = profile.get_level()
        adjusted_difficulty = profile.get_adjusted_difficulty()
        
        # Find slightly harder concepts
        difficulty_order = ['beginner', 'elementary', 'intermediate', 'advanced', 'expert']
        current_idx = difficulty_order.index(adjusted_difficulty)
        target_idx = min(current_idx + 1, len(difficulty_order) - 1)
        target_difficulty = difficulty_order[target_idx]
        
        recommendations = []
        
        for concept_id, data in concepts.items():
            if concept_id in completed:
                continue
            
            difficulty = data.get('difficulty_level', 'intermediate')
            
            # Look for concepts at target difficulty
            if difficulty == target_difficulty:
                # Check prerequisites
                prereqs = graph.get_prerequisites(concept_id, recursive=False)
                
                # Allow if most prerequisites are completed
                completed_prereqs = [p for p in prereqs if p in completed]
                
                if len(completed_prereqs) >= len(prereqs) * 0.7:
                    priority = 0.5
                    
                    recommendation = self._build_recommendation(
                        concept_id, data,
                        RecommendationType.CHALLENGE,
                        priority,
                        f"Challenge yourself with {data.get('name', concept_id)}!",
                        prereqs_needed=list(set(prereqs) - completed),
                        graph=graph
                    )
                    recommendations.append(recommendation)
        
        return recommendations[:3]
    
    def _get_visual_recommendations(
        self,
        graph: SimpleGraph,
        concepts: Dict[str, Dict[str, Any]],
        profile: LearnerProfile
    ) -> List[ContentRecommendation]:
        """Get recommendations that have good visual aids"""
        recommendations = []
        
        # Find concepts with visual aids
        for concept_id in list(self.animation._concept_to_assets.keys())[:10]:
            if concept_id in profile.completed_concepts:
                continue
            
            data = concepts.get(concept_id)
            if not data:
                continue
            
            # Get best asset
            mappings = self.animation.get_mappings_for_concept(
                concept_id,
                relevance_types=[RelevanceType.PRIMARY_EXPLANATION],
                approved_only=True
            )
            
            if not mappings:
                mappings = self.animation.get_mappings_for_concept(
                    concept_id,
                    approved_only=True
                )
            
            if mappings:
                mapping = mappings[0]
                asset = self.animation.get_asset(mapping.asset_id)
                
                if asset:
                    recommendation = self._build_recommendation(
                        concept_id, data,
                        RecommendationType.VISUAL_AID,
                        0.55,
                        f"Visual learning: {data.get('name', concept_id)} with animation",
                        has_visual_aid=True,
                        visual_asset_id=asset.id,
                        visual_asset_url=f"/api/v1/animations/{asset.id}/view",
                        estimated_minutes=int(asset.duration_seconds / 60) if asset.duration_seconds else 30,
                        graph=graph
                    )
                    recommendations.append(recommendation)
        
        return recommendations[:3]
    
    def _build_recommendation(
        self,
        concept_id: str,
        data: Dict[str, Any],
        rec_type: RecommendationType,
        priority: float,
        rationale: str,
        prerequisites_needed: Optional[List[str]] = None,
        has_visual_aid: bool = False,
        visual_asset_id: Optional[str] = None,
        visual_asset_url: Optional[str] = None,
        estimated_minutes: int = 30,
        graph: Optional[SimpleGraph] = None
    ) -> ContentRecommendation:
        """Build a recommendation object"""
        return ContentRecommendation(
            recommendation_id=f"rec-{concept_id}-{datetime.now().timestamp()}",
            recommendation_type=rec_type,
            concept_id=concept_id,
            concept_name=data.get('name', data.get('display_name', concept_id)),
            subject_id=data.get('subject_id', ''),
            difficulty=data.get('difficulty_level', 'intermediate'),
            priority_score=priority,
            rationale=rationale,
            has_visual_aid=has_visual_aid,
            visual_asset_id=visual_asset_id,
            visual_asset_url=visual_asset_url,
            estimated_minutes=estimated_minutes or data.get('estimated_duration', 30),
            prerequisites_needed=prerequisites_needed or [],
            related_concepts=self._get_related_concepts(concept_id, graph) if graph else [],
            action_url=f"/learn/{data.get('subject_id', 'general')}/{concept_id}"
        )
    
    def _calculate_priority(
        self,
        concept_id: str,
        data: Dict[str, Any],
        prerequisites: List[str],
        profile: LearnerProfile
    ) -> float:
        """Calculate priority score for a recommendation"""
        priority = 0.5
        
        # Prefer concepts in preferred subject
        if data.get('subject_id') in profile.preferred_styles:
            priority += 0.2
        
        # Adjust for difficulty
        adjusted = profile.get_adjusted_difficulty()
        if data.get('difficulty_level') == adjusted:
            priority += 0.15
        elif self._difficulty_order(data.get('difficulty_level', 'intermediate')) < \
             self._difficulty_order(adjusted):
            priority += 0.1
        
        # Boost for concepts with visual aids
        if concept_id in self.animation._concept_to_assets:
            priority += 0.1
        
        return min(1.0, priority)
    
    def _difficulty_order(self, level: str) -> int:
        """Get numeric order for difficulty level"""
        order = {
            'beginner': 0, 'elementary': 1, 'intermediate': 2,
            'advanced': 3, 'expert': 4
        }
        return order.get(level.lower(), 2)
    
    def _get_related_concepts(
        self,
        concept_id: str,
        graph: Optional[SimpleGraph]
    ) -> List[str]:
        """Get related concept IDs"""
        if not graph:
            return []
        
        related = []
        
        # Get neighbors
        neighbors = graph.get_neighbors(concept_id)
        related.extend(neighbors[:3])
        
        # Get similar concepts
        for node_id in graph.nodes():
            if node_id != concept_id and len(related) < 5:
                # Simple tag-based similarity
                node_data = graph.get_node_data(node_id)
                current_data = graph.get_node_data(concept_id)
                
                if node_data and current_data:
                    node_tags = set(node_data.get('tags', []))
                    current_tags = set(current_data.get('tags', []))
                    
                    if node_tags & current_tags:
                        related.append(node_id)
        
        return related[:5]
    
    # =========================================================================
    # Learning Session Generation
    # =========================================================================
    
    def generate_learning_session(
        self,
        learner_id: str,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        duration_minutes: int = 30,
        subject_focus: Optional[str] = None,
        use_mastery: bool = True
    ) -> LearningSession:
        """
        Generate a complete learning session.
        
        Args:
            learner_id: Learner ID
            concepts: Concept data
            relationships: Relationship data
            duration_minutes: Target session duration
            subject_focus: Optional subject to focus on
            use_mastery: Whether to use mastery-aware recommendations
            
        Returns:
            Generated learning session
        """
        # Get profile
        profile = self.get_or_create_profile(learner_id)
        
        # Filter concepts by subject if specified
        if subject_focus:
            filtered_concepts = {
                cid: data for cid, data in concepts.items()
                if data.get('subject_id') == subject_focus
            }
        else:
            filtered_concepts = concepts
        
        # Generate recommendations
        if use_mastery:
            recs = self.generate_mastery_aware_recommendations(
                learner_id,
                {k: Concept(**v) if isinstance(v, dict) and 'id' in v else None for k, v in filtered_concepts.items() if v},
                relationships,
                max_recommendations=10
            )
        else:
            recs = self.generate_recommendations(
                learner_id,
                filtered_concepts,
                relationships,
                max_recommendations=10
            )
        
        # Select recommendations to fit duration
        session_recommendations = []
        total_duration = 0
        difficulty_progression = []
        
        for rec in recs:
            if total_duration + rec.estimated_minutes > duration_minutes:
                # Try to fit a shorter review instead
                break
            
            session_recommendations.append(rec)
            total_duration += rec.estimated_minutes
            difficulty_progression.append(rec.difficulty)
        
        self._stats['sessions_generated'] += 1
        
        session = LearningSession(
            session_id=f"session-{learner_id}-{datetime.now().timestamp()}",
            learner_id=learner_id,
            recommendations=session_recommendations,
            total_duration_minutes=total_duration,
            difficulty_progression=difficulty_progression,
            subject_focus=subject_focus or 'mixed'
        )
        
        logger.info(
            f"Generated session {session.session_id} with "
            f"{len(session_recommendations)} recommendations"
        )
        
        return session
    
    # =========================================================================
    # Remedial Path Generation
    # =========================================================================
    
    def generate_remedial_path(
        self,
        learner_id: str,
        struggling_concept_id: str,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> List[ContentRecommendation]:
        """
        Generate a remedial path for a struggling concept.
        
        Uses inverse reasoning to find what foundational concept was missed.
        
        Args:
            learner_id: Learner ID
            struggling_concept_id: Concept the learner is struggling with
            concepts: Concept data
            relationships: Relationship data
            
        Returns:
            Ordered list of remedial recommendations
        """
        profile = self.get_or_create_profile(learner_id)
        
        # Build graph
        graph = self.reasoning.build_concept_graph(concepts, relationships)
        
        # Find prerequisites
        prereqs = graph.get_prerequisites(struggling_concept_id, recursive=True)
        
        # Filter to unlearned prerequisites
        unlearned = [p for p in prereqs if p not in profile.completed_concepts]
        
        # Sort by depth (closest prerequisites first)
        depth_map = {}
        for prereq in unlearned:
            prereq_depth = graph.get_prerequisites(prereq, recursive=True)
            depth_map[prereq] = len([p for p in prereq_depth if p not in profile.completed_concepts])
        
        unlearned.sort(key=lambda p: depth_map.get(p, 0))
        
        recommendations = []
        
        for concept_id in unlearned[:5]:  # Max 5 remedial concepts
            data = concepts.get(concept_id)
            if not data:
                continue
            
            recommendation = self._build_recommendation(
                concept_id, data,
                RecommendationType.REMEDIAL,
                0.85,
                f"Foundational: {data.get('name', concept_id)}",
                graph=graph
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    # =========================================================================
    # Statistics and Utilities
    # =========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        recs_by_type = dict(self._stats['recommendations_by_type'])
        
        return {
            'total_recommendations': self._stats['total_recommendations'],
            'recommendations_by_type': recs_by_type,
            'sessions_generated': self._stats['sessions_generated'],
            'cached_profiles': len(self._profiles),
            'mastery_stats': self.mastery.get_statistics()
        }
    
    def get_recommendation_analytics(
        self,
        learner_id: str,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        days: int = 30
    ) -> Dict[str, Any]:
        """Get analytics for a learner's recommendations"""
        profile = self.get_or_create_profile(learner_id)
        
        # Generate current recommendations
        current = self.generate_recommendations(
            learner_id, concepts, relationships, max_recommendations=20
        )
        
        # Analyze patterns
        type_distribution = defaultdict(int)
        difficulty_distribution = defaultdict(int)
        subject_distribution = defaultdict(int)
        
        for rec in current:
            type_distribution[rec.recommendation_type.value] += 1
            difficulty_distribution[rec.difficulty] += 1
            subject_distribution[rec.subject_id] += 1
        
        # Get mastery metrics
        mastery_metrics = self.mastery.calculate_metrics(learner_id)
        
        return {
            'learner_level': profile.get_level().value,
            'concepts_completed': len(profile.completed_concepts),
            'struggling_concepts': len(profile.struggling_concepts),
            'learning_rate': profile.learning_rate,
            'current_recommendations': len(current),
            'recommendation_types': dict(type_distribution),
            'difficulty_focus': dict(difficulty_distribution),
            'subject_focus': dict(subject_distribution),
            'suggested_difficulty': profile.get_adjusted_difficulty(),
            'mastery_metrics': {
                'global_mastery_average': mastery_metrics.global_mastery_average,
                'concepts_mastered': mastery_metrics.total_concepts_mastered,
                'concepts_due_for_review': mastery_metrics.concepts_due_for_review,
                'weakest_domain': mastery_metrics.weakest_domain
            }
        }
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._profiles.clear()
        self._stats = {
            'total_recommendations': 0,
            'recommendations_by_type': defaultdict(int),
            'average_priority_score': 0.0,
            'sessions_generated': 0
        }
        self.mastery.clear_cache()
        logger.info("Cleared recommendation service cache")
