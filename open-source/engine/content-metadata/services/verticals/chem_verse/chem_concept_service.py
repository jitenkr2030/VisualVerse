"""
ChemVerse Concept Service

This module provides the concept management and educational content services for
the VisualVerse chemistry learning platform. It handles curriculum mapping, lesson
content, and chemistry concept explanations.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import json


class ChemDomain(str, Enum):
    """Chemistry domains for curriculum organization."""
    GENERAL = "general"
    ATOMIC_STRUCTURE = "atomic_structure"
    STOICHIOMETRY = "stoichiometry"
    THERMOCHEMISTRY = "thermochemistry"
    ACIDS_BASES = "acids_bases"
    ELECTROCHEMISTRY = "electrochemistry"
    ORGANIC = "organic"
    EQUILIBRIUM = "equilibrium"
    KINETICS = "kinetics"
    SOLUTIONS = "solutions"


class DifficultyLevel(str, Enum):
    """Difficulty levels for chemistry concepts."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class ChemistryConcept:
    """Represents a chemistry concept with educational content."""
    id: str
    name: str
    domain: ChemDomain
    difficulty: DifficultyLevel
    definition: str
    explanation: str
    key_points: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    formulas: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    visual_aids: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain.value,
            "difficulty": self.difficulty.value,
            "definition": self.definition,
            "explanation": self.explanation,
            "key_points": self.key_points,
            "examples": self.examples,
            "formulas": self.formulas,
            "related_concepts": self.related_concepts,
            "visual_aids": self.visual_aids
        }


@dataclass
class LessonContent:
    """Represents a chemistry lesson with structured content."""
    id: str
    title: str
    domain: ChemDomain
    difficulty: DifficultyLevel
    objectives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    sections: List[Dict[str, Any]] = field(default_factory=list)
    practice_problems: List[Dict[str, Any]] = field(default_factory=list)
    summary_points: List[str] = field(default_factory=list)
    estimated_minutes: int = 30
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "domain": self.domain.value,
            "difficulty": self.difficulty.value,
            "objectives": self.objectives,
            "prerequisites": self.prerequisites,
            "sections": self.sections,
            "practice_problems": self.practice_problems,
            "summary_points": self.summary_points,
            "estimated_minutes": self.estimated_minutes
        }


@dataclass
class PracticeProblem:
    """Represents a practice problem for chemistry concepts."""
    id: str
    concept_id: str
    problem_type: str
    question: str
    hint: str = ""
    solution_steps: List[str] = field(default_factory=list)
    final_answer: str = ""
    explanation: str = ""
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    points: int = 10
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "concept_id": self.concept_id,
            "problem_type": self.problem_type,
            "question": self.question,
            "hint": self.hint,
            "solution_steps": self.solution_steps,
            "final_answer": self.final_answer,
            "explanation": self.explanation,
            "difficulty": self.difficulty.value,
            "points": self.points
        }


