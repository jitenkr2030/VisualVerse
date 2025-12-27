"""
Engagement Services Package.

Provides gamification, notifications, leaderboards, and learner
motivation features for the VisualVerse platform.
"""

from .engagement_service import (
    EngagementService,
    Notification,
    GamificationRule,
    LearnerGamification,
    Leaderboard,
    LeaderboardEntry,
    EngagementMetrics,
    NotificationType,
    NotificationPriority,
    GamificationEvent,
    create_engagement_service
)

__all__ = [
    "EngagementService",
    "Notification",
    "GamificationRule",
    "LearnerGamification",
    "Leaderboard",
    "LeaderboardEntry",
    "EngagementMetrics",
    "NotificationType",
    "NotificationPriority",
    "GamificationEvent",
    "create_engagement_service"
]
