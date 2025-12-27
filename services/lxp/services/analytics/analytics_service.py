"""
Analytics Service for Learner Experience Platform.

Provides comprehensive learning analytics including progress tracking,
engagement metrics, performance analysis, skill assessments, and reporting
for learners, educators, and administrators.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import json


class MetricType(Enum):
    """Types of analytics metrics."""
    ENGAGEMENT = "engagement"
    PERFORMANCE = "performance"
    PROGRESS = "progress"
    TIME_SPENT = "time_spent"
    COMPLETION = "completion"
    ASSESSMENT = "assessment"
    SKILL = "skill"
    BEHAVIOR = "behavior"


class TimeGranularity(Enum):
    """Time granularity for analytics queries."""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


@dataclass
class LearnerMetrics:
    """Comprehensive metrics for a learner."""
    learner_id: str
    total_time_spent: int  # seconds
    total_content_completed: int
    total_assessments_taken: int
    average_score: float
    average_engagement: float
    current_streak: int  # days
    longest_streak: int
    last_active: Optional[datetime]
    total_sessions: int
    average_session_duration: float
    completion_rate: float
    skill_levels: Dict[str, float]
    recent_activity: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data['last_active'] = self.last_active.isoformat() if self.last_active else None
        return data


@dataclass
class ContentAnalytics:
    """Analytics for a piece of content."""
    content_id: str
    total_views: int
    unique_viewers: int
    total_completions: int
    completion_rate: float
    average_time_spent: float
    average_score: float
    average_rating: float
    drop_off_points: Dict[int, float]  # timestamp -> drop-off rate
    engagement_trend: List[Tuple[datetime, float]]
    difficulty_rating: float
    popularity_rank: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with JSON-serializable types."""
        return {
            'content_id': self.content_id,
            'total_views': self.total_views,
            'unique_viewers': self.unique_viewers,
            'total_completions': self.total_completions,
            'completion_rate': self.completion_rate,
            'average_time_spent': self.average_time_spent,
            'average_score': self.average_score,
            'average_rating': self.average_rating,
            'drop_off_points': self.drop_off_points,
            'engagement_trend': [
                (dt.isoformat(), score) for dt, score in self.engagement_trend
            ],
            'difficulty_rating': self.difficulty_rating,
            'popularity_rank': self.popularity_rank
        }


@dataclass
class CourseAnalytics:
    """Analytics for a course or learning path."""
    course_id: str
    enrolled_learners: int
    active_learners: int
    completion_rate: float
    average_progress: float
    average_time_to_complete: float
    total_content_items: int
    content_completion_breakdown: Dict[str, int]
    assessment_performance: Dict[str, float]
    engagement_metrics: Dict[str, float]
    skill_distribution: Dict[str, List[float]]
    dropoff_analysis: Dict[str, float]
    trend_data: List[Tuple[datetime, Dict[str, float]]]


@dataclass
class ProgressSnapshot:
    """A snapshot of learner progress at a point in time."""
    timestamp: datetime
    content_id: str
    progress_percentage: float
    time_spent_seconds: int
    status: str
    score: Optional[float]


@dataclass
class LearningSession:
    """Represents a learning session."""
    session_id: str
    learner_id: str
    start_time: datetime
    end_time: Optional[datetime]
    content_ids: List[str]
    total_duration: int
    events: List[Dict[str, Any]]
    
    @property
    def is_active(self) -> bool:
        """Check if session is still active."""
        return self.end_time is None


@dataclass
class SkillAssessment:
    """A skill assessment result."""
    assessment_id: str
    learner_id: str
    skill_name: str
    assessment_type: str
    score: float
    max_score: float
    confidence_level: float
    questions_answered: int
    correct_answers: int
    time_taken: int
    timestamp: datetime
    feedback: List[str]
    
    @property
    def percentage_score(self) -> float:
        """Get percentage score."""
        return (self.score / self.max_score * 100) if self.max_score > 0 else 0.0


@dataclass
class AnalyticsReport:
    """A generated analytics report."""
    report_id: str
    report_type: str
    generated_at: datetime
    time_range_start: datetime
    time_range_end: datetime
    data: Dict[str, Any]
    summary: str
    insights: List[str]
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'report_id': self.report_id,
            'report_type': self.report_type,
            'generated_at': self.generated_at.isoformat(),
            'time_range_start': self.time_range_start.isoformat(),
            'time_range_end': self.time_range_end.isoformat(),
            'data': self.data,
            'summary': self.summary,
            'insights': self.insights,
            'recommendations': self.recommendations
        }


