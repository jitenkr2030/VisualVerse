"""
Curriculum Management Service for Learner Experience Platform.

Provides curriculum structure management, alignment with learning standards,
and progress tracking across educational pathways.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import defaultdict


class CurriculumType(Enum):
    """Types of curriculum structures."""
    STANDARD = "standard"  # Traditional academic curriculum
    CUSTOM = "custom"  # Institution-specific curriculum
   Competency = "competency"  # Competency-based curriculum
    PROJECT_BASED = "project_based"  # Project-centered learning
    SELF_PACED = "self_paced"  # Self-directed learning path


class StandardType(Enum):
    """Types of educational standards."""
    COMMON_CORE = "common_core"
    NGSS = "ngss"  # Next Generation Science Standards
    STATE_SPECIFIC = "state_specific"
    INTERNATIONAL = "international"
    INDUSTRY_CERTIFICATION = "industry_certification"
    CUSTOM = "custom"


@dataclass
class LearningStandard:
    """A learning standard or competency requirement."""
    standard_id: str
    code: str
    description: str
    standard_type: StandardType
    grade_level: str
    subject: str
    benchmarks: List[str]
    assessment_methods: List[str]
    prerequisites: List[str] = field(default_factory=list)
    related_standards: List[str] = field(default_factory=list)
    depth_of_knowledge: int = 1  # 1-4 scale


@dataclass
class CurriculumModule:
    """A module within a curriculum."""
    module_id: str
    curriculum_id: str
    title: str
    description: str
    learning_objectives: List[str]
    standards_covered: List[str]
    content_ids: List[str]
    assessment_ids: List[str]
    duration_hours: float
    order_index: int
    is_required: bool = True
    prerequisites: List[str] = field(default_factory=list)
    competencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CurriculumUnit:
    """A unit grouping related modules."""
    unit_id: str
    curriculum_id: str
    title: str
    description: str
    module_ids: List[str]
    duration_weeks: float
    order_index: int
    standards_focus: List[str]
    assessments: List[str] = field(default_factory=list)
    milestones: List[str] = field(default_factory=list)


@dataclass
class Curriculum:
    """A complete curriculum structure."""
    curriculum_id: str
    title: str
    description: str
    curriculum_type: CurriculumType
    target_level: str
    subject_area: str
    total_duration_hours: float
    modules: Dict[str, CurriculumModule]
    units: Dict[str, CurriculumUnit]
    standards_covered: List[str]
    prerequisites: List[str]
    certification_outcomes: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0"


@dataclass
class LearnerCurriculumProgress:
    """Track learner progress through a curriculum."""
    learner_id: str
    curriculum_id: str
    enrolled_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str = "enrolled"  # enrolled, in_progress, completed, paused
    module_progress: Dict[str, float] = field(default_factory=dict)  # module_id -> percentage
    unit_progress: Dict[str, float] = field(default_factory=dict)
    current_module: Optional[str] = None
    current_unit: Optional[str] = None
    total_time_spent: int = 0  # seconds
    assessment_scores: Dict[str, float] = field(default_factory=dict)
    competency_mastery: Dict[str, float] = field(default_factory=dict)
    milestones_achieved: List[str] = field(default_factory=list)
    overall_progress: float = 0.0


class CurriculumService:
    """
    Service for managing curriculum structures and learner pathways.
    
    Handles curriculum creation, standard alignment, progress tracking,
    and competency-based progression through learning paths.
    """
    
    def __init__(self):
        self.curricula: Dict[str, Curriculum] = {}
        self.standards: Dict[str, LearningStandard] = {}
        self.learner_progress: Dict[str, Dict[str, LearnerCurriculumProgress]] = defaultdict(dict)
        self.curriculum_enrollments: Dict[str, List[str]] = defaultdict(list)
    
    # Standard Management
    def register_standard(
        self,
        standard_id: str,
        code: str,
        description: str,
        standard_type: StandardType,
        grade_level: str,
        subject: str,
        benchmarks: List[str],
        assessment_methods: List[str],
        prerequisites: Optional[List[str]] = None,
        related_standards: Optional[List[str]] = None,
        depth_of_knowledge: int = 1
    ) -> LearningStandard:
        """Register a learning standard."""
        standard = LearningStandard(
            standard_id=standard_id,
            code=code,
            description=description,
            standard_type=standard_type,
            grade_level=grade_level,
            subject=subject,
            benchmarks=benchmarks,
            assessment_methods=assessment_methods,
            prerequisites=prerequisites or [],
            related_standards=related_standards or [],
            depth_of_knowledge=depth_of_knowledge
        )
        
        self.standards[standard_id] = standard
        return standard
    
    def get_standard(self, standard_id: str) -> Optional[LearningStandard]:
        """Retrieve a learning standard."""
        return self.standards.get(standard_id)
    
    def get_standards_by_subject(
        self,
        subject: str,
        grade_level: Optional[str] = None
    ) -> List[LearningStandard]:
        """Get standards by subject area."""
        standards = [
            s for s in self.standards.values()
            if s.subject.lower() == subject.lower()
        ]
        
        if grade_level:
            standards = [
                s for s in standards
                if grade_level in s.grade_level
            ]
        
        return standards
    
    def get_standards_by_type(
        self,
        standard_type: StandardType
    ) -> List[LearningStandard]:
        """Get standards by type."""
        return [
            s for s in self.standards.values()
            if s.standard_type == standard_type
        ]
    
    # Curriculum Management
    def create_curriculum(
        self,
        curriculum_id: str,
        title: str,
        description: str,
        curriculum_type: CurriculumType,
        target_level: str,
        subject_area: str,
        total_duration_hours: float,
        prerequisites: Optional[List[str]] = None,
        certification_outcomes: Optional[List[str]] = None
    ) -> Curriculum:
        """Create a new curriculum structure."""
        curriculum = Curriculum(
            curriculum_id=curriculum_id,
            title=title,
            description=description,
            curriculum_type=curriculum_type,
            target_level=target_level,
            subject_area=subject_area,
            total_duration_hours=total_duration_hours,
            modules={},
            units={},
            standards_covered=[],
            prerequisites=prerequisites or [],
            certification_outcomes=certification_outcomes or []
        )
        
        self.curricula[curriculum_id] = curriculum
        return curriculum
    
    def add_module(
        self,
        curriculum_id: str,
        module_id: str,
        title: str,
        description: str,
        learning_objectives: List[str],
        standards_covered: List[str],
        content_ids: List[str],
        assessment_ids: List[str],
        duration_hours: float,
        order_index: int,
        is_required: bool = True,
        prerequisites: Optional[List[str]] = None,
        competencies: Optional[List[str]] = None
    ) -> CurriculumModule:
        """Add a module to a curriculum."""
        if curriculum_id not in self.curricula:
            raise ValueError(f"Curriculum {curriculum_id} not found")
        
        module = CurriculumModule(
            module_id=module_id,
            curriculum_id=curriculum_id,
            title=title,
            description=description,
            learning_objectives=learning_objectives,
            standards_covered=standards_covered,
            content_ids=content_ids,
            assessment_ids=assessment_ids,
            duration_hours=duration_hours,
            order_index=order_index,
            is_required=is_required,
            prerequisites=prerequisites or [],
            competencies=competencies or []
        )
        
        self.curricula[curriculum_id].modules[module_id] = module
        
        # Update curriculum standards
        for standard_id in standards_covered:
            if standard_id not in self.curricula[curriculum_id].standards_covered:
                self.curricula[curriculum_id].standards_covered.append(standard_id)
        
        return module
    
    def add_unit(
        self,
        curriculum_id: str,
        unit_id: str,
        title: str,
        description: str,
        module_ids: List[str],
        duration_weeks: float,
        order_index: int,
        standards_focus: List[str],
        assessments: Optional[List[str]] = None,
        milestones: Optional[List[str]] = None
    ) -> CurriculumUnit:
        """Add a unit to a curriculum."""
        if curriculum_id not in self.curricula:
            raise ValueError(f"Curriculum {curriculum_id} not found")
        
        unit = CurriculumUnit(
            unit_id=unit_id,
            curriculum_id=curriculum_id,
            title=title,
            description=description,
            module_ids=module_ids,
            duration_weeks=duration_weeks,
            order_index=order_index,
            standards_focus=standards_focus,
            assessments=assessments or [],
            milestones=milestones or []
        )
        
        self.curricula[curriculum_id].units[unit_id] = unit
        return unit
    
    def get_curriculum(self, curriculum_id: str) -> Optional[Curriculum]:
        """Retrieve a curriculum by ID."""
        return self.curricula.get(curriculum_id)
    
    def get_curricula_by_subject(
        self,
        subject_area: str
    ) -> List[Curriculum]:
        """Get curricula by subject area."""
        return [
            c for c in self.curricula.values()
            if c.subject_area.lower() == subject_area.lower()
        ]
    
    def get_curricula_by_type(
        self,
        curriculum_type: CurriculumType
    ) -> List[Curriculum]:
        """Get curricula by type."""
        return [
            c for c in self.curricula.values()
            if c.curriculum_type == curriculum_type
        ]
    
    # Enrollment and Progress
    def enroll_learner(
        self,
        learner_id: str,
        curriculum_id: str
    ) -> LearnerCurriculumProgress:
        """Enroll a learner in a curriculum."""
        if curriculum_id not in self.curricula:
            raise ValueError(f"Curriculum {curriculum_id} not found")
        
        progress = LearnerCurriculumProgress(
            learner_id=learner_id,
            curriculum_id=curriculum_id,
            enrolled_at=datetime.now()
        )
        
        self.learner_progress[learner_id][curriculum_id] = progress
        self.curriculum_enrollments[curriculum_id].append(learner_id)
        
        return progress
    
    def start_curriculum(
        self,
        learner_id: str,
        curriculum_id: str
    ) -> Optional[LearnerCurriculumProgress]:
        """Mark curriculum as started and set first module."""
        progress = self.learner_progress[learner_id].get(curriculum_id)
        
        if not progress:
            return None
        
        if not progress.started_at:
            progress.started_at = datetime.now()
            progress.status = "in_progress"
            
            # Set first module as current
            curriculum = self.curricula[curriculum_id]
            if curriculum.modules:
                first_module = min(
                    curriculum.modules.values(),
                    key=lambda m: m.order_index
                )
                progress.current_module = first_module.module_id
                
                # Set containing unit
                for unit in curriculum.units.values():
                    if first_module.module_id in unit.module_ids:
                        progress.current_unit = unit.unit_id
                        break
        
        return progress
    
    def update_module_progress(
        self,
        learner_id: str,
        curriculum_id: str,
        module_id: str,
        progress_percentage: float,
        time_spent_seconds: int = 0,
        assessment_scores: Optional[Dict[str, float]] = None
    ) -> Optional[LearnerCurriculumProgress]:
        """Update progress for a specific module."""
        progress = self.learner_progress[learner_id].get(curriculum_id)
        
        if not progress:
            return None
        
        # Update module progress
        progress.module_progress[module_id] = progress_percentage
        progress.total_time_spent += time_spent_seconds
        
        # Update assessment scores
        if assessment_scores:
            progress.assessment_scores.update(assessment_scores)
        
        # Update overall progress
        curriculum = self.curricula.get(curriculum_id)
        if curriculum:
            progress.overall_progress = self._calculate_overall_progress(
                progress, curriculum
            )
            
            # Check if module completed
            if progress_percentage >= 100:
                self._mark_module_completed(
                    learner_id, curriculum_id, module_id, progress, curriculum
                )
        
        return progress
    
    def _calculate_overall_progress(
        self,
        progress: LearnerCurriculumProgress,
        curriculum: Curriculum
    ) -> float:
        """Calculate overall curriculum progress."""
        if not curriculum.modules:
            return 0.0
        
        required_modules = [
            m for m in curriculum.modules.values()
            if m.is_required
        ]
        
        if not required_modules:
            return 0.0
        
        total_progress = 0.0
        for module in required_modules:
            module_progress = progress.module_progress.get(module.module_id, 0.0)
            total_progress += module_progress
        
        return total_progress / len(required_modules)
    
    def _mark_module_completed(
        self,
        learner_id: str,
        curriculum_id: str,
        module_id: str,
        progress: LearnerCurriculumProgress,
        curriculum: Curriculum
    ):
        """Handle module completion and advance to next."""
        module = curriculum.modules.get(module_id)
        if not module:
            return
        
        # Update competency mastery
        for competency in module.competencies:
            current = progress.competency_mastery.get(competency, 0.0)
            progress.competency_mastery[competency] = min(100.0, current + 25.0)
        
        # Find next module
        next_module = None
        sorted_modules = sorted(
            curriculum.modules.values(),
            key=lambda m: m.order_index
        )
        
        found_current = False
        for m in sorted_modules:
            if found_current and m.is_required:
                # Check prerequisites
                prereqs_met = all(
                    progress.module_progress.get(p, 0) >= 100
                    for p in m.prerequisites
                )
                if prereqs_met or not m.prerequisites:
                    next_module = m
                    break
            if m.module_id == module_id:
                found_current = True
        
        if next_module:
            progress.current_module = next_module.module_id
            # Update current unit
            for unit in curriculum.units.values():
                if next_module.module_id in unit.module_ids:
                    progress.current_unit = unit.unit_id
                    break
        else:
            # Curriculum may be complete
            if progress.overall_progress >= 100:
                progress.status = "completed"
                progress.completed_at = datetime.now()
    
    def get_learner_curriculum_progress(
        self,
        learner_id: str,
        curriculum_id: str
    ) -> Optional[LearnerCurriculumProgress]:
        """Get learner progress for a specific curriculum."""
        return self.learner_progress[learner_id].get(curriculum_id)
    
    def get_all_learner_progress(
        self,
        learner_id: str
    ) -> Dict[str, LearnerCurriculumProgress]:
        """Get all curriculum progress for a learner."""
        return self.learner_progress.get(learner_id, {})
    
    def get_curriculum_completion_rate(
        self,
        curriculum_id: str
    ) -> float:
        """Calculate completion rate for a curriculum."""
        enrolled = self.curriculum_enrollments.get(curriculum_id, [])
        
        if not enrolled:
            return 0.0
        
        completed = 0
        for learner_id in enrolled:
            progress = self.learner_progress[learner_id].get(curriculum_id)
            if progress and progress.status == "completed":
                completed += 1
        
        return completed / len(enrolled) * 100
    
    # Alignment and Analysis
    def get_curriculum_standards(
        self,
        curriculum_id: str
    ) -> List[LearningStandard]:
        """Get all standards covered by a curriculum."""
        curriculum = self.curricula.get(curriculum_id)
        if not curriculum:
            return []
        
        return [
            self.standards.get(sid)
            for sid in curriculum.standards_covered
            if sid in self.standards
        ]
    
    def analyze_standards_coverage(
        self,
        curriculum_id: str
    ) -> Dict[str, Any]:
        """Analyze standards coverage in a curriculum."""
        curriculum = self.curricula.get(curriculum_id)
        if not curriculum:
            return {}
        
        standards = self.get_curriculum_standards(curriculum_id)
        
        # Group by type
        by_type: Dict[StandardType, List[LearningStandard]] = defaultdict(list)
        for standard in standards:
            by_type[standard.standard_type].append(standard)
        
        # Group by subject
        by_subject: Dict[str, List[LearningStandard]] = defaultdict(list)
        for standard in standards:
            by_subject[standard.subject].append(standard)
        
        # Calculate depth of knowledge distribution
        dok_distribution = {1: 0, 2: 0, 3: 0, 4: 0}
        for standard in standards:
            dok_distribution[standard.depth_of_knowledge] += 1
        
        return {
            "total_standards": len(standards),
            "standards_by_type": {
                st.value: len(s_list) for st, s_list in by_type.items()
            },
            "standards_by_subject": {
                subj: len(s_list) for subj, s_list in by_subject.items()
            },
            "depth_of_knowledge_distribution": dok_distribution,
            "standards_list": [
                {"id": s.standard_id, "code": s.code, "description": s.description}
                for s in standards
            ]
        }
    
    def get_competency_progress(
        self,
        learner_id: str,
        curriculum_id: str
    ) -> Dict[str, float]:
        """Get competency mastery progress for a learner."""
        progress = self.learner_progress[learner_id].get(curriculum_id)
        if not progress:
            return {}
        
        return progress.competency_mastery
    
    def check_prerequisites(
        self,
        learner_id: str,
        curriculum_id: str,
        target_module_id: str
    ) -> Dict[str, Any]:
        """Check if learner has met prerequisites for a module."""
        curriculum = self.curricula.get(curriculum_id)
        if not curriculum:
            return {"met": False, "reason": "Curriculum not found"}
        
        module = curriculum.modules.get(target_module_id)
        if not module:
            return {"met": False, "reason": "Module not found"}
        
        progress = self.learner_progress[learner_id].get(curriculum_id)
        if not progress:
            return {"met": False, "reason": "Learner not enrolled"}
        
        unmet = []
        for prereq_id in module.prerequisites:
            prereq_progress = progress.module_progress.get(prereq_id, 0)
            if prereq_progress < 100:
                prereq_module = curriculum.modules.get(prereq_id)
                unmet.append({
                    "module_id": prereq_id,
                    "title": prereq_module.title if prereq_module else "Unknown",
                    "progress": prereq_progress
                })
        
        return {
            "met": len(unmet) == 0,
            "unmet_prerequisites": unmet
        }
    
    def get_learning_path(
        self,
        learner_id: str,
        curriculum_id: str
    ) -> List[Dict[str, Any]]:
        """Get the recommended learning path for a learner."""
        curriculum = self.curricula.get(curriculum_id)
        if not curriculum:
            return []
        
        progress = self.learner_progress[learner_id].get(curriculum_id)
        if not progress:
            return []
        
        path = []
        sorted_modules = sorted(
            curriculum.modules.values(),
            key=lambda m: m.order_index
        )
        
        for module in sorted_modules:
            if not module.is_required:
                continue
            
            module_progress = progress.module_progress.get(module.module_id, 0)
            
            path.append({
                "module_id": module.module_id,
                "title": module.title,
                "status": (
                    "completed" if module_progress >= 100 else
                    "in_progress" if module_progress > 0 else
                    "locked" if progress.module_progress.get(module.module_id, -1) == -1 else
                    "available"
                ),
                "progress": module_progress,
                "duration_hours": module.duration_hours,
                "is_current": module.module_id == progress.current_module
            })
        
        return path
    
    def generate_curriculum_report(
        self,
        learner_id: str,
        curriculum_id: str
    ) -> Dict[str, Any]:
        """Generate a comprehensive progress report for a learner."""
        progress = self.learner_progress[learner_id].get(curriculum_id)
        curriculum = self.curricula.get(curriculum_id)
        
        if not progress or not curriculum:
            return {}
        
        # Calculate statistics
        completed_modules = [
            m for m in curriculum.modules.values()
            if progress.module_progress.get(m.module_id, 0) >= 100
        ]
        
        in_progress_modules = [
            m for m in curriculum.modules.values()
            if 0 < progress.module_progress.get(m.module_id, 0) < 100
        ]
        
        assessment_avg = 0.0
        if progress.assessment_scores:
            assessment_avg = sum(progress.assessment_scores.values()) / len(progress.assessment_scores)
        
        return {
            "learner_id": learner_id,
            "curriculum": {
                "id": curriculum_id,
                "title": curriculum.title,
                "type": curriculum.curriculum_type.value,
                "subject": curriculum.subject_area
            },
            "enrollment": {
                "enrolled_at": progress.enrolled_at.isoformat(),
                "started_at": progress.started_at.isoformat() if progress.started_at else None,
                "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
                "status": progress.status
            },
            "progress_summary": {
                "overall_progress": progress.overall_progress,
                "total_time_spent_hours": progress.total_time_spent / 3600,
                "completed_modules": len(completed_modules),
                "total_modules": len([m for m in curriculum.modules.values() if m.is_required]),
                "in_progress_modules": len(in_progress_modules)
            },
            "assessment_performance": {
                "average_score": assessment_avg,
                "scores": progress.assessment_scores
            },
            "competency_mastery": progress.competency_mastery,
            "milestones_achieved": len(progress.milestones_achieved),
            "learning_path": self.get_learning_path(learner_id, curriculum_id)
        }


# Service factory function
def create_curriculum_service() -> CurriculumService:
    """Create and configure a new curriculum service instance."""
    return CurriculumService()
