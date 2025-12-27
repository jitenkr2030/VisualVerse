"""
Learner Experience Platform - Main Package

This package provides the complete learner experience infrastructure for
the VisualVerse learning system, including progress tracking, personalized
recommendations, learning analytics, and multi-level support.

Author: MiniMax Agent
Version: 1.0.0
"""

# Version information
__version__ = "1.0.0"
__author__ = "MiniMax Agent"

# Progress Tracking Service
from .services.progress import (
    ProgressTrackingService,
    LearnerProgress,
    SessionData,
    ConceptProgress,
    ProgressMilestone,
    Achievement,
    AchievementType,
    ProgressReport,
    create_progress_service
)

# Learning Analytics Service
from .services.analytics import (
    AnalyticsService,
    LearnerMetrics,
    ContentAnalytics,
    CourseAnalytics,
    ProgressSnapshot,
    LearningSession,
    SkillAssessment,
    AnalyticsReport,
    MetricType,
    TimeGranularity,
    create_analytics_service
)

# Recommendation Service
from .services.recommendation import (
    RecommendationService,
    Recommendation,
    RecommendationSet,
    LearnerProfile,
    ContentFeatures,
    RecommendationType,
    create_recommendation_service
)

# Multi-Level Content Service
from .services.multi_level import (
    MultiLevelService,
    LevelType,
    ContentVariant,
    AdaptiveRule,
    LearnerPreferences,
    DifficultyLevel,
    ContentFormat,
    create_multi_level_service
)

# Curriculum Management Service
from .services.multi_level.curriculum_service import (
    CurriculumService,
    Curriculum,
    CurriculumModule,
    CurriculumUnit,
    LearningStandard,
    LearnerCurriculumProgress,
    CurriculumType,
    StandardType,
    create_curriculum_service
)

# Assessment Service
from .services.assessment import (
    AssessmentService,
    Question,
    Answer,
    AssessmentConfig,
    AssessmentAttempt,
    AssessmentAnalytics,
    QuestionAnalytics,
    QuestionType,
    AssessmentType,
    Difficulty,
    AssessmentStatus,
    create_assessment_service
)

