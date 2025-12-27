"""
Recommendation Models for VisualVerse Recommendation Engine

SQLAlchemy models for user interactions and user profiles used in
recommendation algorithms and machine learning.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey, JSON, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class UserInteraction(Base):
    """Model representing user interactions with content"""
    __tablename__ = "user_interactions"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User and content identifiers
    user_id = Column(String(50), nullable=False, index=True)
    content_id = Column(String(50), nullable=False, index=True)
    
    # Interaction details
    interaction_type = Column(String(20), nullable=False, index=True)  # view, like, complete, share, rate
    value = Column(Float, nullable=False, default=1.0)  # Weight of interaction
    
    # Metadata
    duration_seconds = Column(Integer, nullable=True)  # Time spent on content
    completion_percentage = Column(Float, nullable=True)  # 0.0 to 100.0
    rating = Column(Integer, nullable=True)  # 1-5 star rating
    
    # Additional data
    metadata = Column(JSON, nullable=True)  # Additional interaction data
    session_id = Column(String(50), nullable=True, index=True)  # Session grouping
    
    # Timestamps
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user_profile = relationship("UserProfile", back_populates="interactions")
    content_item = relationship("ContentItem", back_populates="interactions")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_user_content_timestamp', 'user_id', 'content_id', 'timestamp'),
        Index('ix_user_interaction_type', 'user_id', 'interaction_type'),
        Index('ix_content_interaction_type', 'content_id', 'interaction_type'),
        Index('ix_timestamp_range', 'timestamp'),
        UniqueConstraint('user_id', 'content_id', 'interaction_type', 'timestamp', name='uq_interaction')
    )
    
    def __repr__(self):
        return f"<UserInteraction(id='{self.id}', user_id='{self.user_id}', content_id='{self.content_id}', type='{self.interaction_type}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content_id": self.content_id,
            "interaction_type": self.interaction_type,
            "value": self.value,
            "duration_seconds": self.duration_seconds,
            "completion_percentage": self.completion_percentage,
            "rating": self.rating,
            "metadata": self.metadata,
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class UserProfile(Base):
    """Model representing user learning profiles and preferences"""
    __tablename__ = "user_profiles"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), nullable=False, unique=True, index=True)
    
    # Learning preferences
    preferred_subjects = Column(JSON, nullable=True)  # List of subject IDs
    difficulty_preference = Column(Integer, nullable=True)  # Preferred difficulty level 1-5
    learning_style = Column(String(20), nullable=True)  # visual, auditory, kinesthetic, reading
    pace_preference = Column(String(20), nullable=True)  # slow, normal, fast
    
    # Engagement metrics
    total_interactions = Column(Integer, nullable=False, default=0)
    total_view_time_hours = Column(Float, nullable=False, default=0.0)
    completion_rate = Column(Float, nullable=False, default=0.0)  # 0.0 to 1.0
    average_session_duration = Column(Float, nullable=False, default=0.0)  # in minutes
    
    # Learning velocity (concepts learned per week)
    learning_velocity = Column(Float, nullable=True)
    streak_days = Column(Integer, nullable=False, default=0)
    
    # Content preferences based on interactions
    most_engaged_subjects = Column(JSON, nullable=True)  # Subject engagement scores
    most_used_tags = Column(JSON, nullable=True)  # Popular tags for user
    preferred_content_types = Column(JSON, nullable=True)  # video, animation, document, etc.
    
    # Recommendation engine data
    recommendation_feedback = Column(JSON, nullable=True)  # Feedback on recommendations
    last_recommendation_update = Column(DateTime, nullable=True)
    
    # Time-based preferences
    active_hours = Column(JSON, nullable=True)  # Hours when user is most active (0-23)
    active_days = Column(JSON, nullable=True)  # Days when user is most active (0-6)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime, nullable=True, index=True)
    
    # Relationships
    interactions = relationship("UserInteraction", back_populates="user_profile", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_user_profile_last_activity', 'last_activity'),
        Index('ix_user_profile_learning_velocity', 'learning_velocity'),
        Index('ix_user_profile_streak', 'streak_days'),
    )
    
    def __repr__(self):
        return f"<UserProfile(user_id='{self.user_id}', total_interactions={self.total_interactions})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "preferred_subjects": self.preferred_subjects,
            "difficulty_preference": self.difficulty_preference,
            "learning_style": self.learning_style,
            "pace_preference": self.pace_preference,
            "total_interactions": self.total_interactions,
            "total_view_time_hours": self.total_view_time_hours,
            "completion_rate": self.completion_rate,
            "average_session_duration": self.average_session_duration,
            "learning_velocity": self.learning_velocity,
            "streak_days": self.streak_days,
            "most_engaged_subjects": self.most_engaged_subjects,
            "most_used_tags": self.most_used_tags,
            "preferred_content_types": self.preferred_content_types,
            "recommendation_feedback": self.recommendation_feedback,
            "last_recommendation_update": self.last_recommendation_update.isoformat() if self.last_recommendation_update else None,
            "active_hours": self.active_hours,
            "active_days": self.active_days,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }

class ContentItem(Base):
    """Extended content item model with recommendation-specific features"""
    __tablename__ = "content_items"
    
    # Primary key
    id = Column(String(50), primary_key=True)
    
    # Basic content info
    title = Column(String(255), nullable=False)
    content_type = Column(String(20), nullable=False, index=True)  # video, animation, document, interactive
    subject_id = Column(String(50), nullable=False, index=True)
    
    # Content characteristics
    difficulty_level = Column(Integer, nullable=False, default=1)  # 1-5
    estimated_duration = Column(Integer, nullable=True)  # in minutes
    tags = Column(JSON, nullable=True)  # List of tags
    learning_objectives = Column(JSON, nullable=True)  # List of learning objectives
    prerequisites = Column(JSON, nullable=True)  # List of prerequisite concept IDs
    
    # Engagement metrics
    view_count = Column(Integer, nullable=False, default=0, index=True)
    like_count = Column(Integer, nullable=False, default=0)
    share_count = Column(Integer, nullable=False, default=0)
    completion_count = Column(Integer, nullable=False, default=0)
    average_rating = Column(Float, nullable=True)
    average_completion_time = Column(Float, nullable=True)  # Actual time vs estimated
    
    # Recommendation engine features
    popularity_score = Column(Float, nullable=False, default=0.0, index=True)
    novelty_score = Column(Float, nullable=False, default=0.0)  # How new/unique this content is
    diversity_score = Column(Float, nullable=False, default=0.0)  # How diverse the content features are
    
    # Content embeddings (for content-based recommendations)
    feature_vector = Column(JSON, nullable=True)  # Pre-computed feature vector
    embedding_vector = Column(JSON, nullable=True)  # Vector representation for ML
    
    # Metadata
    created_by = Column(String(50), nullable=False, index=True)
    is_published = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interactions = relationship("UserInteraction", back_populates="content_item", cascade="all, delete-orphan")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_content_popularity', 'popularity_score', 'view_count'),
        Index('ix_content_difficulty_subject', 'difficulty_level', 'subject_id'),
        Index('ix_content_engagement', 'average_rating', 'completion_count'),
        Index('ix_content_created_published', 'created_at', 'is_published'),
    )
    
    def __repr__(self):
        return f"<ContentItem(id='{self.id}', title='{self.title}', type='{self.content_type}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "title": self.title,
            "content_type": self.content_type,
            "subject_id": self.subject_id,
            "difficulty_level": self.difficulty_level,
            "estimated_duration": self.estimated_duration,
            "tags": self.tags,
            "learning_objectives": self.learning_objectives,
            "prerequisites": self.prerequisites,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "share_count": self.share_count,
            "completion_count": self.completion_count,
            "average_rating": self.average_rating,
            "average_completion_time": self.average_completion_time,
            "popularity_score": self.popularity_score,
            "novelty_score": self.novelty_score,
            "diversity_score": self.diversity_score,
            "created_by": self.created_by,
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class RecommendationLog(Base):
    """Log of recommendations served to users for tracking and improvement"""
    __tablename__ = "recommendation_logs"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Recommendation context
    user_id = Column(String(50), nullable=False, index=True)
    session_id = Column(String(50), nullable=True, index=True)
    
    # Recommendation details
    recommended_content_ids = Column(JSON, nullable=False)  # List of content IDs
    recommendation_algorithm = Column(String(50), nullable=False, index=True)
    algorithm_version = Column(String(20), nullable=True)
    
    # Context information
    context_data = Column(JSON, nullable=True)  # Additional context (page, search terms, etc.)
    user_state = Column(JSON, nullable=True)  # User state at time of recommendation
    
    # Recommendation quality metrics
    click_through_rate = Column(Float, nullable=True)  # CTR for this recommendation
    conversion_rate = Column(Float, nullable=True)  # Conversion rate (views to completions)
    engagement_score = Column(Float, nullable=True)  # Overall engagement score
    
    # Timestamps
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)  # When recommendation expires
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_recommendation_log_user_time', 'user_id', 'timestamp'),
        Index('ix_recommendation_log_algorithm', 'recommendation_algorithm', 'timestamp'),
        Index('ix_recommendation_log_session', 'session_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<RecommendationLog(id='{self.id}', user_id='{self.user_id}', algorithm='{self.recommendation_algorithm}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for analysis"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "recommended_content_ids": self.recommended_content_ids,
            "recommendation_algorithm": self.recommendation_algorithm,
            "algorithm_version": self.algorithm_version,
            "context_data": self.context_data,
            "user_state": self.user_state,
            "click_through_rate": self.click_through_rate,
            "conversion_rate": self.conversion_rate,
            "engagement_score": self.engagement_score,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }

class ModelPerformance(Base):
    """Track performance metrics for recommendation models"""
    __tablename__ = "model_performance"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Model identification
    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(20), nullable=True)
    training_date = Column(DateTime, nullable=False, index=True)
    
    # Performance metrics
    precision_at_k = Column(Float, nullable=True)  # Precision@K scores
    recall_at_k = Column(Float, nullable=True)    # Recall@K scores
    ndcg = Column(Float, nullable=True)           # Normalized Discounted Cumulative Gain
    hit_rate = Column(Float, nullable=True)       # Hit rate
    
    # Coverage metrics
    catalog_coverage = Column(Float, nullable=True)  # % of catalog covered
    user_coverage = Column(Float, nullable=True)     # % of users with recommendations
    
    # Diversity metrics
    intra_list_diversity = Column(Float, nullable=True)  # Diversity within recommendation lists
    inter_list_diversity = Column(Float, nullable=True)  # Diversity across users
    
    # Novelty metrics
    novelty_score = Column(Float, nullable=True)  # How novel recommendations are
    
    # Timestamps
    evaluation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('ix_model_performance_name_date', 'model_name', 'evaluation_date'),
    )
    
    def __repr__(self):
        return f"<ModelPerformance(model='{self.model_name}', version='{self.model_version}', eval_date='{self.evaluation_date}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for reporting"""
        return {
            "id": self.id,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "training_date": self.training_date.isoformat() if self.training_date else None,
            "precision_at_k": self.precision_at_k,
            "recall_at_k": self.recall_at_k,
            "ndcg": self.ndcg,
            "hit_rate": self.hit_rate,
            "catalog_coverage": self.catalog_coverage,
            "user_coverage": self.user_coverage,
            "intra_list_diversity": self.intra_list_diversity,
            "inter_list_diversity": self.inter_list_diversity,
            "novelty_score": self.novelty_score,
            "evaluation_date": self.evaluation_date.isoformat() if self.evaluation_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class LearningPathProgress(Base):
    """Track user progress through learning paths for path-based recommendations"""
    __tablename__ = "learning_path_progress"
    
    # Primary key
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Identification
    user_id = Column(String(50), nullable=False, index=True)
    learning_path_id = Column(String(50), nullable=False, index=True)
    
    # Progress tracking
    current_position = Column(Integer, nullable=False, default=0)  # Current concept index
    total_concepts = Column(Integer, nullable=False)
    completed_concepts = Column(JSON, nullable=True)  # List of completed concept IDs
    skipped_concepts = Column(JSON, nullable=True)   # List of skipped concept IDs
    
    # Progress metrics
    completion_percentage = Column(Float, nullable=False, default=0.0)  # 0.0 to 100.0
    estimated_time_remaining = Column(Integer, nullable=True)  # Minutes remaining
    actual_time_spent = Column(Integer, nullable=True)  # Total minutes spent
    
    # Learning path specific metrics
    path_difficulty_progress = Column(Float, nullable=True)  # How difficulty has changed
    learning_velocity_path = Column(Float, nullable=True)  # Learning velocity on this path
    
    # Timestamps
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_activity = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('ix_learning_path_progress_user_path', 'user_id', 'learning_path_id'),
        Index('ix_learning_path_progress_activity', 'last_activity'),
        Index('ix_learning_path_progress_completion', 'completion_percentage'),
        UniqueConstraint('user_id', 'learning_path_id', name='uq_user_path_progress')
    )
    
    def __repr__(self):
        return f"<LearningPathProgress(user_id='{self.user_id}', path_id='{self.learning_path_id}', progress={self.completion_percentage}%)>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "learning_path_id": self.learning_path_id,
            "current_position": self.current_position,
            "total_concepts": self.total_concepts,
            "completed_concepts": self.completed_concepts,
            "skipped_concepts": self.skipped_concepts,
            "completion_percentage": self.completion_percentage,
            "estimated_time_remaining": self.estimated_time_remaining,
            "actual_time_spent": self.actual_time_spent,
            "path_difficulty_progress": self.path_difficulty_progress,
            "learning_velocity_path": self.learning_velocity_path,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Additional utility functions for model management
