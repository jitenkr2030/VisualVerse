"""
Prediction Service for VisualVerse Recommendation Engine

Aggregates scores from different recommendation engines (weighted average)
to produce final ranked lists of content IDs for users.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import numpy as np
from collections import defaultdict, Counter

from ..models.interaction import UserInteraction, UserProfile, ContentItem
from ..models.user_profile import UserPreferenceProfile, LearningBehaviorPattern
from ..engines.recommendation_engines import (
    BaseRecommendationEngine, Recommendation, CollaborativeFilteringEngine, 
    ContentBasedEngine, HybridRecommendationEngine
)

logger = logging.getLogger(__name__)

@dataclass
class PredictionContext:
    """Context information for predictions"""
    user_id: str
    session_id: Optional[str]
    current_page: Optional[str]
    search_query: Optional[str]
    user_state: Dict[str, Any]
    available_content_ids: List[str]
    context_score: float = 1.0

@dataclass
class WeightedRecommendation:
    """Recommendation with weights and reasoning"""
    content_id: str
    score: float
    confidence: float
    recommendation_type: str
    engine_scores: Dict[str, float]
    reasoning: str
    explanation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PredictionService:
    """Service for generating and aggregating recommendations"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.engines: Dict[str, BaseRecommendationEngine] = {}
        self.engine_weights: Dict[str, float] = {
            "collaborative_filtering": 0.4,
            "content_based": 0.3,
            "hybrid": 0.3
        }
        
        # Context-based weight adjustments
        self.context_weights = {
            "new_user": {"collaborative_filtering": 0.2, "content_based": 0.8},
            "returning_user": {"collaborative_filtering": 0.6, "content_based": 0.4},
            "search_context": {"collaborative_filtering": 0.3, "content_based": 0.7},
            "exploration_mode": {"collaborative_filtering": 0.5, "content_based": 0.5}
        }
    
    def register_engine(self, engine_name: str, engine: BaseRecommendationEngine):
        """Register a recommendation engine"""
        self.engines[engine_name] = engine
        logger.info(f"Registered recommendation engine: {engine_name}")
    
    def set_engine_weights(self, weights: Dict[str, float]):
        """Set weights for different engines"""
        self.engine_weights.update(weights)
        logger.info(f"Updated engine weights: {weights}")
    
    def predict_recommendations(
        self,
        user_id: str,
        num_recommendations: int = 10,
        context: Optional[PredictionContext] = None
    ) -> List[WeightedRecommendation]:
        """
        Generate final recommendations by aggregating multiple engines
        
        Args:
            user_id: User identifier
            num_recommendations: Number of recommendations to generate
            context: Additional context for personalized recommendations
            
        Returns:
            List of weighted recommendations
        """
        try:
            # Get user data and context
            user_data = self._get_user_data(user_id)
            if not user_data:
                logger.warning(f"No data found for user {user_id}")
                return self._get_fallback_recommendations(num_recommendations)
            
            # Determine context and adjust weights
            context_type = self._determine_context_type(user_data, context)
            adjusted_weights = self._adjust_weights_for_context(context_type)
            
            # Get available content
            available_content = self._get_available_content()
            
            # Get user interaction history
            user_history = self._get_user_interactions(user_id)
            
            # Generate recommendations from each engine
            engine_recommendations = {}
            for engine_name, engine in self.engines.items():
                if not engine.is_trained:
                    logger.warning(f"Engine {engine_name} is not trained")
                    continue
                
                try:
                    recommendations = engine.recommend(
                        user_id=user_id,
                        user_history=user_history,
                        available_content=available_content,
                        num_recommendations=num_recommendations * 2  # Get more to ensure good coverage
                    )
                    engine_recommendations[engine_name] = recommendations
                    
                except Exception as e:
                    logger.error(f"Error getting recommendations from {engine_name}: {e}")
                    continue
            
            # Aggregate recommendations
            aggregated = self._aggregate_recommendations(
                engine_recommendations, 
                adjusted_weights, 
                context
            )
            
            # Apply post-processing filters
            filtered_recommendations = self._apply_filters(
                aggregated, 
                user_data, 
                context, 
                num_recommendations
            )
            
            # Rank and return final recommendations
            final_recommendations = self._rank_recommendations(filtered_recommendations)
            
            logger.info(f"Generated {len(final_recommendations)} recommendations for user {user_id}")
            return final_recommendations[:num_recommendations]
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user_id}: {e}")
            return self._get_fallback_recommendations(num_recommendations)
    
    def predict_similar_content(
        self,
        content_id: str,
        num_recommendations: int = 5,
        exclude_interacted: bool = True
    ) -> List[WeightedRecommendation]:
        """
        Generate similar content recommendations
        
        Args:
            content_id: Content to find similarities for
            num_recommendations: Number of similar items to return
            exclude_interacted: Whether to exclude content user has already interacted with
            
        Returns:
            List of similar content recommendations
        """
        try:
            # Get content metadata
            content_metadata = self._get_content_metadata({content_id})
            if not content_metadata:
                return []
            
            # Generate similar content from each engine
            engine_similar = {}
            for engine_name, engine in self.engines.items():
                if not engine.is_trained:
                    continue
                
                try:
                    similar = engine.get_similar_content(
                        content_id=content_id,
                        content_metadata=content_metadata,
                        num_similar=num_recommendations * 2
                    )
                    engine_similar[engine_name] = similar
                    
                except Exception as e:
                    logger.error(f"Error getting similar content from {engine_name}: {e}")
                    continue
            
            # Aggregate similar content
            aggregated = self._aggregate_similar_content(engine_similar, self.engine_weights)
            
            # Apply filters
            if exclude_interacted:
                user_id = self._get_user_for_content(content_id)  # This might need adjustment
                if user_id:
                    interacted_content = self._get_user_interacted_content(user_id)
                    aggregated = [rec for rec in aggregated if rec.content_id not in interacted_content]
            
            # Rank and return
            return self._rank_recommendations(aggregated)[:num_recommendations]
            
        except Exception as e:
            logger.error(f"Error generating similar content recommendations: {e}")
            return []
    
    def predict_next_in_learning_path(
        self,
        user_id: str,
        learning_path_id: str,
        current_position: int
    ) -> List[WeightedRecommendation]:
        """
        Predict next recommended items in a learning path
        
        Args:
            user_id: User identifier
            learning_path_id: Learning path identifier
            current_position: Current position in the path
            
        Returns:
            Recommended next items in the learning path
        """
        try:
            # Get learning path structure
            path_structure = self._get_learning_path_structure(learning_path_id)
            if not path_structure:
                return []
            
            # Get user's progress in this path
            user_progress = self._get_user_learning_path_progress(user_id, learning_path_id)
            
            # Determine next recommended items
            next_items = self._determine_next_learning_items(
                path_structure, 
                user_progress, 
                current_position
            )
            
            # Get recommendations for each next item
            recommendations = []
            for item_id in next_items[:3]:  # Recommend up to 3 next items
                item_recommendations = self.predict_similar_content(
                    content_id=item_id,
                    num_recommendations=1,
                    exclude_interacted=True
                )
                recommendations.extend(item_recommendations)
            
            # Rank by learning path order
            return self._rank_by_learning_path_order(recommendations, next_items)
            
        except Exception as e:
            logger.error(f"Error predicting next learning path items: {e}")
            return []
    
    def get_personalized_diversity(
        self,
        recommendations: List[WeightedRecommendation],
        diversity_target: float = 0.7
    ) -> List[WeightedRecommendation]:
        """
        Apply diversity to recommendations to avoid filter bubbles
        
        Args:
            recommendations: List of recommendations
            diversity_target: Target diversity score (0-1)
            
        Returns:
            Diversified recommendations
        """
        try:
            if len(recommendations) <= 1:
                return recommendations
            
            # Get content metadata for diversity calculation
            content_ids = [rec.content_id for rec in recommendations]
            content_metadata = self._get_content_metadata(content_ids)
            
            # Calculate diversity scores
            diversity_scores = self._calculate_content_diversity(
                recommendations, 
                content_metadata
            )
            
            # Re-rank for diversity
            diversified = self._optimize_for_diversity(
                recommendations, 
                diversity_scores, 
                diversity_target
            )
            
            return diversified
            
        except Exception as e:
            logger.error(f"Error applying diversity to recommendations: {e}")
            return recommendations
    
    def explain_recommendation(
        self,
        recommendation: WeightedRecommendation,
        user_id: str,
        context: Optional[PredictionContext] = None
    ) -> Dict[str, Any]:
        """
        Generate explanation for why a recommendation was made
        
        Args:
            recommendation: The recommendation to explain
            user_id: User identifier
            context: Context information
            
        Returns:
            Explanation details
        """
        try:
            # Get user data
            user_data = self._get_user_data(user_id)
            content_metadata = self._get_content_metadata({recommendation.content_id})
            
            # Generate explanation based on recommendation type
            if recommendation.recommendation_type == "collaborative":
                explanation = self._explain_collaborative_recommendation(
                    recommendation, user_data, content_metadata
                )
            elif recommendation.recommendation_type == "content_based":
                explanation = self._explain_content_based_recommendation(
                    recommendation, user_data, content_metadata
                )
            elif recommendation.recommendation_type == "hybrid":
                explanation = self._explain_hybrid_recommendation(
                    recommendation, user_data, content_metadata
                )
            else:
                explanation = {"reason": "Recommended based on your learning profile"}
            
            # Add confidence and reasoning
            explanation.update({
                "confidence": recommendation.confidence,
                "engine_scores": recommendation.engine_scores,
                "reasoning": recommendation.reasoning,
                "recommendation_type": recommendation.recommendation_type
            })
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating recommendation explanation: {e}")
            return {"reason": "Recommended for you", "confidence": recommendation.confidence}
    
    def _get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive user data for recommendations"""
        try:
            # Get user profile
            user_profile = self.db.query(UserProfile).filter(
                UserProfile.user_id == user_id
            ).first()
            
            # Get preference profile
            preference_profile = self.db.query(UserPreferenceProfile).filter(
                UserPreferenceProfile.user_id == user_id
            ).first()
            
            # Get learning behavior patterns
            behavior_patterns = self.db.query(LearningBehaviorPattern).filter(
                LearningBehaviorPattern.user_id == user_id
            ).all()
            
            return {
                "user_profile": user_profile,
                "preference_profile": preference_profile,
                "behavior_patterns": [bp.to_dict() for bp in behavior_patterns] if behavior_patterns else []
            }
            
        except Exception as e:
            logger.error(f"Error getting user data for {user_id}: {e}")
            return None
    
    def _get_user_interactions(self, user_id: str) -> List[UserInteraction]:
        """Get user interaction history"""
        try:
            interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).order_by(UserInteraction.timestamp.desc()).all()
            
            return interactions
            
        except Exception as e:
            logger.error(f"Error getting user interactions for {user_id}: {e}")
            return []
    
    def _get_available_content(self) -> List[str]:
        """Get list of available content IDs"""
        try:
            content_items = self.db.query(ContentItem).filter(
                ContentItem.is_published == True
            ).all()
            
            return [item.id for item in content_items]
            
        except Exception as e:
            logger.error(f"Error getting available content: {e}")
            return []
    
    def _get_content_metadata(self, content_ids: List[str]) -> Dict[str, Any]:
        """Get metadata for specified content items"""
        try:
            if not content_ids:
                return {}
            
            content_items = self.db.query(ContentItem).filter(
                ContentItem.id.in_(content_ids)
            ).all()
            
            metadata = {}
            for item in content_items:
                metadata[item.id] = {
                    "title": item.title,
                    "content_type": item.content_type,
                    "subject_id": item.subject_id,
                    "difficulty_level": item.difficulty_level,
                    "estimated_duration": item.estimated_duration,
                    "tags": item.tags or [],
                    "learning_objectives": item.learning_objectives or [],
                    "prerequisites": item.prerequisites or [],
                    "popularity_score": item.popularity_score
                }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error getting content metadata: {e}")
            return {}
    
    def _determine_context_type(self, user_data: Dict[str, Any], context: Optional[PredictionContext]) -> str:
        """Determine the context type for weight adjustment"""
        try:
            user_profile = user_data.get("user_profile")
            
            # Check if user is new (few interactions)
            if not user_profile or user_profile.total_interactions < 5:
                return "new_user"
            
            # Check if this is a search context
            if context and context.search_query:
                return "search_context"
            
            # Check if user prefers exploration
            preference_profile = user_data.get("preference_profile")
            if preference_profile and preference_profile.goal_specificity == "exploratory":
                return "exploration_mode"
            
            # Default to returning user
            return "returning_user"
            
        except Exception as e:
            logger.error(f"Error determining context type: {e}")
            return "returning_user"
    
    def _adjust_weights_for_context(self, context_type: str) -> Dict[str, float]:
        """Adjust engine weights based on context"""
        base_weights = self.engine_weights.copy()
        context_adjustments = self.context_weights.get(context_type, {})
        
        adjusted_weights = {}
        for engine_name, base_weight in base_weights.items():
            if engine_name in context_adjustments:
                adjusted_weights[engine_name] = context_adjustments[engine_name]
            else:
                adjusted_weights[engine_name] = base_weight
        
        # Normalize weights
        total_weight = sum(adjusted_weights.values())
        if total_weight > 0:
            adjusted_weights = {k: v / total_weight for k, v in adjusted_weights.items()}
        
        return adjusted_weights
    
    def _aggregate_recommendations(
        self,
        engine_recommendations: Dict[str, List[Recommendation]],
        weights: Dict[str, float],
        context: Optional[PredictionContext]
    ) -> List[WeightedRecommendation]:
        """Aggregate recommendations from multiple engines"""
        try:
            # Combine all recommendations
            content_scores = defaultdict(lambda: {
                "total_score": 0.0,
                "engine_scores": {},
                "confidences": [],
                "reasons": [],
                "types": []
            })
            
            for engine_name, recommendations in engine_recommendations.items():
                weight = weights.get(engine_name, 0.0)
                
                for rec in recommendations:
                    content_id = rec.content_id
                    
                    content_scores[content_id]["total_score"] += rec.score * weight
                    content_scores[content_id]["engine_scores"][engine_name] = rec.score
                    content_scores[content_id]["confidences"].append(rec.confidence)
                    content_scores[content_id]["reasons"].append(rec.reason)
                    content_scores[content_id]["types"].append(rec.recommendation_type)
            
            # Convert to WeightedRecommendations
            aggregated = []
            for content_id, scores in content_scores.items():
                avg_confidence = sum(scores["confidences"]) / len(scores["confidences"]) if scores["confidences"] else 0.0
                
                # Combine reasons
                combined_reason = "; ".join(scores["reasons"][:2])  # Top 2 reasons
                
                # Determine primary recommendation type
                type_counts = Counter(scores["types"])
                primary_type = type_counts.most_common(1)[0][0] if type_counts else "hybrid"
                
                aggregated.append(WeightedRecommendation(
                    content_id=content_id,
                    score=scores["total_score"],
                    confidence=avg_confidence,
                    recommendation_type=primary_type,
                    engine_scores=scores["engine_scores"],
                    reasoning=combined_reason
                ))
            
            return aggregated
            
        except Exception as e:
            logger.error(f"Error aggregating recommendations: {e}")
            return []
    
    def _apply_filters(
 recommendations: List[        self,
       WeightedRecommendation],
        user_data: Dict[str, Any],
        context: Optional[PredictionContext],
        target_count: int
    ) -> List[WeightedRecommendation]:
        """Apply filters to recommendations"""
        try:
            filtered = recommendations.copy()
            
            # Filter by content availability
            available_content = set(self._get_available_content())
            filtered = [rec for rec in filtered if rec.content_id in available_content]
            
            # Filter out already consumed content
            user_history = self._get_user_interactions(list(user_data.keys())[0] if user_data else "")
            consumed_content = {interaction.content_id for interaction in user_history}
            filtered = [rec for rec in filtered if rec.content_id not in consumed_content]
            
            # Apply context-specific filters
            if context and context.search_query:
                # For search context, prioritize relevant content
                filtered = self._prioritize_search_relevance(filtered, context.search_query)
            
            # Ensure minimum count
            if len(filtered) < target_count:
                logger.warning(f"Only {len(filtered)} recommendations after filtering, need {target_count}")
            
            return filtered
            
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            return recommendations
    
    def _rank_recommendations(self, recommendations: List[WeightedRecommendation]) -> List[WeightedRecommendation]:
        """Rank recommendations by score and diversity"""
        try:
            # Sort by score primarily
            ranked = sorted(recommendations, key=lambda x: x.score, reverse=True)
            
            # Apply diversity if we have enough recommendations
            if len(ranked) > 5:
                ranked = self.get_personalized_diversity(ranked, diversity_target=0.6)
            
            return ranked
            
        except Exception as e:
            logger.error(f"Error ranking recommendations: {e}")
            return recommendations
    
    def _get_fallback_recommendations(self, num_recommendations: int) -> List[WeightedRecommendation]:
        """Get fallback recommendations when user data is insufficient"""
        try:
            # Get popular content
            popular_content = self.db.query(ContentItem).filter(
                ContentItem.is_published == True
            ).order_by(ContentItem.popularity_score.desc()).limit(num_recommendations).all()
            
            recommendations = []
            for i, content in enumerate(popular_content):
                recommendations.append(WeightedRecommendation(
                    content_id=content.id,
                    score=(num_recommendations - i) / num_recommendations,  # Decreasing scores
                    confidence=0.3,  # Low confidence for fallback
                    recommendation_type="fallback",
                    engine_scores={},
                    reasoning="Popular content among users",
                    explanation="This content is popular among other learners"
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting fallback recommendations: {e}")
            return []
    
    def _explain_collaborative_recommendation(
        self,
        recommendation: WeightedRecommendation,
        user_data: Dict[str, Any],
        content_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Explain collaborative filtering recommendation"""
        return {
            "primary_reason": "Users with similar learning patterns also engaged with this content",
            "supporting_factors": [
                "Similar user preferences",
                "High engagement from peer group",
                "Matches your learning style"
            ],
            "algorithm": "collaborative_filtering"
        }
    
    def _explain_content_based_recommendation(
        self,
        recommendation: WeightedRecommendation,
        user_data: Dict[str, Any],
        content_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Explain content-based recommendation"""
        return {
            "primary_reason": "This content matches your learning preferences and interests",
            "supporting_factors": [
                "Aligns with your subject preferences",
                "Matches your preferred difficulty level",
                "Similar to content you've completed"
            ],
            "algorithm": "content_based"
        }
    
    def _explain_hybrid_recommendation(
        self,
        recommendation: WeightedRecommendation,
        user_data: Dict[str, Any],
        content_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Explain hybrid recommendation"""
        return {
            "primary_reason": "Recommended based on both content similarity and user preferences",
            "supporting_factors": [
                "Matches your learning profile",
                "Popular among similar users",
                "Aligns with your goals"
            ],
            "algorithm": "hybrid"
        }
    
    # Additional helper methods would be implemented here...
    def _calculate_content_diversity(self, recommendations: List[WeightedRecommendation], content_metadata: Dict[str, Any]) -> Dict[str, float]:
        """Calculate diversity scores for content"""
        # Simplified diversity calculation
        diversity_scores = {}
        subjects = set()
        
        for rec in recommendations:
            content_id = rec.content_id
            if content_id in content_metadata:
                subject_id = content_metadata[content_id].get("subject_id")
                if subject_id:
                    subjects.add(subject_id)
                    diversity_scores[content_id] = len(subjects) / len(recommendations)
                else:
                    diversity_scores[content_id] = 0.0
            else:
                diversity_scores[content_id] = 0.0
        
        return diversity_scores
    
    def _optimize_for_diversity(
        self,
        recommendations: List[WeightedRecommendation],
        diversity_scores: Dict[str, float],
        target_diversity: float
    ) -> List[WeightedRecommendation]:
        """Optimize recommendations for diversity"""
        # Simple diversification: ensure subject diversity
        selected = []
        used_subjects = set()
        
        # Sort by a combination of score and diversity
        for rec in recommendations:
            content_id = rec.content_id
            if content_id not in diversity_scores:
                continue
            
            diversity_score = diversity_scores[content_id]
            combined_score = rec.score * (1 - target_diversity) + diversity_score * target_diversity
            
            # Create new recommendation with adjusted score
            adjusted_rec = WeightedRecommendation(
                content_id=content_id,
                score=combined_score,
                confidence=rec.confidence,
                recommendation_type=rec.recommendation_type,
                engine_scores=rec.engine_scores,
                reasoning=rec.reasoning
            )
            selected.append(adjusted_rec)
        
        return sorted(selected, key=lambda x: x.score, reverse=True)
    
    # Placeholder methods for database operations
    def _get_user_for_content(self, content_id: str) -> Optional[str]:
        """Get user ID associated with content (placeholder)"""
        # This would need to be implemented based on your specific use case
        return None
    
    def _get_user_interacted_content(self, user_id: str) -> List[str]:
        """Get content user has already interacted with"""
        try:
            interactions = self._get_user_interactions(user_id)
            return list(set(interaction.content_id for interaction in interactions))
        except:
            return []
    
    def _get_learning_path_structure(self, learning_path_id: str) -> Optional[Dict[str, Any]]:
        """Get learning path structure (placeholder)"""
        # This would be implemented based on your learning path model
        return None
    
    def _get_user_learning_path_progress(self, user_id: str, learning_path_id: str) -> Optional[Dict[str, Any]]:
        """Get user's progress in learning path (placeholder)"""
        # This would be implemented based on your progress tracking model
        return None
    
    def _determine_next_learning_items(self, path_structure: Dict[str, Any], progress: Dict[str, Any], position: int) -> List[str]:
        """Determine next items in learning path (placeholder)"""
        # This would be implemented based on your learning path logic
        return []
    
    def _rank_by_learning_path_order(self, recommendations: List[WeightedRecommendation], path_order: List[str]) -> List[WeightedRecommendation]:
        """Rank recommendations by learning path order (placeholder)"""
        # This would rank recommendations according to path sequence
        return sorted(recommendations, key=lambda x: path_order.index(x.content_id) if x.content_id in path_order else float('inf'))
    
    def _prioritize_search_relevance(self, recommendations: List[WeightedRecommendation], search_query: str) -> List[WeightedRecommendation]:
        """Prioritize recommendations relevant to search query (placeholder)"""
        # This would boost scores for content matching search terms
        return recommendations