# Engagement Service
from .services.engagement import (
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
    # Version
    "__version__",
    
    # Progress Tracking
    "ProgressTrackingService",
    "LearnerProgress",
    "SessionData",
    "ConceptProgress",
    "ProgressMilestone",
    "Achievement",
    "AchievementType",
    "ProgressReport",
    "create_progress_service",
    
    # Learning Analytics
    "AnalyticsService",
    "LearnerMetrics",
    "ContentAnalytics",
    "CourseAnalytics",
    "ProgressSnapshot",
    "LearningSession",
    "SkillAssessment",
    "AnalyticsReport",
    "MetricType",
    "TimeGranularity",
    "create_analytics_service",
    
    # Recommendations
    "RecommendationService",
    "Recommendation",
    "RecommendationSet",
    "LearnerProfile",
    "ContentFeatures",
    "RecommendationType",
    "create_recommendation_service",
    
    # Multi-Level Content
    "MultiLevelService",
    "LevelType",
    "ContentVariant",
    "AdaptiveRule",
    "LearnerPreferences",
    "DifficultyLevel",
    "ContentFormat",
    "create_multi_level_service",
    
    # Curriculum Management
    "CurriculumService",
    "Curriculum",
    "CurriculumModule",
    "CurriculumUnit",
    "LearningStandard",
    "LearnerCurriculumProgress",
    "CurriculumType",
    "StandardType",
    "create_curriculum_service",
    
    # Assessment
    "AssessmentService",
    "Question",
    "Answer",
    "AssessmentConfig",
    "AssessmentAttempt",
    "AssessmentAnalytics",
    "QuestionAnalytics",
    "QuestionType",
    "AssessmentType",
    "Difficulty",
    "AssessmentStatus",
    "create_assessment_service",
    
    # Engagement
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


def get_lxp_version() -> str:
    """Get the LXP version."""
    return __version__


def initialize_lxp() -> Dict[str, Any]:
    """
    Initialize all LXP services.
    
    Returns:
        Dictionary of initialized services
    """
    from .services.progress import create_progress_service
    from .services.analytics import create_analytics_service
    from .services.recommendation import create_recommendation_service
    from .services.multi_level import create_multi_level_service
    from .services.multi_level.curriculum_service import create_curriculum_service
    from .services.assessment import create_assessment_service
    from .services.engagement import create_engagement_service
    
    return {
        "progress": create_progress_service(),
        "analytics": create_analytics_service(),
        "recommendations": create_recommendation_service(),
        "multi_level": create_multi_level_service(),
        "curriculum": create_curriculum_service(),
        "assessment": create_assessment_service(),
        "engagement": create_engagement_service()
    }


# Example usage documentation
EXAMPLE_PROGRESS = '''
# Example: Tracking Learner Progress

from visualverse_lxp import create_progress_service

# Initialize progress service
progress = create_progress_service()

# Record a learning session
session = progress.record_session(
    user_id="student-001",
    content_id="math-quadratic-equations",
    time_spent=1800,  # 30 minutes
    interactions=45,
    completed=True,
    score=0.85
)

print(f"Session completed: {session.completed}")
print(f"New mastery level: {session.mastery_level:.2f}")

# Check achievements
achievements = progress.get_user_achievements("student-001")
print(f"Achievements: {len(achievements)}")

# Get progress report
report = progress.get_progress_report(
    user_id="student-001",
    period="weekly"
)
print(f"Weekly progress: {report.completion_rate:.1f}%")
'''

EXAMPLE_ANALYTICS = '''
# Example: Learning Analytics

from visualverse_lxp import create_analytics_service

# Initialize analytics service
analytics = create_analytics_service()

# Track learning event
analytics.track_engagement(
    learner_id="student-001",
    content_id="physics-newton-laws",
    engagement_score=0.85,
    duration=1800
)

# Get learner metrics
metrics = analytics.get_learner_progress("student-001")
print(f"Average engagement: {metrics.average_engagement:.2f}")
print(f"Total time spent: {metrics.total_time_spent / 3600:.1f} hours")

# Generate learner report
report = analytics.generate_learner_report("student-001", time_range_days=30)
print(f"Report summary: {report.summary}")
'''

EXAMPLE_RECOMMENDATIONS = '''
# Example: Personalized Recommendations

from visualverse_lxp import create_recommendation_service

# Initialize recommendation service
recommendations = create_recommendation_service()

# Get personalized recommendations
rec_set = recommendations.get_recommendations(
    learner_id="student-001",
    max_items=10
)

for rec in rec_set.recommendations:
    print(f"{rec.title} (score: {rec.score:.2f})")
    print(f"  Reason: {rec.reasoning}")

# Find similar content
similar = recommendations.find_similar_content("content-123")
'''

EXAMPLE_MULTI_LEVEL = '''
# Example: Multi-Level Content

from visualverse_lxp import create_multi_level_service

# Initialize multi-level service
multi_level = create_multi_level_service()

# Register base content
multi_level.register_base_content(
    content_id="intro-physics",
    title="Introduction to Physics",
    description="Basic physics concepts",
    core_objectives=["motion", "forces", "energy"],
    topics=["physics", "mechanics", "kinematics"],
    default_duration=45
)

# Generate variant for specific level
variant = multi_level.generate_variant(
    base_content_id="intro-physics",
    target_level=LevelType.HIGH_SCHOOL
)

# Select optimal variant for learner
prefs = LearnerPreferences(preferred_level=LevelType.HIGH_SCHOOL)
optimal = multi_level.select_optimal_variant("intro-physics", prefs)
'''

EXAMPLE_CURRICULUM = '''
# Example: Curriculum Management

from visualverse_lxp import create_curriculum_service

# Initialize curriculum service
curriculum = create_curriculum_service()

# Create curriculum
curriculum.create_curriculum(
    curriculum_id="physics-fundamentals",
    title="Physics Fundamentals",
    description="Introduction to physics principles",
    curriculum_type=CurriculumType.STANDARD,
    target_level="High School",
    subject_area="Physics",
    total_duration_hours=40
)

# Add module
curriculum.add_module(
    curriculum_id="physics-fundamentals",
    module_id="module-1",
    title="Mechanics Basics",
    description="Introduction to mechanics",
    learning_objectives=["understand motion", "calculate velocity"],
    standards_covered=["std-1", "std-2"],
    content_ids=["content-1", "content-2"],
    assessment_ids=["quiz-1"],
    duration_hours=8,
    order_index=1
)

# Enroll learner
progress = curriculum.enroll_learner("student-001", "physics-fundamentals")
'''

EXAMPLE_ASSESSMENT = '''
# Example: Assessment Management

from visualverse_lxp import create_assessment_service

# Initialize assessment service
assessment = create_assessment_service()

# Create assessment
assessment.create_assessment(
    assessment_id="math-quiz-1",
    title="Algebra Quiz",
    assessment_type=AssessmentType.QUIZ,
    total_time_minutes=20,
    passing_score=70.0,
    question_count=10
)

# Add question
assessment.add_question(
    question_id="q1",
    assessment_id="math-quiz-1",
    question_type=QuestionType.MULTIPLE_CHOICE,
    content="What is the solution to 2x + 5 = 15?",
    options=["x=5", "x=10", "x=15", "x=20"],
    correct_answer="x=5",
    explanation="Subtract 5 from both sides: 2x = 10, then divide by 2: x = 5",
    difficulty=Difficulty.EASY,
    points=10
)

# Start assessment
attempt, error = assessment.start_assessment("student-001", "math-quiz-1")

# Get current question
question, _ = assessment.get_current_question(attempt.attempt_id)
'''

EXAMPLE_ENGAGEMENT = '''
# Example: Engagement and Gamification

from visualverse_lxp import create_engagement_service

# Initialize engagement service
engagement = create_engagement_service()

# Award points for completing content
points, levels, badges = engagement.award_points(
    learner_id="student-001",
    event_type=GamificationEvent.CONTENT_COMPLETED,
    metadata={"content_type": "lesson", "difficulty": "medium"}
)

print(f"Points earned: {points}")
print(f"Levels gained: {levels}")
print(f"New badges: {badges}")

# Send notification
engagement.send_notification(
    learner_id="student-001",
    notification_type=NotificationType.ACHIEVEMENT,
    title="Great Job!",
    message="You've completed your first lesson!",
    priority=NotificationPriority.HIGH
)

# Create leaderboard
leaderboard = engagement.create_leaderboard(
    leaderboard_id="weekly-top-learners",
    name="Weekly Top Learners",
    description="Top performers this week",
    category="overall",
    time_range="weekly"
)

# Get engagement report
report = engagement.get_engagement_report("student-001", period="weekly")
'''
