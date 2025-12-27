"""
Learner Experience Platform - Multi-Level Support System

This module provides infrastructure for supporting multiple education levels
including K-12, higher education, and professional training paths.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json
import logging

from .curriculum_service import (
    CurriculumNode,
    CurriculumTree,
    CurriculumService,
    create_curriculum_service,
    EducationLevel,
    SubjectArea
)


logger = logging.getLogger(__name__)


class AdaptiveDifficulty(str, Enum):
    """Adaptive difficulty levels for content."""
    FOUNDATIONAL = "foundational"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class LearnerProfile:
    """
    Comprehensive learner profile with preferences, history, and competencies.
    
    Attributes:
        user_id: Associated user identifier
        education_level: Current education level
        target_path: Career or learning path
        preferences: Learning preferences
        accessibility_needs: Accessibility requirements
        current_level: Current competency level
        strength_areas: Areas of strength
        growth_areas: Areas needing improvement
        learning_style: Preferred learning style
        available_hours: Weekly study hours available
        goals: Learning goals
        created_at: Profile creation timestamp
        updated_at: Last update timestamp
    """
    user_id: str
    education_level: str = "K12"
    target_path: str = ""
    preferences: Dict[str, Any] = field(default_factory=dict)
    accessibility_needs: Dict[str, Any] = field(default_factory=dict)
    current_level: str = "beginner"
    strength_areas: List[str] = field(default_factory=list)
    growth_areas: List[str] = field(default_factory=list)
    learning_style: str = "visual"
    available_hours: float = 5.0
    goals: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "userId": self.user_id,
            "educationLevel": self.education_level,
            "targetPath": self.target_path,
            "preferences": self.preferences,
            "accessibilityNeeds": self.accessibility_needs,
            "currentLevel": self.current_level,
            "strengthAreas": self.strength_areas,
            "growthAreas": self.growth_areas,
            "learningStyle": self.learning_style,
            "availableHours": self.available_hours,
            "goals": self.goals,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }


@dataclass
class ScaffoldingConfig:
    """
    Configuration for adaptive scaffolding during learning.
    
    Attributes:
        initial_complexity: Starting complexity multiplier
        max_complexity: Maximum complexity multiplier
        min_complexity: Minimum complexity multiplier
        adjustment_rate: How fast difficulty adjusts
        success_threshold: Success rate to increase difficulty
        struggle_threshold: Success rate to decrease difficulty
        hint_frequency: How often to provide hints
        examples_per_concept: Number of examples to provide
        practice_problems: Number of practice problems per session
    """
    initial_complexity: float = 1.0
    max_complexity: float = 2.0
    min_complexity: float = 0.5
    adjustment_rate: float = 0.1
    success_threshold: float = 0.8
    struggle_threshold: float = 0.4
    hint_frequency: int = 3
    examples_per_concept: int = 2
    practice_problems: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "initialComplexity": self.initial_complexity,
            "maxComplexity": self.max_complexity,
            "minComplexity": self.min_complexity,
            "adjustmentRate": self.adjustment_rate,
            "successThreshold": self.success_threshold,
            "struggleThreshold": self.struggle_threshold,
            "hintFrequency": self.hint_frequency,
            "examplesPerConcept": self.examples_per_concept,
            "practiceProblems": self.practice_problems
        }


@dataclass
class ContentLocalization:
    """
    Localization data for content across languages.
    
    Attributes:
        content_id: Associated content identifier
        language: Language code (ISO 639-1)
        title: Localized title
        description: Localized description
        voiceover_url: URL to voiceover audio
        transcript_url: URL to transcript
        subtitles_url: URL to subtitle file
        alternative_text: Screen reader alternative text
        cultural_notes: Cultural adaptation notes
    """
    content_id: str
    language: str
    title: str = ""
    description: str = ""
    voiceover_url: Optional[str] = None
    transcript_url: Optional[str] = None
    subtitles_url: Optional[str] = None
    alternative_text: str = ""
    cultural_notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "contentId": self.content_id,
            "language": self.language,
            "title": self.title,
            "description": self.description,
            "voiceoverUrl": self.voiceover_url,
            "transcriptUrl": self.transcript_url,
            "subtitlesUrl": self.subtitles_url,
            "alternativeText": self.alternative_text,
            "culturalNotes": self.cultural_notes
        }


@dataclass
class MultiLevelConfig:
    """
    Configuration for multi-level support.
    
    Attributes:
        level: Education level
        curriculum_standards: Standards to follow
        content_depth: Depth of content coverage
        assessment_style: Style of assessments
        pacing_guide: Weekly pacing recommendations
        prerequisites: Required prerequisites
        certifications: Available certifications
    """
    level: str
    curriculum_standards: List[str] = field(default_factory=list)
    content_depth: str = "standard"
    assessment_style: str = "formative"
    pacing_guide: Dict[str, int] = field(default_factory=dict)
    prerequisites: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level,
            "curriculumStandards": self.curriculum_standards,
            "contentDepth": self.content_depth,
            "assessmentStyle": self.assessment_style,
            "pacingGuide": self.pacing_guide,
            "prerequisites": self.prerequisites,
            "certifications": self.certifications
        }


class MultiLevelSupportService:
    """
    Service providing multi-level support for learners across K-12,
    higher education, and professional training.
    
    This service manages:
    - Learner profile management
    - Adaptive difficulty scaling
    - Curriculum alignment per level
    - Content localization
    - Scaffolding configuration
    - Learning style adaptation
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the multi-level support service.
        
        Args:
            storage_dir: Directory for persisting data
        """
        self.storage_dir = storage_dir or "/tmp/visualverse-multi-level"
        
        self.learner_profiles: Dict[str, LearnerProfile] = {}
        self.localizations: Dict[str, List[ContentLocalization]] = {}
        self.level_configs: Dict[str, MultiLevelConfig] = {}
        self.scaffolding_configs: Dict[str, ScaffoldingConfig] = {}
        self._load_state()
        
        # Initialize default level configurations
        if not self.level_configs:
            self._initialize_level_configs()
        
        logger.info("MultiLevelSupportService initialized")
    
    def _load_state(self):
        """Load persisted state."""
        import os
        os.makedirs(self.storage_dir, exist_ok=True)
        
        profiles_file = f"{self.storage_dir}/profiles.json"
        localizations_file = f"{self.storage_dir}/localizations.json"
        level_configs_file = f"{self.storage_dir}/level_configs.json"
        
        if os.path.exists(profiles_file):
            try:
                with open(profiles_file, 'r') as f:
                    data = json.load(f)
                    self.learner_profiles = {
                        uid: LearnerProfile(**p) for uid, p in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load profiles: {e}")
        
        if os.path.exists(localizations_file):
            try:
                with open(localizations_file, 'r') as f:
                    data = json.load(f)
                    self.localizations = {
                        cid: [ContentLocalization(**l) for l in locs]
                        for cid, locs in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load localizations: {e}")
        
        if os.path.exists(level_configs_file):
            try:
                with open(level_configs_file, 'r') as f:
                    data = json.load(f)
                    self.level_configs = {
                        level: MultiLevelConfig(**cfg) 
                        for level, cfg in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load level configs: {e}")
    
    def _save_state(self):
        """Persist state to storage."""
        import os
        from pathlib import Path
        
        Path(self.storage_dir).mkdir(parents=True, exist_ok=True)
        
        profiles_file = f"{self.storage_dir}/profiles.json"
        localizations_file = f"{self.storage_dir}/localizations.json"
        level_configs_file = f"{self.storage_dir}/level_configs.json"
        
        with open(profiles_file, 'w') as f:
            json.dump(
                {uid: p.to_dict() for uid, p in self.learner_profiles.items()},
                f, indent=2
            )
        
        with open(localizations_file, 'w') as f:
            json.dump(
                {cid: [l.to_dict() for l in locs] 
                 for cid, locs in self.localizations.items()},
                f, indent=2
            )
        
        with open(level_configs_file, 'w') as f:
            json.dump(
                {level: cfg.to_dict() for level, cfg in self.level_configs.items()},
                f, indent=2
            )
    
    def _initialize_level_configs(self):
        """Initialize default configurations for each education level."""
        self.level_configs = {
            "K12_Primary": MultiLevelConfig(
                level="K12_Primary",
                curriculum_standards=["NCERT", "CBSE_Primary"],
                content_depth="foundational",
                assessment_style="formative",
                pacing_guide={"math": 4, "science": 3, "english": 3},
                prerequisites=[],
                certifications=["Primary_Math_Certificate"]
            ),
            "K12_Middle": MultiLevelConfig(
                level="K12_Middle",
                curriculum_standards=["NCERT", "CBSE_Middle", "ICSE"],
                content_depth="developmental",
                assessment_style="mixed",
                pacing_guide={"math": 5, "science": 4, "english": 3},
                prerequisites=["K12_Primary"],
                certifications=["Middle_School_Certificate"]
            ),
            "K12_Secondary": MultiLevelConfig(
                level="K12_Secondary",
                curriculum_standards=["CBSE", "ICSE", "IB_MYP"],
                content_depth="intermediate",
                assessment_style="summative",
                pacing_guide={"mathematics": 5, "physics": 4, "chemistry": 4, "biology": 3},
                prerequisites=["K12_Middle"],
                certifications=["Secondary_Certificate", "Board_Exam_Prep"]
            ),
            "K12_HigherSecondary": MultiLevelConfig(
                level="K12_HigherSecondary",
                curriculum_standards=["CBSE", "ICSE", "IB_DP", "State_Board"],
                content_depth="advanced",
                assessment_style="examinations",
                pacing_guide={"mathematics": 6, "physics": 5, "chemistry": 5, "biology": 4},
                prerequisites=["K12_Secondary"],
                certifications=["Higher_Secondary_Certificate", "JEE_Prep", "NEET_Prep"]
            ),
            "College_Undergraduate": MultiLevelConfig(
                level="College_Undergraduate",
                curriculum_standards=["University_Curriculum", "NBA"],
                content_depth="comprehensive",
                assessment_style="continuous",
                pacing_guide={"core": 6, "electives": 4},
                prerequisites=["K12_HigherSecondary"],
                certifications=["Degree_Program", "Specialization_Certificate"]
            ),
            "College_Graduate": MultiLevelConfig(
                level="College_Graduate",
                curriculum_standards=["University_Curriculum", "UGC"],
                content_depth="specialized",
                assessment_style="research",
                pacing_guide={"thesis": 8, "coursework": 4},
                prerequisites=["College_Undergraduate"],
                certifications=["Masters_Degree", "Research_Paper"]
            ),
            "Professional": MultiLevelConfig(
                level="Professional",
                curriculum_standards=["Industry_Standards", "Professional_Bodies"],
                content_depth="expert",
                assessment_style="practical",
                pacing_guide={"core": 8, "practical": 6},
                prerequisites=[],
                certifications=["Professional_Certification", "Skill_Badges", "Industry_Recognition"]
            ),
            "Corporate_Training": MultiLevelConfig(
                level="Corporate_Training",
                curriculum_standards=["Corporate_LMS", "L&D_Frameworks"],
                content_depth="targeted",
                assessment_style="competency",
                pacing_guide={"onboarding": 2, "skills": 4, "leadership": 6},
                prerequisites=[],
                certifications=["Company_Certificate", "Skill_Verification"]
            )
        }
        
        self._save_state()
    
    # Learner Profile Management
    def create_learner_profile(self, user_id: str, education_level: str = "K12",
                               **kwargs) -> LearnerProfile:
        """
        Create a new learner profile.
        
        Args:
            user_id: User identifier
            education_level: Education level
            **kwargs: Additional profile fields
            
        Returns:
            Created LearnerProfile
        """
        with self.lock:
            if user_id in self.learner_profiles:
                raise ValueError(f"Profile for user {user_id} already exists")
            
            profile = LearnerProfile(
                user_id=user_id,
                education_level=education_level,
                **kwargs
            )
            
            self.learner_profiles[user_id] = profile
            
            # Create default scaffolding config
            self.scaffolding_configs[user_id] = ScaffoldingConfig()
            
            self._save_state()
            
            logger.info(f"Learner profile created: {user_id}")
            return profile
    
    def get_learner_profile(self, user_id: str) -> Optional[LearnerProfile]:
        """
        Get a learner profile by user ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            LearnerProfile or None if not found
        """
        return self.learner_profiles.get(user_id)
    
    def update_learner_profile(self, user_id: str, **updates) -> Optional[LearnerProfile]:
        """
        Update a learner profile.
        
        Args:
            user_id: User to update
            **updates: Fields to update
            
        Returns:
            Updated LearnerProfile or None if not found
        """
        with self.lock:
            if user_id not in self.learner_profiles:
                return None
            
            profile = self.learner_profiles[user_id]
            
            for field, value in updates.items():
                if hasattr(profile, field) and field not in ["user_id"]:
                    setattr(profile, field, value)
            
            profile.updated_at = datetime.utcnow()
            self._save_state()
            
            return profile
    
    # Adaptive Difficulty Management
    def get_adaptive_difficulty(self, user_id: str, 
                               performance_history: List[Dict]) -> float:
        """
        Calculate adaptive difficulty multiplier based on performance.
        
        Args:
            user_id: User identifier
            performance_history: Recent performance data
            
        Returns:
            Difficulty multiplier (0.5 to 2.0)
        """
        profile = self.learner_profiles.get(user_id)
        if not profile:
            return 1.0
        
        config = self.scaffolding_configs.get(user_id, ScaffoldingConfig())
        
        if not performance_history:
            return config.initial_complexity
        
        # Calculate success rate
        recent_successes = sum(1 for p in performance_history if p.get("success", False))
        success_rate = recent_successes / len(performance_history)
        
        # Adjust complexity based on performance
        if success_rate >= config.success_threshold:
            # Increase difficulty
            new_complexity = config.initial_complexity + config.adjustment_rate
        elif success_rate <= config.struggle_threshold:
            # Decrease difficulty
            new_complexity = config.initial_complexity - config.adjustment_rate
        else:
            # Maintain current level
            new_complexity = config.initial_complexity
        
        # Clamp to allowed range
        return max(config.min_complexity, min(config.max_complexity, new_complexity))
    
    def record_performance(self, user_id: str, content_id: str,
                          success: bool, time_spent: int, 
                          hints_used: int = 0) -> Dict[str, Any]:
        """
        Record a learning session performance.
        
        Args:
            user_id: User identifier
            content_id: Content completed
            success: Whether successful
            time_spent: Time spent in seconds
            hints_used: Number of hints used
            
        Returns:
            Performance analysis result
        """
        profile = self.learner_profiles.get(user_id)
        if not profile:
            return {"error": "Profile not found"}
        
        config = self.scaffolding_configs.get(user_id, ScaffoldingConfig())
        
        # Calculate performance score
        base_score = 1.0 if success else 0.0
        time_bonus = min(0.2, (300 - time_spent) / 1500) if success else 0
        hint_penalty = min(0.3, hints_used * 0.1)
        
        performance_score = max(0, base_score + time_bonus - hint_penalty)
        
        # Determine if difficulty should change
        should_increase = performance_score >= 0.85 and hints_used == 0
        should_decrease = performance_score < 0.5 or hints_used >= 3
        
        new_complexity = config.initial_complexity
        if should_increase:
            new_complexity = min(config.max_complexity, config.initial_complexity + 0.15)
        elif should_decrease:
            new_complexity = max(config.min_complexity, config.initial_complexity - 0.15)
        
        # Update scaffolding config
        config.initial_complexity = new_complexity
        self.scaffolding_configs[user_id] = config
        
        # Update learner profile
        if success:
            if content_id not in profile.strength_areas:
                profile.strength_areas.append(content_id)
        else:
            if content_id not in profile.growth_areas:
                profile.growth_areas.append(content_id)
        
        profile.updated_at = datetime.utcnow()
        self._save_state()
        
        return {
            "performanceScore": round(performance_score, 2),
            "newComplexity": round(new_complexity, 2),
            "shouldIncreaseDifficulty": should_increase,
            "shouldDecreaseDifficulty": should_decrease,
            "feedback": self._generate_feedback(performance_score, hints_used)
        }
    
    def _generate_feedback(self, score: float, hints: int) -> str:
        """Generate feedback message based on performance."""
        if score >= 0.9:
            return "Excellent work! You're ready to advance."
        elif score >= 0.7:
            return "Good progress! Keep practicing to solidify your understanding."
        elif score >= 0.5:
            return "You're on the right track. Review the hints and try again."
        else:
            return "Let's review the fundamentals. Try the easier version first."
    
    # Scaffolding Configuration
    def get_scaffolding_config(self, user_id: str) -> ScaffoldingConfig:
        """
        Get scaffolding configuration for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            ScaffoldingConfig
        """
        return self.scaffolding_configs.get(user_id, ScaffoldingConfig())
    
    def update_scaffolding_config(self, user_id: str, 
                                 **updates) -> ScaffoldingConfig:
        """
        Update scaffolding configuration.
        
        Args:
            user_id: User identifier
            **updates: Configuration fields to update
            
        Returns:
            Updated ScaffoldingConfig
        """
        with self.lock:
            config = self.scaffolding_configs.get(user_id, ScaffoldingConfig())
            
            for field, value in updates.items():
                if hasattr(config, field):
                    setattr(config, field, value)
            
            self.scaffolding_configs[user_id] = config
            self._save_state()
            
            return config
    
    # Level Configuration
    def get_level_config(self, level: str) -> Optional[MultiLevelConfig]:
        """
        Get configuration for an education level.
        
        Args:
            level: Education level identifier
            
        Returns:
            MultiLevelConfig or None if not found
        """
        return self.level_configs.get(level)
    
    def list_level_configs(self) -> List[MultiLevelConfig]:
        """List all available level configurations."""
        return list(self.level_configs.values())
    
    # Localization Management
    def add_localization(self, content_id: str, language: str,
                        title: str, description: str = "",
                        **kwargs) -> ContentLocalization:
        """
        Add localization for content.
        
        Args:
            content_id: Content identifier
            language: Language code
            title: Localized title
            description: Localized description
            **kwargs: Additional localization fields
            
        Returns:
            Created ContentLocalization
        """
        with self.lock:
            if content_id not in self.localizations:
                self.localizations[content_id] = []
            
            localization = ContentLocalization(
                content_id=content_id,
                language=language,
                title=title,
                description=description,
                **kwargs
            )
            
            self.localizations[content_id].append(localization)
            self._save_state()
            
            return localization
    
    def get_localization(self, content_id: str, language: str) -> Optional[ContentLocalization]:
        """
        Get localization for content in a specific language.
        
        Args:
            content_id: Content identifier
            language: Language code
            
        Returns:
            ContentLocalization or None if not found
        """
        if content_id not in self.localizations:
            return None
        
        for loc in self.localizations[content_id]:
            if loc.language == language:
                return loc
        
        # Fall back to English
        for loc in self.localizations[content_id]:
            if loc.language == "en":
                return loc
        
        return None
    
    def get_available_languages(self, content_id: str) -> List[str]:
        """
        Get list of available languages for content.
        
        Args:
            content_id: Content identifier
            
        Returns:
            List of language codes
        """
        if content_id not in self.localizations:
            return []
        
        return [loc.language for loc in self.localizations[content_id]]
    
    # Learning Path Generation
    def generate_level_learning_path(self, user_id: str, 
                                     target_level: str) -> Dict[str, Any]:
        """
        Generate a learning path for a target education level.
        
        Args:
            user_id: User identifier
            target_level: Target education level
            
        Returns:
            Learning path with modules and milestones
        """
        profile = self.learner_profiles.get(user_id)
        if not profile:
            return {"error": "Profile not found"}
        
        level_config = self.level_configs.get(target_level)
        if not level_config:
            return {"error": f"Level configuration not found: {target_level}"}
        
        # Check prerequisites
        missing_prerequisites = []
        for prereq in level_config.prerequisites:
            if prereq not in profile.strength_areas:
                missing_prerequisites.append(prereq)
        
        path = {
            "targetLevel": target_level,
            "estimatedWeeks": sum(level_config.pacing_guide.values()),
            "modules": [],
            "prerequisites": missing_prerequisites,
            "certifications": level_config.certifications,
            "assessmentStyle": level_config.assessment_style,
            "contentDepth": level_config.content_depth
        }
        
        # Generate modules from pacing guide
        for subject, weeks in level_config.pacing_guide.items():
            module = {
                "subject": subject,
                "weeks": weeks,
                "topics": self._generate_topics_for_subject(subject, target_level),
                "assessments": self._generate_assessments_for_subject(subject, level_config.assessment_style)
            }
            path["modules"].append(module)
        
        # Add milestones
        path["milestones"] = self._generate_milestones(path["modules"], target_level)
        
        return path
    
    def _generate_topics_for_subject(self, subject: str, 
                                     level: str) -> List[Dict[str, Any]]:
        """Generate topics for a subject at a given level."""
        topics = []
        
        # Subject-specific topic generation
        if subject in ["math", "mathematics"]:
            base_topics = [
                {"topic": "Number Systems", "difficulty": "foundational"},
                {"topic": "Algebra", "difficulty": "developmental"},
                {"topic": "Geometry", "difficulty": "intermediate"},
                {"topic": "Calculus", "difficulty": "advanced"},
                {"topic": "Statistics", "difficulty": "intermediate"}
            ]
        elif subject in ["physics", "science"]:
            base_topics = [
                {"topic": "Mechanics", "difficulty": "foundational"},
                {"topic": "Thermodynamics", "difficulty": "developmental"},
                {"topic": "Electromagnetism", "difficulty": "intermediate"},
                {"topic": "Quantum Physics", "difficulty": "advanced"},
                {"topic": "Relativity", "difficulty": "expert"}
            ]
        elif subject == "chemistry":
            base_topics = [
                {"topic": "Atomic Structure", "difficulty": "foundational"},
                {"topic": "Chemical Bonding", "difficulty": "developmental"},
                {"topic": "Thermodynamics", "difficulty": "intermediate"},
                {"topic": "Organic Chemistry", "difficulty": "advanced"},
                {"topic": "Biochemistry", "difficulty": "expert"}
            ]
        else:
            base_topics = [
                {"topic": f"{subject.capitalize()} Basics", "difficulty": "foundational"},
                {"topic": f"{subject.capitalize()} Fundamentals", "difficulty": "developmental"},
                {"topic": f"{subject.capitalize()} Applications", "difficulty": "intermediate"},
                {"topic": f"{subject.capitalize()} Advanced Topics", "difficulty": "advanced"}
            ]
        
        # Adjust difficulty based on level
        level_multiplier = {
            "K12_Primary": 0.5,
            "K12_Middle": 0.7,
            "K12_Secondary": 1.0,
            "K12_HigherSecondary": 1.2,
            "College_Undergraduate": 1.3,
            "College_Graduate": 1.5,
            "Professional": 1.4,
            "Corporate_Training": 1.1
        }.get(level, 1.0)
        
        for base_topic in base_topics:
            adjusted_difficulty = self._adjust_difficulty(
                base_topic["difficulty"], level_multiplier
            )
            topics.append({
                "name": base_topic["topic"],
                "difficulty": adjusted_difficulty,
                "estimatedHours": 4 * level_multiplier
            })
        
        return topics
    
    def _adjust_difficulty(self, base: str, multiplier: float) -> str:
        """Adjust difficulty level based on multiplier."""
        levels = ["foundational", "developing", "proficient", "advanced", "expert"]
        base_index = levels.index(base) if base in levels else 2
        new_index = min(4, max(0, int(base_index * multiplier)))
        return levels[new_index]
    
    def _generate_assessments_for_subject(self, subject: str, 
                                          style: str) -> List[Dict[str, Any]]:
        """Generate assessment structure for a subject."""
        assessments = []
        
        if style == "formative":
            assessments = [
                {"type": "quiz", "count": 5, "weight": 0.2},
                {"type": "interactive", "count": 3, "weight": 0.3},
                {"type": "project", "count": 1, "weight": 0.5}
            ]
        elif style == "summative":
            assessments = [
                {"type": "midterm", "count": 1, "weight": 0.3},
                {"type": "quiz", "count": 3, "weight": 0.2},
                {"type": "final", "count": 1, "weight": 0.5}
            ]
        else:  # continuous
            assessments = [
                {"type": "weekly_quiz", "count": 8, "weight": 0.3},
                {"type": "assignment", "count": 4, "weight": 0.3},
                {"type": "presentation", "count": 2, "weight": 0.2},
                {"type": "research", "count": 1, "weight": 0.2}
            ]
        
        return assessments
    
    def _generate_milestones(self, modules: List, level: str) -> List[Dict[str, Any]]:
        """Generate learning milestones."""
        milestones = []
        cumulative_weeks = 0
        
        for i, module in enumerate(modules):
            cumulative_weeks += module["weeks"]
            milestones.append({
                "name": f"{module['subject'].capitalize()} Milestone {i+1}",
                "week": cumulative_weeks,
                "modules": [module["subject"]],
                "certification": f"{module['subject']}_Certificate_{level}"
            })
        
        # Final milestone
        milestones.append({
            "name": f"{level} Completion",
            "week": cumulative_weeks,
            "modules": [m["subject"] for m in modules],
            "certification": f"{level}_Certificate",
            "isFinal": True
        })
        
        return milestones


# Thread lock for thread-safe operations
MultiLevelSupportService.lock = __import__('threading').RLock()


def create_multi_level_service(storage_dir: str = None) -> MultiLevelSupportService:
    """
    Create and return the global multi-level support service.
    
    Args:
        storage_dir: Optional storage directory
        
    Returns:
        MultiLevelSupportService instance
    """
    return MultiLevelSupportService(storage_dir)


__all__ = [
    "AdaptiveDifficulty",
    "LearnerProfile",
    "ScaffoldingConfig",
    "ContentLocalization",
    "MultiLevelConfig",
    "MultiLevelSupportService",
    "create_multi_level_service"
]