class PeriodicTable:
    """Provides access to element data and periodic table information."""
    
    _table_data: Dict[str, Dict[str, Any]] = {
        "H": {
            "name": "Hydrogen", "symbol": "H", "atomic_number": 1,
            "atomic_mass": 1.008, "category": "nonmetal",
            "group": 1, "period": 1, "block": "s"
        },
        "He": {
            "name": "Helium", "symbol": "He", "atomic_number": 2,
            "atomic_mass": 4.0026, "category": "noble_gas",
            "group": 18, "period": 1, "block": "s"
        },
        "Li": {
            "name": "Lithium", "symbol": "Li", "atomic_number": 3,
            "atomic_mass": 6.94, "category": "alkali_metal",
            "group": 1, "period": 2, "block": "s"
        },
        "Be": {
            "name": "Beryllium", "symbol": "Be", "atomic_number": 4,
            "atomic_mass": 9.0122, "category": "alkaline_earth",
            "group": 2, "period": 2, "block": "s"
        },
        "B": {
            "name": "Boron", "symbol": "B", "atomic_number": 5,
            "atomic_mass": 10.81, "category": "metalloid",
            "group": 13, "period": 2, "block": "p"
        },
        "C": {
            "name": "Carbon", "symbol": "C", "atomic_number": 6,
            "atomic_mass": 12.011, "category": "nonmetal",
            "group": 14, "period": 2, "block": "p"
        },
        "N": {
            "name": "Nitrogen", "symbol": "N", "atomic_number": 7,
            "atomic_mass": 14.007, "category": "nonmetal",
            "group": 15, "period": 2, "block": "p"
        },
        "O": {
            "name": "Oxygen", "symbol": "O", "atomic_number": 8,
            "atomic_mass": 15.999, "category": "nonmetal",
            "group": 16, "period": 2, "block": "p"
        },
        "F": {
            "name": "Fluorine", "symbol": "F", "atomic_number": 9,
            "atomic_mass": 18.998, "category": "halogen",
            "group": 17, "period": 2, "block": "p"
        },
        "Ne": {
            "name": "Neon", "symbol": "Ne", "atomic_number": 10,
            "atomic_mass": 20.180, "category": "noble_gas",
            "group": 18, "period": 2, "block": "p"
        },
        "Na": {
            "name": "Sodium", "symbol": "Na", "atomic_number": 11,
            "atomic_mass": 22.990, "category": "alkali_metal",
            "group": 1, "period": 3, "block": "s"
        },
        "Mg": {
            "name": "Magnesium", "symbol": "Mg", "atomic_number": 12,
            "atomic_mass": 24.305, "category": "alkaline_earth",
            "group": 2, "period": 3, "block": "s"
        },
        "Al": {
            "name": "Aluminum", "symbol": "Al", "atomic_number": 13,
            "atomic_mass": 26.982, "category": "post_transition_metal",
            "group": 13, "period": 3, "block": "p"
        },
        "Si": {
            "name": "Silicon", "symbol": "Si", "atomic_number": 14,
            "atomic_mass": 28.085, "category": "metalloid",
            "group": 14, "period": 3, "block": "p"
        },
        "P": {
            "name": "Phosphorus", "symbol": "P", "atomic_number": 15,
            "atomic_mass": 30.974, "category": "nonmetal",
            "group": 15, "period": 3, "block": "p"
        },
        "S": {
            "name": "Sulfur", "symbol": "S", "atomic_number": 16,
            "atomic_mass": 32.06, "category": "nonmetal",
            "group": 16, "period": 3, "block": "p"
        },
        "Cl": {
            "name": "Chlorine", "symbol": "Cl", "atomic_number": 17,
            "atomic_mass": 35.45, "category": "halogen",
            "group": 17, "period": 3, "block": "p"
        },
        "K": {
            "name": "Potassium", "symbol": "K", "atomic_number": 19,
            "atomic_mass": 39.098, "category": "alkali_metal",
            "group": 1, "period": 4, "block": "s"
        },
        "Ca": {
            "name": "Calcium", "symbol": "Ca", "atomic_number": 20,
            "atomic_mass": 40.078, "category": "alkaline_earth",
            "group": 2, "period": 4, "block": "s"
        },
        "Fe": {
            "name": "Iron", "symbol": "Fe", "atomic_number": 26,
            "atomic_mass": 55.845, "category": "transition_metal",
            "group": 8, "period": 4, "block": "d"
        },
        "Cu": {
            "name": "Copper", "symbol": "Cu", "atomic_number": 29,
            "atomic_mass": 63.546, "category": "transition_metal",
            "group": 11, "period": 4, "block": "d"
        },
        "Zn": {
            "name": "Zinc", "symbol": "Zn", "atomic_number": 30,
            "atomic_mass": 65.38, "category": "transition_metal",
            "group": 12, "period": 4, "block": "d"
        },
        "Br": {
            "name": "Bromine", "symbol": "Br", "atomic_number": 35,
            "atomic_mass": 79.904, "category": "halogen",
            "group": 17, "period": 4, "block": "p"
        },
        "Ag": {
            "name": "Silver", "symbol": "Ag", "atomic_number": 47,
            "atomic_mass": 107.87, "category": "transition_metal",
            "group": 11, "period": 5, "block": "d"
        },
        "I": {
            "name": "Iodine", "symbol": "I", "atomic_number": 53,
            "atomic_mass": 126.90, "category": "halogen",
            "group": 17, "period": 5, "block": "p"
        },
        "Au": {
            "name": "Gold", "symbol": "Au", "atomic_number": 79,
            "atomic_mass": 196.97, "category": "transition_metal",
            "group": 11, "period": 6, "block": "d"
        },
        "Hg": {
            "name": "Mercury", "symbol": "Hg", "atomic_number": 80,
            "atomic_mass": 200.59, "category": "transition_metal",
            "group": 12, "period": 6, "block": "d"
        },
        "Pb": {
            "name": "Lead", "symbol": "Pb", "atomic_number": 82,
            "atomic_mass": 207.2, "category": "post_transition_metal",
            "group": 14, "period": 6, "block": "p"
        }
    }
    
    @classmethod
    def get_element(cls, symbol: str) -> Optional[Dict[str, Any]]:
        """Get element data by symbol."""
        return cls._table_data.get(symbol.capitalize())
    
    @classmethod
    def get_all_elements(cls) -> List[Dict[str, Any]]:
        """Get all element data."""
        return list(cls._table_data.values())
    
    @classmethod
    def get_elements_by_group(cls, group: int) -> List[Dict[str, Any]]:
        """Get all elements in a group."""
        return [e for e in cls._table_data.values() if e["group"] == group]
    
    @classmethod
    def get_elements_by_period(cls, period: int) -> List[Dict[str, Any]]:
        """Get all elements in a period."""
        return [e for e in cls._table_data.values() if e["period"] == period]
    
    @classmethod
    def get_elements_by_category(cls, category: str) -> List[Dict[str, Any]]:
        """Get all elements in a category."""
        return [e for e in cls._table_data.values() if e["category"] == category]


