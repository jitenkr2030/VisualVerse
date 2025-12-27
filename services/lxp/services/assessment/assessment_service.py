"""
Assessment Service for Learner Experience Platform.

Provides comprehensive assessment capabilities including question banks,
test delivery, scoring, adaptive testing, and analytics.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import defaultdict
import json


class QuestionType(Enum):
    """Types of assessment questions."""
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECT = "multiple_select"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    FILL_BLANK = "fill_blank"
    MATCHING = "matching"
    ORDERING = "ordering"
    CODE = "code"
    SIMULATION = "simulation"


class AssessmentType(Enum):
    """Types of assessments."""
    QUIZ = "quiz"
    EXAM = "exam"
    PRACTICE = "practice"
    DIAGNOSTIC = "diagnostic"
    FORMATIVE = "formative"
    SUMMATIVE = "summative"
    ADAPTIVE = "adaptive"
    SKILL_CHECK = "skill_check"


class Difficulty(Enum):
    """Question difficulty levels."""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


class AssessmentStatus(Enum):
    """Status of an assessment attempt."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    TIMED_OUT = "timed_out"
    ABANDONED = "abandoned"


@dataclass
class Question:
    """An assessment question."""
    question_id: str
    assessment_id: str
    question_type: QuestionType
    content: str
    options: List[str] = field(default_factory=list)
    correct_answer: Any = None
    explanation: str = ""
    difficulty: Difficulty = Difficulty.MEDIUM
    points: int = 10
    time_limit_seconds: Optional[int] = None
    topics: List[str] = field(default_factory=list)
    skills_tested: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Answer:
    """A learner's answer to a question."""
    question_id: str
    answer: Any
    time_spent_seconds: int
    is_correct: bool = False
    points_earned: float = 0.0
    feedback: str = ""
    answered_at: datetime = field(default_factory=datetime.now)


@dataclass
class AssessmentConfig:
    """Configuration for an assessment."""
    assessment_id: str
    title: str
    assessment_type: AssessmentType
    total_time_minutes: int
    passing_score: float = 70.0
    max_attempts: int = 3
    shuffle_questions: bool = True
    show_results: bool = True
    show_correct_answers: bool = False
    allow_review: bool = True
    adaptive_mode: bool = False
    difficulty_start: Difficulty = Difficulty.MEDIUM
    question_count: int = 10
    randomize_options: bool = True


@dataclass
class AssessmentAttempt:
    """An attempt at an assessment."""
    attempt_id: str
    learner_id: str
    assessment_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: AssessmentStatus = AssessmentStatus.NOT_STARTED
    answers: List[Answer] = field(default_factory=list)
    current_question_index: int = 0
    score: float = 0.0
    percentage_score: float = 0.0
    time_spent_seconds: int = 0
    is_passed: bool = False
    feedback: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuestionAnalytics:
    """Analytics for a specific question."""
    question_id: str
    total_attempts: int = 0
    correct_attempts: int = 0
    average_time_seconds: float = 0.0
    difficulty_rating: float = 0.0
    discrimination_index: float = 0.0
    point_biserial: float = 0.0
    skip_rate: float = 0.0


@dataclass
class AssessmentAnalytics:
    """Analytics for an entire assessment."""
    assessment_id: str
    total_attempts: int = 0
    unique_attempts: int = 0
    completion_rate: float = 0.0
    average_score: float = 0.0
    pass_rate: float = 0.0
    average_time_minutes: float = 0.0
    question_analytics: Dict[str, QuestionAnalytics] = field(default_factory=dict)
    score_distribution: Dict[str, int] = field(default_factory=dict)


