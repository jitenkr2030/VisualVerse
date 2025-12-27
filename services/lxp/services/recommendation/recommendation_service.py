"""
Recommendation Service for Learner Experience Platform.

Provides personalized content recommendations using hybrid filtering approaches,
learner profile analysis, and adaptive learning path suggestions.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import math
from collections import defaultdict


class RecommendationType(Enum):
    """Types of recommendations supported by the service."""
    CONTENT_BASED = "content_based"
    COLLABORATIVE = "collaborative"
    HYBRID = "hybrid"
    LEARNING_PATH = "learning_path"
    SIMILAR_CONTENT = "similar_content"
    POPULAR_NOW = "popular_now"
    TRENDING = "trending"
    NEXT_STEP = "next_step"
    FILL_GAPS = "fill_gaps"


@dataclass
class LearnerProfile:
    """Learner profile for recommendation engine."""
    learner_id: str
    completed_content: List[str] = field(default_factory=list)
    in_progress_content: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    learning_style: Optional[str] = None
    difficulty_preference: float = 0.5
    preferred_duration: Optional[int] = None
    engagement_history: Dict[str, float] = field(default_factory=dict)
    skill_levels: Dict[str, float] = field(default_factory=dict)
    time_spent_patterns: Dict[str, float] = field(default_factory=dict)
    last_active: Optional[datetime] = None
    interaction_count: int = 0


@dataclass
class ContentFeatures:
    """Features extracted from content for recommendation."""
    content_id: str
    title: str
    description: str
    topics: List[str]
    difficulty_level: float
    duration_minutes: int
    content_type: str
    format_type: str
    tags: List[str]
    prerequisites: List[str]
    target_audience: List[str]
    engagement_score: float
    completion_rate: float
    average_rating: float
    popularity_score: float


@dataclass
class Recommendation:
    """A single recommendation with metadata."""
    content_id: str
    title: str
    recommendation_type: RecommendationType
    score: float
    confidence: float
    reasoning: str
    features_matched: List[str]
    estimated_value: float
    created_at: datetime


@dataclass
class RecommendationSet:
    """A collection of recommendations for a learner."""
    learner_id: str
    recommendations: List[Recommendation]
    generated_at: datetime
    context: Dict[str, Any]
    total_count: int
    diversity_score: float


class ContentSimilarityEngine:
    """Engine for calculating content similarity using multiple metrics."""
    
    def __init__(self):
        self.topic_weights = {
            'primary': 2.0,
            'secondary': 1.0,
            'tertiary': 0.5
        }
        self.tag_weights = {
            'exact_match': 1.5,
            'related': 0.8,
            'semantic': 0.5
        }
    
    def calculate_topic_similarity(
        self, 
        content1: ContentFeatures, 
        content2: ContentFeatures
    ) -> float:
        """Calculate similarity based on topic overlap."""
        if not content1.topics or not content2.topics:
            return 0.0
        
        topics1_set = set(content1.topics)
        topics2_set = set(content2.topics)
        
        intersection = topics1_set & topics2_set
        union = topics1_set | topics2_set
        
        if not union:
            return 0.0
        
        jaccard = len(intersection) / len(union)
        
        # Bonus for primary topic match
        if topics1_set & topics2_set:
            return min(1.0, jaccard * 1.5)
        
        return jaccard
    
    def calculate_difficulty_match(
        self, 
        content: ContentFeatures, 
        learner_profile: LearnerProfile
    ) -> float:
        """Calculate how well content difficulty matches learner preference."""
        difficulty_diff = abs(content.difficulty_level - learner_profile.difficulty_preference)
        # Return 1.0 for perfect match, decreasing to 0.0 for large differences
        return max(0.0, 1.0 - difficulty_diff * 2)
    
    def calculate_duration_fit(
        self, 
        content: ContentFeatures, 
        learner_profile: LearnerProfile
    ) -> float:
        """Calculate how well content duration fits learner preference."""
        if not learner_profile.preferred_duration:
            return 0.8  # Default moderate preference
        
        preferred = learner_profile.preferred_duration
        actual = content.duration_minutes
        
        if actual <= preferred:
            return 1.0 - (preferred - actual) / preferred * 0.5
        
        # Penalize content longer than preferred
        return max(0.0, 1.0 - (actual - preferred) / preferred)
    
    def calculate_engagement_prediction(
        self, 
        content: ContentFeatures, 
        learner_profile: LearnerProfile
    ) -> float:
        """Predict likely engagement level with content."""
        # Base engagement from content quality metrics
        base_engagement = (
            content.engagement_score * 0.3 +
            content.completion_rate * 0.3 +
            content.average_rating * 0.4
        )
        
        # Adjust for learner preferences
        difficulty_fit = self.calculate_difficulty_match(content, learner_profile)
        duration_fit = self.calculate_duration_fit(content, learner_profile)
        
        return base_engagement * difficulty_fit * duration_fit
    
    def calculate_overall_similarity(
        self, 
        content1: ContentFeatures, 
        content2: ContentFeatures,
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """Calculate overall content similarity score."""
        if weights is None:
            weights = {
                'topic': 0.4,
                'tag': 0.3,
                'type': 0.2,
                'difficulty': 0.1
            }
        
        topic_sim = self.calculate_topic_similarity(content1, content2)
        
        # Tag similarity
        tags1_set = set(content1.tags)
        tags2_set = set(content2.tags)
        tag_sim = len(tags1_set & tags2_set) / max(len(tags1_set | tags2_set), 1)
        
        # Content type match
        type_match = 1.0 if content1.content_type == content2.content_type else 0.5
        
        # Difficulty similarity
        diff_sim = 1.0 - abs(content1.difficulty_level - content2.difficulty_level)
        
        weighted_score = (
            weights['topic'] * topic_sim +
            weights['tag'] * tag_sim +
            weights['type'] * type_match +
            weights['difficulty'] * diff_sim
        )
        
        return weighted_score


class CollaborativeFilteringEngine:
    """Engine for collaborative filtering recommendations."""
    
    def __init__(self):
        self.user_item_matrix: Dict[str, Dict[str, float]] = {}
        self.item_similarity_cache: Dict[Tuple[str, str], float] = {}
        self.popular_items: Dict[str, float] = {}
    
    def record_interaction(
        self, 
        learner_id: str, 
        content_id: str, 
        rating: float,
        timestamp: Optional[datetime] = None
    ):
        """Record a learner-content interaction."""
        if learner_id not in self.user_item_matrix:
            self.user_item_matrix[learner_id] = {}
        
        self.user_item_matrix[learner_id][content_id] = rating
        
        # Update popular items
        avg_rating = self._calculate_average_rating(content_id)
        self.popular_items[content_id] = avg_rating
    
    def _calculate_average_rating(self, content_id: str) -> float:
        """Calculate average rating for an item."""
        ratings = []
        for user_matrix in self.user_item_matrix.values():
            if content_id in user_matrix:
                ratings.append(user_matrix[content_id])
        
        return sum(ratings) / len(ratings) if ratings else 0.0
    
    def _calculate_item_similarity(
        self, 
        item1: str, 
        item2: str
    ) -> float:
        """Calculate similarity between two items based on user interactions."""
        cache_key = (item1, item2) if item1 < item2 else (item2, item1)
        
        if cache_key in self.item_similarity_cache:
            return self.item_similarity_cache[cache_key]
        
        # Get ratings for both items
        ratings1 = {}
        ratings2 = {}
        
        for user_id, user_matrix in self.user_item_matrix.items():
            if item1 in user_matrix:
                ratings1[user_id] = user_matrix[item1]
            if item2 in user_matrix:
                ratings2[user_id] = user_matrix[item2]
        
        # Find common users
        common_users = set(ratings1.keys()) & set(ratings2.keys())
        
        if len(common_users) < 2:
            similarity = 0.0
        else:
            # Pearson correlation
            values1 = [ratings1[u] for u in common_users]
            values2 = [ratings2[u] for u in common_users]
            
            mean1 = sum(values1) / len(values1)
            mean2 = sum(values2) / len(values2)
            
            numerator = sum(
                (values1[i] - mean1) * (values2[i] - mean2) 
                for i in range(len(common_users))
            )
            
            std1 = math.sqrt(sum((v - mean1) ** 2 for v in values1))
            std2 = math.sqrt(sum((v - mean2) ** 2 for v in values2))
            
            if std1 == 0 or std2 == 0:
                similarity = 0.0
            else:
                similarity = numerator / (std1 * std2)
        
        self.item_similarity_cache[cache_key] = similarity
        return similarity
    
    def get_similar_items(
        self, 
        content_id: str, 
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Get items similar to the given content."""
        similarities = []
        
        for item_id in self.popular_items.keys():
            if item_id != content_id:
                sim = self._calculate_item_similarity(content_id, item_id)
                if sim > 0:
                    similarities.append((item_id, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def predict_rating(
        self, 
        learner_id: str, 
        content_id: str
    ) -> float:
        """Predict rating for a learner-content pair."""
        if learner_id not in self.user_item_matrix:
            return self.popular_items.get(content_id, 0.0)
        
        learner_ratings = self.user_item_matrix[learner_id]
        
        if content_id in learner_ratings:
            return learner_ratings[content_id]
        
        # Calculate weighted average based on similar items
        similar_items = self.get_similar_items(content_id, top_k=20)
        
        if not similar_items:
            return self.popular_items.get(content_id, 0.0)
        
        numerator = 0.0
        denominator = 0.0
        
        for item_id, similarity in similar_items:
            if item_id in learner_ratings:
                rating = learner_ratings[item_id]
                numerator += similarity * rating
                denominator += abs(similarity)
        
        if denominator == 0:
            return self.popular_items.get(content_id, 0.0)
        
        return numerator / denominator


class LearningPathEngine:
    """Engine for generating adaptive learning paths."""
    
    def __init__(self):
        self.path_templates: Dict[str, List[str]] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
    
    def add_content_dependency(
        self, 
        content_id: str, 
        prerequisite_id: str
    ):
        """Add a prerequisite dependency between content items."""
        self.dependency_graph[content_id].append(prerequisite_id)
    
    def get_prerequisites(self, content_id: str) -> List[str]:
        """Get all prerequisites for content."""
        return self.dependency_graph.get(content_id, [])
    
    def is_content_available(
        self, 
        content_id: str, 
        completed_content: List[str]
    ) -> bool:
        """Check if content is available based on prerequisites."""
        prerequisites = self.get_prerequisites(content_id)
        return all(prereq in completed_content for prereq in prerequisites)
    
    def generate_learning_path(
        self, 
        target_content: str,
        completed_content: List[str],
        learner_profile: LearnerProfile,
        max_items: int = 10
    ) -> List[str]:
        """Generate an ordered learning path to target content."""
        path = []
        available_content = set(completed_content)
        
        # Add completed content to path
        for content_id in completed_content:
            if content_id != target_content:
                path.append(content_id)
        
        # Find missing prerequisites
        missing_prerequisites = []
        to_visit = [target_content]
        visited = set()
        
        while to_visit:
            current = to_visit.pop(0)
            if current in visited:
                continue
            visited.add(current)
            
            prerequisites = self.get_prerequisites(current)
            for prereq in prerequisites:
                if prereq not in completed_content and prereq not in visited:
                    missing_prerequisites.append(prereq)
                    to_visit.append(prereq)
        
        # Add missing prerequisites to path
        path.extend(missing_prerequisites[:max_items - len(path)])
        path.append(target_content)
        
        return path[:max_items]
    
    def get_next_recommended_content(
        self, 
        learner_profile: LearnerProfile,
        available_content: List[ContentFeatures],
        completed_ids: List[str],
        top_k: int = 5
    ) -> List[ContentFeatures]:
        """Get the next recommended content based on learning path."""
        # Filter available content
        available = [
            c for c in available_content 
            if c.content_id not in completed_ids and
            self.is_content_available(c.content_id, completed_ids)
        ]
        
        # Score based on prerequisites and learner preferences
        scored = []
        for content in available:
            prereq_score = len([
                p for p in content.prerequisites 
                if p in completed_ids
            ]) / max(len(content.prerequisites), 1)
            
            difficulty_match = 1.0 - abs(
                content.difficulty_level - learner_profile.difficulty_preference
            )
            
            total_score = prereq_score * 0.6 + difficulty_match * 0.4
            scored.append((content, total_score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]


class RecommendationService:
    """
    Main recommendation service combining multiple recommendation strategies.
    """
    
    def __init__(self):
        self.content_similarity_engine = ContentSimilarityEngine()
        self.collaborative_engine = CollaborativeFilteringEngine()
        self.learning_path_engine = LearningPathEngine()
        
        # Content database (would be replaced with actual database)
        self.content_database: Dict[str, ContentFeatures] = {}
        
        # Learner profiles (would be replaced with actual database)
        self.learner_profiles: Dict[str, LearnerProfile] = {}
    
    def register_content(self, content: ContentFeatures):
        """Register content in the recommendation system."""
        self.content_database[content.content_id] = content
    
    def update_learner_profile(self, profile: LearnerProfile):
        """Update learner profile in the system."""
        self.learner_profiles[profile.learner_id] = profile
    
    def record_learner_interaction(
        self,
        learner_id: str,
        content_id: str,
        interaction_type: str,
        duration_seconds: int,
        completed: bool,
        rating: Optional[float] = None
    ):
        """Record a learner interaction for collaborative filtering."""
        # Calculate engagement score
        if content_id in self.content_database:
            content = self.content_database[content_id]
            expected_duration = content.duration_minutes * 60
            engagement = min(1.0, duration_seconds / expected_duration) if expected_duration > 0 else 0.8
            
            if completed:
                engagement = min(1.0, engagement + 0.2)
            
            self.collaborative_engine.record_interaction(
                learner_id, content_id, engagement
            )
        
        # Update learner profile
        if learner_id in self.learner_profiles:
            profile = self.learner_profiles[learner_id]
            
            if interaction_type == 'completed':
                if content_id not in profile.completed_content:
                    profile.completed_content.append(content_id)
                    if content_id in profile.in_progress_content:
                        profile.in_progress_content.remove(content_id)
            
            profile.interaction_count += 1
            profile.last_active = datetime.now()
            
            # Update engagement history
            if content_id not in profile.engagement_history:
                profile.engagement_history[content_id] = 0.0
            profile.engagement_history[content_id] = (
                profile.engagement_history[content_id] * 0.7 + 
                (1.0 if completed else 0.5) * 0.3
            )
    
    def get_recommendations(
        self,
        learner_id: str,
        recommendation_types: Optional[List[RecommendationType]] = None,
        max_items: int = 20,
        context: Optional[Dict[str, Any]] = None
    ) -> RecommendationSet:
        """
        Get personalized recommendations for a learner.
        
        Args:
            learner_id: The learner's unique identifier
            recommendation_types: Types of recommendations to include
            max_items: Maximum number of recommendations to return
            context: Additional context for recommendations
            
        Returns:
            A RecommendationSet containing personalized recommendations
        """
        if learner_id not in self.learner_profiles:
            return RecommendationSet(
                learner_id=learner_id,
                recommendations=[],
                generated_at=datetime.now(),
                context=context or {},
                total_count=0,
                diversity_score=0.0
            )
        
        profile = self.learner_profiles[learner_id]
        all_recommendations: List[Recommendation] = []
        
        if recommendation_types is None:
            recommendation_types = [
                RecommendationType.HYBRID,
                RecommendationType.LEARNING_PATH,
                RecommendationType.NEXT_STEP
            ]
        
        # Get content-based recommendations
        if RecommendationType.CONTENT_BASED in recommendation_types:
            content_based = self._get_content_based_recommendations(profile, max_items // 3)
            all_recommendations.extend(content_based)
        
        # Get collaborative recommendations
        if RecommendationType.COLLABORATIVE in recommendation_types:
            collaborative = self._get_collaborative_recommendations(profile, max_items // 3)
            all_recommendations.extend(collaborative)
        
        # Get similar content recommendations
        if RecommendationType.SIMILAR_CONTENT in recommendation_types:
            similar = self._get_similar_content_recommendations(profile, max_items // 4)
            all_recommendations.extend(similar)
        
        # Get learning path recommendations
        if RecommendationType.LEARNING_PATH in recommendation_types:
            learning_path = self._get_learning_path_recommendations(profile, max_items // 4)
            all_recommendations.extend(learning_path)
        
        # Get next step recommendations
        if RecommendationType.NEXT_STEP in recommendation_types:
            next_steps = self._get_next_step_recommendations(profile, max_items // 4)
            all_recommendations.extend(next_steps)
        
        # Get trending recommendations
        if RecommendationType.TRENDING in recommendation_types:
            trending = self._get_trending_recommendations(max_items // 4)
            all_recommendations.extend(trending)
        
        # Remove already completed content
        completed_ids = set(profile.completed_content)
        filtered = [
            r for r in all_recommendations 
            if r.content_id not in completed_ids
        ]
        
        # Deduplicate and re-score
        content_scores: Dict[str, List[float]] = defaultdict(list)
        for rec in filtered:
            content_scores[rec.content_id].append(rec.score)
        
        final_recommendations = []
        for content_id, scores in content_scores.items():
            if content_id in self.content_database:
                content = self.content_database[content_id]
                avg_score = sum(scores) / len(scores)
                confidence = len(scores) / len(recommendation_types)
                
                recommendation = Recommendation(
                    content_id=content_id,
                    title=content.title,
                    recommendation_type=RecommendationType.HYBRID,
                    score=avg_score,
                    confidence=confidence,
                    reasoning="Combined recommendation from multiple strategies",
                    features_matched=["multiple_sources"],
                    estimated_value=content.engagement_score,
                    created_at=datetime.now()
                )
                final_recommendations.append(recommendation)
        
        # Sort by score and limit
        final_recommendations.sort(key=lambda x: x.score, reverse=True)
        final_recommendations = final_recommendations[:max_items]
        
        # Calculate diversity score
        diversity_score = self._calculate_diversity_score(final_recommendations)
        
        return RecommendationSet(
            learner_id=learner_id,
            recommendations=final_recommendations,
            generated_at=datetime.now(),
            context=context or {},
            total_count=len(final_recommendations),
            diversity_score=diversity_score
        )
    
    def _get_content_based_recommendations(
        self,
        profile: LearnerProfile,
        max_items: int
    ) -> List[Recommendation]:
        """Generate content-based recommendations."""
        recommendations = []
        
        if not profile.completed_content:
            return self._get_popular_recommendations(max_items)
        
        # Get completed content features
        completed_features = [
            self.content_database[c] for c in profile.completed_content
            if c in self.content_database
        ]
        
        if not completed_features:
            return self._get_popular_recommendations(max_items)
        
        # Score all content
        content_scores: Dict[str, float] = {}
        
        for content_id, content in self.content_database.items():
            if content_id in profile.completed_content:
                continue
            
            # Calculate similarity to completed content
            similarities = [
                self.content_similarity_engine.calculate_overall_similarity(content, cf)
                for cf in completed_features
            ]
            
            avg_similarity = sum(similarities) / len(similarities)
            
            # Factor in engagement prediction
            engagement = self.content_similarity_engine.calculate_engagement_prediction(
                content, profile
            )
            
            # Combine scores
            combined_score = avg_similarity * 0.6 + engagement * 0.4
            content_scores[content_id] = combined_score
        
        # Sort and create recommendations
        sorted_content = sorted(
            content_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for content_id, score in sorted_content[:max_items]:
            if content_id in self.content_database:
                content = self.content_database[content_id]
                matched_topics = list(
                    set(content.topics) & set(profile.interests)
                )
                
                recommendations.append(Recommendation(
                    content_id=content_id,
                    title=content.title,
                    recommendation_type=RecommendationType.CONTENT_BASED,
                    score=score,
                    confidence=min(1.0, 0.5 + score * 0.5),
                    reasoning=f"Matches your interests in {', '.join(matched_topics[:3])}",
                    features_matched=matched_topics,
                    estimated_value=content.engagement_score,
                    created_at=datetime.now()
                ))
        
        return recommendations
    
    def _get_collaborative_recommendations(
        self,
        profile: LearnerProfile,
        max_items: int
    ) -> List[Recommendation]:
        """Generate collaborative filtering recommendations."""
        recommendations = []
        
        for content_id in self.content_database:
            if content_id in profile.completed_content:
                continue
            
            predicted_rating = self.collaborative_engine.predict_rating(
                profile.learner_id, content_id
            )
            
            if predicted_rating > 0.5:
                content = self.content_database[content_id]
                
                recommendations.append(Recommendation(
                    content_id=content_id,
                    title=content.title,
                    recommendation_type=RecommendationType.COLLABORATIVE,
                    score=predicted_rating,
                    confidence=0.7,
                    reasoning="Recommended based on similar learners' preferences",
                    features_matched=["collaborative_signal"],
                    estimated_value=content.engagement_score,
                    created_at=datetime.now()
                ))
        
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:max_items]
    
    def _get_similar_content_recommendations(
        self,
        profile: LearnerProfile,
        max_items: int
    ) -> List[Recommendation]:
        """Get content similar to what learner has engaged with."""
        recommendations = []
        
        if not profile.completed_content:
            return []
        
        # Get the most recently completed content
        recent_content = profile.completed_content[-3:]
        
        similar_content: Dict[str, float] = {}
        
        for content_id in recent_content:
            if content_id in self.content_database:
                similar_items = self.collaborative_engine.get_similar_items(
                    content_id, top_k=5
                )
                
                for similar_id, similarity in similar_items:
                    if similar_id not in profile.completed_content:
                        if similar_id not in similar_content:
                            similar_content[similar_id] = 0.0
                        similar_content[similar_id] = max(
                            similar_content[similar_id], similarity
                        )
        
        for content_id, score in sorted(
            similar_content.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:max_items]:
            if content_id in self.content_database:
                content = self.content_database[content_id]
                
                recommendations.append(Recommendation(
                    content_id=content_id,
                    title=content.title,
                    recommendation_type=RecommendationType.SIMILAR_CONTENT,
                    score=score,
                    confidence=0.6,
                    reasoning="Similar to content you recently completed",
                    features_matched=["similar_content"],
                    estimated_value=content.engagement_score,
                    created_at=datetime.now()
                ))
        
        return recommendations
    
    def _get_learning_path_recommendations(
        self,
        profile: LearnerProfile,
        max_items: int
    ) -> List[Recommendation]:
        """Generate learning path-based recommendations."""
        recommendations = []
        
        if not profile.completed_content:
            return []
        
        # Find content that has prerequisites in completed content
        potential_next = []
        
        for content_id, content in self.content_database.items():
            if content_id in profile.completed_content:
                continue
            
            prerequisites = self.learning_path_engine.get_prerequisites(content_id)
            completed_prereqs = [
                p for p in prerequisites 
                if p in profile.completed_content
            ]
            
            if prerequisites and len(completed_prereqs) > 0:
                completion_ratio = len(completed_prereqs) / len(prerequisites)
                difficulty_fit = 1.0 - abs(
                    content.difficulty_level - profile.difficulty_preference
                )
                
                score = completion_ratio * 0.7 + difficulty_fit * 0.3
                potential_next.append((content, score))
        
        potential_next.sort(key=lambda x: x[1], reverse=True)
        
        for content, score in potential_next[:max_items]:
            recommendations.append(Recommendation(
                content_id=content.content_id,
                title=content.title,
                recommendation_type=RecommendationType.LEARNING_PATH,
                score=score,
                confidence=0.8,
                reasoning="Next step in your learning journey",
                features_matched=["learning_path"],
                estimated_value=content.engagement_score,
                created_at=datetime.now()
            ))
        
        return recommendations
    
    def _get_next_step_recommendations(
        self,
        profile: LearnerProfile,
        max_items: int
    ) -> List[Recommendation]:
        """Get the next immediate step recommendations."""
        recommendations = []
        
        available_content = [
            c for c in self.content_database.values()
            if c.content_id not in profile.completed_content and
            self.learning_path_engine.is_content_available(
                c.content_id, profile.completed_content
            )
        ]
        
        next_content = self.learning_path_engine.get_next_recommended_content(
            profile, available_content, profile.completed_content, max_items
        )
        
        for content in next_content:
            # Score based on learner preferences
            difficulty_fit = 1.0 - abs(
                content.difficulty_level - profile.difficulty_preference
            )
            duration_fit = self.content_similarity_engine.calculate_duration_fit(
                content, profile
            )
            
            score = (difficulty_fit + duration_fit) / 2
            
            recommendations.append(Recommendation(
                content_id=content.content_id,
                title=content.title,
                recommendation_type=RecommendationType.NEXT_STEP,
                score=score,
                confidence=0.9,
                reasoning="Perfect next step based on your progress",
                features_matched=["next_step"],
                estimated_value=content.engagement_score,
                created_at=datetime.now()
            ))
        
        return recommendations
    
    def _get_trending_recommendations(
        self,
        max_items: int
    ) -> List[Recommendation]:
        """Get trending content recommendations."""
        recommendations = []
        
        sorted_content = sorted(
            self.content_database.values(),
            key=lambda x: x.popularity_score,
            reverse=True
        )
        
        for content in sorted_content[:max_items]:
            recommendations.append(Recommendation(
                content_id=content.content_id,
                title=content.title,
                recommendation_type=RecommendationType.TRENDING,
                score=content.popularity_score,
                confidence=0.5,
                reasoning="Currently trending among learners",
                features_matched=["trending"],
                estimated_value=content.engagement_score,
                created_at=datetime.now()
            ))
        
        return recommendations
    
    def _get_popular_recommendations(
        self,
        max_items: int
    ) -> List[Recommendation]:
        """Get popular content recommendations for new learners."""
        recommendations = []
        
        sorted_content = sorted(
            self.content_database.values(),
            key=lambda x: (x.average_rating, x.completion_rate),
            reverse=True
        )
        
        for content in sorted_content[:max_items]:
            recommendations.append(Recommendation(
                content_id=content.content_id,
                title=content.title,
                recommendation_type=RecommendationType.POPULAR_NOW,
                score=(content.average_rating + content.completion_rate) / 2,
                confidence=0.6,
                reasoning="Popular among learners like you",
                features_matched=["popular"],
                estimated_value=content.engagement_score,
                created_at=datetime.now()
            ))
        
        return recommendations
    
    def _calculate_diversity_score(
        self,
        recommendations: List[Recommendation]
    ) -> float:
        """Calculate the diversity of recommendations."""
        if len(recommendations) <= 1:
            return 1.0
        
        if not recommendations:
            return 0.0
        
        # Get all topics covered
        all_topics = set()
        for rec in recommendations:
            if rec.content_id in self.content_database:
                content = self.content_database[rec.content_id]
                all_topics.update(content.topics)
        
        # Get recommendation types diversity
        type_counts = defaultdict(int)
        for rec in recommendations:
            type_counts[rec.recommendation_type] += 1
        
        type_diversity = len(type_counts) / len(RecommendationType)
        topic_coverage = len(all_topics) / 20  # Assume 20 is good coverage
        
        return (type_diversity * 0.4 + topic_coverage * 0.6)
    
    def find_similar_content(
        self,
        content_id: str,
        max_items: int = 10
    ) -> List[Tuple[ContentFeatures, float]]:
        """Find content similar to the given content."""
        if content_id not in self.content_database:
            return []
        
        target = self.content_database[content_id]
        similarities = []
        
        for other_id, other_content in self.content_database.items():
            if other_id != content_id:
                sim = self.content_similarity_engine.calculate_overall_similarity(
                    target, other_content
                )
                similarities.append((other_content, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:max_items]
    
    def get_learning_gap_recommendations(
        self,
        learner_id: str,
        target_skills: Dict[str, float],
        max_items: int = 10
    ) -> List[Recommendation]:
        """Get recommendations to fill skill gaps."""
        if learner_id not in self.learner_profiles:
            return []
        
        profile = self.learner_profiles[learner_id]
        recommendations = []
        
        for content_id, content in self.content_database.items():
            if content_id in profile.completed_content:
                continue
            
            # Calculate skill gap coverage
            gap_coverage = 0.0
            covered_skills = []
            
            for skill, target_level in target_skills.items():
                current_level = profile.skill_levels.get(skill, 0.0)
                gap = target_level - current_level
                
                if gap > 0:
                    # Check if content covers this skill
                    if skill in content.topics or skill in content.tags:
                        coverage = min(1.0, gap / target_level)
                        gap_coverage += coverage
                        covered_skills.append(skill)
            
            if gap_coverage > 0 and covered_skills:
                content_score = gap_coverage / len(target_skills)
                
                recommendations.append(Recommendation(
                    content_id=content_id,
                    title=content.title,
                    recommendation_type=RecommendationType.FILL_GAPS,
                    score=content_score,
                    confidence=0.75,
                    reasoning=f"Helps build skills in {', '.join(covered_skills[:3])}",
                    features_matched=covered_skills,
                    estimated_value=content.engagement_score,
                    created_at=datetime.now()
                ))
        
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:max_items]


# Service factory function
def create_recommendation_service() -> RecommendationService:
    """Create and configure a new recommendation service instance."""
    return RecommendationService()
