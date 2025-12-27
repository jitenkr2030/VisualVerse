# Learner Experience Platform - Progress Tracking Service

This module provides comprehensive progress tracking capabilities for the
VisualVerse Learner Experience Platform, including session management,
concept mastery evaluation, achievements, and progress reporting.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
from uuid import uuid4
import json
import logging
import threading

from .analytics_service import LearningAnalyticsService, EventType


logger = logging.getLogger(__name__)


class ProgressStatus(str, Enum):
    """Status of learning progress."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"
    NEEDS_REVIEW = "needs_review"


class AchievementType(str, Enum):
    """Types of achievements that can be earned."""
    FIRST_STEPS = "first_steps"          # Complete first lesson
    QUICK_LEARNER = "quick_learner"       # Complete 5 lessons in one day
    STREAK_MASTER = "streak_master"       # 7-day streak
    PERFECTIONIST = "perfectionist"       # Score 100% on assessment
    CONCEPT_CHAMPION = "concept_champion" # Master a concept
    EXPLORER = "explorer"                 # Try content from all domains
    CONSISTENT = "consistent"             # Study 30 days in a row
    SPEED_DEMON = "speed_demon"           # Complete lesson under time target
    HELPFUL = "helpful"                   # Use hints appropriately
    MASTEREducator = "master_educator"    # Complete all content in a domain


@dataclass
class LearnerProgress:
    """
    Comprehensive learner progress data.
    
    Attributes:
        user_id: Associated user identifier
        total_time_spent: Total learning time in seconds
        sessions_completed: Number of completed sessions
        current_streak: Current learning streak in days
        longest_streak: Longest learning streak achieved
        concepts_started: Number of concepts started
        concepts_completed: Number of concepts completed
        concepts_mastered: Number of concepts mastered
        average_score: Average assessment score
        last_activity: Last learning activity timestamp
        domains_explored: List of domains explored
        achievements_earned: Number of achievements earned
        level: Current user level
        xp_points: Experience points
    """
    user_id: str
    total_time_spent: int = 0
    sessions_completed: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    concepts_started: int = 0
    concepts_completed: int = 0
    concepts_mastered: int = 0
    average_score: float = 0.0
    last_activity: Optional[datetime] = None
    domains_explored: List[str] = field(default_factory=list)
    achievements_earned: int = 0
    level: int = 1
    xp_points: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "userId": self.user_id,
            "totalTimeSpent": self.total_time_spent,
            "sessionsCompleted": self.sessions_completed,
            "currentStreak": self.current_streak,
            "longestStreak": self.longest_streak,
            "conceptsStarted": self.concepts_started,
            "conceptsCompleted": self.concepts_completed,
            "conceptsMastered": self.concepts_mastered,
            "averageScore": self.average_score,
            "lastActivity": self.last_activity.isoformat() if self.last_activity else None,
            "domainsExplored": self.domains_explored,
            "achievementsEarned": self.achievements_earned,
            "level": self.level,
            "xpPoints": self.xp_points,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    def add_xp(self, points: int) -> Tuple[int, int]:
        """
        Add XP points and return (new_total, new_level).
        
        Args:
            points: Points to add
            
        Returns:
            Tuple of (new XP total, new level)
        """
        self.xp_points += points
        new_level = 1 + (self.xp_points // 1000)
        if new_level > self.level:
            old_level = self.level
            self.level = new_level
            return self.xp_points, new_level - old_level
        return self.xp_points, 0


@dataclass
class SessionData:
    """
    Learning session data.
    
    Attributes:
        id: Unique session identifier
        user_id: Associated user
        content_id: Content accessed
        start_time: Session start timestamp
        end_time: Session end timestamp
        time_spent: Duration in seconds
        interactions: Number of interactions
        completed: Whether session completed
        score: Assessment score (0-1)
        mastery_level: Mastery level achieved (0-1)
        notes: User notes
        metadata: Additional session data
    """
    id: str
    user_id: str
    content_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    time_spent: int = 0
    interactions: int = 0
    completed: bool = False
    score: float = 0.0
    mastery_level: float = 0.0
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "contentId": self.content_id,
            "startTime": self.start_time.isoformat(),
            "endTime": self.end_time.isoformat() if self.end_time else None,
            "timeSpent": self.time_spent,
            "interactions": self.interactions,
            "completed": self.completed,
            "score": self.score,
            "masteryLevel": self.mastery_level,
            "notes": self.notes,
            "metadata": self.metadata
        }


@dataclass
class ConceptProgress:
    """
    Progress on a specific concept.
    
    Attributes:
        user_id: User identifier
        concept_id: Concept identifier
        status: Current status
        attempts: Number of attempts
        last_attempt: Last attempt timestamp
        time_spent: Total time spent
        average_score: Average score across attempts
        mastery_level: Current mastery level (0-1)
        hints_used: Total hints used
        strengths: Identified strengths
        weaknesses: Identified weaknesses
        next_review: Recommended next review date
    """
    user_id: str
    concept_id: str
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    attempts: int = 0
    last_attempt: Optional[datetime] = None
    time_spent: int = 0
    average_score: float = 0.0
    mastery_level: float = 0.0
    hints_used: int = 0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    next_review: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "userId": self.user_id,
            "conceptId": self.concept_id,
            "status": self.status.value,
            "attempts": self.attempts,
            "lastAttempt": self.last_attempt.isoformat() if self.last_attempt else None,
            "timeSpent": self.time_spent,
            "averageScore": self.average_score,
            "masteryLevel": self.mastery_level,
            "hintsUsed": self.hints_used,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "nextReview": self.next_review.isoformat() if self.next_review else None
        }


@dataclass
class ProgressMilestone:
    """
    Learning milestone.
    
    Attributes:
        id: Unique milestone identifier
        user_id: Associated user
        title: Milestone title
        description: Milestone description
        category: Milestone category
        target_value: Target value to achieve
        current_value: Current progress value
        completed: Whether completed
        completed_at: Completion timestamp
        xp_reward: XP reward for completion
    """
    id: str
    user_id: str
    title: str
    description: str
    category: str
    target_value: int
    current_value: int = 0
    completed: bool = False
    completed_at: Optional[datetime] = None
    xp_reward: int = 100
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "targetValue": self.target_value,
            "currentValue": self.current_value,
            "completed": self.completed,
            "completedAt": self.completed_at.isoformat() if self.completed_at else None,
            "xpReward": self.xp_reward
        }
    
    @property
    def progress_percentage(self) -> float:
        """Get progress percentage."""
        if self.target_value == 0:
            return 100.0
        return min(100.0, (self.current_value / self.target_value) * 100)


@dataclass
class Achievement:
    """
    Learner achievement.
    
    Attributes:
        id: Unique achievement identifier
        user_id: Associated user
        achievement_type: Type of achievement
        title: Achievement title
        description: Achievement description
        icon_url: Achievement icon URL
        earned_at: When it was earned
        xp_value: XP value of achievement
    """
    id: str
    user_id: str
    achievement_type: str
    title: str
    description: str
    icon_url: Optional[str] = None
    earned_at: datetime = field(default_factory=datetime.utcnow)
    xp_value: int = 50
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "userId": self.user_id,
            "achievementType": self.achievement_type,
            "title": self.title,
            "description": self.description,
            "iconUrl": self.icon_url,
            "earnedAt": self.earned_at.isoformat(),
            "xpValue": self.xp_value
        }


@dataclass
class ProgressReport:
    """
    Comprehensive progress report.
    
    Attributes:
        user_id: User identifier
        period: Report period
        start_date: Report start date
        end_date: Report end date
        total_time: Total learning time
        sessions_completed: Number of sessions
        concepts_completed: Concepts completed
        concepts_mastered: Concepts mastered
        average_score: Average assessment score
        completion_rate: Session completion rate
        strongest_areas: Strongest topic areas
        growth_areas: Areas needing improvement
        streak_data: Streak information
        achievements_earned: Achievements earned this period
        recommendations: Learning recommendations
    """
    user_id: str
    period: str
    start_date: datetime
    end_date: datetime
    total_time: int
    sessions_completed: int
    concepts_completed: int
    concepts_mastered: int
    average_score: float
    completion_rate: float
    strongest_areas: List[str] = field(default_factory=list)
    growth_areas: List[str] = field(default_factory=list)
    streak_data: Dict[str, Any] = field(default_factory=dict)
    achievements_earned: List[Achievement] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "userId": self.user_id,
            "period": self.period,
            "startDate": self.start_date.isoformat(),
            "endDate": self.end_date.isoformat(),
            "totalTime": self.total_time,
            "sessionsCompleted": self.sessions_completed,
            "conceptsCompleted": self.concepts_completed,
            "conceptsMastered": self.concepts_mastered,
            "averageScore": self.average_score,
            "completionRate": self.completion_rate,
            "strongestAreas": self.strongest_areas,
            "growthAreas": self.growth_areas,
            "streakData": self.streak_data,
            "achievementsEarned": [a.to_dict() for a in self.achievements_earned],
            "recommendations": self.recommendations
        }


class ProgressTrackingService:
    """
    Service for tracking learner progress across the VisualVerse platform.
    
    This service manages:
    - Learner progress summaries
    - Learning sessions
    - Concept-level progress
    - Achievements and milestones
    - Progress reports and analytics
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the progress tracking service.
        
        Args:
            storage_dir: Directory for persisting data
        """
        self.storage_dir = storage_dir or "/tmp/visualverse-lxp/progress"
        
        # In-memory storage (would be database in production)
        self.learner_progress: Dict[str, LearnerProgress] = {}
        self.sessions: Dict[str, SessionData] = {}
        self.concept_progress: Dict[str, Dict[str, ConceptProgress]] = {}  # user_id -> concept_id -> progress
        self.milestones: Dict[str, List[ProgressMilestone]] = {}
        self.achievements: Dict[str, List[Achievement]] = {}
        self.active_sessions: Dict[str, SessionData] = {}
        
        # Analytics integration
        self.analytics_service = None
        
        self.lock = threading.RLock()
        
        # Load existing data
        self._load_state()
        
        logger.info("ProgressTrackingService initialized")
    
    def _load_state(self):
        """Load persisted state from storage."""
        import os
        os.makedirs(self.storage_dir, exist_ok=True)
        
        progress_file = f"{self.storage_dir}/learner_progress.json"
        sessions_file = f"{self.storage_dir}/sessions.json"
        concepts_file = f"{self.storage_dir}/concept_progress.json"
        milestones_file = f"{self.storage_dir}/milestones.json"
        achievements_file = f"{self.storage_dir}/achievements.json"
        
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r') as f:
                    data = json.load(f)
                    self.learner_progress = {
                        uid: LearnerProgress(**p) for uid, p in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load progress: {e}")
        
        if os.path.exists(sessions_file):
            try:
                with open(sessions_file, 'r') as f:
                    data = json.load(f)
                    self.sessions = {
                        sid: SessionData(**s) for sid, s in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load sessions: {e}")
        
        if os.path.exists(concepts_file):
            try:
                with open(concepts_file, 'r') as f:
                    data = json.load(f)
                    self.concept_progress = {}
                    for uid, concepts in data.items():
                        self.concept_progress[uid] = {
                            cid: ConceptProgress(**cp) 
                            for cid, cp in concepts.items()
                        }
            except Exception as e:
                logger.warning(f"Failed to load concept progress: {e}")
        
        if os.path.exists(milestones_file):
            try:
                with open(milestones_file, 'r') as f:
                    data = json.load(f)
                    self.milestones = {
                        uid: [ProgressMilestone(**m) for m in ms] 
                        for uid, ms in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load milestones: {e}")
        
        if os.path.exists(achievements_file):
            try:
                with open(achievements_file, 'r') as f:
                    data = json.load(f)
                    self.achievements = {
                        uid: [Achievement(**a) for a in achs] 
                        for uid, achs in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load achievements: {e}")
    
    def _save_state(self):
        """Persist state to storage."""
        import os
        from pathlib import Path
        
        Path(self.storage_dir).mkdir(parents=True, exist_ok=True)
        
        progress_file = f"{self.storage_dir}/learner_progress.json"
        sessions_file = f"{self.storage_dir}/sessions.json"
        concepts_file = f"{self.storage_dir}/concept_progress.json"
        milestones_file = f"{self.storage_dir}/milestones.json"
        achievements_file = f"{self.storage_dir}/achievements.json"
        
        with open(progress_file, 'w') as f:
            json.dump(
                {uid: p.to_dict() for uid, p in self.learner_progress.items()},
                f, indent=2
            )
        
        with open(sessions_file, 'w') as f:
            json.dump(
                {sid: s.to_dict() for sid, s in self.sessions.items()},
                f, indent=2
            )
        
        with open(concepts_file, 'w') as f:
            json.dump(
                {
                    uid: {cid: cp.to_dict() for cid, cp in concepts.items()}
                    for uid, concepts in self.concept_progress.items()
                },
                f, indent=2
            )
        
        with open(milestones_file, 'w') as f:
            json.dump(
                {uid: [m.to_dict() for m in ms] 
                 for uid, ms in self.milestones.items()},
                f, indent=2
            )
        
        with open(achievements_file, 'w') as f:
            json.dump(
                {uid: [a.to_dict() for a in achs] 
                 for uid, achs in self.achievements.items()},
                f, indent=2
            )
    
    def set_analytics_service(self, service):
        """Set the analytics service for event tracking."""
        self.analytics_service = service
    
    # Learner Progress Management
    def get_or_create_progress(self, user_id: str) -> LearnerProgress:
        """
        Get or create learner progress.
        
        Args:
            user_id: User identifier
            
        Returns:
            LearnerProgress object
        """
        with self.lock:
            if user_id not in self.learner_progress:
                self.learner_progress[user_id] = LearnerProgress(user_id=user_id)
                self._save_state()
            
            return self.learner_progress[user_id]
    
    def get_progress(self, user_id: str) -> Optional[LearnerProgress]:
        """
        Get learner progress.
        
        Args:
            user_id: User identifier
            
        Returns:
            LearnerProgress or None if not found
        """
        return self.learner_progress.get(user_id)
    
    # Session Management
    def start_session(self, user_id: str, content_id: str) -> SessionData:
        """
        Start a new learning session.
        
        Args:
            user_id: User identifier
            content_id: Content being accessed
            
        Returns:
            Created SessionData
        """
        with self.lock:
            # End any active session for this user
            if user_id in self.active_sessions:
                self._end_session(self.active_sessions[user_id])
            
            session = SessionData(
                id=f"session-{uuid4().hex[:12]}",
                user_id=user_id,
                content_id=content_id,
                start_time=datetime.utcnow()
            )
            
            self.active_sessions[user_id] = session
            self.sessions[session.id] = session
            
            # Ensure learner progress exists
            self.get_or_create_progress(user_id)
            
            logger.info(f"Session started: {session.id} for user {user_id}")
            return session
    
    def record_interaction(self, user_id: str, interaction_type: str, 
                          metadata: Dict[str, Any] = None):
        """
        Record an interaction within a session.
        
        Args:
            user_id: User identifier
            interaction_type: Type of interaction
            metadata: Interaction metadata
        """
        with self.lock:
            if user_id not in self.active_sessions:
                return
            
            session = self.active_sessions[user_id]
            session.interactions += 1
            if metadata:
                session.metadata[interaction_type] = session.metadata.get(interaction_type, 0) + 1
            
            # Track analytics event
            if self.analytics_service:
                self.analytics_service.track_event(
                    user_id=user_id,
                    event_type=EventType.INTERACTION.value,
                    content_id=session.content_id,
                    metadata={
                        "interaction_type": interaction_type,
                        "session_id": session.id,
                        **(metadata or {})
                    }
                )
    
    def _end_session(self, session: SessionData) -> SessionData:
        """
        End a session and update progress.
        
        Args:
            session: Session to end
            
        Returns:
            Updated SessionData
        """
        with self.lock:
            session.end_time = datetime.utcnow()
            session.time_spent = int((session.end_time - session.start_time).total_seconds())
            
            # Update learner progress
            if session.user_id in self.learner_progress:
                progress = self.learner_progress[session.user_id]
                progress.total_time_spent += session.time_spent
                progress.sessions_completed += 1
                progress.last_activity = session.end_time
                
                # Update streak
                self._update_streak(progress)
                
                # Add XP for time spent
                xp_earned = min(100, session.time_spent // 60)  # 1 XP per minute, max 100
                new_xp, levels_gained = progress.add_xp(xp_earned)
                
                if levels_gained > 0:
                    self._award_achievement(
                        session.user_id,
                        AchievementType.FIRST_STEPS,
                        f"Reached Level {progress.level}!",
                        "You've advanced to a new level!"
                    )
            
            # Remove from active sessions
            if session.user_id in self.active_sessions:
                del self.active_sessions[session.user_id]
            
            self._save_state()
            
            # Track session completion
            if self.analytics_service:
                self.analytics_service.track_event(
                    user_id=session.user_id,
                    event_type=EventType.SESSION_COMPLETE.value,
                    content_id=session.content_id,
                    metadata={
                        "session_id": session.id,
                        "time_spent": session.time_spent,
                        "interactions": session.interactions,
                        "completed": session.completed,
                        "score": session.score
                    }
                )
            
            return session
    
    def _update_streak(self, progress: LearnerProgress):
        """Update learning streak."""
        if progress.last_activity:
            last_activity_date = progress.last_activity.date()
            today = datetime.utcnow().date()
            
            if last_activity_date == today:
                return  # Same day, no change
            
            if last_activity_date == today - timedelta(days=1):
                # Consecutive day
                progress.current_streak += 1
                if progress.current_streak > progress.longest_streak:
                    progress.longest_streak = progress.current_streak
                
                # Check for streak achievements
                if progress.current_streak == 7:
                    self._award_achievement(
                        progress.user_id,
                        AchievementType.STREAK_MASTER,
                        "Week Warrior",
                        "Maintained a 7-day learning streak!"
                    )
                elif progress.current_streak == 30:
                    self._award_achievement(
                        progress.user_id,
                        AchievementType.CONSISTENT,
                        "Monthly Master",
                        "Studied for 30 consecutive days!"
                    )
            else:
                # Streak broken
                progress.current_streak = 0
    
    def complete_session(self, user_id: str, score: float, 
                        mastery_level: float = None) -> SessionData:
        """
        Complete a learning session with results.
        
        Args:
            user_id: User identifier
            score: Assessment score (0-1)
            mastery_level: Optional mastery level achieved
            
        Returns:
            Completed SessionData
        """
        with self.lock:
            if user_id not in self.active_sessions:
                raise ValueError(f"No active session for user {user_id}")
            
            session = self.active_sessions[user_id]
            session.completed = True
            session.score = score
            if mastery_level is not None:
                session.mastery_level = mastery_level
            
            # Check for perfect score achievement
            if score >= 1.0:
                self._award_achievement(
                    user_id,
                    AchievementType.PERFECTIONIST,
                    "Perfect Score",
                    "Achieved 100% on an assessment!"
                )
            
            # Update concept progress
            self._update_concept_progress(session)
            
            return self._end_session(session)
    
    def record_session(self, user_id: str, content_id: str, 
                      time_spent: int, interactions: int,
                      completed: bool, score: float = 0.0,
                      metadata: Dict[str, Any] = None) -> SessionData:
        """
        Record a completed session (convenience method).
        
        Args:
            user_id: User identifier
            content_id: Content identifier
            time_spent: Time spent in seconds
            interactions: Number of interactions
            completed: Whether session was completed
            score: Assessment score
            metadata: Additional session data
            
        Returns:
            Created SessionData
        """
        with self.lock:
            session = SessionData(
                id=f"session-{uuid4().hex[:12]}",
                user_id=user_id,
                content_id=content_id,
                start_time=datetime.utcnow() - timedelta(seconds=time_spent),
                end_time=datetime.utcnow(),
                time_spent=time_spent,
                interactions=interactions,
                completed=completed,
                score=score,
                metadata=metadata or {}
            )
            
            self.sessions[session.id] = session
            
            # Ensure learner progress exists
            progress = self.get_or_create_progress(user_id)
            progress.total_time_spent += time_spent
            progress.sessions_completed += 1
            progress.last_activity = datetime.utcnow()
            self._update_streak(progress)
            
            # Update concept progress
            self._update_concept_progress(session)
            
            # Check achievements
            if completed and score >= 0.8:
                self._award_achievement(
                    user_id,
                    AchievementType.QUICK_LEARNER,
                    "Quick Learner",
                    "Completed 5 lessons in one day!"
                )
            
            self._save_state()
            return session
    
    def get_active_session(self, user_id: str) -> Optional[SessionData]:
        """Get the active session for a user."""
        return self.active_sessions.get(user_id)
    
    def get_user_sessions(self, user_id: str, limit: int = 50) -> List[SessionData]:
        """Get recent sessions for a user."""
        user_sessions = [
            s for s in self.sessions.values() 
            if s.user_id == user_id
        ]
        user_sessions.sort(key=lambda s: s.start_time, reverse=True)
        return user_sessions[:limit]
    
    # Concept Progress Management
    def _update_concept_progress(self, session: SessionData):
        """Update concept progress based on session."""
        with self.lock:
            if session.user_id not in self.concept_progress:
                self.concept_progress[session.user_id] = {}
            
            concept_progress = self.concept_progress[session.user_id]
            
            if session.content_id not in concept_progress:
                concept_progress[session.content_id] = ConceptProgress(
                    user_id=session.user_id,
                    concept_id=session.content_id
                )
            
            cp = concept_progress[session.content_id]
            cp.attempts += 1
            cp.last_attempt = datetime.utcnow()
            cp.time_spent += session.time_spent
            
            # Update average score
            total_score = cp.average_score * (cp.attempts - 1) + session.score
            cp.average_score = total_score / cp.attempts
            
            # Update mastery level
            if session.completed:
                if cp.mastery_level < session.mastery_level or cp.mastery_level == 0:
                    cp.mastery_level = max(cp.mastery_level, session.mastery_level)
                
                if cp.mastery_level >= 0.8:
                    cp.status = ProgressStatus.MASTERED
                    self._award_achievement(
                        session.user_id,
                        AchievementType.CONCEPT_CHAMPION,
                        f"Mastered: {session.content_id}",
                        f"Became a master of {session.content_id}!"
                    )
                elif cp.mastery_level >= 0.5:
                    cp.status = ProgressStatus.COMPLETED
                else:
                    cp.status = ProgressStatus.IN_PROGRESS
            
            # Schedule next review (spaced repetition)
            if cp.status in [ProgressStatus.COMPLETED, ProgressStatus.MASTERED]:
                days_until_review = [1, 3, 7, 14, 30][min(cp.attempts - 1, 4)]
                cp.next_review = datetime.utcnow() + timedelta(days=days_until_review)
    
    def get_concept_progress(self, user_id: str, concept_id: str) -> Optional[ConceptProgress]:
        """
        Get progress for a specific concept.
        
        Args:
            user_id: User identifier
            concept_id: Concept identifier
            
        Returns:
            ConceptProgress or None if not found
        """
        if user_id in self.concept_progress:
            return self.concept_progress[user_id].get(concept_id)
        return None
    
    def get_all_concept_progress(self, user_id: str) -> List[ConceptProgress]:
        """Get all concept progress for a user."""
        if user_id not in self.concept_progress:
            return []
        return list(self.concept_progress[user_id].values())
    
    def get_concepts_for_review(self, user_id: str) -> List[ConceptProgress]:
        """Get concepts due for review."""
        now = datetime.utcnow()
        if user_id not in self.concept_progress:
            return []
        
        return [
            cp for cp in self.concept_progress[user_id].values()
            if cp.next_review and cp.next_review <= now
        ]
    
    # Achievement Management
    def _award_achievement(self, user_id: str, achievement_type: AchievementType,
                          title: str, description: str, xp_value: int = 50):
        """Award an achievement to a user."""
        with self.lock:
            achievement = Achievement(
                id=f"ach-{uuid4().hex[:12]}",
                user_id=user_id,
                achievement_type=achievement_type.value,
                title=title,
                description=description,
                xp_value=xp_value
            )
            
            if user_id not in self.achievements:
                self.achievements[user_id] = []
            
            # Check if already earned
            for existing in self.achievements[user_id]:
                if existing.achievement_type == achievement_type.value:
                    return  # Already earned
            
            self.achievements[user_id].append(achievement)
            
            # Update learner progress
            if user_id in self.learner_progress:
                progress = self.learner_progress[user_id]
                progress.achievements_earned += 1
                progress.add_xp(xp_value)
            
            self._save_state()
            
            logger.info(f"Achievement awarded: {title} to user {user_id}")
            return achievement
    
    def get_user_achievements(self, user_id: str) -> List[Achievement]:
        """Get all achievements for a user."""
        return self.achievements.get(user_id, [])
    
    def get_achievement_progress(self, user_id: str) -> Dict[str, Any]:
        """Get achievement progress summary."""
        achievements = self.get_user_achievements(user_id)
        
        earned_types = {a.achievement_type for a in achievements}
        
        # All possible achievements
        all_achievements = {
            AchievementType.FIRST_STEPS.value: {"title": "First Steps", "xp": 50},
            AchievementType.QUICK_LEARNER.value: {"title": "Quick Learner", "xp": 100},
            AchievementType.STREAK_MASTER.value: {"title": "Streak Master", "xp": 200},
            AchievementType.PERFECTIONIST.value: {"title": "Perfectionist", "xp": 150},
            AchievementType.CONCEPT_CHAMPION.value: {"title": "Concept Champion", "xp": 100},
            AchievementType.EXPLORER.value: {"title": "Explorer", "xp": 100},
            AchievementType.CONSISTENT.value: {"title": "Consistent", "xp": 300},
            AchievementType.SPEED_DEMON.value: {"title": "Speed Demon", "xp": 75},
            AchievementType.HELPFUL.value: {"title": "Helpful", "xp": 50},
        }
        
        earned = []
        available = []
        
        for ach_type, info in all_achievements.items():
            if ach_type in earned_types:
                earned.append({
                    "type": ach_type,
                    **info,
                    "earned": True
                })
            else:
                available.append({
                    "type": ach_type,
                    **info,
                    "earned": False
                })
        
        total_earned_xp = sum(a.xp_value for a in achievements)
        
        return {
            "earned": earned,
            "available": available,
            "totalEarned": len(achievements),
            "totalAvailable": len(all_achievements),
            "totalXp": total_earned_xp
        }
    
    # Milestone Management
    def create_milestone(self, user_id: str, title: str, description: str,
                        category: str, target_value: int, 
                        xp_reward: int = 100) -> ProgressMilestone:
        """
        Create a new milestone for a user.
        
        Args:
            user_id: User identifier
            title: Milestone title
            description: Milestone description
            category: Milestone category
            target_value: Target value to achieve
            xp_reward: XP reward for completion
            
        Returns:
            Created ProgressMilestone
        """
        with self.lock:
            milestone = ProgressMilestone(
                id=f"milestone-{uuid4().hex[:12]}",
                user_id=user_id,
                title=title,
                description=description,
                category=category,
                target_value=target_value,
                xp_reward=xp_reward
            )
            
            if user_id not in self.milestones:
                self.milestones[user_id] = []
            
            self.milestones[user_id].append(milestone)
            self._save_state()
            
            return milestone
    
    def update_milestone(self, user_id: str, milestone_id: str, 
                        increment: int) -> Optional[ProgressMilestone]:
        """
        Update milestone progress.
        
        Args:
            user_id: User identifier
            milestone_id: Milestone identifier
            increment: Amount to add to current value
            
        Returns:
            Updated ProgressMilestone or None
        """
        with self.lock:
            if user_id not in self.milestones:
                return None
            
            for milestone in self.milestones[user_id]:
                if milestone.id == milestone_id:
                    milestone.current_value += increment
                    
                    if milestone.current_value >= milestone.target_value and not milestone.completed:
                        milestone.completed = True
                        milestone.completed_at = datetime.utcnow()
                        
                        # Award XP
                        if user_id in self.learner_progress:
                            self.learner_progress[user_id].add_xp(milestone.xp_reward)
                    
                    self._save_state()
                    return milestone
            
            return None
    
    def get_user_milestones(self, user_id: str) -> List[ProgressMilestone]:
        """Get all milestones for a user."""
        return self.milestones.get(user_id, [])
    
    # Progress Reports
    def get_progress_report(self, user_id: str, period: str = "weekly",
                           start_date: datetime = None,
                           end_date: datetime = None) -> ProgressReport:
        """
        Generate a progress report for a user.
        
        Args:
            user_id: User identifier
            period: Report period (daily, weekly, monthly)
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            ProgressReport
        """
        with self.lock:
            # Calculate date range
            end_date = end_date or datetime.utcnow()
            
            if period == "daily":
                start_date = end_date - timedelta(days=1)
            elif period == "weekly":
                start_date = end_date - timedelta(weeks=1)
            elif period == "monthly":
                start_date = end_date - timedelta(days=30)
            else:
                start_date = start_date or end_date - timedelta(weeks=1)
            
            # Get sessions in range
            user_sessions = [
                s for s in self.sessions.values()
                if s.user_id == user_id and 
                s.start_time >= start_date and 
                s.start_time <= end_date
            ]
            
            # Calculate metrics
            total_time = sum(s.time_spent for s in user_sessions)
            completed_sessions = [s for s in user_sessions if s.completed]
            sessions_completed = len(completed_sessions)
            
            concepts_completed = set()
            concepts_mastered = set()
            
            for s in user_sessions:
                if s.user_id in self.concept_progress:
                    if s.content_id in self.concept_progress[s.user_id]:
                        cp = self.concept_progress[s.user_id][s.content_id]
                        if cp.status == ProgressStatus.COMPLETED:
                            concepts_completed.add(s.content_id)
                        if cp.status == ProgressStatus.MASTERED:
                            concepts_mastered.add(s.content_id)
            
            average_score = 0.0
            if completed_sessions:
                average_score = sum(s.score for s in completed_sessions) / len(completed_sessions)
            
            completion_rate = 0.0
            if user_sessions:
                completion_rate = (sessions_completed / len(user_sessions)) * 100
            
            # Get achievements in range
            achievements = [
                a for a in self.get_user_achievements(user_id)
                if a.earned_at >= start_date and a.earned_at <= end_date
            ]
            
            # Get streak data
            progress = self.get_progress(user_id)
            streak_data = {
                "currentStreak": progress.current_streak if progress else 0,
                "longestStreak": progress.longest_streak if progress else 0
            }
            
            # Generate recommendations
            recommendations = self._generate_recommendations(user_id, user_sessions)
            
            return ProgressReport(
                user_id=user_id,
                period=period,
                start_date=start_date,
                end_date=end_date,
                total_time=total_time,
                sessions_completed=sessions_completed,
                concepts_completed=len(concepts_completed),
                concepts_mastered=len(concepts_mastered),
                average_score=average_score,
                completion_rate=completion_rate,
                achievements_earned=achievements,
                streak_data=streak_data,
                recommendations=recommendations
            )
    
    def _generate_recommendations(self, user_id: str, 
                                  sessions: List[SessionData]) -> List[str]:
        """Generate progress-based recommendations."""
        recommendations = []
        
        if not sessions:
            recommendations.append("Start by exploring a topic that interests you!")
            return recommendations
        
        # Analyze session patterns
        avg_time = sum(s.time_spent for s in sessions) / len(sessions)
        
        if avg_time < 600:  # Less than 10 minutes
            recommendations.append("Try to spend at least 15-20 minutes per session for better retention")
        
        completion_rate = len([s for s in sessions if s.completed]) / len(sessions)
        if completion_rate < 0.5:
            recommendations.append("Focus on completing fewer topics with better understanding")
        
        # Check for domains not explored
        domains_explored = set(s.content_id.split('-')[0] for s in sessions)
        if len(domains_explored) < 2:
            recommendations.append("Explore different domains to find your strengths")
        
        # Check recent struggle
        recent_scores = [s.score for s in sorted(sessions, key=lambda s: s.start_time)[-5:]]
        if recent_scores and sum(recent_scores) / len(recent_scores) < 0.6:
            recommendations.append("Consider reviewing the basics before moving on")
        
        if not recommendations:
            recommendations.append("Great progress! Keep up the excellent work!")
        
        return recommendations


# Thread lock for thread-safe operations
ProgressTrackingService.lock = __import__('threading').RLock()


def create_progress_service(storage_dir: str = None) -> ProgressTrackingService:
    """
    Create and return the global progress tracking service.
    
    Args:
        storage_dir: Optional storage directory
        
    Returns:
        ProgressTrackingService instance
    """
    return ProgressTrackingService(storage_dir)


__all__ = [
    "ProgressStatus",
    "AchievementType",
    "LearnerProgress",
    "SessionData",
    "ConceptProgress",
    "ProgressMilestone",
    "Achievement",
    "ProgressReport",
    "ProgressTrackingService",
    "create_progress_service"
]
