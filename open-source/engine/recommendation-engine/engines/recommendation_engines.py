"""
Recommendation Engines for VisualVerse

Implements collaborative filtering and content-based recommendation engines
for personalized learning content suggestions.
"""

from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from collections import defaultdict, Counter
import math

logger = logging.getLogger(__name__)

@dataclass
class UserInteraction:
    """Represents a user interaction with content"""
    user_id: str
    content_id: str
    interaction_type: str  # view, like, complete, share, rate
    timestamp: datetime
    value: float = 1.0  # Weight of the interaction (1.0 = normal)
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Recommendation:
    """A recommendation with score and reasoning"""
    content_id: str
    score: float
    reason: str
    confidence: float
    recommendation_type: str  # collaborative, content_based, hybrid
    metadata: Optional[Dict[str, Any]] = None

class BaseRecommendationEngine(ABC):
    """Abstract base class for recommendation engines"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_trained = False
    
    @abstractmethod
    def train(self, interactions: List[UserInteraction], content_metadata: Dict[str, Any]) -> None:
        """Train the recommendation model"""
        pass
    
    @abstractmethod
    def recommend(
        self, 
        user_id: str, 
        user_history: List[UserInteraction],
        available_content: List[str],
        num_recommendations: int = 10
    ) -> List[Recommendation]:
        """Generate recommendations for a user"""
        pass
    
    @abstractmethod
    def get_similar_content(
        self, 
        content_id: str, 
        content_metadata: Dict[str, Any],
        num_similar: int = 5
    ) -> List[Recommendation]:
        """Find similar content to given content"""
        pass

class CollaborativeFilteringEngine(BaseRecommendationEngine):
    """Collaborative filtering recommendation engine"""
    
    def __init__(self, name: str = "collaborative_filtering"):
        super().__init__(name)
        self.user_item_matrix = None
        self.similarity_matrix = None
        self.content_similarity = None
        self.interaction_weights = {
            'view': 1.0,
            'like': 3.0,
            'complete': 5.0,
            'share': 2.0,
            'rate': 4.0
        }
    
    def train(self, interactions: List[UserInteraction], content_metadata: Dict[str, Any]) -> None:
        """Train collaborative filtering model"""
        try:
            logger.info(f"Training collaborative filtering engine with {len(interactions)} interactions")
            
            # Convert interactions to DataFrame
            df = pd.DataFrame([
                {
                    'user_id': interaction.user_id,
                    'content_id': interaction.content_id,
                    'weight': self.interaction_weights.get(interaction.interaction_type, 1.0) * interaction.value,
                    'timestamp': interaction.timestamp
                }
                for interaction in interactions
            ])
            
            if df.empty:
                logger.warning("No interactions provided for training")
                return
            
            # Create user-item matrix
            self.user_item_matrix = df.pivot_table(
                index='user_id',
                columns='content_id',
                values='weight',
                fill_value=0.0
            )
            
            # Calculate user similarity using cosine similarity
            self._calculate_user_similarity()
            
            # Calculate content similarity
            self._calculate_content_similarity()
            
            self.is_trained = True
            logger.info("Collaborative filtering engine training completed")
            
        except Exception as e:
            logger.error(f"Error training collaborative filtering engine: {e}")
            raise
    
    def recommend(
        self,
        user_id: str,
        user_history: List[UserInteraction],
        available_content: List[str],
        num_recommendations: int = 10
    ) -> List[Recommendation]:
        """Generate collaborative filtering recommendations"""
        if not self.is_trained:
            logger.warning("Engine not trained yet")
            return []
        
        try:
            if user_id not in self.user_item_matrix.index:
                # Cold start problem - return popular content
                return self._get_popular_content(available_content, num_recommendations)
            
            # Get user's interaction vector
            user_vector = self.user_item_matrix.loc[user_id].values
            user_similarities = self.similarity_matrix.loc[user_id].values if user_id in self.similarity_matrix.index else []
            
            # Calculate predicted scores for unrated items
            scores = {}
            for content_id in available_content:
                if content_id not in self.user_item_matrix.columns:
                    continue
                
                content_idx = list(self.user_item_matrix.columns).index(content_id)
                
                if user_vector[content_idx] > 0:
                    continue  # Already interacted with this content
                
                # Calculate weighted average from similar users
                numerator = 0.0
                denominator = 0.0
                
                for other_user_idx, other_user_id in enumerate(self.user_item_matrix.index):
                    if other_user_id == user_id:
                        continue
                    
                    other_user_vector = self.user_item_matrix.iloc[other_user_idx].values
                    similarity = user_similarities[other_user_idx] if len(user_similarities) > other_user_idx else 0.0
                    
                    if similarity > 0 and other_user_vector[content_idx] > 0:
                        numerator += similarity * other_user_vector[content_idx]
                        denominator += abs(similarity)
                
                if denominator > 0:
                    scores[content_id] = numerator / denominator
            
            # Sort by score and return top recommendations
            sorted_content = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for content_id, score in sorted_content[:num_recommendations]:
                recommendations.append(Recommendation(
                    content_id=content_id,
                    score=score,
                    reason="Users with similar preferences also engaged with this content",
                    confidence=min(score / 5.0, 1.0),  # Normalize confidence
                    recommendation_type="collaborative",
                    metadata={"algorithm": "collaborative_filtering"}
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating collaborative filtering recommendations: {e}")
            return []
    
    def get_similar_content(
        self,
        content_id: str,
        content_metadata: Dict[str, Any],
        num_similar: int = 5
    ) -> List[Recommendation]:
        """Find content similar to given content"""
        if not self.is_trained or content_id not in self.content_similarity.index:
            return []
        
        try:
            # Get similarity scores for the content
            similarities = self.content_similarity.loc[content_id].sort_values(ascending=False)
            
            # Remove self-similarity and get top similar content
            similar_content = []
            for other_content_id, similarity in similarities.items():
                if other_content_id != content_id and similarity > 0:
                    similar_content.append((other_content_id, similarity))
            
            # Convert to recommendations
            recommendations = []
            for content_id, score in similar_content[:num_similar]:
                recommendations.append(Recommendation(
                    content_id=content_id,
                    score=score,
                    reason="Users who engaged with this content also engaged with similar content",
                    confidence=score,
                    recommendation_type="collaborative",
                    metadata={"algorithm": "collaborative_filtering", "similarity_score": score}
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error finding similar content: {e}")
            return []
    
    def _calculate_user_similarity(self):
        """Calculate user-user similarity matrix"""
        try:
            # Calculate cosine similarity between users
            user_matrix = self.user_item_matrix.values
            
            # Calculate norms
            norms = np.linalg.norm(user_matrix, axis=1, keepdims=True)
            
            # Calculate cosine similarity matrix
            similarity_matrix = np.dot(user_matrix, user_matrix.T)
            similarity_matrix = similarity_matrix / (norms * norms.T)
            
            # Replace NaN and inf with 0
            similarity_matrix = np.nan_to_num(similarity_matrix, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Convert to DataFrame
            self.similarity_matrix = pd.DataFrame(
                similarity_matrix,
                index=self.user_item_matrix.index,
                columns=self.user_item_matrix.index
            )
            
        except Exception as e:
            logger.error(f"Error calculating user similarity: {e}")
            self.similarity_matrix = pd.DataFrame()
    
    def _calculate_content_similarity(self):
        """Calculate content-content similarity matrix"""
        try:
            # Calculate cosine similarity between content
            content_matrix = self.user_item_matrix.T.values
            
            # Calculate norms
            norms = np.linalg.norm(content_matrix, axis=0, keepdims=True)
            
            # Calculate cosine similarity matrix
            similarity_matrix = np.dot(content_matrix.T, content_matrix)
            similarity_matrix = similarity_matrix / (norms.T * norms)
            
            # Replace NaN and inf with 0
            similarity_matrix = np.nan_to_num(similarity_matrix, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Convert to DataFrame
            self.content_similarity = pd.DataFrame(
                similarity_matrix,
                index=self.user_item_matrix.columns,
                columns=self.user_item_matrix.columns
            )
            
        except Exception as e:
            logger.error(f"Error calculating content similarity: {e}")
            self.content_similarity = pd.DataFrame()
    
    def _get_popular_content(self, available_content: List[str], num_recommendations: int) -> List[Recommendation]:
        """Get popular content for cold start users"""
        try:
            if self.user_item_matrix.empty:
                return []
            
            # Calculate popularity scores
            popularity_scores = self.user_item_matrix.sum(axis=0)
            popular_content = popularity_scores.sort_values(ascending=False)
            
            recommendations = []
            for content_id in popular_content.index[:num_recommendations]:
                if content_id in available_content:
                    score = float(popular_content[content_id])
                    recommendations.append(Recommendation(
                        content_id=content_id,
                        score=score,
                        reason="Popular content among users",
                        confidence=min(score / 10.0, 1.0),
                        recommendation_type="collaborative",
                        metadata={"algorithm": "collaborative_filtering", "popularity_score": score}
                    ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting popular content: {e}")
            return []

class ContentBasedEngine(BaseRecommendationEngine):
    """Content-based recommendation engine"""
    
    def __init__(self, name: str = "content_based"):
        super().__init__(name)
        self.content_features = None
        self.feature_weights = {
            'difficulty_level': 1.0,
            'estimated_duration': 0.8,
            'tags': 2.0,
            'subject_id': 1.5,
            'learning_objectives': 1.2
        }
    
    def train(self, interactions: List[UserInteraction], content_metadata: Dict[str, Any]) -> None:
        """Train content-based model"""
        try:
            logger.info(f"Training content-based engine with {len(content_metadata)} content items")
            
            if not content_metadata:
                logger.warning("No content metadata provided for training")
                return
            
            # Create content feature matrix
            self._create_feature_matrix(content_metadata)
            
            self.is_trained = True
            logger.info("Content-based engine training completed")
            
        except Exception as e:
            logger.error(f"Error training content-based engine: {e}")
            raise
    
    def recommend(
        self,
        user_id: str,
        user_history: List[UserInteraction],
        available_content: List[str],
        num_recommendations: int = 10
    ) -> List[Recommendation]:
        """Generate content-based recommendations"""
        if not self.is_trained:
            logger.warning("Engine not trained yet")
            return []
        
        try:
            if not user_history:
                # No user history - return content based on general preferences
                return self._get_default_recommendations(available_content, num_recommendations)
            
            # Build user preference profile
            user_profile = self._build_user_profile(user_history)
            
            # Calculate similarity scores for available content
            scores = {}
            for content_id in available_content:
                if content_id not in self.content_features.index:
                    continue
                
                content_features = self.content_features.loc[content_id].values
                similarity = self._calculate_cosine_similarity(user_profile, content_features)
                
                if similarity > 0:
                    scores[content_id] = similarity
            
            # Sort by score and return top recommendations
            sorted_content = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for content_id, score in sorted_content[:num_recommendations]:
                recommendations.append(Recommendation(
                    content_id=content_id,
                    score=score,
                    reason="Content matches your learning preferences and history",
                    confidence=score,
                    recommendation_type="content_based",
                    metadata={"algorithm": "content_based", "similarity_score": score}
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating content-based recommendations: {e}")
            return []
    
    def get_similar_content(
        self,
        content_id: str,
        content_metadata: Dict[str, Any],
        num_similar: int = 5
    ) -> List[Recommendation]:
        """Find content similar to given content based on features"""
        if not self.is_trained or content_id not in self.content_features.index:
            return []
        
        try:
            # Get features of the target content
            target_features = self.content_features.loc[content_id].values
            
            # Calculate similarity with all other content
            similarities = {}
            for other_content_id in self.content_features.index:
                if other_content_id != content_id:
                    other_features = self.content_features.loc[other_content_id].values
                    similarity = self._calculate_cosine_similarity(target_features, other_features)
                    if similarity > 0:
                        similarities[other_content_id] = similarity
            
            # Sort by similarity and return top results
            sorted_similar = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for content_id, score in sorted_similar[:num_similar]:
                recommendations.append(Recommendation(
                    content_id=content_id,
                    score=score,
                    reason="Content has similar features and characteristics",
                    confidence=score,
                    recommendation_type="content_based",
                    metadata={"algorithm": "content_based", "similarity_score": score}
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error finding similar content: {e}")
            return []
    
    def _create_feature_matrix(self, content_metadata: Dict[str, Any]):
        """Create feature matrix from content metadata"""
        try:
            features_data = []
            feature_names = set()
            
            for content_id, metadata in content_metadata.items():
                row = {'content_id': content_id}
                
                # Add numeric features
                if 'difficulty_level' in metadata:
                    row['difficulty_level'] = metadata['difficulty_level']
                    feature_names.add('difficulty_level')
                
                if 'estimated_duration' in metadata:
                    row['estimated_duration'] = metadata['estimated_duration'] or 0
                    feature_names.add('estimated_duration')
                
                # Add categorical features (one-hot encoded)
                if 'subject_id' in metadata:
                    row[f'subject_{metadata["subject_id"]}'] = 1
                    feature_names.add(f'subject_{metadata["subject_id"]}')
                
                # Add tag features
                if 'tags' in metadata and metadata['tags']:
                    for tag in metadata['tags']:
                        tag_key = f'tag_{tag.lower().replace(" ", "_")}'
                        row[tag_key] = 1
                        feature_names.add(tag_key)
                
                features_data.append(row)
            
            # Convert to DataFrame
            df = pd.DataFrame(features_data)
            df = df.set_index('content_id')
            
            # Fill missing values with 0
            df = df.fillna(0)
            
            # Normalize numeric features
            numeric_columns = ['difficulty_level', 'estimated_duration']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = (df[col] - df[col].mean()) / (df[col].std() + 1e-8)
            
            self.content_features = df
            
        except Exception as e:
            logger.error(f"Error creating feature matrix: {e}")
            raise
    
    def _build_user_profile(self, user_history: List[UserInteraction]) -> np.ndarray:
        """Build user preference profile from interaction history"""
        try:
            if not self.content_features.empty:
                # Weight interactions by type
                weighted_features = None
                total_weight = 0
                
                for interaction in user_history:
                    if interaction.content_id in self.content_features.index:
                        weight = self.interaction_weights.get(interaction.interaction_type, 1.0) * interaction.value
                        
                        if weighted_features is None:
                            weighted_features = self.content_features.loc[interaction.content_id].values * weight
                        else:
                            weighted_features += self.content_features.loc[interaction.content_id].values * weight
                        
                        total_weight += weight
                
                if weighted_features is not None and total_weight > 0:
                    return weighted_features / total_weight
            
            # Fallback: return mean features
            return self.content_features.mean().values if not self.content_features.empty else np.array([])
            
        except Exception as e:
            logger.error(f"Error building user profile: {e}")
            return np.array([])
    
    def _calculate_cosine_similarity(self, vector1: np.ndarray, vector2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            if len(vector1) != len(vector2):
                return 0.0
            
            # Calculate dot product and norms
            dot_product = np.dot(vector1, vector2)
            norm1 = np.linalg.norm(vector1)
            norm2 = np.linalg.norm(vector2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return max(0.0, similarity)  # Ensure non-negative
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def _get_default_recommendations(self, available_content: List[str], num_recommendations: int) -> List[Recommendation]:
        """Get default recommendations for users with no history"""
        try:
            if self.content_features.empty:
                return []
            
            # Use content with highest average similarity to all other content
            content_scores = {}
            
            for content_id in available_content:
                if content_id in self.content_features.index:
                    features = self.content_features.loc[content_id].values
                    
                    # Calculate similarity with all other content
                    total_similarity = 0
                    count = 0
                    
                    for other_id in self.content_features.index:
                        if other_id != content_id:
                            other_features = self.content_features.loc[other_id].values
                            similarity = self._calculate_cosine_similarity(features, other_features)
                            total_similarity += similarity
                            count += 1
                    
                    if count > 0:
                        content_scores[content_id] = total_similarity / count
            
            # Sort by score and return recommendations
            sorted_content = sorted(content_scores.items(), key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for content_id, score in sorted_content[:num_recommendations]:
                recommendations.append(Recommendation(
                    content_id=content_id,
                    score=score,
                    reason="Popular content with good feature diversity",
                    confidence=min(score, 1.0),
                    recommendation_type="content_based",
                    metadata={"algorithm": "content_based", "diversity_score": score}
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting default recommendations: {e}")
            return []

class HybridRecommendationEngine(BaseRecommendationEngine):
    """Hybrid recommendation engine combining multiple approaches"""
    
    def __init__(self, engines: List[BaseRecommendationEngine], name: str = "hybrid"):
        super().__init__(name)
        self.engines = engines
        self.weights = {engine.name: 1.0 for engine in engines}
    
    def set_engine_weights(self, weights: Dict[str, float]):
        """Set weights for different engines"""
        for engine_name, weight in weights.items():
            if engine_name in self.weights:
                self.weights[engine_name] = weight
    
    def train(self, interactions: List[UserInteraction], content_metadata: Dict[str, Any]) -> None:
        """Train all component engines"""
        try:
            logger.info(f"Training hybrid engine with {len(self.engines)} component engines")
            
            for engine in self.engines:
                logger.info(f"Training {engine.name} engine")
                engine.train(interactions, content_metadata)
            
            self.is_trained = True
            logger.info("Hybrid engine training completed")
            
        except Exception as e:
            logger.error(f"Error training hybrid engine: {e}")
            raise
    
    def recommend(
        self,
        user_id: str,
        user_history: List[UserInteraction],
        available_content: List[str],
        num_recommendations: int = 10
    ) -> List[Recommendation]:
        """Generate hybrid recommendations"""
        if not self.is_trained:
            logger.warning("Engine not trained yet")
            return []
        
        try:
            # Get recommendations from all engines
            all_recommendations = defaultdict(lambda: {'score': 0.0, 'reasons': [], 'confidences': [], 'types': []})
            
            for engine in self.engines:
                if not engine.is_trained:
                    continue
                
                engine_recommendations = engine.recommend(user_id, user_history, available_content, num_recommendations * 2)
                weight = self.weights.get(engine.name, 1.0)
                
                for rec in engine_recommendations:
                    content_id = rec.content_id
                    weighted_score = rec.score * weight
                    
                    all_recommendations[content_id]['score'] += weighted_score
                    all_recommendations[content_id]['reasons'].append(rec.reason)
                    all_recommendations[content_id]['confidences'].append(rec.confidence)
                    all_recommendations[content_id]['types'].append(rec.recommendation_type)
            
            # Normalize scores and create final recommendations
            final_recommendations = []
            max_score = max(rec['score'] for rec in all_recommendations.values()) if all_recommendations else 1.0
            
            for content_id, data in all_recommendations.items():
                if data['score'] > 0:
                    normalized_score = data['score'] / max_score
                    avg_confidence = sum(data['confidences']) / len(data['confidences'])
                    combined_reason = f"Recommended by {', '.join(set(data['types']))}: {'; '.join(data['reasons'][:2])}"
                    
                    final_recommendations.append(Recommendation(
                        content_id=content_id,
                        score=normalized_score,
                        reason=combined_reason,
                        confidence=avg_confidence,
                        recommendation_type="hybrid",
                        metadata={
                            "algorithm": "hybrid",
                            "component_engines": list(set(data['types'])),
                            "component_scores": {engine.name: data['score'] for engine in self.engines if engine.name in data['types']}
                        }
                    ))
            
            # Sort by score and return top recommendations
            final_recommendations.sort(key=lambda x: x.score, reverse=True)
            return final_recommendations[:num_recommendations]
            
        except Exception as e:
            logger.error(f"Error generating hybrid recommendations: {e}")
            return []
    
    def get_similar_content(
        self,
        content_id: str,
        content_metadata: Dict[str, Any],
        num_similar: int = 5
    ) -> List[Recommendation]:
        """Find similar content using hybrid approach"""
        if not self.is_trained:
            return []
        
        try:
            # Get similar content from all engines
            all_similar = defaultdict(lambda: {'score': 0.0, 'reasons': [], 'confidences': [], 'types': []})
            
            for engine in self.engines:
                if not engine.is_trained:
                    continue
                
                engine_similar = engine.get_similar_content(content_id, content_metadata, num_similar * 2)
                weight = self.weights.get(engine.name, 1.0)
                
                for rec in engine_similar:
                    content_id = rec.content_id
                    weighted_score = rec.score * weight
                    
                    all_similar[content_id]['score'] += weighted_score
                    all_similar[content_id]['reasons'].append(rec.reason)
                    all_similar[content_id]['confidences'].append(rec.confidence)
                    all_similar[content_id]['types'].append(rec.recommendation_type)
            
            # Sort by score and return top similar content
            sorted_similar = sorted(all_similar.items(), key=lambda x: x[1]['score'], reverse=True)
            
            recommendations = []
            for content_id, data in sorted_similar[:num_similar]:
                avg_confidence = sum(data['confidences']) / len(data['confidences'])
                combined_reason = f"Similar to your content ({', '.join(set(data['types']))})"
                
                recommendations.append(Recommendation(
                    content_id=content_id,
                    score=data['score'],
                    reason=combined_reason,
                    confidence=avg_confidence,
                    recommendation_type="hybrid",
                    metadata={
                        "algorithm": "hybrid",
                        "component_engines": list(set(data['types']))
                    }
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error finding similar content: {e}")
            return []

def create_recommendation_engine(engine_type: str = "hybrid") -> BaseRecommendationEngine:
    """Factory function to create recommendation engines"""
    if engine_type == "collaborative":
        return CollaborativeFilteringEngine()
    elif engine_type == "content_based":
        return ContentBasedEngine()
    elif engine_type == "hybrid":
        # Create a hybrid engine with both approaches
        collaborative = CollaborativeFilteringEngine()
        content_based = ContentBasedEngine()
        hybrid = HybridRecommendationEngine([collaborative, content_based])
        
        # Set balanced weights
        hybrid.set_engine_weights({
            "collaborative_filtering": 0.6,
            "content_based": 0.4
        })
        
        return hybrid
    else:
        raise ValueError(f"Unknown engine type: {engine_type}")