def create_user_interaction(
    user_id: str,
    content_id: str,
    interaction_type: str,
    value: float = 1.0,
    **kwargs
) -> UserInteraction:
    """Factory function to create user interactions"""
    return UserInteraction(
        user_id=user_id,
        content_id=content_id,
        interaction_type=interaction_type,
        value=value,
        **kwargs
    )

def create_user_profile(user_id: str, **kwargs) -> UserProfile:
    """Factory function to create user profiles"""
    return UserProfile(user_id=user_id, **kwargs)

def calculate_popularity_score(content_item: ContentItem) -> float:
    """Calculate popularity score for content based on engagement metrics"""
    try:
        # Weighted combination of engagement metrics
        view_weight = 1.0
        like_weight = 3.0
        completion_weight = 5.0
        share_weight = 2.0
        rating_weight = 4.0
        
        score = (
            content_item.view_count * view_weight +
            content_item.like_count * like_weight +
            content_item.completion_count * completion_weight +
            content_item.share_count * share_weight
        )
        
        # Add rating component if available
        if content_item.average_rating:
            rating_contribution = content_item.average_rating * content_item.completion_count * rating_weight
            score += rating_contribution
        
        # Normalize by recency (newer content gets slight boost)
        if content_item.created_at:
            days_old = (datetime.utcnow() - content_item.created_at).days
            recency_boost = max(0.1, 1.0 - (days_old / 365.0))  # Boost decreases over year
            score *= recency_boost
        
        return max(0.0, score)
        
    except Exception as e:
        logger.error(f"Error calculating popularity score: {e}")
        return 0.0

def update_content_engagement_metrics(content_item: ContentItem, interactions: List[UserInteraction]):
    """Update engagement metrics for content based on interactions"""
    try:
        # Reset counters
        content_item.view_count = 0
        content_item.like_count = 0
        content_item.share_count = 0
        content_item.completion_count = 0
        total_rating = 0
        rating_count = 0
        
        for interaction in interactions:
            if interaction.interaction_type == "view":
                content_item.view_count += 1
            elif interaction.interaction_type == "like":
                content_item.like_count += 1
            elif interaction.interaction_type == "share":
                content_item.share_count += 1
            elif interaction.interaction_type == "complete":
                content_item.completion_count += 1
            elif interaction.interaction_type == "rate" and interaction.rating:
                total_rating += interaction.rating
                rating_count += 1
        
        # Calculate average rating
        if rating_count > 0:
            content_item.average_rating = total_rating / rating_count
        
        # Update popularity score
        content_item.popularity_score = calculate_popularity_score(content_item)
        
    except Exception as e:
        logger.error(f"Error updating content engagement metrics: {e}")