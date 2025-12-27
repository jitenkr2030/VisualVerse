"""
Multi-level Content Service for Learner Experience Platform.

Provides intelligent content adaptation across different educational levels
(K-12, Higher Education, Professional) with variant management.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class LevelType(Enum):
    """Educational level types for content adaptation."""
    ELEMENTARY = "elementary"  # Grades K-5
    MIDDLE_SCHOOL = "middle_school"  # Grades 6-8
    HIGH_SCHOOL = "high_school"  # Grades 9-12
    UNDERGRADUATE = "undergraduate"  # College/University
    GRADUATE = "graduate"  # Master's and above
    PROFESSIONAL = "professional"  # Workplace learning
    SELF_DIRECTED = "self_directed"  # Personal learning


class DifficultyLevel(Enum):
    """Content difficulty levels."""
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


class ContentFormat(Enum):
    """Content format types."""
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    ASSESSMENT = "assessment"
    PROJECT = "project"
    DISCUSSION = "discussion"
    SIMULATION = "simulation"


@dataclass
class ContentVariant:
    """A variant of content adapted for a specific level."""
    variant_id: str
    base_content_id: str
    level_type: LevelType
    title: str
    description: str
    content_body: str
    difficulty_level: DifficultyLevel
    format_type: ContentFormat
    estimated_minutes: int
    learning_objectives: List[str]
    prerequisites: List[str] = field(default_factory=list)
    vocabulary_level: int = 3  # 1-5 scale for reading level
    abstraction_level: int = 3  # 1-5 scale for conceptual depth
    scaffolding_depth: int = 3  # 1-5 scale for guided support
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class AdaptiveRule:
    """Rules for content adaptation."""
    rule_id: str
    condition: Dict[str, Any]
    action: Dict[str, Any]
    priority: int
    is_active: bool = True


@dataclass
class LearnerPreferences:
    """Learner preferences for content adaptation."""
    preferred_level: LevelType
    preferred_format: Optional[ContentFormat] = None
    difficulty_offset: float = 0.0  # -1.0 to 1.0
    scaffolding_preference: int = 3  # 1-5 scale
    pacing_preference: str = "standard"  # "accelerated", "standard", "extended"
    visual_preference: bool = True
    interactive_preference: bool = True


class MultiLevelService:
    """
    Service for managing multi-level educational content.
    
    Handles content adaptation, variant selection, and personalized
    learning experiences across different educational levels.
    """
    
    def __init__(self):
        self.content_variants: Dict[str, Dict[LevelType, ContentVariant]] = {}
        self.base_content: Dict[str, Dict[str, Any]] = {}
        self.adaptive_rules: List[AdaptiveRule] = []
        self.level_mappings: Dict[LevelType, Dict[str, Any]] = {}
        
        # Initialize default level configurations
        self._init_level_configurations()
    
    def _init_level_configurations(self):
        """Initialize default configurations for each educational level."""
        self.level_mappings = {
            LevelType.ELEMENTARY: {
                "min_age": 5,
                "max_age": 11,
                "reading_level": "K-5",
                "cognitive_stage": "concrete_operational",
                "typical_grade": "K-5",
                "attention_span_minutes": 15,
                "vocabulary_complexity": "basic",
                "abstraction_preference": "low",
                "scaffolding_needs": "high",
                "examples_needed": True,
                "multimedia_preference": "high",
                "assessment_style": "formative_short"
            },
            LevelType.MIDDLE_SCHOOL: {
                "min_age": 11,
                "max_age": 14,
                "reading_level": "6-8",
                "cognitive_stage": "formal_operational_emerging",
                "typical_grade": "6-8",
                "attention_span_minutes": 25,
                "vocabulary_complexity": "intermediate",
                "abstraction_preference": "medium",
                "scaffolding_needs": "medium",
                "examples_needed": True,
                "multimedia_preference": "medium",
                "assessment_style": "mixed"
            },
            LevelType.HIGH_SCHOOL: {
                "min_age": 14,
                "max_age": 18,
                "reading_level": "9-12",
                "cognitive_stage": "formal_operational",
                "typical_grade": "9-12",
                "attention_span_minutes": 45,
                "vocabulary_complexity": "academic",
                "abstraction_preference": "high",
                "scaffolding_needs": "low",
                "examples_needed": False,
                "multimedia_preference": "low",
                "assessment_style": "summative"
            },
            LevelType.UNDERGRADUATE: {
                "min_age": 18,
                "max_age": 22,
                "reading_level": "college",
                "cognitive_stage": "formal_operational_advanced",
                "typical_grade": "Freshman-Senior",
                "attention_span_minutes": 60,
                "vocabulary_complexity": "technical",
                "abstraction_preference": "high",
                "scaffolding_needs": "minimal",
                "examples_needed": False,
                "multimedia_preference": "low",
                "assessment_style": "research_project"
            },
            LevelType.GRADUATE: {
                "min_age": 22,
                "max_age": 100,
                "reading_level": "graduate",
                "cognitive_stage": "expert",
                "typical_grade": "Graduate",
                "attention_span_minutes": 90,
                "vocabulary_complexity": "research",
                "abstraction_preference": "expert",
                "scaffolding_needs": "none",
                "examples_needed": False,
                "multimedia_preference": "optional",
                "assessment_style": "dissertation"
            },
            LevelType.PROFESSIONAL: {
                "min_age": 21,
                "max_age": 100,
                "reading_level": "professional",
                "cognitive_stage": "practical_expert",
                "typical_grade": "Professional",
                "attention_span_minutes": 45,
                "vocabulary_complexity": "industry_specific",
                "abstraction_preference": "high",
                "scaffolding_needs": "low",
                "examples_needed": False,
                "multimedia_preference": "medium",
                "assessment_style": "performance_based"
            },
            LevelType.SELF_DIRECTED: {
                "min_age": 16,
                "max_age": 100,
                "reading_level": "flexible",
                "cognitive_stage": "self_directed",
                "typical_grade": "Personal",
                "attention_span_minutes": 30,
                "vocabulary_complexity": "adaptable",
                "abstraction_preference": "adaptable",
                "scaffolding_needs": "preference_based",
                "examples_needed": "preference_based",
                "multimedia_preference": "preference_based",
                "assessment_style": "self_reflection"
            }
        }
    
    def register_base_content(
        self,
        content_id: str,
        title: str,
        description: str,
        core_objectives: List[str],
        topics: List[str],
        default_duration: int = 30
    ):
        """Register base content that will have variants."""
        self.base_content[content_id] = {
            "content_id": content_id,
            "title": title,
            "description": description,
            "core_objectives": core_objectives,
            "topics": topics,
            "default_duration": default_duration,
            "created_at": datetime.now()
        }
        self.content_variants[content_id] = {}
    
    def create_variant(
        self,
        base_content_id: str,
        level_type: LevelType,
        title: str,
        description: str,
        content_body: str,
        difficulty_level: DifficultyLevel,
        format_type: ContentFormat,
        estimated_minutes: int,
        learning_objectives: List[str],
        prerequisites: Optional[List[str]] = None,
        vocabulary_level: int = 3,
        abstraction_level: int = 3,
        scaffolding_depth: int = 3
    ) -> ContentVariant:
        """Create a variant of content for a specific level."""
        if base_content_id not in self.base_content:
            raise ValueError(f"Base content {base_content_id} not found")
        
        variant_id = f"{base_content_id}_{level_type.value}"
        
        variant = ContentVariant(
            variant_id=variant_id,
            base_content_id=base_content_id,
            level_type=level_type,
            title=title,
            description=description,
            content_body=content_body,
            difficulty_level=difficulty_level,
            format_type=format_type,
            estimated_minutes=estimated_minutes,
            learning_objectives=learning_objectives,
            prerequisites=prerequisites or [],
            vocabulary_level=vocabulary_level,
            abstraction_level=abstraction_level,
            scaffolding_depth=scaffolding_depth
        )
        
        if base_content_id not in self.content_variants:
            self.content_variants[base_content_id] = {}
        
        self.content_variants[base_content_id][level_type] = variant
        return variant
    
    def generate_variant(
        self,
        base_content_id: str,
        target_level: LevelType,
        learner_profile: Optional[LearnerPreferences] = None
    ) -> Optional[ContentVariant]:
        """Generate or retrieve a variant for a specific level."""
        if base_content_id not in self.content_variants:
            return None
        
        variants = self.content_variants[base_content_id]
        
        # Check if variant exists
        if target_level in variants:
            return variants[target_level]
        
        # Generate new variant based on base content and level config
        base = self.base_content.get(base_content_id)
        if not base:
            return None
        
        level_config = self.level_mappings.get(target_level, {})
        
        # Generate adapted content (simplified version)
        difficulty = self._map_level_to_difficulty(target_level)
        
        variant = ContentVariant(
            variant_id=f"{base_content_id}_{target_level.value}",
            base_content_id=base_content_id,
            level_type=target_level,
            title=f"{base['title']} ({target_level.value.replace('_', ' ').title()})",
            description=base['description'],
            content_body=self._generate_adapted_content(
                base_content_id, target_level, level_config
            ),
            difficulty_level=difficulty,
            format_type=ContentFormat.INTERACTIVE,
            estimated_minutes=level_config.get("attention_span_minutes", 30),
            learning_objectives=base['core_objectives'],
            vocabulary_level=self._calculate_vocabulary_level(target_level),
            abstraction_level=self._calculate_abstraction_level(target_level),
            scaffolding_depth=self._calculate_scaffolding_level(target_level)
        )
        
        variants[target_level] = variant
        return variant
    
    def _map_level_to_difficulty(self, level: LevelType) -> DifficultyLevel:
        """Map educational level to difficulty level."""
        mapping = {
            LevelType.ELEMENTARY: DifficultyLevel.BEGINNER,
            LevelType.MIDDLE_SCHOOL: DifficultyLevel.ELEMENTARY,
            LevelType.HIGH_SCHOOL: DifficultyLevel.INTERMEDIATE,
            LevelType.UNDERGRADUATE: DifficultyLevel.ADVANCED,
            LevelType.GRADUATE: DifficultyLevel.EXPERT,
            LevelType.PROFESSIONAL: DifficultyLevel.ADVANCED,
            LevelType.SELF_DIRECTED: DifficultyLevel.INTERMEDIATE
        }
        return mapping.get(level, DifficultyLevel.INTERMEDIATE)
    
    def _calculate_vocabulary_level(self, level: LevelType) -> int:
        """Calculate vocabulary complexity level (1-5)."""
        mapping = {
            LevelType.ELEMENTARY: 1,
            LevelType.MIDDLE_SCHOOL: 2,
            LevelType.HIGH_SCHOOL: 3,
            LevelType.UNDERGRADUATE: 4,
            LevelType.GRADUATE: 5,
            LevelType.PROFESSIONAL: 4,
            LevelType.SELF_DIRECTED: 3
        }
        return mapping.get(level, 3)
    
    def _calculate_abstraction_level(self, level: LevelType) -> int:
        """Calculate abstraction/conceptual level (1-5)."""
        mapping = {
            LevelType.ELEMENTARY: 1,
            LevelType.MIDDLE_SCHOOL: 2,
            LevelType.HIGH_SCHOOL: 3,
            LevelType.UNDERGRADUATE: 4,
            LevelType.GRADUATE: 5,
            LevelType.PROFESSIONAL: 4,
            LevelType.SELF_DIRECTED: 3
        }
        return mapping.get(level, 3)
    
    def _calculate_scaffolding_level(self, level: LevelType) -> int:
        """Calculate required scaffolding depth (1-5)."""
        mapping = {
            LevelType.ELEMENTARY: 5,
            LevelType.MIDDLE_SCHOOL: 4,
            LevelType.HIGH_SCHOOL: 3,
            LevelType.UNDERGRADUATE: 2,
            LevelType.GRADUATE: 1,
            LevelType.PROFESSIONAL: 2,
            LevelType.SELF_DIRECTED: 3
        }
        return mapping.get(level, 3)
    
    def _generate_adapted_content(
        self,
        base_content_id: str,
        target_level: LevelType,
        level_config: Dict[str, Any]
    ) -> str:
        """Generate adapted content body for target level."""
        base = self.base_content.get(base_content_id)
        if not base:
            return ""
        
        # Simplified content adaptation logic
        needs_examples = level_config.get("examples_needed", True)
        abstraction = level_config.get("abstraction_preference", "medium")
        
        adapted_parts = []
        
        # Add appropriate introduction based on level
        if target_level == LevelType.ELEMENTARY:
            adapted_parts.append("Let's explore this topic together!")
        elif target_level == LevelType.MIDDLE_SCHOOL:
            adapted_parts.append("Today we're going to learn about:")
        else:
            adapted_parts.append("This module covers:")
        
        # Add core content with appropriate abstraction
        adapted_parts.append(f"## {base['title']}\n")
        
        for topic in base['topics']:
            if abstraction == "low":
                adapted_parts.append(f"- We know that {topic} is important because...")
            elif abstraction == "medium":
                adapted_parts.append(f"- {topic}: Understanding its role and significance")
            else:
                adapted_parts.append(f"- {topic}: Theoretical frameworks and applications")
        
        # Add examples if needed
        if needs_examples:
            adapted_parts.append("\n### Real-World Examples:")
            adapted_parts.append("- Example 1: [Relevant case study]")
            adapted_parts.append("- Example 2: [Practical application]")
        
        # Add reflection for higher levels
        if abstraction in ["high", "expert"]:
            adapted_parts.append("\n### Critical Thinking:")
            adapted_parts.append("- How does this connect to other concepts?")
            adapted_parts.append("- What are the implications for practice?")
        
        return "\n".join(adapted_parts)
    
    def select_optimal_variant(
        self,
        base_content_id: str,
        learner_preferences: LearnerPreferences,
        current_performance: Optional[Dict[str, float]] = None
    ) -> Optional[ContentVariant]:
        """Select the optimal content variant for a learner."""
        if base_content_id not in self.content_variants:
            return None
        
        variants = self.content_variants[base_content_id]
        
        if not variants:
            return None
        
        # Primary: Check preferred level
        preferred_level = learner_preferences.preferred_level
        if preferred_level in variants:
            return variants[preferred_level]
        
        # Secondary: Find closest level
        closest_level = self._find_closest_level(
            preferred_level, list(variants.keys())
        )
        if closest_level and closest_level in variants:
            return variants[closest_level]
        
        # Fallback: Return first available variant
        return list(variants.values())[0]
    
    def _find_closest_level(
        self,
        target: LevelType,
        available: List[LevelType]
    ) -> Optional[LevelType]:
        """Find the closest matching level from available options."""
        if not available:
            return None
        
        # Define level progression order
        level_order = [
            LevelType.ELEMENTARY,
            LevelType.MIDDLE_SCHOOL,
            LevelType.HIGH_SCHOOL,
            LevelType.UNDERGRADUATE,
            LevelType.GRADUATE
        ]
        
        target_index = level_order.index(target) if target in level_order else -1
        
        if target_index == -1:
            # Handle special cases
            if target == LevelType.PROFESSIONAL:
                return LevelType.UNDERGRADUATE if LevelType.UNDERGRADUATE in available else None
            if target == LevelType.SELF_DIRECTED:
                return LevelType.HIGH_SCHOOL if LevelType.HIGH_SCHOOL in available else None
        
        # Find closest index in available levels
        closest = None
        min_distance = float('inf')
        
        for level in available:
            if level in level_order:
                index = level_order.index(level)
                distance = abs(index - target_index)
                if distance < min_distance:
                    min_distance = distance
                    closest = level
        
        return closest
    
    def get_level_configuration(self, level: LevelType) -> Dict[str, Any]:
        """Get the configuration for an educational level."""
        return self.level_mappings.get(level, {})
    
    def add_adaptive_rule(self, rule: AdaptiveRule):
        """Add a rule for adaptive content selection."""
        self.adaptive_rules.append(rule)
        self.adaptive_rules.sort(key=lambda x: x.priority, reverse=True)
    
    def apply_adaptive_rules(
        self,
        base_content_id: str,
        learner_preferences: LearnerPreferences,
        performance_data: Dict[str, float]
    ) -> LevelType:
        """Apply adaptive rules to determine optimal level."""
        current_level = learner_preferences.preferred_level
        
        for rule in self.adaptive_rules:
            if not rule.is_active:
                continue
            
            if self._check_rule_condition(rule.condition, learner_preferences, performance_data):
                action = rule.action
                if "level_adjustment" in action:
                    adjustment = action["level_adjustment"]
                    current_level = self._apply_level_adjustment(current_level, adjustment)
        
        return current_level
    
    def _check_rule_condition(
        self,
        condition: Dict[str, Any],
        preferences: LearnerPreferences,
        performance: Dict[str, float]
    ) -> bool:
        """Check if a rule condition is met."""
        # Simplified condition checking
        if "min_score_below" in condition:
            if performance.get("average_score", 100) >= condition["min_score_below"]:
                return False
        
        if "max_score_above" in condition:
            if performance.get("average_score", 0) <= condition["max_score_above"]:
                return False
        
        return True
    
    def _apply_level_adjustment(
        self,
        current: LevelType,
        adjustment: str
    ) -> LevelType:
        """Apply level adjustment based on rule action."""
        level_order = [
            LevelType.ELEMENTARY,
            LevelType.MIDDLE_SCHOOL,
            LevelType.HIGH_SCHOOL,
            LevelType.UNDERGRADUATE,
            LevelType.GRADUATE
        ]
        
        try:
            current_index = level_order.index(current)
        except ValueError:
            return current
        
        if adjustment == "step_up" and current_index < len(level_order) - 1:
            return level_order[current_index + 1]
        elif adjustment == "step_down" and current_index > 0:
            return level_order[current_index - 1]
        elif adjustment == "keep":
            return current
        
        return current
    
    def get_available_levels(self, base_content_id: str) -> List[LevelType]:
        """Get all available levels for content."""
        if base_content_id in self.content_variants:
            return list(self.content_variants[base_content_id].keys())
        return []
    
    def get_variant(
        self,
        base_content_id: str,
        level: LevelType
    ) -> Optional[ContentVariant]:
        """Get a specific content variant."""
        if base_content_id in self.content_variants:
            return self.content_variants[base_content_id].get(level)
        return None


# Service factory function
def create_multi_level_service() -> MultiLevelService:
    """Create and configure a new multi-level service instance."""
    return MultiLevelService()
