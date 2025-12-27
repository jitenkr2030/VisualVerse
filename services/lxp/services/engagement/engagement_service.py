"""
Engagement Service for Learner Experience Platform.

Provides engagement tracking, gamification, notifications,
and learner motivation systems.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import json


class NotificationType(Enum):
    """Types of notifications."""
    ACHIEVEMENT = "achievement"
    MILESTONE = "milestone"
    REMINDER = "reminder"
    FEEDBACK = "feedback"
    STREAK = "streak"
    RECOMMENDATION = "recommendation"
    SOCIAL = "social"
    SYSTEM = "system"


class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class GamificationEvent(Enum):
    """Gamification events."""
    SESSION_COMPLETE = "session_complete"
    CONTENT_COMPLETED = "content_completed"
    STREAK_MAINTAINED = "streak_maintained"
    ACHIEVEMENT_EARNED = "achievement_earned"
    SKILL_MASTERED = "skill_mastered"
    ASSESSMENT_PASSED = "assessment_passed"
    HELPFUL_ACTION = "helpful_action"
    PEER_HELP = "peer_help"


@dataclass
class Notification:
    """A learner notification."""
    notification_id: str
    learner_id: str
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    read: bool = False
    read_at: Optional[datetime] = None
    action_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "learner_id": self.learner_id,
            "type": self.notification_type.value,
            "title": self.title,
            "message": self.message,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "read": self.read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "action_url": self.action_url,
            "metadata": self.metadata,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }


@dataclass
class GamificationRule:
    """A rule for gamification point awards."""
    rule_id: str
    event_type: GamificationEvent
    base_points: int
    multiplier: float = 1.0
    conditions: Dict[str, Any] = field(default_factory=dict)
    max_daily: Optional[int] = None
    description: str = ""
    is_active: bool = True


@dataclass
class LearnerGamification:
    """Gamification state for a learner."""
    learner_id: str
    total_points: int = 0
    level: int = 1
    xp_to_next_level: int = 1000
    badges: List[str] = field(default_factory=list)
    streaks: Dict[str, int] = field(default_factory=dict)  # streak_type -> days
    ranks: Dict[str, int] = field(default_factory=dict)  # category -> rank
    daily_points: Dict[str, int] = field(default_factory=dict)  # date -> points
    weekly_points: Dict[str, int] = field(default_factory=dict)  # week -> points
    total_sessions: int = 0
    total_content_completed: int = 0
    total_achievements: int = 0
    
    def add_xp(self, points: int) -> Tuple[int, int]:
        """Add XP and return (new_total, levels_gained)."""
        self.total_points += points
        self.daily_points[datetime.now().strftime("%Y-%m-%d")] = (
            self.daily_points.get(datetime.now().strftime("%Y-%m-%d"), 0) + points
        )
        
        # Level up logic
        levels_gained = 0
        while self.total_points >= self.xp_to_next_level:
            self.total_points -= self.xp_to_next_level
            self.level += 1
            self.xp_to_next_level = int(self.xp_to_next_level * 1.2)
            levels_gained += 1
        
        return self.total_points, levels_gained


@dataclass
class LeaderboardEntry:
    """An entry on a leaderboard."""
    learner_id: str
    learner_name: str
    score: float
    rank: int
    previous_rank: int
    trend: str = "stable"  # "up", "down", "stable"
    avatar_url: Optional[str] = None


@dataclass
class Leaderboard:
    """A leaderboard configuration and entries."""
    leaderboard_id: str
    name: str
    description: str
    category: str
    time_range: str  # "daily", "weekly", "all_time"
    entries: List[LeaderboardEntry] = field(default_factory=list)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class EngagementMetrics:
    """Engagement metrics for a learner."""
    learner_id: str
    daily_active_days: int = 0
    weekly_active_days: int = 0
    monthly_active_days: int = 0
    average_session_length: float = 0.0
    average_daily_time: float = 0.0
    interaction_rate: float = 0.0
    completion_rate: float = 0.0
    return_rate: float = 0.0
    engagement_score: float = 0.0
    peak_activity_hours: List[int] = field(default_factory=list)
    preferred_content_types: List[str] = field(default_factory=list)


class EngagementService:
    """
    Service for managing learner engagement, gamification, and notifications.
    
    Handles point systems, achievements, leaderboards, notifications,
    and engagement analytics.
    """
    
    def __init__(self):
        self.notifications: Dict[str, Notification] = {}
        self.learner_notifications: Dict[str, List[str]] = defaultdict(list)
        
        self.gamification_rules: Dict[str, GamificationRule] = {}
        self.learner_gamification: Dict[str, LearnerGamification] = {}
        
        self.leaderboards: Dict[str, Leaderboard] = {}
        
        self.engagement_metrics: Dict[str, EngagementMetrics] = {}
        
        # Initialize default rules
        self._init_default_rules()
    
    def _init_default_rules(self):
        """Initialize default gamification rules."""
        rules = [
            GamificationRule(
                rule_id="session_complete",
                event_type=GamificationEvent.SESSION_COMPLETE,
                base_points=10,
                max_daily=100,
                description="Complete a learning session"
            ),
            GamificationRule(
                rule_id="content_complete",
                event_type=GamificationEvent.CONTENT_COMPLETED,
                base_points=50,
                description="Complete a content item"
            ),
            GamificationRule(
                rule_id="streak_day",
                event_type=GamificationEvent.STREAK_MAINTAINED,
                base_points=20,
                max_daily=20,
                description="Maintain daily streak"
            ),
            GamificationRule(
                rule_id="achievement",
                event_type=GamificationEvent.ACHIEVEMENT_EARNED,
                base_points=100,
                description="Earn an achievement"
            ),
            GamificationRule(
                rule_id="skill_master",
                event_type=GamificationEvent.SKILL_MASTERED,
                base_points=200,
                description="Master a skill"
            ),
            GamificationRule(
                rule_id="assessment_pass",
                event_type=GamificationEvent.ASSESSMENT_PASSED,
                base_points=75,
                description="Pass an assessment"
            ),
            GamificationRule(
                rule_id="helpful",
                event_type=GamificationEvent.HELPFUL_ACTION,
                base_points=25,
                description="Use help features appropriately"
            )
        ]
        
        for rule in rules:
            self.gamification_rules[rule.rule_id] = rule
    
    # Notification Management
    def send_notification(
        self,
        learner_id: str,
        notification_type: NotificationType,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        action_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        expires_at: Optional[datetime] = None
    ) -> Notification:
        """Send a notification to a learner."""
        notification = Notification(
            notification_id=f"notif_{learner_id}_{datetime.now().timestamp()}",
            learner_id=learner_id,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            action_url=action_url,
            metadata=metadata or {},
            expires_at=expires_at
        )
        
        self.notifications[notification.notification_id] = notification
        self.learner_notifications[learner_id].append(notification.notification_id)
        
        return notification
    
    def get_notification(
        self,
        notification_id: str
    ) -> Optional[Notification]:
        """Get a specific notification."""
        return self.notifications.get(notification_id)
    
    def get_learner_notifications(
        self,
        learner_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Notification]:
        """Get notifications for a learner."""
        notification_ids = self.learner_notifications.get(learner_id, [])
        notifications = [
            self.notifications[nid] for nid in notification_ids
            if nid in self.notifications
        ]
        
        if unread_only:
            notifications = [n for n in notifications if not n.read]
        
        notifications.sort(
            key=lambda n: n.created_at,
            reverse=True
        )
        
        return notifications[:limit]
    
    def mark_notification_read(
        self,
        notification_id: str
    ) -> Optional[Notification]:
        """Mark a notification as read."""
        notification = self.notifications.get(notification_id)
        if notification:
            notification.read = True
            notification.read_at = datetime.now()
        return notification
    
    def mark_all_read(
        self,
        learner_id: str
    ) -> int:
        """Mark all notifications as read for a learner."""
        count = 0
        for nid in self.learner_notifications.get(learner_id, []):
            notification = self.notifications.get(nid)
            if notification and not notification.read:
                notification.read = True
                notification.read_at = datetime.now()
                count += 1
        return count
    
    def delete_notification(
        self,
        notification_id: str
    ) -> bool:
        """Delete a notification."""
        if notification_id in self.notifications:
            notification = self.notifications[notification_id]
            learner_id = notification.learner_id
            
            if notification_id in self.learner_notifications[learner_id]:
                self.learner_notifications[learner_id].remove(notification_id)
            
            del self.notifications[notification_id]
            return True
        return False
    
    def delete_expired_notifications(self):
        """Delete all expired notifications."""
        now = datetime.now()
        expired = [
            nid for nid, n in self.notifications.items()
            if n.expires_at and n.expires_at < now
        ]
        
        for nid in expired:
            self.delete_notification(nid)
    
    # Gamification
    def get_learner_gamification(
        self,
        learner_id: str
    ) -> LearnerGamification:
        """Get or create gamification state for a learner."""
        if learner_id not in self.learner_gamification:
            self.learner_gamification[learner_id] = LearnerGamification(
                learner_id=learner_id
            )
        return self.learner_gamification[learner_id]
    
    def award_points(
        self,
        learner_id: str,
        event_type: GamificationEvent,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, int, List[str]]:
        """
        Award points for an event.
        
        Returns:
            Tuple of (points_awarded, levels_gained, badges_earned)
        """
        gamification = self.get_learner_gamification(learner_id)
        
        # Find applicable rules
        applicable_rules = [
            rule for rule in self.gamification_rules.values()
            if rule.event_type == event_type and rule.is_active
        ]
        
        points_awarded = 0
        badges_earned = []
        
        for rule in applicable_rules:
            # Check conditions
            if not self._check_rule_conditions(rule, metadata):
                continue
            
            # Check daily limit
            today = datetime.now().strftime("%Y-%m-%d")
            daily_total = gamification.daily_points.get(today, 0)
            if rule.max_daily and daily_total >= rule.max_daily:
                continue
            
            # Calculate points
            rule_points = int(rule.base_points * rule.multiplier)
            
            # Apply daily limit
            remaining = (rule.max_daily or float('inf')) - daily_total
            if rule_points > remaining:
                rule_points = int(remaining)
            
            points_awarded += rule_points
        
        # Award points and check for level up
        if points_awarded > 0:
            _, levels_gained = gamification.add_xp(points_awarded)
            
            # Check for badges
            badges_earned = self._check_badges(gamification)
            
            # Send notification
            if levels_gained > 0:
                self.send_notification(
                    learner_id,
                    NotificationType.ACHIEVEMENT,
                    f"Level Up!",
                    f"Congratulations! You've reached Level {gamification.level}!",
                    priority=NotificationPriority.HIGH,
                    action_url="/profile"
                )
        
        return points_awarded, levels_gained, badges_earned
    
    def _check_rule_conditions(
        self,
        rule: GamificationRule,
        metadata: Optional[Dict[str, Any]]
    ) -> bool:
        """Check if rule conditions are met."""
        if not rule.conditions or not metadata:
            return True
        
        for key, expected in rule.conditions.items():
            if key not in metadata:
                return False
            if metadata[key] != expected:
                return False
        
        return True
    
    def _check_badges(
        self,
        gamification: LearnerGamification
    ) -> List[str]:
        """Check and award badges based on gamification state."""
        badges = []
        
        # Level badges
        level_badges = {
            5: "Rising Star",
            10: "Shining Star",
            25: "Super Star",
            50: "Mega Star",
            100: "Ultimate Star"
        }
        
        for level, badge_name in level_badges.items():
            if gamification.level >= level and badge_name not in gamification.badges:
                gamification.badges.append(badge_name)
                badges.append(badge_name)
        
        # Streak badges
        if 'daily' in gamification.streaks:
            streak_badges = {
                7: "Week Warrior",
                30: "Monthly Master",
                100: "Century Champion"
            }
            
            for streak_days, badge_name in streak_badges.items():
                if gamification.streaks['daily'] >= streak_days and badge_name not in gamification.badges:
                    gamification.badges.append(badge_name)
                    badges.append(badge_name)
        
        return badges
    
    def update_streak(
        self,
        learner_id: str,
        streak_type: str = "daily"
    ) -> Tuple[int, bool]:
        """
        Update a learning streak.
        
        Returns:
            Tuple of (current_streak, is_new_record)
        """
        gamification = self.get_learner_gamification(learner_id)
        
        current = gamification.streaks.get(streak_type, 0)
        today = datetime.now().date()
        
        # Get last activity
        last_activity = self._get_last_activity_date(learner_id)
        
        is_consecutive = (
            last_activity is None or
            last_activity == today or
            last_activity == today - timedelta(days=1)
        )
        
        if last_activity == today:
            # Already updated today
            return current, False
        
        if is_consecutive:
            gamification.streaks[streak_type] = current + 1
            is_new_record = gamification.streaks[streak_type] > current
            current = gamification.streaks[streak_type]
            
            # Award streak points
            self.award_points(learner_id, GamificationEvent.STREAK_MAINTAINED)
            
            # Check for streak milestones
            if current in [7, 30, 100]:
                self.send_notification(
                    learner_id,
                    NotificationType.STREAK,
                    f"Streak Milestone!",
                    f"Amazing! You've maintained a {current}-day streak!",
                    priority=NotificationPriority.HIGH,
                    action_url="/streaks"
                )
        else:
            # Streak broken
            gamification.streaks[streak_type] = 1
        
        return gamification.streaks[streak_type], False
    
    def _get_last_activity_date(
        self,
        learner_id: str
    ) -> Optional[datetime.date]:
        """Get the last activity date for a learner."""
        gamification = self.get_learner_gamification(learner_id)
        
        # Check daily points
        today = datetime.now().strftime("%Y-%m-%d")
        if gamification.daily_points.get(today):
            return datetime.now().date()
        
        # Check other data sources
        # This would integrate with actual activity tracking
        return None
    
    # Leaderboards
    def create_leaderboard(
        self,
        leaderboard_id: str,
        name: str,
        description: str,
        category: str,
        time_range: str = "weekly"
    ) -> Leaderboard:
        """Create a new leaderboard."""
        leaderboard = Leaderboard(
            leaderboard_id=leaderboard_id,
            name=name,
            description=description,
            category=category,
            time_range=time_range
        )
        
        self.leaderboards[leaderboard_id] = leaderboard
        return leaderboard
    
    def update_leaderboard(
        self,
        leaderboard_id: str
    ) -> Optional[Leaderboard]:
        """Update leaderboard with current scores."""
        leaderboard = self.leaderboards.get(leaderboard_id)
        if not leaderboard:
            return None
        
        # Get all gamification data
        entries = []
        for learner_id, gamification in self.learner_gamification.items():
            score = self._calculate_leaderboard_score(
                leaderboard, gamification
            )
            
            entry = LeaderboardEntry(
                learner_id=learner_id,
                learner_name=f"Learner {learner_id[:8]}",  # Placeholder
                score=score,
                rank=0,
                previous_rank=0,
                trend="stable"
            )
            entries.append(entry)
        
        # Sort by score
        entries.sort(key=lambda e: e.score, reverse=True)
        
        # Assign ranks
        for i, entry in enumerate(entries):
            entry.rank = i + 1
        
        leaderboard.entries = entries
        leaderboard.updated_at = datetime.now()
        
        return leaderboard
    
    def _calculate_leaderboard_score(
        self,
        leaderboard: Leaderboard,
        gamification: LearnerGamification
    ) -> float:
        """Calculate score for leaderboard."""
        if leaderboard.time_range == "daily":
            today = datetime.now().strftime("%Y-%m-%d")
            return gamification.daily_points.get(today, 0)
        elif leaderboard.time_range == "weekly":
            week = datetime.now().strftime("%Y-W%U")
            return gamification.weekly_points.get(week, 0)
        else:
            return gamification.total_points
    
    def get_leaderboard(
        self,
        leaderboard_id: str,
        limit: int = 10
    ) -> Optional[Leaderboard]:
        """Get a leaderboard."""
        leaderboard = self.leaderboards.get(leaderboard_id)
        if not leaderboard:
            return None
        
        # Update if needed
        if datetime.now() - leaderboard.updated_at > timedelta(hours=1):
            self.update_leaderboard(leaderboard_id)
        
        leaderboard.entries = leaderboard.entries[:limit]
        return leaderboard
    
    def get_learner_rank(
        self,
        leaderboard_id: str,
        learner_id: str
    ) -> Optional[LeaderboardEntry]:
        """Get a learner's rank on a leaderboard."""
        leaderboard = self.get_leaderboard(leaderboard_id)
        if not leaderboard:
            return None
        
        for entry in leaderboard.entries:
            if entry.learner_id == learner_id:
                return entry
        return None
    
    # Engagement Tracking
    def track_engagement(
        self,
        learner_id: str,
        session_data: Dict[str, Any]
    ):
        """Track engagement data for a learner."""
        if learner_id not in self.engagement_metrics:
            self.engagement_metrics[learner_id] = EngagementMetrics(
                learner_id=learner_id
            )
        
        metrics = self.engagement_metrics[learner_id]
        
        # Update session count
        metrics.average_session_length = (
            (metrics.average_session_length * metrics.total_sessions +
             session_data.get('duration', 0)) /
            (metrics.total_sessions + 1)
        )
        metrics.total_sessions += 1
        
        # Update daily active days
        today = datetime.now().date()
        if today not in getattr(metrics, '_active_days', set()):
            if not hasattr(metrics, '_active_days'):
                metrics._active_days = set()
            metrics._active_days.add(today)
            metrics.daily_active_days += 1
            metrics.weekly_active_days += 1
            metrics.monthly_active_days += 1
    
    def get_engagement_metrics(
        self,
        learner_id: str
    ) -> Optional[EngagementMetrics]:
        """Get engagement metrics for a learner."""
        return self.engagement_metrics.get(learner_id)
    
    def calculate_engagement_score(
        self,
        learner_id: str
    ) -> float:
        """Calculate overall engagement score (0-100)."""
        gamification = self.get_learner_gamification(learner_id)
        metrics = self.engagement_metrics.get(learner_id)
        
        if not metrics:
            return 0.0
        
        # Factors:
        # - Consistency (streak)
        # - Activity (sessions, time)
        # - Progress (completion, achievements)
        
        streak_score = min(100, gamification.streaks.get('daily', 0) * 3.33)
        activity_score = min(100, metrics.daily_active_days * 14.28)  # 7 days max
        progress_score = min(100, gamification.total_achievements * 10)
        
        engagement_score = (
            streak_score * 0.3 +
            activity_score * 0.3 +
            progress_score * 0.4
        )
        
        return engagement_score
    
    # Motivation and Reminders
    def schedule_reminder(
        self,
        learner_id: str,
        reminder_type: str,
        message: str,
        scheduled_time: datetime
    ) -> Notification:
        """Schedule a reminder notification."""
        return self.send_notification(
            learner_id,
            NotificationType.REMINDER,
            "Learning Reminder",
            message,
            priority=NotificationPriority.MEDIUM,
            action_url="/learn",
            metadata={"reminder_type": reminder_type},
            expires_at=scheduled_time + timedelta(hours=24)
        )
    
    def get_motivation_message(
        self,
        learner_id: str
    ) -> str:
        """Get a personalized motivation message."""
        gamification = self.get_learner_gamification(learner_id)
        
        # Context-based messages
        if gamification.streaks.get('daily', 0) >= 7:
            return "You're on fire! Keep that streak going!"
        elif gamification.streaks.get('daily', 0) >= 3:
            return "Great momentum! Your streak is building!"
        elif gamification.total_content_completed == 0:
            return "Ready to start your learning journey?"
        elif gamification.level < 5:
            return "Every expert was once a beginner. Let's learn!"
        else:
            return "Keep up the excellent progress!"
    
    def send_achievement_notification(
        self,
        learner_id: str,
        achievement_name: str,
        description: str,
        points_earned: int
    ):
        """Send notification for earned achievement."""
        self.send_notification(
            learner_id,
            NotificationType.ACHIEVEMENT,
            f"Achievement Unlocked: {achievement_name}!",
            f"{description}\n+{points_earned} XP",
            priority=NotificationPriority.HIGH,
            action_url="/achievements",
            metadata={
                "achievement_name": achievement_name,
                "points": points_earned
            }
        )
    
    # Reports
    def get_engagement_report(
        self,
        learner_id: str,
        period: str = "weekly"
    ) -> Dict[str, Any]:
        """Generate engagement report for a learner."""
        gamification = self.get_learner_gamification(learner_id)
        metrics = self.get_engagement_metrics(learner_id)
        notifications = self.get_learner_notifications(learner_id, limit=100)
        
        # Calculate period stats
        if period == "weekly":
            days = 7
        elif period == "monthly":
            days = 30
        else:
            days = 1
        
        # Get daily points for period
        period_points = 0
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            period_points += gamification.daily_points.get(date, 0)
        
        return {
            "learner_id": learner_id,
            "period": period,
            "gamification": {
                "level": gamification.level,
                "total_points": gamification.total_points,
                "xp_to_next_level": gamification.xp_to_next_level,
                "badges": gamification.badges,
                "streaks": gamification.streaks,
                "points_earned_this_period": period_points
            },
            "engagement": {
                "engagement_score": self.calculate_engagement_score(learner_id),
                "total_sessions": gamification.total_sessions,
                "average_session_length": metrics.average_session_length if metrics else 0,
                "daily_active_days": metrics.daily_active_days if metrics else 0
            },
            "notifications": {
                "total": len(notifications),
                "unread": sum(1 for n in notifications if not n.read)
            }
        }


# Service factory function
def create_engagement_service() -> EngagementService:
    """Create and configure a new engagement service instance."""
    return EngagementService()