class EngagementAnalyzer:
    """Analyzes learner engagement patterns."""
    
    def __init__(self):
        self.engagement_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    def record_engagement(
        self,
        learner_id: str,
        content_id: str,
        engagement_score: float,
        duration: int,
        timestamp: datetime
    ):
        """Record an engagement event."""
        self.engagement_history[learner_id].append({
            'content_id': content_id,
            'engagement_score': engagement_score,
            'duration': duration,
            'timestamp': timestamp
        })
    
    def calculate_engagement_score(
        self,
        learner_id: str,
        time_range_days: int = 30
    ) -> float:
        """Calculate average engagement score for a learner."""
        cutoff = datetime.now() - timedelta(days=time_range_days)
        recent_engagements = [
            e for e in self.engagement_history[learner_id]
            if e['timestamp'] >= cutoff
        ]
        
        if not recent_engagements:
            return 0.0
        
        scores = [e['engagement_score'] for e in recent_engagements]
        return sum(scores) / len(scores)
    
    def get_engagement_trend(
        self,
        learner_id: str,
        granularity: TimeGranularity = TimeGranularity.DAILY,
        days: int = 30
    ) -> List[Tuple[datetime, float]]:
        """Get engagement trend over time."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            e for e in self.engagement_history[learner_id]
            if e['timestamp'] >= cutoff
        ]
        
        # Group by time period
        grouped = defaultdict(list)
        for engagement in recent:
            if granularity == TimeGranularity.DAILY:
                key = engagement['timestamp'].date()
            elif granularity == TimeGranularity.WEEKLY:
                # Get Monday of the week
                date = engagement['timestamp'].date()
                monday = date - timedelta(days=date.weekday())
                key = monday
            else:  # MONTHLY
                key = datetime(
                    engagement['timestamp'].year,
                    engagement['timestamp'].month,
                    1
                )
            
            grouped[key].append(engagement['engagement_score'])
        
        # Calculate averages
        trend = []
        for time_period, scores in sorted(grouped.items()):
            avg_score = sum(scores) / len(scores)
            if isinstance(time_period, datetime):
                trend.append((time_period, avg_score))
            else:
                trend.append((datetime.combine(time_period, datetime.min.time()), avg_score))
        
        return trend
    
    def identify_peak_engagement_times(
        self,
        learner_id: str,
        days: int = 30
    ) -> Dict[int, float]:
        """Identify peak engagement times by hour of day."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            e for e in self.engagement_history[learner_id]
            if e['timestamp'] >= cutoff
        ]
        
        hourly_scores: Dict[int, List[float]] = defaultdict(list)
        
        for engagement in recent:
            hour = engagement['timestamp'].hour
            hourly_scores[hour].append(engagement['engagement_score'])
        
        # Calculate average engagement per hour
        hourly_avg = {}
        for hour, scores in hourly_scores.items():
            hourly_avg[hour] = sum(scores) / len(scores)
        
        return hourly_avg
    
    def detect_engagement_patterns(
        self,
        learner_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Detect engagement patterns for a learner."""
        trend = self.get_engagement_trend(learner_id, TimeGranularity.DAILY, days)
        peak_times = self.identify_peak_engagement_times(learner_id, days)
        
        patterns = {
            'overall_trend': 'stable',
            'improving': False,
            'declining': False,
            'peak_hours': [],
            'consistency_score': 0.0
        }
        
        if len(trend) >= 7:
            first_week = [s for _, s in trend[:7]]
            last_week = [s for _, s in trend[-7:]]
            
            first_avg = sum(first_week) / len(first_week)
            last_avg = sum(last_week) / len(last_week)
            
            if last_avg > first_avg * 1.1:
                patterns['improving'] = True
                patterns['overall_trend'] = 'increasing'
            elif last_avg < first_week[0] * 0.9:
                patterns['declining'] = True
                patterns['overall_trend'] = 'decreasing'
        
        # Find peak hours
        sorted_hours = sorted(peak_times.items(), key=lambda x: x[1], reverse=True)
        patterns['peak_hours'] = [h for h, _ in sorted_hours[:3]]
        
        # Calculate consistency
        if trend:
            scores = [s for _, s in trend]
            if len(scores) > 1:
                patterns['consistency_score'] = max(0, 1 - statistics.stdev(scores))
        
        return patterns


class ProgressTracker:
    """Tracks and manages learner progress."""
    
    def __init__(self):
        self.progress_records: Dict[str, List[ProgressSnapshot]] = defaultdict(list)
        self.content_status: Dict[str, Dict[str, str]] = defaultdict(dict)
    
    def update_progress(
        self,
        learner_id: str,
        content_id: str,
        progress_percentage: float,
        time_spent_seconds: int,
        status: str,
        score: Optional[float] = None
    ):
        """Update learner progress for content."""
        snapshot = ProgressSnapshot(
            timestamp=datetime.now(),
            content_id=content_id,
            progress_percentage=progress_percentage,
            time_spent_seconds=time_spent_seconds,
            status=status,
            score=score
        )
        
        self.progress_records[learner_id].append(snapshot)
        self.content_status[learner_id][content_id] = status
    
    def get_content_progress(
        self,
        learner_id: str,
        content_id: str
    ) -> Optional[ProgressSnapshot]:
        """Get the latest progress snapshot for content."""
        records = [
            r for r in self.progress_records[learner_id]
            if r.content_id == content_id
        ]
        
        return records[-1] if records else None
    
    def get_overall_progress(
        self,
        learner_id: str,
        total_content_items: int
    ) -> float:
        """Calculate overall progress percentage."""
        status = self.content_status.get(learner_id, {})
        completed = sum(1 for s in status.values() if s == 'completed')
        
        return (completed / total_content_items * 100) if total_content_items > 0 else 0.0
    
    def get_progress_by_content(
        self,
        learner_id: str
    ) -> Dict[str, ProgressSnapshot]:
        """Get latest progress for all content."""
        latest = {}
        for record in self.progress_records[learner_id]:
            if record.content_id not in latest:
                latest[record.content_id] = record
        return latest
    
    def get_completion_rate(
        self,
        learner_id: str,
        started_content: List[str]
    ) -> float:
        """Calculate completion rate for started content."""
        status = self.content_status.get(learner_id, {})
        completed = sum(1 for c_id in started_content if status.get(c_id) == 'completed')
        
        return (completed / len(started_content) * 100) if started_content else 0.0
    
    def get_progress_trend(
        self,
        learner_id: str,
        days: int = 30
    ) -> List[Tuple[datetime, float]]:
        """Get progress trend over time."""
        cutoff = datetime.now() - timedelta(days=days)
        records = [
            r for r in self.progress_records[learner_id]
            if r.timestamp >= cutoff
        ]
        
        # Group by date
        daily_progress: Dict[datetime, List[float]] = defaultdict(list)
        for record in records:
            date = record.timestamp.date()
            daily_progress[date].append(record.progress_percentage)
        
        trend = []
        for date, progresses in sorted(daily_progress.items()):
            avg_progress = sum(progresses) / len(progresses)
            trend.append((datetime.combine(date, datetime.min.time()), avg_progress))
        
        return trend
    
    def estimate_completion_time(
        self,
        learner_id: str,
        content_id: str
    ) -> Optional[int]:
        """Estimate remaining time to complete content."""
        current = self.get_content_progress(learner_id, content_id)
        
        if not current:
            return None
        
        if current.status == 'completed':
            return 0
        
        # Calculate average pace
        pace = current.progress_percentage / current.time_spent_seconds if current.time_spent_seconds > 0 else 0
        
        if pace == 0:
            return None
        
        remaining_percentage = 100 - current.progress_percentage
        estimated_remaining = remaining_percentage / pace
        
        return int(estimated_remaining)


class PerformanceAnalyzer:
    """Analyzes learner performance on assessments and activities."""
    
    def __init__(self):
        self.assessment_results: Dict[str, List[SkillAssessment]] = defaultdict(list)
        self.score_history: Dict[str, List[Tuple[datetime, float]]] = defaultdict(list)
    
    def record_assessment(
        self,
        assessment: SkillAssessment
    ):
        """Record an assessment result."""
        self.assessment_results[assessment.learner_id].append(assessment)
        self.score_history[assessment.learner_id].append(
            (assessment.timestamp, assessment.percentage_score)
        )
    
    def get_average_score(
        self,
        learner_id: str,
        assessment_type: Optional[str] = None,
        days: Optional[int] = None
    ) -> float:
        """Calculate average score for a learner."""
        assessments = self.assessment_results.get(learner_id, [])
        
        if assessment_type:
            assessments = [a for a in assessments if a.assessment_type == assessment_type]
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            assessments = [a for a in assessments if a.timestamp >= cutoff]
        
        if not assessments:
            return 0.0
        
        return sum(a.percentage_score for a in assessments) / len(assessments)
    
    def get_score_trend(
        self,
        learner_id: str,
        assessment_type: Optional[str] = None
    ) -> List[Tuple[datetime, float]]:
        """Get score improvement trend."""
        scores = self.score_history.get(learner_id, [])
        
        if assessment_type:
            assessments = [
                a for a in self.assessment_results.get(learner_id, [])
                if a.assessment_type == assessment_type
            ]
            scores = [(a.timestamp, a.percentage_score) for a in assessments]
        
        return sorted(scores, key=lambda x: x[0])
    
    def get_skill_levels(
        self,
        learner_id: str
    ) -> Dict[str, float]:
        """Get current skill levels for a learner."""
        latest_skills: Dict[str, SkillAssessment] = {}
        
        for assessment in self.assessment_results.get(learner_id, []):
            key = (assessment.skill_name, assessment.assessment_type)
            if key not in latest_skills or assessment.timestamp > latest_skills[key].timestamp:
                latest_skills[key] = assessment
        
        return {
            assessment.skill_name: assessment.percentage_score
            for assessment in latest_skills.values()
        }
    
    def get_skill_improvement(
        self,
        learner_id: str,
        skill_name: str
    ) -> Dict[str, float]:
        """Get improvement metrics for a specific skill."""
        skill_assessments = [
            a for a in self.assessment_results.get(learner_id, [])
            if a.skill_name == skill_name
        ]
        
        if len(skill_assessments) < 2:
            return {
                'current_level': skill_assessments[0].percentage_score if skill_assessments else 0.0,
                'improvement': 0.0,
                'trend': 'insufficient_data'
            }
        
        first = skill_assessments[0].percentage_score
        last = skill_assessments[-1].percentage_score
        
        return {
            'current_level': last,
            'improvement': last - first,
            'trend': 'improving' if last > first else 'stable' if last == first else 'declining'
        }
    
    def identify_strengths_and_weaknesses(
        self,
        learner_id: str,
        threshold: float = 70.0
    ) -> Dict[str, List[str]]:
        """Identify learner strengths and weaknesses."""
        skill_levels = self.get_skill_levels(learner_id)
        
        strengths = [skill for skill, level in skill_levels.items() if level >= threshold]
        weaknesses = [skill for skill, level in skill_levels.items() if level < threshold]
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'average_level': sum(skill_levels.values()) / len(skill_levels) if skill_levels else 0.0
        }
    
    def get_assessment_analytics(
        self,
        learner_id: str,
        assessment_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed assessment analytics."""
        assessments = self.assessment_results.get(learner_id, [])
        
        if assessment_id:
            assessments = [a for a in assessments if a.assessment_id == assessment_id]
            if not assessments:
                return {}
        
        if not assessments:
            return {}
        
        assessment = assessments[-1]
        
        return {
            'total_assessments': len(assessments),
            'average_score': self.get_average_score(learner_id),
            'latest_score': assessment.percentage_score,
            'questions_answered': sum(a.questions_answered for a in assessments),
            'correct_answers': sum(a.correct_answers for a in assessments),
            'accuracy_rate': (
                sum(a.correct_answers for a in assessments) /
                sum(a.questions_answered for a in assessments) * 100
            ) if assessments else 0.0,
            'average_time_per_assessment': (
                sum(a.time_taken for a in assessments) / len(assessments)
            ) if assessments else 0
        }


class SkillGapAnalyzer:
    """Analyzes skill gaps between current and target skill levels."""
    
    def __init__(self):
        self.target_profiles: Dict[str, Dict[str, float]] = {}
        self.skill_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    def set_target_profile(
        self,
        profile_id: str,
        target_skills: Dict[str, float]
    ):
        """Set target skill profile."""
        self.target_profiles[profile_id] = target_skills
    
    def analyze_gaps(
        self,
        learner_id: str,
        current_skills: Dict[str, float],
        target_profile_id: Optional[str] = None,
        custom_targets: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Analyze skill gaps against targets."""
        if target_profile_id:
            targets = self.target_profiles.get(target_profile_id, {})
        elif custom_targets:
            targets = custom_targets
        else:
            targets = {}
        
        gaps = {}
        priority_gaps = []
        
        for skill, target_level in targets.items():
            current_level = current_skills.get(skill, 0.0)
            gap = target_level - current_level
            
            if gap > 0:
                gaps[skill] = {
                    'current': current_level,
                    'target': target_level,
                    'gap': gap,
                    'priority': self._calculate_priority(gap, target_level)
                }
                
                if gap > target_level * 0.3:
                    priority_gaps.append(skill)
        
        # Sort by priority
        sorted_gaps = sorted(
            gaps.items(),
            key=lambda x: x[1]['priority'],
            reverse=True
        )
        
        return {
            'gaps': dict(sorted_gaps),
            'priority_gaps': priority_gaps,
            'total_gaps': len(gaps),
            'coverage': len(current_skills) / len(targets) if targets else 1.0,
            'overall_readiness': self._calculate_readiness(current_skills, targets)
        }
    
    def _calculate_priority(
        self,
        gap: float,
        target: float
    ) -> float:
        """Calculate priority score for a skill gap."""
        gap_percentage = gap / target if target > 0 else 0
        return gap_percentage
    
    def _calculate_readiness(
        self,
        current: Dict[str, float],
        targets: Dict[str, float]
    ) -> float:
        """Calculate overall readiness percentage."""
        if not targets:
            return 100.0
        
        readiness_scores = []
        for skill, target in targets.items():
            current_level = current.get(skill, 0.0)
            if target > 0:
                readiness = min(100, current_level / target * 100)
                readiness_scores.append(readiness)
        
        return sum(readiness_scores) / len(readiness_scores) if readiness_scores else 0.0
    
    def recommend_content_for_gaps(
        self,
        gaps: Dict[str, Any],
        available_content: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Recommend content to address skill gaps."""
        recommendations = []
        
        for skill, gap_info in gaps.get('gaps', {}).items():
            for content in available_content:
                if skill in content.get('topics', []):
                    recommendations.append({
                        'content_id': content['id'],
                        'title': content['title'],
                        'skill_addressed': skill,
                        'gap_size': gap_info['gap'],
                        'priority': gap_info['priority']
                    })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        return recommendations
    
    def get_learning_recommendations(
        self,
        learner_id: str,
        current_skills: Dict[str, float]
    ) -> List[str]:
        """Generate natural language learning recommendations."""
        gaps = self.analyze_gaps(learner_id, current_skills)
        
        recommendations = []
        
        if gaps['total_gaps'] == 0:
            recommendations.append("You've mastered all target skills! Consider exploring advanced topics.")
        else:
            for skill, gap_info in list(gaps['gaps'].items())[:3]:
                if gap_info['gap'] > 20:
                    recommendations.append(
                        f"Focus on improving {skill} - you're {gap_info['gap']:.1f}% below your target."
                    )
                elif gap_info['gap'] > 10:
                    recommendations.append(
                        f"Slight practice needed in {skill} to reach your goal."
                    )
        
        if gaps['priority_gaps']:
            recommendations.append(
                f"Priority areas: {', '.join(gaps['priority_gaps'][:3])}"
            )
        
        return recommendations


class AnalyticsService:
    """
    Main analytics service aggregating multiple analysis engines.
    """
    
    def __init__(self):
        self.engagement_analyzer = EngagementAnalyzer()
        self.progress_tracker = ProgressTracker()
        self.performance_analyzer = PerformanceAnalyzer()
        self.skill_gap_analyzer = SkillGapAnalyzer()
        
        # Data storage (would be replaced with actual database)
        self.sessions: Dict[str, LearningSession] = {}
        self.content_analytics: Dict[str, ContentAnalytics] = {}
        self.course_analytics: Dict[str, CourseAnalytics] = {}
        self.reports: List[AnalyticsReport] = []
    
    # Session Management
    def start_session(
        self,
        session_id: str,
        learner_id: str
    ) -> LearningSession:
        """Start a new learning session."""
        session = LearningSession(
            session_id=session_id,
            learner_id=learner_id,
            start_time=datetime.now(),
            end_time=None,
            content_ids=[],
            total_duration=0,
            events=[]
        )
        
        self.sessions[session_id] = session
        return session
    
    def end_session(
        self,
        session_id: str
    ) -> Optional[LearningSession]:
        """End a learning session."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.end_time = datetime.now()
            session.total_duration = int(
                (session.end_time - session.start_time).total_seconds()
            )
            return session
        return None
    
    def record_session_event(
        self,
        session_id: str,
        event_type: str,
        event_data: Dict[str, Any]
    ):
        """Record an event in a learning session."""
        if session_id in self.sessions:
            event = {
                'type': event_type,
                'data': event_data,
                'timestamp': datetime.now()
            }
            self.sessions[session_id]['events'].append(event)
    
    # Engagement Methods
    def track_engagement(
        self,
        learner_id: str,
        content_id: str,
        engagement_score: float,
        duration: int
    ):
        """Track learner engagement."""
        self.engagement_analyzer.record_engagement(
            learner_id, content_id, engagement_score, duration, datetime.now()
        )
        
        # Also record in session
        for session in self.sessions.values():
            if session.learner_id == learner_id and session.is_active:
                session.events.append({
                    'type': 'engagement',
                    'content_id': content_id,
                    'score': engagement_score,
                    'duration': duration,
                    'timestamp': datetime.now()
                })
                if content_id not in session.content_ids:
                    session.content_ids.append(content_id)
    
    def get_learner_engagement(
        self,
        learner_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get comprehensive engagement data for a learner."""
        return {
            'average_engagement': self.engagement_analyzer.calculate_engagement_score(
                learner_id, days
            ),
            'engagement_trend': self.engagement_analyzer.get_engagement_trend(
                learner_id, TimeGranularity.DAILY, days
            ),
            'patterns': self.engagement_analyzer.detect_engagement_patterns(
                learner_id, days
            ),
            'peak_times': self.engagement_analyzer.identify_peak_engagement_times(
                learner_id, days
            )
        }
    
    # Progress Methods
    def track_progress(
        self,
        learner_id: str,
        content_id: str,
        progress_percentage: float,
        time_spent_seconds: int,
        status: str,
        score: Optional[float] = None
    ):
        """Track learner progress."""
        self.progress_tracker.update_progress(
            learner_id, content_id, progress_percentage,
            time_spent_seconds, status, score
        )
        
        # Update performance if assessment
        if score is not None and status == 'completed':
            self.performance_analyzer.record_assessment(SkillAssessment(
                assessment_id=f"auto_{content_id}_{datetime.now().timestamp()}",
                learner_id=learner_id,
                skill_name=content_id,
                assessment_type='content_completion',
                score=score,
                max_score=100,
                confidence_level=0.8,
                questions_answered=1,
                correct_answers=1 if score >= 70 else 0,
                time_taken=time_spent_seconds,
                timestamp=datetime.now(),
                feedback=[]
            ))
    
    def get_learner_progress(
        self,
        learner_id: str,
        total_content_items: int = 0
    ) -> LearnerMetrics:
        """Get comprehensive progress metrics for a learner."""
        # Calculate session statistics
        learner_sessions = [
            s for s in self.sessions.values() 
            if s.learner_id == learner_id
        ]
        
        total_time = sum(s.total_duration for s in learner_sessions)
        avg_session = (
            total_time / len(learner_sessions) 
            if learner_sessions else 0
        )
        
        # Calculate streaks
        activity_dates = set()
        for session in learner_sessions:
            activity_dates.add(session.start_time.date())
        
        if activity_dates:
            sorted_dates = sorted(activity_dates)
            streaks = self._calculate_streaks(sorted_dates)
        else:
            streaks = {'current': 0, 'longest': 0}
        
        # Get progress records
        progress = self.progress_tracker.get_progress_by_content(learner_id)
        completed = sum(
            1 for p in progress.values() 
            if p.status == 'completed'
        )
        
        # Get skill levels
        skill_levels = self.performance_analyzer.get_skill_levels(learner_id)
        
        return LearnerMetrics(
            learner_id=learner_id,
            total_time_spent=total_time,
            total_content_completed=completed,
            total_assessments_taken=len(
                self.performance_analyzer.assessment_results.get(learner_id, [])
            ),
            average_score=self.performance_analyzer.get_average_score(learner_id),
            average_engagement=self.engagement_analyzer.calculate_engagement_score(
                learner_id
            ),
            current_streak=streaks['current'],
            longest_streak=streaks['longest'],
            last_active=learner_sessions[-1].start_time if learner_sessions else None,
            total_sessions=len(learner_sessions),
            average_session_duration=avg_session,
            completion_rate=self.progress_tracker.get_completion_rate(
                learner_id, list(progress.keys())
            ),
            skill_levels=skill_levels,
            recent_activity=[
                {
                    'timestamp': s.start_time.isoformat(),
                    'content_count': len(s.content_ids),
                    'duration': s.total_duration
                }
                for s in learner_sessions[-10:]
            ]
        )
    
    def _calculate_streaks(
        self,
        activity_dates: set
    ) -> Dict[str, int]:
        """Calculate current and longest streaks from activity dates."""
        if not activity_dates:
            return {'current': 0, 'longest': 0}
        
        sorted_dates = sorted(activity_dates)
        
        current_streak = 0
        today = datetime.now().date()
        
        # Check if streak is still active (activity today or yesterday)
        if sorted_dates[-1] >= today - timedelta(days=1):
            current_streak = 1
            for i in range(len(sorted_dates) - 2, -1, -1):
                if (sorted_dates[i + 1] - sorted_dates[i]).days == 1:
                    current_streak += 1
                else:
                    break
        
        # Calculate longest streak
        longest_streak = 1
        current = 1
        
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
                current += 1
            else:
                longest_streak = max(longest_streak, current)
                current = 1
        
        longest_streak = max(longest_streak, current)
        
        return {'current': current_streak, 'longest': longest_streak}
    
    # Performance Methods
    def record_assessment_result(
        self,
        assessment_id: str,
        learner_id: str,
        skill_name: str,
        assessment_type: str,
        score: float,
        max_score: float,
        questions_answered: int,
        correct_answers: int,
        time_taken: int,
        feedback: List[str]
    ):
        """Record an assessment result."""
        assessment = SkillAssessment(
            assessment_id=assessment_id,
            learner_id=learner_id,
            skill_name=skill_name,
            assessment_type=assessment_type,
            score=score,
            max_score=max_score,
            confidence_level=self._calculate_confidence(questions_answered, correct_answers),
            questions_answered=questions_answered,
            correct_answers=correct_answers,
            time_taken=time_taken,
            timestamp=datetime.now(),
            feedback=feedback
        )
        
        self.performance_analyzer.record_assessment(assessment)
    
    def _calculate_confidence(
        self,
        questions_answered: int,
        correct_answers: int
    ) -> float:
        """Calculate confidence level based on assessment."""
        if questions_answered == 0:
            return 0.0
        
        accuracy = correct_answers / questions_answered
        
        # Higher confidence for more questions
        if questions_answered >= 20:
            base_confidence = 0.9
        elif questions_answered >= 10:
            base_confidence = 0.75
        else:
            base_confidence = 0.6
        
        # Adjust based on accuracy
        return min(1.0, base_confidence * (0.5 + accuracy * 0.5))
    
    def get_learner_performance(
        self,
        learner_id: str
    ) -> Dict[str, Any]:
        """Get comprehensive performance data for a learner."""
        return {
            'average_score': self.performance_analyzer.get_average_score(learner_id),
            'score_trend': self.performance_analyzer.get_score_trend(learner_id),
            'skill_levels': self.performance_analyzer.get_skill_levels(learner_id),
            'skill_improvements': {
                skill: self.performance_analyzer.get_skill_improvement(learner_id, skill)
                for skill in self.performance_analyzer.get_skill_levels(learner_id)
            },
            'strengths_weaknesses': self.performance_analyzer.identify_strengths_and_weaknesses(
                learner_id
            ),
            'assessment_analytics': self.performance_analyzer.get_assessment_analytics(learner_id)
        }
    
    # Skill Gap Methods
    def set_learner_targets(
        self,
        learner_id: str,
        target_skills: Dict[str, float]
    ):
        """Set target skills for a learner."""
        self.skill_gap_analyzer.set_target_profile(learner_id, target_skills)
    
    def analyze_skill_gaps(
        self,
        learner_id: str,
        current_skills: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze skill gaps for a learner."""
        gaps = self.skill_gap_analyzer.analyze_gaps(
            learner_id, current_skills, learner_id
        )
        
        gaps['recommendations'] = self.skill_gap_analyzer.get_learning_recommendations(
            learner_id, current_skills
        )
        
        return gaps
    
    # Content Analytics Methods
    def update_content_analytics(
        self,
        content_id: str,
        view_count: int = 0,
        completion_count: int = 0,
        avg_time_spent: float = 0.0,
        avg_score: float = 0.0,
        avg_rating: float = 0.0
    ):
        """Update analytics for content."""
        if content_id in self.content_analytics:
            analytics = self.content_analytics[content_id]
            analytics.total_views += view_count
            analytics.total_completions += completion_count
            analytics.average_time_spent = (
                (analytics.average_time_spent + avg_time_spent) / 2
            )
            analytics.average_score = (
                (analytics.average_score + avg_score) / 2
            )
            analytics.average_rating = (
                (analytics.average_rating + avg_rating) / 2
            )
        else:
            self.content_analytics[content_id] = ContentAnalytics(
                content_id=content_id,
                total_views=view_count,
                unique_viewers=0,
                total_completions=completion_count,
                completion_rate=0.0,
                average_time_spent=avg_time_spent,
                average_score=avg_score,
                average_rating=avg_rating,
                drop_off_points={},
                engagement_trend=[],
                difficulty_rating=0.0,
                popularity_rank=0
            )
    
    def get_content_analytics(
        self,
        content_id: str
    ) -> Optional[ContentAnalytics]:
        """Get analytics for specific content."""
        return self.content_analytics.get(content_id)
    
    # Report Generation
    def generate_learner_report(
        self,
        learner_id: str,
        time_range_days: int = 30
    ) -> AnalyticsReport:
        """Generate a comprehensive learner report."""
        progress = self.get_learner_progress(learner_id)
        engagement = self.get_learner_engagement(learner_id, time_range_days)
        performance = self.get_learner_performance(learner_id)
        
        skill_levels = performance['skill_levels']
        gaps = self.analyze_skill_gaps(learner_id, skill_levels)
        
        # Generate insights
        insights = []
        recommendations = []
        
        if progress.average_engagement > 0.7:
            insights.append("Consistently high engagement levels observed.")
        elif progress.average_engagement < 0.4:
            insights.append("Engagement has been below average - consider more interactive content.")
        
        if progress.completion_rate > 80:
            insights.append("Excellent completion rates across learning content.")
        
        if performance['average_score'] > 85:
            insights.append("Strong performance on assessments.")
        elif performance['average_score'] < 60:
            insights.append("Assessment performance could be improved with more practice.")
        
        # Skill gap recommendations
        for gap_skill in gaps.get('priority_gaps', [])[:3]:
            recommendations.append(f"Focus on improving {gap_skill} skills")
        
        # Engagement recommendations
        if engagement['patterns'].get('declining'):
            recommendations.append("Consider setting a consistent learning schedule")
        
        # Streak recommendations
        if progress.current_streak < 3 and progress.current_streak > 0:
            recommendations.append("Try to maintain a 3-day learning streak for better retention")
        
        report = AnalyticsReport(
            report_id=f"learner_{learner_id}_{datetime.now().timestamp()}",
            report_type="learner_progress",
            generated_at=datetime.now(),
            time_range_start=datetime.now() - timedelta(days=time_range_days),
            time_range_end=datetime.now(),
            data={
                'progress': progress.to_dict(),
                'engagement': engagement,
                'performance': performance,
                'skill_gaps': gaps
            },
            summary=f"Progress: {progress.completion_rate:.1f}% complete, "
                   f"Average Score: {performance['average_score']:.1f}%, "
                   f"Engagement: {progress.average_engagement:.2f}",
            insights=insights,
            recommendations=recommendations
        )
        
        self.reports.append(report)
        return report
    
    def generate_course_report(
        self,
        course_id: str,
        enrolled_learners: List[str]
    ) -> AnalyticsReport:
        """Generate a course-level analytics report."""
        progress_rates = []
        avg_scores = []
        avg_engagement = []
        skill_distributions: Dict[str, List[float]] = defaultdict(list)
        
        for learner_id in enrolled_learners:
            progress = self.get_learner_progress(learner_id)
            performance = self.get_learner_performance(learner_id)
            engagement = self.get_learner_engagement(learner_id)
            
            progress_rates.append(progress.completion_rate)
            avg_scores.append(performance['average_score'])
            avg_engagement.append(engagement['average_engagement'])
            
            for skill, level in progress.skill_levels.items():
                skill_distributions[skill].append(level)
        
        avg_progress = sum(progress_rates) / len(progress_rates) if progress_rates else 0
        avg_score = sum(avg_scores) / len(avg_scores) if avg_scores else 0
        avg_engage = sum(avg_engagement) / len(avg_engagement) if avg_engagement else 0
        
        active_count = sum(1 for e in avg_engagement if e > 0.3)
        
        insights = [
            f"Average completion rate: {avg_progress:.1f}%",
            f"Average assessment score: {avg_score:.1f}%",
            f"Active learners: {active_count}/{len(enrolled_learners)}"
        ]
        
        if avg_progress < 50:
            insights.append("Course completion rates are below target - consider content improvements")
        
        if avg_engage < 0.5:
            insights.append("Engagement levels suggest need for more interactive elements")
        
        report = AnalyticsReport(
            report_id=f"course_{course_id}_{datetime.now().timestamp()}",
            report_type="course_analytics",
            generated_at=datetime.now(),
            time_range_start=datetime.now() - timedelta(days=30),
            time_range_end=datetime.now(),
            data={
                'course_id': course_id,
                'enrolled_count': len(enrolled_learners),
                'active_count': active_count,
                'completion_rate': avg_progress,
                'avg_score': avg_score,
                'avg_engagement': avg_engage,
                'skill_distributions': dict(skill_distributions)
            },
            summary=f"Course Analytics: {avg_progress:.1f}% avg completion, "
                   f"{avg_score:.1f}% avg score, {active_count} active learners",
            insights=insights,
            recommendations=[]
        )
        
        self.reports.append(report)
        return report
    
    def get_dashboard_summary(
        self,
        learner_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get dashboard summary for multiple learners."""
        if learner_ids is None:
            learner_ids = list(set(s.learner_id for s in self.sessions.values()))
        
        metrics = []
        
        for learner_id in learner_ids:
            progress = self.get_learner_progress(learner_id)
            metrics.append({
                'learner_id': learner_id,
                'completion_rate': progress.completion_rate,
                'average_score': progress.average_score,
                'engagement': progress.average_engagement,
                'streak': progress.current_streak,
                'total_time': progress.total_time_spent
            })
        
        if not metrics:
            return {
                'total_learners': 0,
                'avg_completion': 0,
                'avg_score': 0,
                'avg_engagement': 0,
                'active_streaks': 0,
                'top_learners': []
            }
        
        completion_rates = [m['completion_rate'] for m in metrics]
        scores = [m['average_score'] for m in metrics]
        engagements = [m['engagement'] for m in metrics]
        streaks = [m['streak'] for m in metrics]
        
        top_learners = sorted(
            metrics,
            key=lambda x: (x['completion_rate'], x['average_score']),
            reverse=True
        )[:5]
        
        return {
            'total_learners': len(metrics),
            'avg_completion': sum(completion_rates) / len(completion_rates),
            'avg_score': sum(scores) / len(scores),
            'avg_engagement': sum(engagements) / len(engagements),
            'active_streaks': sum(1 for s in streaks if s > 0),
            'top_learners': [
                {
                    'learner_id': l['learner_id'],
                    'completion': l['completion_rate'],
                    'score': l['average_score']
                }
                for l in top_learners
            ]
        }


# Service factory function
def create_analytics_service() -> AnalyticsService:
    """Create and configure a new analytics service instance."""
    return AnalyticsService()