class ConceptRepository:
    """Repository for chemistry concepts and educational content."""
    
    _concepts: Dict[str, ChemistryConcept] = {}
    _lessons: Dict[str, LessonContent] = {}
    _problems: Dict[str, PracticeProblem] = {}
    
    @classmethod
    def register_concept(cls, concept: ChemistryConcept) -> None:
        """Register a new chemistry concept."""
        cls._concepts[concept.id] = concept
    
    @classmethod
    def get_concept(cls, concept_id: str) -> Optional[ChemistryConcept]:
        """Get a concept by ID."""
        return cls._concepts.get(concept_id)
    
    @classmethod
    def get_concepts_by_domain(cls, domain: ChemDomain) -> List[ChemistryConcept]:
        """Get all concepts in a domain."""
        return [c for c in cls._concepts.values() if c.domain == domain]
    
    @classmethod
    def get_concepts_by_difficulty(
        cls, difficulty: DifficultyLevel
    ) -> List[ChemistryConcept]:
        """Get all concepts at a difficulty level."""
        return [c for c in cls._concepts.values() if c.difficulty == difficulty]
    
    @classmethod
    def register_lesson(cls, lesson: LessonContent) -> None:
        """Register a new lesson."""
        cls._lessons[lesson.id] = lesson
    
    @classmethod
    def get_lesson(cls, lesson_id: str) -> Optional[LessonContent]:
        """Get a lesson by ID."""
        return cls._lessons.get(lesson_id)
    
    @classmethod
    def get_lessons_by_domain(cls, domain: ChemDomain) -> List[LessonContent]:
        """Get all lessons in a domain."""
        return [l for l in cls._lessons.values() if l.domain == domain]
    
    @classmethod
    def register_problem(cls, problem: PracticeProblem) -> None:
        """Register a new practice problem."""
        cls._problems[problem.id] = problem
    
    @classmethod
    def get_problem(cls, problem_id: str) -> Optional[PracticeProblem]:
        """Get a problem by ID."""
        return cls._problems.get(problem_id)
    
    @classmethod
    def get_problems_by_concept(
        cls, concept_id: str
    ) -> List[PracticeProblem]:
        """Get all problems for a concept."""
        return [p for p in cls._problems.values() if p.concept_id == concept_id]
    
    @classmethod
    def search_concepts(
        cls, query: str, domain: Optional[ChemDomain] = None
    ) -> List[ChemistryConcept]:
        """Search concepts by name or definition."""
        query_lower = query.lower()
        results = []
        for concept in cls._concepts.values():
            if domain and concept.domain != domain:
                continue
            if (query_lower in concept.name.lower() or
                query_lower in concept.definition.lower()):
                results.append(concept)
        return results


