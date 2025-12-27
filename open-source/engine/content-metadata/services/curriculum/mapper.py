"""
Curriculum Mapper Service for VisualVerse Content Metadata Layer

This module provides functionality for importing curriculum standards from
common frameworks (Common Core, NGSS, etc.), mapping concepts to standardized
benchmarks, and validating curriculum coverage.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import json
import re
from collections import defaultdict

from ..models.curriculum import (
    CurriculumFramework,
    StandardBenchmark,
    SyllabusUnit,
    LearningOutcome,
    Curriculum,
    CurriculumFrameworkType,
    DifficultyScale,
    AssessmentType,
    GradeLevel
)


logger = logging.getLogger(__name__)


class MappingConfidence(Enum):
    """Confidence levels for concept-standard mappings"""
    HIGH = "high"      # Direct match
    MEDIUM = "medium"  # Partial match with some interpretation
    LOW = "low"        # Weak match, requires review
    NONE = "none"      # No match found


@dataclass
class ConceptMapping:
    """Represents a mapping between a concept and a standard"""
    concept_id: str
    concept_name: str
    standard_id: str
    standard_code: str
    confidence: MappingConfidence
    match_evidence: List[str] = field(default_factory=list)
    rationale: str = ""
    is_reviewed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'concept_id': self.concept_id,
            'concept_name': self.concept_name,
            'standard_id': self.standard_id,
            'standard_code': self.standard_code,
            'confidence': self.confidence.value,
            'match_evidence': self.match_evidence,
            'rationale': self.rationale,
            'is_reviewed': self.is_reviewed,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class MappingSuggestion:
    """Represents a suggested mapping for review"""
    concept_id: str
    concept_name: str
    concept_description: str
    suggested_standard_ids: List[str]
    suggested_standard_codes: List[str]
    match_reasons: List[str] = field(default_factory=list)
    requires_review: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'concept_id': self.concept_id,
            'concept_name': self.concept_name,
            'concept_description': self.concept_description,
            'suggested_standard_ids': self.suggested_standard_ids,
            'suggested_standard_codes': self.suggested_standard_codes,
            'match_reasons': self.match_reasons,
            'requires_review': self.requires_review
        }


@dataclass
class CoverageReport:
    """Report on curriculum coverage"""
    framework_id: str
    framework_name: str
    total_standards: int
    covered_standards: int
    uncovered_standards: List[Dict[str, Any]]
    coverage_percentage: float
    concept_coverage: Dict[str, int]
    recommendations: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'framework_id': self.framework_id,
            'framework_name': self.framework_name,
            'total_standards': self.total_standards,
            'covered_standards': self.covered_standards,
            'uncovered_standards': self.uncovered_standards,
            'coverage_percentage': self.coverage_percentage,
            'concept_coverage': self.concept_coverage,
            'recommendations': self.recommendations,
            'generated_at': self.generated_at.isoformat()
        }


class CurriculumMapper:
    """
    Service for mapping concepts to curriculum standards.
    
    This mapper supports importing standards from various frameworks,
    automatically suggesting mappings based on concept content, and
    validating curriculum coverage.
    """
    
    # Keyword mappings for common frameworks
    FRAMEWORK_KEYWORDS = {
        'CCSS': {
            'mathematics': [
                'expression', 'equation', 'function', 'number', 'operation',
                'algebra', 'geometry', 'statistics', 'probability', 'ratio',
                'fraction', 'decimal', 'integer', 'polynomial', 'matrix',
                'derivative', 'integral', 'sequence', 'series', 'vector'
            ],
            'ela': [
                'reading', 'writing', 'speaking', 'listening', 'language',
                'literature', 'rhetoric', 'argument', 'narrative', 'informational'
            ]
        },
        'NGSS': {
            'physics': [
                'motion', 'force', 'energy', 'wave', 'electricity',
                'magnetism', 'thermodynamics', 'quantum', 'relativity'
            ],
            'chemistry': [
                'matter', 'reaction', 'bond', 'solution', 'acid', 'base',
                'stoichiometry', 'equilibrium', 'kinetics', 'thermodynamics'
            ],
            'biology': [
                'cell', 'genetics', 'evolution', 'ecosystem', 'organism',
                'metabolism', 'homeostasis', 'reproduction', 'inheritance'
            ]
        },
        'IB': {
            'mathematics': [
                'mathematical', 'problem', 'reasoning', 'investigation',
                'application', 'technology', 'modelling', 'pattern'
            ],
            'sciences': [
                'scientific', 'inquiry', 'hypothesis', 'experiment',
                'analysis', 'conclusion', 'theory', 'practical'
            ]
        }
    }
    
    def __init__(self):
        """Initialize the curriculum mapper"""
        self._frameworks: Dict[str, CurriculumFramework] = {}
        self._benchmarks: Dict[str, StandardBenchmark] = {}
        self._mappings: Dict[str, List[ConceptMapping]] = defaultdict(list)
        self._concept_keywords: Dict[str, Set[str]] = defaultdict(set)
    
    # =========================================================================
    # Framework and Standard Management
    # =========================================================================
    
    def add_framework(self, framework: CurriculumFramework) -> str:
        """
        Add a curriculum framework.
        
        Args:
            framework: The framework to add
            
        Returns:
            The framework ID
        """
        self._frameworks[framework.id] = framework
        logger.info(f"Added framework: {framework.name} ({framework.code})")
        return framework.id
    
    def add_benchmark(self, benchmark: StandardBenchmark) -> str:
        """
        Add a standard benchmark.
        
        Args:
            benchmark: The benchmark to add
            
        Returns:
            The benchmark ID
        """
        self._benchmarks[benchmark.id] = benchmark
        logger.info(f"Added benchmark: {benchmark.code}")
        return benchmark.id
    
    def add_benchmarks_batch(self, benchmarks: List[StandardBenchmark]) -> int:
        """
        Add multiple benchmarks in batch.
        
        Args:
            benchmarks: List of benchmarks to add
            
        Returns:
            Number of benchmarks added
        """
        for benchmark in benchmarks:
            self.add_benchmark(benchmark)
        return len(benchmarks)
    
    def get_framework(self, framework_id: str) -> Optional[CurriculumFramework]:
        """Get a framework by ID"""
        return self._frameworks.get(framework_id)
    
    def get_benchmark(self, benchmark_id: str) -> Optional[StandardBenchmark]:
        """Get a benchmark by ID"""
        return self._benchmarks.get(benchmark_id)
    
    def get_benchmarks_by_framework(self, framework_id: str) -> List[StandardBenchmark]:
        """Get all benchmarks for a framework"""
        return [
            b for b in self._benchmarks.values()
            if b.framework_id == framework_id
        ]
    
    # =========================================================================
    # Standard Import
    # =========================================================================
    
    def import_common_core_math(self) -> Tuple[str, int]:
        """
        Import Common Core State Standards for Mathematics.
        
        Creates the framework and key standards. In production, this would
        parse the actual CCSS documents.
        
        Returns:
            Tuple of (framework_id, standards_count)
        """
        framework = CurriculumFramework(
            id="ccss-math",
            name="Common Core State Standards - Mathematics",
            code="CCSS",
            framework_type=CurriculumFrameworkType.NATIONAL,
            version="2023",
            region="United States",
            description="A set of high-quality academic standards in mathematics that outline what a student should know and be able to do at the end of each grade level.",
            subject_scope=["mathematics"],
            grade_range=("K", "12"),
            publisher="National Governors Association"
        )
        self.add_framework(framework)
        
        # Add key standards (simplified - would include hundreds in production)
        standards = self._generate_common_core_math_standards()
        count = self.add_benchmarks_batch(standards)
        
        return framework.id, count
    
    def import_ngss(self) -> Tuple[str, int]:
        """
        Import Next Generation Science Standards.
        
        Returns:
            Tuple of (framework_id, standards_count)
        """
        framework = CurriculumFramework(
            id="ngss",
            name="Next Generation Science Standards",
            code="NGSS",
            framework_type=CurriculumFrameworkType.NATIONAL,
            version="2013",
            region="United States",
            description="K-12 science content standards that set the expectations for what students should know and be able to do.",
            subject_scope=["physics", "chemistry", "biology", "earth_science"],
            grade_range=("K", "12"),
            publisher="NGSS Lead States"
        )
        self.add_framework(framework)
        
        standards = self._generate_ngss_standards()
        count = self.add_benchmarks_batch(standards)
        
        return framework.id, count
    
    def import_from_file(self, file_path: str) -> Tuple[str, int]:
        """
        Import standards from a JSON or YAML file.
        
        Args:
            file_path: Path to the standards file
            
        Returns:
            Tuple of (framework_id, standards_count)
        """
        import json
        import yaml
        
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        
        # Create framework
        framework_data = data.get('framework', data)
        framework = CurriculumFramework(
            id=framework_data.get('id', f"custom-{datetime.now().timestamp()}"),
            name=framework_data.get('name', 'Custom Framework'),
            code=framework_data.get('code', 'CUSTOM'),
            framework_type=CurriculumFrameworkType(framework_data.get('framework_type', 'custom')),
            version=framework_data.get('version', '1.0'),
            region=framework_data.get('region'),
            description=framework_data.get('description'),
            subject_scope=framework_data.get('subject_scope', []),
            grade_range=tuple(framework_data.get('grade_range', ['K', '12']))
        )
        self.add_framework(framework)
        
        # Add standards
        standards_data = data.get('standards', data.get('benchmarks', []))
        standards = []
        
        for item in standards_data:
            grade_levels = item.get('grade_levels', [])
            if isinstance(grade_levels, str):
                grade_levels = [grade_levels]
            
            standard = StandardBenchmark(
                framework_id=framework.id,
                code=item.get('code', ''),
                category=item.get('category', ''),
                subcategory=item.get('subcategory'),
                description=item.get('description', ''),
                difficulty=DifficultyScale(item.get('difficulty', 'developing')),
                grade_levels=[GradeLevel(g) for g in grade_levels],
                suggested_instructional_hours=item.get('suggested_instructional_hours'),
                assessment_methods=[
                    AssessmentType(a) for a in item.get('assessment_methods', [])
                ]
            )
            standards.append(standard)
        
        count = self.add_benchmarks_batch(standards)
        
        return framework.id, count
    
    def _generate_common_core_math_standards(self) -> List[StandardBenchmark]:
        """Generate sample Common Core Math standards"""
        standards = []
        
        # Counting and Cardinality (K)
        standards.append(StandardBenchmark(
            framework_id="ccss-math",
            code="CCSS.MATH.CONTENT.K.CC.A.1",
            category="Counting and Cardinality",
            subcategory="Know number names and the count sequence",
            description="Count to 100 by ones and by tens.",
            difficulty=DifficultyScale.FOUNDATIONAL,
            grade_levels=[GradeLevel.K],
            suggested_instructional_hours=5.0,
            assessment_methods=[AssessmentType.FORMATIVE]
        ))
        
        # Operations and Algebraic Thinking (Grade 1)
        standards.append(StandardBenchmark(
            framework_id="ccss-math",
            code="CCSS.MATH.CONTENT.1.OA.A.1",
            category="Operations and Algebraic Thinking",
            subcategory="Represent and solve problems involving addition and subtraction",
            description="Use addition and subtraction within 20 to solve word problems involving situations of adding to, taking from, putting together, taking apart, and comparing, with unknowns in all positions.",
            difficulty=DifficultyScale.DEVELOPING,
            grade_levels=[GradeLevel.GRADE_1],
            suggested_instructional_hours=10.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.SUMMATIVE]
        ))
        
        # Number and Operations in Base Ten (Grade 5)
        standards.append(StandardBenchmark(
            framework_id="ccss-math",
            code="CCSS.MATH.CONTENT.5.NBT.B.5",
            category="Number and Operations in Base Ten",
            subcategory="Perform operations with multi-digit whole numbers",
            description="Fluently multiply multi-digit whole numbers using the standard algorithm.",
            difficulty=DifficultyScale.PROFICIENT,
            grade_levels=[GradeLevel.GRADE_5],
            suggested_instructional_hours=8.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.SUMMATIVE]
        ))
        
        # Algebra (High School)
        standards.append(StandardBenchmark(
            framework_id="ccss-math",
            code="CCSS.MATH.CONTENT.HSF.IF.A.1",
            category="Interpreting Functions",
            subcategory="Understand the concept of a function",
            description="Understand that a function from one set (called the domain) to another set (called the range) assigns to each element of the domain exactly one element of the range.",
            difficulty=DifficultyScale.PROFICIENT,
            grade_levels=[GradeLevel.GRADE_9, GradeLevel.GRADE_10, GradeLevel.GRADE_11],
            suggested_instructional_hours=6.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.SUMMATIVE]
        ))
        
        standards.append(StandardBenchmark(
            framework_id="ccss-math",
            code="CCSS.MATH.CONTENT.HSF.IF.C.7",
            category="Interpreting Functions",
            subcategory="Analyze functions using different representations",
            description="Graph functions expressed symbolically and show key features of the graph, including intercepts, intervals of increase/decrease, relative maximums/minimums, symmetries, and end behavior.",
            difficulty=DifficultyScale.ADVANCED,
            grade_levels=[GradeLevel.GRADE_10, GradeLevel.GRADE_11, GradeLevel.GRADE_12],
            suggested_instructional_hours=8.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.SUMMATIVE]
        ))
        
        return standards
    
    def _generate_ngss_standards(self) -> List[StandardBenchmark]:
        """Generate sample NGSS standards"""
        standards = []
        
        # Middle School Physical Science
        standards.append(StandardBenchmark(
            framework_id="ngss",
            code="MS-PS1-1",
            category="Matter and Its Interactions",
            subcategory="Develop models to describe the atomic composition of simple molecules and extended structures",
            description="Develop models to describe the atomic composition of simple molecules and extended structures.",
            difficulty=DifficultyScale.DEVELOPING,
            grade_levels=[GradeLevel.GRADE_6, GradeLevel.GRADE_7, GradeLevel.GRADE_8],
            suggested_instructional_hours=8.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.PERFORMANCE]
        ))
        
        # High School Physics
        standards.append(StandardBenchmark(
            framework_id="ngss",
            code="HS-PS2-1",
            category="Motion and Stability: Forces and Interactions",
            subcategory="Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the net force on a macroscopic object, its mass, and its acceleration",
            description="Analyze data to support the claim that Newton's second law of motion describes the mathematical relationship among the net force on a macroscopic object, its mass, and its acceleration.",
            difficulty=DifficultyScale.PROFICIENT,
            grade_levels=[GradeLevel.GRADE_9, GradeLevel.GRADE_10, GradeLevel.GRADE_11],
            suggested_instructional_hours=10.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.SUMMATIVE]
        ))
        
        standards.append(StandardBenchmark(
            framework_id="ngss",
            code="HS-PS3-1",
            category="Energy",
            subcategory="Create a computational model to calculate the change in the energy of one component in a system when the change in energy of the other component(s) and energy flows in and out of the system are known",
            description="Create a computational model to calculate the change in the energy of one component in a system when the change in energy of the other component(s) and energy flows in and out of the system are known.",
            difficulty=DifficultyScale.ADVANCED,
            grade_levels=[GradeLevel.GRADE_10, GradeLevel.GRADE_11, GradeLevel.GRADE_12],
            suggested_instructional_hours=12.0,
            assessment_methods=[AssessmentType.FORMATIVE, AssessmentType.PERFORMANCE]
        ))
        
        return standards
    
    # =========================================================================
    # Concept Mapping
    # =========================================================================
    
    def suggest_mappings(
        self,
        concept_id: str,
        concept_name: str,
        concept_description: str,
        concept_tags: Optional[List[str]] = None,
        framework_id: Optional[str] = None
    ) -> List[MappingSuggestion]:
        """
        Suggest standard mappings for a concept.
        
        Args:
            concept_id: The concept ID
            concept_name: The concept name
            concept_description: The concept description
            concept_tags: Optional concept tags
            framework_id: Optional specific framework to search
            
        Returns:
            List of mapping suggestions
        """
        suggestions = []
        
        # Build concept profile
        profile = self._build_concept_profile(
            concept_name, concept_description, concept_tags or []
        )
        
        # Get benchmarks to search
        benchmarks = self._get_benchmarks_to_search(framework_id)
        
        for benchmark in benchmarks:
            match_score, match_reasons = self._calculate_match_score(profile, benchmark)
            
            if match_score >= 0.5:
                suggestions.append(MappingSuggestion(
                    concept_id=concept_id,
                    concept_name=concept_name,
                    concept_description=concept_description,
                    suggested_standard_ids=[benchmark.id],
                    suggested_standard_codes=[benchmark.code],
                    match_reasons=match_reasons,
                    requires_review=match_score < 0.8
                ))
        
        # Sort by match quality
        suggestions.sort(key=lambda x: len(x.match_reasons), reverse=True)
        
        return suggestions[:10]  # Limit suggestions
    
    def _build_concept_profile(
        self,
        name: str,
        description: str,
        tags: List[str]
    ) -> Dict[str, Set[str]]:
        """Build a searchable profile from concept data"""
        profile = {
            'keywords': set(),
            'bigrams': set(),
            'contexts': set()
        }
        
        # Extract keywords from name
        words = re.findall(r'\w+', name.lower())
        profile['keywords'].update(words)
        
        # Extract keywords from description
        desc_words = re.findall(r'\w+', description.lower())
        profile['keywords'].update(desc_words)
        
        # Add tags
        profile['keywords'].update([t.lower() for t in tags])
        
        # Extract bigrams
        all_text = f"{name} {description}"
        words = all_text.split()
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}".lower()
            profile['bigrams'].add(bigram)
        
        # Identify contexts
        context_indicators = {
            'mathematics': ['solve', 'calculate', 'equation', 'function', 'value', 'number'],
            'physics': ['force', 'motion', 'energy', 'wave', 'velocity', 'acceleration'],
            'chemistry': ['reaction', 'molecule', 'bond', 'solution', 'compound'],
            'biology': ['cell', 'organism', 'genetic', 'evolution', 'metabolism'],
            'ela': ['text', 'read', 'write', 'argument', 'narrative', 'author']
        }
        
        for context, indicators in context_indicators.items():
            if any(ind in description.lower() for ind in indicators):
                profile['contexts'].add(context)
        
        return profile
    
    def _calculate_match_score(
        self,
        profile: Dict[str, Set[str]],
        benchmark: StandardBenchmark
    ) -> Tuple[float, List[str]]:
        """Calculate match score between concept and benchmark"""
        score = 0.0
        reasons = []
        
        benchmark_text = f"{benchmark.code} {benchmark.description} {benchmark.category}"
        benchmark_words = set(re.findall(r'\w+', benchmark_text.lower()))
        
        # Keyword overlap
        keyword_overlap = len(profile['keywords'] & benchmark_words)
        if keyword_overlap > 0:
            score += min(0.5, keyword_overlap * 0.1)
            reasons.append(f"Keyword overlap: {keyword_overlap} shared terms")
        
        # Context match
        if profile['contexts']:
            for context in profile['contexts']:
                if context in benchmark_text.lower():
                    score += 0.2
                    reasons.append(f"Context match: {context}")
                    break
        
        # Category match
        if any(word in benchmark.category.lower() for word in profile['keywords']):
            score += 0.15
            reasons.append("Category alignment")
        
        # Grade level compatibility (bonus)
        if benchmark.grade_levels:
            score += 0.1
            reasons.append("Grade level defined")
        
        return min(1.0, score), reasons
    
    def _get_benchmarks_to_search(
        self,
        framework_id: Optional[str]
    ) -> List[StandardBenchmark]:
        """Get benchmarks to search for mappings"""
        if framework_id:
            return self.get_benchmarks_by_framework(framework_id)
        return list(self._benchmarks.values())
    
    def create_mapping(
        self,
        concept_id: str,
        concept_name: str,
        standard_id: str,
        confidence: MappingConfidence,
        rationale: str,
        match_evidence: Optional[List[str]] = None
    ) -> ConceptMapping:
        """
        Create a confirmed concept-standard mapping.
        
        Args:
            concept_id: The concept ID
            concept_name: The concept name
            standard_id: The standard ID
            confidence: Mapping confidence level
            rationale: Rationale for the mapping
            match_evidence: Evidence supporting the mapping
            
        Returns:
            The created ConceptMapping
        """
        standard = self._benchmarks.get(standard_id)
        if not standard:
            raise ValueError(f"Standard {standard_id} not found")
        
        mapping = ConceptMapping(
            concept_id=concept_id,
            concept_name=concept_name,
            standard_id=standard_id,
            standard_code=standard.code,
            confidence=confidence,
            rationale=rationale,
            match_evidence=match_evidence or [],
            is_reviewed=True
        )
        
        self._mappings[concept_id].append(mapping)
        
        logger.info(f"Created mapping: {concept_id} -> {standard_id} ({confidence.value})")
        
        return mapping
    
    def get_mappings_for_concept(
        self,
        concept_id: str,
        include_unreviewed: bool = False
    ) -> List[ConceptMapping]:
        """Get all mappings for a concept"""
        mappings = self._mappings.get(concept_id, [])
        
        if not include_unreviewed:
            mappings = [m for m in mappings if m.is_reviewed]
        
        return mappings
    
    def get_concepts_for_standard(
        self,
        standard_id: str
    ) -> List[ConceptMapping]:
        """Get all concepts mapped to a standard"""
        return [
            m for mappings in self._mappings.values()
            for m in mappings
            if m.standard_id == standard_id
        ]
    
    # =========================================================================
    # Coverage Analysis
    # =========================================================================
    
    def generate_coverage_report(
        self,
        framework_id: str,
        mapped_concept_ids: Set[str]
    ) -> CoverageReport:
        """
        Generate a curriculum coverage report.
        
        Args:
            framework_id: The framework to analyze
            mapped_concept_ids: Set of concept IDs that are mapped
            
        Returns:
            CoverageReport with analysis
        """
        framework = self._frameworks.get(framework_id)
        if not framework:
            raise ValueError(f"Framework {framework_id} not found")
        
        benchmarks = self.get_benchmarks_by_framework(framework_id)
        
        # Find covered and uncovered standards
        covered_standard_ids = set()
        for concept_id in mapped_concept_ids:
            for mapping in self.get_mappings_for_concept(concept_id):
                if mapping.standard_id in [b.id for b in benchmarks]:
                    covered_standard_ids.add(mapping.standard_id)
        
        covered_count = len(covered_standard_ids)
        total_count = len(benchmarks)
        
        uncovered = [
            {
                'id': b.id,
                'code': b.code,
                'description': b.description,
                'category': b.category
            }
            for b in benchmarks
            if b.id not in covered_standard_ids
        ]
        
        # Calculate concept coverage
        concept_coverage = {
            'total_mapped': len(mapped_concept_ids),
            'high_confidence': len([
                c for mappings in self._mappings.values()
                for c in mappings
                if c.confidence == MappingConfidence.HIGH
            ]),
            'medium_confidence': len([
                c for mappings in self._mappings.values()
                for c in mappings
                if c.confidence == MappingConfidence.MEDIUM
            ]),
            'low_confidence': len([
                c for mappings in self._mappings.values()
                for c in mappings
                if c.confidence == MappingConfidence.LOW
            ])
        }
        
        # Generate recommendations
        recommendations = self._generate_coverage_recommendations(
            covered_count, total_count, uncovered
        )
        
        return CoverageReport(
            framework_id=framework_id,
            framework_name=framework.name,
            total_standards=total_count,
            covered_standards=covered_count,
            uncovered_standards=uncovered,
            coverage_percentage=(covered_count / total_count * 100) if total_count > 0 else 0,
            concept_coverage=concept_coverage,
            recommendations=recommendations
        )
    
    def _generate_coverage_recommendations(
        self,
        covered: int,
        total: int,
        uncovered: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations based on coverage"""
        recommendations = []
        
        coverage_pct = (covered / total * 100) if total > 0 else 0
        
        if coverage_pct < 50:
            recommendations.append("Coverage is below 50%. Consider reviewing unmapped concepts for potential alignments.")
        elif coverage_pct < 75:
            recommendations.append("Good coverage but room for improvement. Focus on high-priority standards.")
        else:
            recommendations.append("Strong curriculum coverage. Continue monitoring for new standards.")
        
        # Specific recommendations for uncovered
        if uncovered:
            categories = set(u.get('category', 'Unknown') for u in uncovered[:10])
            if len(categories) > 1:
                recommendations.append(f"Review standards in categories: {', '.join(list(categories)[:3])}")
        
        return recommendations
    
    def validate_syllabus_coverage(
        self,
        syllabus_units: List[SyllabusUnit],
        framework_id: str
    ) -> Dict[str, Any]:
        """
        Validate that a syllabus covers required standards.
        
        Args:
            syllabus_units: List of syllabus units
            framework_id: The framework to validate against
            
        Returns:
            Validation results
        """
        benchmarks = self.get_benchmarks_by_framework(framework_id)
        covered_benchmarks = set()
        
        # Collect all aligned standards from syllabus
        for unit in syllabus_units:
            for standard_id in unit.aligned_standard_ids:
                if standard_id in [b.id for b in benchmarks]:
                    covered_benchmarks.add(standard_id)
        
        # Check for gaps
        gaps = []
        for benchmark in benchmarks:
            if benchmark.id not in covered_benchmarks:
                gaps.append({
                    'standard_id': benchmark.id,
                    'standard_code': benchmark.code,
                    'description': benchmark.description,
                    'category': benchmark.category,
                    'severity': 'high' if len(benchmark.grade_levels) <= 2 else 'medium'
                })
        
        return {
            'total_standards': len(benchmarks),
            'covered_standards': len(covered_benchmarks),
            'coverage_percentage': (
                len(covered_benchmarks) / len(benchmarks) * 100
            ) if benchmarks else 0,
            'gaps': sorted(gaps, key=lambda x: x['severity']),
            'is_complete': len(gaps) == 0,
            'recommendations': self._generate_syllabus_recommendations(gaps)
        }
    
    def _generate_syllabus_recommendations(
        self,
        gaps: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate recommendations for syllabus gaps"""
        recommendations = []
        
        if not gaps:
            recommendations.append("Syllabus fully covers the framework standards.")
            return recommendations
        
        high_severity = [g for g in gaps if g['severity'] == 'high']
        if high_severity:
            recommendations.append(
                f"Add coverage for {len(high_severity)} critical standards "
                f"in categories: {', '.join(set(g['category'] for g in high_severity))}"
            )
        
        return recommendations
    
    # =========================================================================
    # Export Functions
    # =========================================================================
    
    def export_mappings(self, concept_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        export mappings for backup or analysis.
        
        Args:
            concept_ids: Specific concepts to export, or None for all
            
        Returns:
            Dictionary representation of mappings
        """
        if concept_ids:
            selected_mappings = {
                cid: [m.to_dict() for m in mappings]
                for cid, mappings in self._mappings.items()
                if cid in concept_ids
            }
        else:
            selected_mappings = {
                cid: [m.to_dict() for m in mappings]
                for cid, mappings in self._mappings.items()
            }
        
        return {
            'exported_at': datetime.now().isoformat(),
            'total_concepts': len(selected_mappings),
            'total_mappings': sum(len(m) for m in selected_mappings.values()),
            'mappings': selected_mappings
        }
    
    def import_mappings(self, data: Dict[str, Any]) -> int:
        """
        Import mappings from exported data.
        
        Args:
            data: Exported mapping data
            
        Returns:
            Number of mappings imported
        """
        count = 0
        
        for cid, mappings_data in data.get('mappings', {}).items():
            for m_data in mappings_data:
                try:
                    confidence = MappingConfidence(m_data.get('confidence', 'low'))
                    mapping = ConceptMapping(
                        concept_id=m_data['concept_id'],
                        concept_name=m_data['concept_name'],
                        standard_id=m_data['standard_id'],
                        standard_code=m_data['standard_code'],
                        confidence=confidence,
                        rationale=m_data.get('rationale', ''),
                        match_evidence=m_data.get('match_evidence', []),
                        is_reviewed=m_data.get('is_reviewed', False)
                    )
                    self._mappings[mapping.concept_id].append(mapping)
                    count += 1
                except (KeyError, ValueError) as e:
                    logger.warning(f"Error importing mapping: {e}")
        
        return count