class AssessmentService:
    """
    Service for managing assessments, questions, and test delivery.
    
    Handles the complete assessment lifecycle including creation,
    delivery, scoring, and analytics.
    """
    
    def __init__(self):
        self.assessments: Dict[str, AssessmentConfig] = {}
        self.questions: Dict[str, Question] = {}
        self.attempts: Dict[str, AssessmentAttempt] = {}
        self.learner_attempts: Dict[str, List[str]] = defaultdict(list)
        self.assessment_analytics: Dict[str, AssessmentAnalytics] = {}
        
        # Question bank by topic
        self.question_bank: Dict[str, List[str]] = defaultdict(list)
        
        # Initialize sample assessments
        self._init_sample_assessments()
    
    def _init_sample_assessments(self):
        """Initialize sample assessments for testing."""
        # Sample assessment config
        sample_assessment = AssessmentConfig(
            assessment_id="sample_math_quiz",
            title="Sample Math Quiz",
            assessment_type=AssessmentType.QUIZ,
            total_time_minutes=15,
            passing_score=70.0,
            max_attempts=3,
            question_count=5
        )
        self.assessments["sample_math_quiz"] = sample_assessment
        
        # Sample questions
        sample_questions = [
            Question(
                question_id="q1",
                assessment_id="sample_math_quiz",
                question_type=QuestionType.MULTIPLE_CHOICE,
                content="What is 2 + 2?",
                options=["3", "4", "5", "6"],
                correct_answer="4",
                explanation="Basic addition: 2 + 2 = 4",
                difficulty=Difficulty.EASY,
                points=10,
                topics=["math", "arithmetic"],
                skills_tested=["basic_math"]
            ),
            Question(
                question_id="q2",
                assessment_id="sample_math_quiz",
                question_type=QuestionType.MULTIPLE_CHOICE,
                content="What is the square root of 16?",
                options=["2", "4", "8", "16"],
                correct_answer="4",
                explanation="4 × 4 = 16, so √16 = 4",
                difficulty=Difficulty.EASY,
                points=10,
                topics=["math", "algebra"],
                skills_tested=["square_roots"]
            )
        ]
        
        for q in sample_questions:
            self.questions[q.question_id] = q
            self.question_bank[q.assessment_id].append(q.question_id)
    
    # Assessment Management
    def create_assessment(
        self,
        assessment_id: str,
        title: str,
        assessment_type: AssessmentType,
        total_time_minutes: int,
        question_count: int = 10,
        passing_score: float = 70.0,
        **kwargs
    ) -> AssessmentConfig:
        """Create a new assessment configuration."""
        config = AssessmentConfig(
            assessment_id=assessment_id,
            title=title,
            assessment_type=assessment_type,
            total_time_minutes=total_time_minutes,
            question_count=question_count,
            passing_score=passing_score,
            **{k: v for k, v in kwargs.items() if k in [
                'max_attempts', 'shuffle_questions', 'show_results',
                'show_correct_answers', 'allow_review', 'adaptive_mode',
                'difficulty_start', 'randomize_options'
            ]}
        )
        
        self.assessments[assessment_id] = config
        self.assessment_analytics[assessment_id] = AssessmentAnalytics(
            assessment_id=assessment_id
        )
        
        return config
    
    def get_assessment(self, assessment_id: str) -> Optional[AssessmentConfig]:
        """Get an assessment configuration."""
        return self.assessments.get(assessment_id)
    
    def update_assessment(
        self,
        assessment_id: str,
        **updates
    ) -> Optional[AssessmentConfig]:
        """Update an assessment configuration."""
        if assessment_id not in self.assessments:
            return None
        
        config = self.assessments[assessment_id]
        for key, value in updates.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config
    
    # Question Management
    def add_question(
        self,
        question_id: str,
        assessment_id: str,
        question_type: QuestionType,
        content: str,
        correct_answer: Any,
        options: Optional[List[str]] = None,
        explanation: str = "",
        difficulty: Difficulty = Difficulty.MEDIUM,
        points: int = 10,
        topics: Optional[List[str]] = None,
        skills_tested: Optional[List[str]] = None
    ) -> Question:
        """Add a question to an assessment."""
        question = Question(
            question_id=question_id,
            assessment_id=assessment_id,
            question_type=question_type,
            content=content,
            options=options or [],
            correct_answer=correct_answer,
            explanation=explanation,
            difficulty=difficulty,
            points=points,
            topics=topics or [],
            skills_tested=skills_tested or []
        )
        
        self.questions[question_id] = question
        self.question_bank[assessment_id].append(question_id)
        
        return question
    
    def get_question(self, question_id: str) -> Optional[Question]:
        """Get a specific question."""
        return self.questions.get(question_id)
    
    def get_questions_for_assessment(
        self,
        assessment_id: str,
        count: Optional[int] = None,
        shuffle: bool = True
    ) -> List[Question]:
        """Get questions for an assessment."""
        question_ids = self.question_bank.get(assessment_id, [])
        
        if shuffle:
            import random
            selected = random.sample(
                question_ids,
                min(count or len(question_ids), len(question_ids))
            )
        else:
            selected = question_ids[:count or len(question_ids)]
        
        return [
            self.questions[qid] for qid in selected
            if qid in self.questions
        ]
    
    def get_questions_by_topic(
        self,
        topic: str,
        count: int = 10,
        difficulty: Optional[Difficulty] = None
    ) -> List[Question]:
        """Get questions filtered by topic."""
        questions = [
            q for q in self.questions.values()
            if topic in q.topics
        ]
        
        if difficulty:
            questions = [q for q in questions if q.difficulty == difficulty]
        
        return questions[:count]
    
    def get_questions_by_skill(
        self,
        skill: str,
        count: int = 10
    ) -> List[Question]:
        """Get questions testing a specific skill."""
        return [
            q for q in self.questions.values()
            if skill in q.skills_tested
        ][:count]
    
    # Assessment Taking
    def start_assessment(
        self,
        learner_id: str,
        assessment_id: str
    ) -> Tuple[Optional[AssessmentAttempt], Optional[str]]:
        """
        Start an assessment attempt.
        
        Returns:
            Tuple of (AssessmentAttempt, error_message)
        """
        if assessment_id not in self.assessments:
            return None, "Assessment not found"
        
        config = self.assessments[assessment_id]
        
        # Check attempt limit
        existing_attempts = [
            a for a in self.learner_attempts[learner_id]
            if a in self.attempts and self.attempts[a].assessment_id == assessment_id
        ]
        
        if len(existing_attempts) >= config.max_attempts:
            return None, "Maximum attempts reached"
        
        # Get questions
        questions = self.get_questions_for_assessment(
            assessment_id,
            count=config.question_count,
            shuffle=config.shuffle_questions
        )
        
        if not questions:
            return None, "No questions available for this assessment"
        
        attempt = AssessmentAttempt(
            attempt_id=f"attempt_{learner_id}_{assessment_id}_{datetime.now().timestamp()}",
            learner_id=learner_id,
            assessment_id=assessment_id,
            started_at=datetime.now(),
            status=AssessmentStatus.IN_PROGRESS,
            current_question_index=0
        )
        
        self.attempts[attempt.attempt_id] = attempt
        self.learner_attempts[learner_id].append(attempt.attempt_id)
        
        # Update analytics
        analytics = self.assessment_analytics.get(assessment_id)
        if analytics:
            analytics.total_attempts += 1
            analytics.unique_attempts = len(set(
                a.learner_id for a in self.attempts.values()
                if a.assessment_id == assessment_id
            ))
        
        return attempt, None
    
    def get_current_question(
        self,
        attempt_id: str
    ) -> Tuple[Optional[Question], Optional[str]]:
        """Get the current question for an attempt."""
        if attempt_id not in self.attempts:
            return None, "Attempt not found"
        
        attempt = self.attempts[attempt_id]
        config = self.assessments.get(attempt.assessment_id)
        
        if not config:
            return None, "Assessment not found"
        
        questions = self.get_questions_for_assessment(
            attempt.assessment_id,
            count=config.question_count,
            shuffle=False  # Keep consistent order
        )
        
        if attempt.current_question_index >= len(questions):
            return None, "Assessment complete"
        
        return questions[attempt.current_question_index], None
    
    def submit_answer(
        self,
        attempt_id: str,
        question_id: str,
        answer: Any,
        time_spent_seconds: int
    ) -> Tuple[Optional[Answer], Optional[str]]:
        """Submit an answer to a question."""
        if attempt_id not in self.attempts:
            return None, "Attempt not found"
        
        attempt = self.attempts[attempt_id]
        question = self.questions.get(question_id)
        
        if not question:
            return None, "Question not found"
        
        # Grade the answer
        is_correct = self._grade_answer(question, answer)
        
        # Calculate points
        if is_correct:
            points_earned = question.points
        else:
            # Partial credit could be implemented here
            points_earned = 0.0
        
        # Generate feedback
        feedback = ""
        if is_correct:
            feedback = "Correct! " + question.explanation
        else:
            feedback = "Incorrect. " + question.explanation
        
        answer_obj = Answer(
            question_id=question_id,
            answer=answer,
            time_spent_seconds=time_spent_seconds,
            is_correct=is_correct,
            points_earned=points_earned,
            feedback=feedback
        )
        
        attempt.answers.append(answer_obj)
        
        # Update question analytics
        self._update_question_analytics(question_id, answer_obj)
        
        # Advance to next question
        attempt.current_question_index += 1
        
        return answer_obj, None
    
    def _grade_answer(
        self,
        question: Question,
        answer: Any
    ) -> bool:
        """Grade an answer against correct answer."""
        correct = question.correct_answer
        
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            return str(answer).strip() == str(correct).strip()
        
        elif question.question_type == QuestionType.TRUE_FALSE:
            return str(answer).lower() == str(correct).lower()
        
        elif question.question_type == QuestionType.MULTIPLE_SELECT:
            # Compare sets
            answer_set = set(str(a).strip() for a in answer)
            correct_set = set(str(c).strip() for c in correct)
            return answer_set == correct_set
        
        elif question.question_type == QuestionType.FILL_BLANK:
            return str(answer).strip().lower() == str(correct).strip().lower()
        
        elif question.question_type == QuestionType.MATCHING:
            # For matching, answer should be dict of match pairs
            if isinstance(answer, dict) and isinstance(correct, dict):
                return answer == correct
        
        elif question.question_type == QuestionType.ORDERING:
            # Compare lists
            if isinstance(answer, list) and isinstance(correct, list):
                return answer == correct
        
        return False
    
    def complete_assessment(
        self,
        attempt_id: str
    ) -> Tuple[Optional[AssessmentAttempt], Optional[str]]:
        """Complete an assessment attempt."""
        if attempt_id not in self.attempts:
            return None, "Attempt not found"
        
        attempt = self.attempts[attempt_id]
        attempt.completed_at = datetime.now()
        attempt.status = AssessmentStatus.COMPLETED
        
        # Calculate total time
        attempt.time_spent_seconds = int(
            (attempt.completed_at - attempt.started_at).total_seconds()
        )
        
        # Calculate score
        total_points = sum(
            self.questions.get(a.question_id, self.questions.get(a.question_id, type('Q', (), {'points': 0})())).points
            for a in attempt.answers
            if a.question_id in self.questions
        )
        
        earned_points = sum(a.points_earned for a in attempt.answers)
        
        if total_points > 0:
            attempt.score = earned_points
            attempt.percentage_score = (earned_points / total_points) * 100
        else:
            attempt.score = 0
            attempt.percentage_score = 0
        
        # Check if passed
        config = self.assessments.get(attempt.assessment_id)
        if config:
            attempt.is_passed = attempt.percentage_score >= config.passing_score
        
        # Generate feedback
        attempt.feedback = self._generate_attempt_feedback(attempt)
        
        # Update assessment analytics
        self._update_assessment_analytics(attempt)
        
        return attempt, None
    
    def _generate_attempt_feedback(
        self,
        attempt: AssessmentAttempt
    ) -> Dict[str, Any]:
        """Generate feedback for an assessment attempt."""
        correct_count = sum(1 for a in attempt.answers if a.is_correct)
        total_count = len(attempt.answers)
        
        # Identify strengths and weaknesses
        skill_scores: Dict[str, Tuple[int, int]] = defaultdict(lambda: [0, 0])  # correct, total
        
        for answer in attempt.answers:
            question = self.questions.get(answer.question_id)
            if question:
                for skill in question.skills_tested:
                    skill_scores[skill][1] += 1
                    if answer.is_correct:
                        skill_scores[skill][0] += 1
        
        strengths = [
            skill for skill, (correct, total) in skill_scores.items()
            if total > 0 and correct / total >= 0.7
        ]
        
        weaknesses = [
            skill for skill, (correct, total) in skill_scores.items()
            if total > 0 and correct / total < 0.5
        ]
        
        return {
            "correct_answers": correct_count,
            "total_questions": total_count,
            "time_spent_minutes": attempt.time_spent_seconds / 60,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "pass_status": "passed" if attempt.is_passed else "failed",
            "message": (
                "Congratulations! You passed the assessment."
                if attempt.is_passed else
                "Keep practicing to improve your skills."
            )
        }
    
    def _update_question_analytics(
        self,
        question_id: str,
        answer: Answer
    ):
        """Update analytics for a question."""
        # Get or create analytics
        if question_id not in self.questions:
            return
        
        question = self.questions[question_id]
        
        # Find or create assessment analytics
        analytics = self.assessment_analytics.get(question.assessment_id)
        if not analytics:
            analytics = AssessmentAnalytics(assessment_id=question.assessment_id)
            self.assessment_analytics[question.assessment_id] = analytics
        
        if question_id not in analytics.question_analytics:
            analytics.question_analytics[question_id] = QuestionAnalytics(
                question_id=question_id
            )
        
        qa = analytics.question_analytics[question_id]
        qa.total_attempts += 1
        
        if answer.is_correct:
            qa.correct_attempts += 1
        
        # Update average time
        total_time = qa.average_time_seconds * (qa.total_attempts - 1)
        qa.average_time_seconds = (total_time + answer.time_spent_seconds) / qa.total_attempts
    
    def _update_assessment_analytics(
        self,
        attempt: AssessmentAttempt
    ):
        """Update analytics for an assessment."""
        analytics = self.assessment_analytics.get(attempt.assessment_id)
        if not analytics:
            return
        
        analytics.total_attempts += 1
        
        # Update completion rate
        completed = sum(
            1 for a in self.attempts.values()
            if a.assessment_id == attempt.assessment_id and
            a.status == AssessmentStatus.COMPLETED
        )
        analytics.completion_rate = completed / analytics.total_attempts * 100
        
        # Update average score
        scores = [
            a.percentage_score for a in self.attempts.values()
            if a.assessment_id == attempt.assessment_id and
            a.status == AssessmentStatus.COMPLETED
        ]
        if scores:
            analytics.average_score = sum(scores) / len(scores)
        
        # Update pass rate
        passed = sum(
            1 for a in self.attempts.values()
            if a.assessment_id == attempt.assessment_id and
            a.is_passed
        )
        if completed > 0:
            analytics.pass_rate = passed / completed * 100
        
        # Update average time
        times = [
            a.time_spent_seconds / 60 for a in self.attempts.values()
            if a.assessment_id == attempt.assessment_id and
            a.status == AssessmentStatus.COMPLETED
        ]
        if times:
            analytics.average_time_minutes = sum(times) / len(times)
        
        # Update score distribution
        score_range = self._get_score_range(attempt.percentage_score)
        analytics.score_distribution[score_range] = (
            analytics.score_distribution.get(score_range, 0) + 1
        )
    
    def _get_score_range(self, percentage: float) -> str:
        """Get score range category."""
        if percentage >= 90:
            return "90-100"
        elif percentage >= 80:
            return "80-89"
        elif percentage >= 70:
            return "70-79"
        elif percentage >= 60:
            return "60-69"
        else:
            return "0-59"
    
    # Attempt Management
    def get_attempt(self, attempt_id: str) -> Optional[AssessmentAttempt]:
        """Get an assessment attempt."""
        return self.attempts.get(attempt_id)
    
    def get_learner_attempts(
        self,
        learner_id: str,
        assessment_id: Optional[str] = None
    ) -> List[AssessmentAttempt]:
        """Get all attempts for a learner."""
        attempts = [
            self.attempts[aid] for aid in self.learner_attempts.get(learner_id, [])
            if aid in self.attempts
        ]
        
        if assessment_id:
            attempts = [
                a for a in attempts if a.assessment_id == assessment_id
            ]
        
        return attempts
    
    def get_best_attempt(
        self,
        learner_id: str,
        assessment_id: str
    ) -> Optional[AssessmentAttempt]:
        """Get the best attempt for an assessment."""
        attempts = self.get_learner_attempts(learner_id, assessment_id)
        completed = [
            a for a in attempts if a.status == AssessmentStatus.COMPLETED
        ]
        
        if not completed:
            return None
        
        return max(completed, key=lambda a: a.percentage_score)
    
    # Analytics
    def get_assessment_analytics(
        self,
        assessment_id: str
    ) -> Optional[AssessmentAnalytics]:
        """Get analytics for an assessment."""
        return self.assessment_analytics.get(assessment_id)
    
    def get_question_analytics(
        self,
        question_id: str
    ) -> Optional[QuestionAnalytics]:
        """Get analytics for a specific question."""
        question = self.questions.get(question_id)
        if not question:
            return None
        
        analytics = self.assessment_analytics.get(question.assessment_id)
        if not analytics:
            return None
        
        return analytics.question_analytics.get(question_id)
    
    def get_learner_assessment_summary(
        self,
        learner_id: str
    ) -> Dict[str, Any]:
        """Get a summary of all assessments for a learner."""
        attempts = self.get_learner_attempts(learner_id)
        
        by_assessment: Dict[str, List[AssessmentAttempt]] = defaultdict(list)
        for attempt in attempts:
            by_assessment[attempt.assessment_id].append(attempt)
        
        summary = {
            "total_attempts": len(attempts),
            "completed_attempts": sum(
                1 for a in attempts if a.status == AssessmentStatus.COMPLETED
            ),
            "passed_attempts": sum(1 for a in attempts if a.is_passed),
            "assessments_completed": [],
            "assessments_in_progress": []
        }
        
        for assessment_id, assessment_attempts in by_assessment.items():
            config = self.assessments.get(assessment_id)
            if not config:
                continue
            
            best = self.get_best_attempt(learner_id, assessment_id)
            completed = [
                a for a in assessment_attempts
                if a.status == AssessmentStatus.COMPLETED
            ]
            
            attempt_info = {
                "assessment_id": assessment_id,
                "title": config.title,
                "attempts_made": len(assessment_attempts),
                "best_score": best.percentage_score if best else None,
                "passed": best.is_passed if best else False,
                "total_completed": len(completed)
            }
            
            in_progress = [
                a for a in assessment_attempts
                if a.status == AssessmentStatus.IN_PROGRESS
            ]
            
            if in_progress:
                summary["assessments_in_progress"].append(attempt_info)
            else:
                summary["assessments_completed"].append(attempt_info)
        
        return summary
    
    # Adaptive Testing
    def select_next_question_adaptive(
        self,
        attempt_id: str
    ) -> Tuple[Optional[Question], Optional[str]]:
        """Select the next question using adaptive difficulty."""
        attempt = self.attempts.get(attempt_id)
        if not attempt:
            return None, "Attempt not found"
        
        # Calculate current performance
        if not attempt.answers:
            # Start at configured difficulty
            config = self.assessments.get(attempt.assessment_id)
            difficulty = config.difficulty_start if config else Difficulty.MEDIUM
        else:
            # Adjust based on performance
            correct_rate = sum(1 for a in attempt.answers if a.is_correct) / len(attempt.answers)
            
            if correct_rate >= 0.8:
                difficulty = Difficulty(max(1, attempt.current_question_index - 2))
            elif correct_rate <= 0.4:
                difficulty = Difficulty(min(4, attempt.current_question_index + 2))
            else:
                difficulty = Difficulty(attempt.current_question_index + 1)
        
        # Get questions at appropriate difficulty
        questions = [
            q for q in self.questions.values()
            if q.assessment_id == attempt.assessment_id and
            q.difficulty == difficulty and
            q.question_id not in [a.question_id for a in attempt.answers]
        ]
        
        if not questions:
            # Fall back to any available question
            questions = self.get_questions_for_assessment(
                attempt.assessment_id,
                count=1,
                shuffle=True
            )
        
        return (questions[0], None) if questions else (None, "No questions available")
    
    def get_skill_assessment(
        self,
        learner_id: str,
        skill: str,
        question_count: int = 10
    ) -> Dict[str, Any]:
        """Generate a skill assessment for a learner."""
        questions = self.get_questions_by_skill(skill, question_count * 2)
        
        # Filter out questions already answered
        learner_attempts = self.get_learner_attempts(learner_id)
        answered_ids = set()
        for attempt in learner_attempts:
            for answer in attempt.answers:
                answered_ids.add(answer.question_id)
        
        available = [q for q in questions if q.question_id not in answered_ids]
        
        if len(available) < question_count:
            # Add more questions from same topic
            more = self.get_questions_by_topic(skill, question_count * 3)
            for q in more:
                if q.question_id not in answered_ids and q not in available:
                    available.append(q)
        
        selected = available[:question_count]
        
        return {
            "skill": skill,
            "questions": [
                {
                    "question_id": q.question_id,
                    "content": q.content,
                    "type": q.question_type.value,
                    "options": q.options if q.question_type in [
                        QuestionType.MULTIPLE_CHOICE,
                        QuestionType.MULTIPLE_SELECT
                    ] else None,
                    "points": q.points,
                    "time_limit": q.time_limit_seconds
                }
                for q in selected
            ],
            "total_points": sum(q.points for q in selected),
            "estimated_time_minutes": sum(
                (q.time_limit_seconds or 60) for q in selected
            ) // 60
        }


# Service factory function
def create_assessment_service() -> AssessmentService:
    """Create and configure a new assessment service instance."""
    return AssessmentService()