class ChemVerseConceptService:
    """
    Service for managing chemistry educational content and curriculum.
    
    This service provides access to concepts, lessons, practice problems,
    and element data for the chemistry learning platform.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the concept service with optional configuration."""
        self._repository = ConceptRepository()
        self._initialize_default_content()
    
    def _initialize_default_content(self) -> None:
        """Initialize with default chemistry content."""
        # Register atomic structure concepts
        ConceptRepository.register_concept(ChemistryConcept(
            id="atom-basic",
            name="Atomic Structure",
            domain=ChemDomain.ATOMIC_STRUCTURE,
            difficulty=DifficultyLevel.BEGINNER,
            definition="Atoms are the basic building blocks of matter, consisting of protons, neutrons, and electrons.",
            explanation="Every atom has a nucleus at its center containing protons (positively charged) and neutrons (neutral). Electrons (negatively charged) orbit the nucleus in energy levels. The number of protons determines the element, while the number of electrons determines the charge.",
            key_points=[
                "Protons determine the element identity",
                "Neutrons contribute to atomic mass and stability",
                "Electrons determine chemical behavior",
                "Atoms are mostly empty space"
            ],
            examples=[
                "Carbon has 6 protons, 6 neutrons, and 6 electrons",
                "An ion forms when an atom gains or loses electrons"
            ],
            formulas=["Atomic Number (Z) = number of protons"],
            related_concepts=["electron-configuration", "isotopes", "ions"]
        ))
        
        # Register stoichiometry concepts
        ConceptRepository.register_concept(ChemistryConcept(
            id="stoichiometry-basic",
            name="Stoichiometry",
            domain=ChemDomain.STOICHIOMETRY,
            difficulty=DifficultyLevel.INTERMEDIATE,
            definition="Stoichiometry is the calculation of reactants and products in chemical reactions based on the law of conservation of mass.",
            explanation="Stoichiometry uses the balanced chemical equation to determine the mole ratios between reactants and products. The coefficients in a balanced equation tell us the exact proportion of each substance involved in the reaction.",
            key_points=[
                "Balanced equations show mole ratios",
                "Molar mass converts between grams and moles",
                "Limiting reagent determines maximum product",
                "Percent yield compares actual to theoretical yield"
            ],
            examples=[
                "For 2H₂ + O₂ → 2H₂O, 2 moles of H₂ react with 1 mole of O₂",
                "If 4 moles of H₂ react, 2 moles of O₂ are needed"
            ],
            formulas=[
                "moles = mass / molar mass",
                "mole ratio = coefficient_product / coefficient_reactant"
            ],
            related_concepts=["balancing-equations", "molar-mass", "limiting-reagent"]
        ))
        
        # Register thermochemistry concepts
        ConceptRepository.register_concept(ChemistryConcept(
            id="enthalpy",
            name="Enthalpy and Heat",
            domain=ChemDomain.THERMOCHEMISTRY,
            difficulty=DifficultyLevel.INTERMEDIATE,
            definition="Enthalpy (H) is the total heat content of a system at constant pressure. Changes in enthalpy (ΔH) indicate whether a reaction releases or absorbs heat.",
            explanation="Exothermic reactions release heat (ΔH < 0), while endothermic reactions absorb heat (ΔH > 0). The enthalpy change can be calculated from the heat absorbed or released by a reaction at constant pressure.",
            key_points=[
                "Exothermic: ΔH < 0, releases heat",
                "Endothermic: ΔH > 0, absorbs heat",
                "q = mcΔT relates heat to temperature change",
                "Bond breaking requires energy, bond forming releases energy"
            ],
            examples=[
                "Combustion is exothermic (releases heat)",
                "Photosynthesis is endothermic (absorbs heat)"
            ],
            formulas=[
                "ΔH = q (at constant pressure)",
                "q = mcΔT",
                "ΔH = Σ(bond energies broken) - Σ(bond energies formed)"
            ],
            related_concepts=["thermodynamics", "hess-law", "calorimetry"]
        ))
        
        # Register acid-base concepts
        ConceptRepository.register_concept(ChemistryConcept(
            id="ph-scale",
            name="pH and Acid-Base Reactions",
            domain=ChemDomain.ACIDS_BASES,
            difficulty=DifficultyLevel.INTERMEDIATE,
            definition="pH is a measure of the hydrogen ion concentration in a solution, ranging from 0 to 14. Acids have pH < 7, bases have pH > 7.",
            explanation="Strong acids completely dissociate in water, while weak acids only partially dissociate. Acid-base reactions (neutralization) produce water and a salt. The pH can be calculated from the hydrogen ion concentration.",
            key_points=[
                "pH = -log[H⁺]",
                "Acids donate H⁺ ions",
                "Bases accept H⁺ ions",
                "Neutral solution has pH = 7"
            ],
            examples=[
                "Stomach acid (HCl) has pH ≈ 1-2",
                "Bleach (NaOCl) has pH ≈ 12"
            ],
            formulas=[
                "pH = -log[H⁺]",
                "pOH = -log[OH⁻]",
                "pH + pOH = 14"
            ],
            related_concepts=["indicators", "buffers", "titration"]
        ))
        
        # Register electrochemistry concepts
        ConceptRepository.register_concept(ChemistryConcept(
            id="electrochemistry",
            name="Electrochemistry",
            domain=ChemDomain.ELECTROCHEMISTRY,
            difficulty=DifficultyLevel.ADVANCED,
            definition="Electrochemistry studies the relationship between electricity and chemical reactions, including voltaic cells and electrolysis.",
            explanation="Redox reactions involve electron transfer. In electrochemical cells, oxidation occurs at the anode and reduction at the cathode. The cell potential (voltage) determines if a reaction is spontaneous.",
            key_points=[
                "Oxidation: loss of electrons (anode)",
                "Reduction: gain of electrons (cathode)",
                "E°cell > 0 for spontaneous reactions",
                "Nernst equation accounts for concentration effects"
            ],
            examples=[
                "Batteries convert chemical energy to electrical energy",
                "Electroplating uses electrolysis to deposit metal coatings"
            ],
            formulas=[
                "E°cell = E°cathode - E°anode",
                "ΔG = -nFE",
                "E = E° - (RT/nF)ln(Q)"
            ],
            related_concepts=["oxidation-reduction", "cells", "corrosion"]
        ))
        
        # Register default lessons
        ConceptRepository.register_lesson(LessonContent(
            id="lesson-intro-chemistry",
            title="Introduction to Chemistry",
            domain=ChemDomain.GENERAL,
            difficulty=DifficultyLevel.BEGINNER,
            objectives=[
                "Understand the definition of chemistry",
                "Identify the states of matter",
                "Recognize matter and its properties"
            ],
            prerequisites=[],
            sections=[
                {
                    "title": "What is Chemistry?",
                    "content": "Chemistry is the study of matter, its properties, and how matter changes.",
                    "type": "text"
                },
                {
                    "title": "States of Matter",
                    "content": "Matter exists in three states: solid, liquid, and gas.",
                    "type": "text"
                }
            ],
            summary_points=[
                "Chemistry studies matter and its changes",
                "Matter has mass and takes up space"
            ],
            estimated_minutes=20
        ))
        
        ConceptRepository.register_lesson(LessonContent(
            id="lesson-stoichiometry",
            title="Stoichiometry Fundamentals",
            domain=ChemDomain.STOICHIOMETRY,
            difficulty=DifficultyLevel.INTERMEDIATE,
            objectives=[
                "Balance chemical equations",
                "Use mole ratios in calculations",
                "Calculate limiting reagents"
            ],
            prerequisites=["lesson-atomic-structure"],
            sections=[
                {
                    "title": "Balancing Equations",
                    "content": "Chemical equations must be balanced to obey the law of conservation of mass.",
                    "type": "text"
                },
                {
                    "title": "Mole Ratios",
                    "content": "The coefficients in a balanced equation give us mole ratios for the reaction.",
                    "type": "text"
                }
            ],
            practice_problems=[
                {
                    "question": "Balance the equation: H₂ + O₂ → H₂O",
                    "answer": "2H₂ + O₂ → 2H₂O"
                }
            ],
            summary_points=[
                "Always balance chemical equations",
                "Mole ratios come from coefficients"
            ],
            estimated_minutes=45
        ))
    
    def get_element_data(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive data for an element."""
        element = PeriodicTable.get_element(symbol)
        if element:
            return element
        return {"error": f"Element {symbol} not found"}
    
    def get_concept(self, concept_id: str) -> Optional[ChemistryConcept]:
        """Get a chemistry concept by ID."""
        return ConceptRepository.get_concept(concept_id)
    
    def get_concepts_by_domain(
        self, domain: ChemDomain
    ) -> List[ChemistryConcept]:
        """Get all concepts in a chemistry domain."""
        return ConceptRepository.get_concepts_by_domain(domain)
    
    def get_lesson(self, lesson_id: str) -> Optional[LessonContent]:
        """Get a lesson by ID."""
        return ConceptRepository.get_lesson(lesson_id)
    
    def get_lessons_by_domain(
        self, domain: ChemDomain
    ) -> List[LessonContent]:
        """Get all lessons in a domain."""
        return ConceptRepository.get_lessons_by_domain(domain)
    
    def get_practice_problem(
        self, problem_id: str
    ) -> Optional[PracticeProblem]:
        """Get a practice problem by ID."""
        return ConceptRepository.get_problem(problem_id)
    
    def get_problems_for_concept(
        self, concept_id: str
    ) -> List[PracticeProblem]:
        """Get all practice problems for a concept."""
        return ConceptRepository.get_problems_by_concept(concept_id)
    
    def search_content(self, query: str) -> Dict[str, List]:
        """Search for concepts and lessons matching a query."""
        concepts = ConceptRepository.search_concepts(query)
        return {
            "concepts": [c.to_dict() for c in concepts],
            "lessons": []  # Add lesson search if needed
        }
    
    def get_curriculum_map(
        self, domain: Optional[ChemDomain] = None
    ) -> List[Dict[str, Any]]:
        """Get a curriculum map showing concepts and their prerequisites."""
        curriculum = []
        concepts = (ConceptRepository.get_concepts_by_domain(domain)
                   if domain else list(ConceptRepository._concepts.values()))
        
        for concept in concepts:
            curriculum.append({
                "id": concept.id,
                "name": concept.name,
                "domain": concept.domain.value,
                "difficulty": concept.difficulty.value,
                "prerequisites": concept.related_concepts[:2],  # First 2 as prereqs
                "estimated_time": f"{len(concept.key_points) * 5} minutes"
            })
        
        return curriculum
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the service with custom settings."""
        if "custom_content_path" in config:
            # Load custom content from the specified path
            pass
        if "default_domain" in config:
            self._default_domain = config["default_domain"]


def create_chem_concept_service(config: dict = None) -> ChemVerseConceptService:
    """
    Create a ChemVerseConceptService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseConceptService instance
    """
    service = ChemVerseConceptService(config)
    return service


__all__ = [
    "ChemDomain",
    "DifficultyLevel",
    "ChemistryConcept",
    "LessonContent",
    "PracticeProblem",
    "PeriodicTable",
    "ConceptRepository",
    "ChemVerseConceptService",
    "create_chem_concept_service"
]
