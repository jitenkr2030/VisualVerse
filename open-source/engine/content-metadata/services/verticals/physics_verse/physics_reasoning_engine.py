"""
PhysicsVerse Reasoning Engine

This module provides comprehensive physics analysis and reasoning capabilities
for the PhysicsVerse learning platform. It offers problem solving, step-by-step
explanation generation, formula derivation assistance, and conceptual verification.

Key Features:
- Physics problem analysis and solving
- Step-by-step solution generation
- Formula application guidance
- Dimensional analysis verification
- Unit consistency checking
- Conceptual misconception identification
- Multiple solution approach comparison
- Physics principle explanation generation

Licensed under the Apache License, Version 2.0
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from math import sqrt, sin, cos, tan, pi, radians, degrees, log
import logging

from .physics_core import (
    Vector2D,
    Vector3D,
    PhysicsConstants,
    UnitConverter,
    PhysicsFormula,
    PhysicsFormulaRegistry,
    calculate_kinematic_motion,
    calculate_projectile_motion,
    calculate_orbit_parameters,
    calculate_shock_parameters
)

logger = logging.getLogger(__name__)


class PhysicsDomain(Enum):
    """Physics domains for reasoning."""
    MECHANICS = "mechanics"
    OPTICS = "optics"
    ELECTROMAGNETISM = "electromagnetism"
    THERMODYNAMICS = "thermodynamics"
    WAVE_PHYSICS = "wave_physics"
    MODERN_PHYSICS = "modern_physics"


class ProblemDifficulty(Enum):
    """Problem difficulty levels."""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class SolutionStatus(Enum):
    """Status of a solution attempt."""
    SOLVED = "solved"
    PARTIAL = "partial"
    INCORRECT = "incorrect"
    NEEDS_REVIEW = "needs_review"


@dataclass
class PhysicsProblem:
    """
    Represents a physics problem for analysis.
    
    Attributes:
        problem_id: Unique identifier
        title: Problem title
        description: Full problem description
        domain: Physics domain
        difficulty: Difficulty level
        given: Dictionary of given quantities
        unknown: List of quantities to find
        constraints: Physical constraints
        assumptions: Assumptions made
    """
    problem_id: str
    title: str
    description: str
    domain: PhysicsDomain
    difficulty: ProblemDifficulty
    given: Dict[str, Any] = field(default_factory=dict)
    unknown: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)


@dataclass
class SolutionStep:
    """
    Represents a step in a physics solution.
    
    Attributes:
        step_number: Sequential step number
        description: Step description
        formula: Formula used
        variables: Variables with values
        result: Calculated result
        explanation: Why this step is valid
    """
    step_number: int
    description: str
    formula: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)
    result: Optional[float] = None
    unit: Optional[str] = None
    explanation: str = ""


@dataclass
class PhysicsSolution:
    """
    Complete solution to a physics problem.
    
    Attributes:
        solution_id: Unique identifier
        problem_id: Reference to problem
        status: Solution status
        steps: List of solution steps
        final_answers: Final numerical answers
        units: Units of answers
        verification: Verification results
        alternative_methods: Alternative approaches
    """
    solution_id: str
    problem_id: str
    status: SolutionStatus
    steps: List[SolutionStep] = field(default_factory=list)
    final_answers: Dict[str, float] = field(default_factory=dict)
    units: Dict[str, str] = field(default_factory=dict)
    verification: Dict[str, Any] = field(default_factory=dict)
    alternative_methods: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ConceptualAnalysis:
    """
    Analysis of physics concepts in a problem.
    
    Attributes:
        concepts: List of relevant concepts
        principles: Physics principles applied
        misconceptions: Potential misconceptions
        related_topics: Related topics for study
    """
    concepts: List[Dict[str, str]] = field(default_factory=list)
    principles: List[Dict[str, str]] = field(default_factory=list)
    misconceptions: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)


@dataclass
class DimensionalAnalysis:
    """
    Dimensional analysis result.
    
    Attributes:
        is_consistent: Whether dimensions are consistent
        derived_unit: Derived unit from calculation
        expected_unit: Expected unit
        check_details: Details of the check
    """
    is_consistent: bool
    derived_unit: Optional[str] = None
    expected_unit: Optional[str] = None
    check_details: List[str] = field(default_factory=list)


class PhysicsVerseReasoningEngine:
    """
    PhysicsVerse reasoning engine.
    
    This engine provides comprehensive physics analysis capabilities:
    - Problem decomposition and analysis
    - Step-by-step solution generation
    - Dimensional analysis verification
    - Conceptual explanation generation
    - Multiple solution approach comparison
    - Mistake identification and correction
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the reasoning engine.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._formula_registry = PhysicsFormulaRegistry()
        self._principles = self._initialize_physics_principles()
        self._common_misconceptions = self._initialize_misconceptions()
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        print("PhysicsVerseReasoningEngine configured with settings:", list(config.keys()))
    
    def _initialize_physics_principles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize physics principles database."""
        return {
            "conservation_of_energy": {
                "statement": "Energy cannot be created or destroyed, only transformed from one form to another.",
                "formula": "E_initial = E_final",
                "conditions": ["Isolated system", "No non-conservative forces"],
                "applications": ["Mechanics", "Thermodynamics", "Electromagnetism"]
            },
            "conservation_of_momentum": {
                "statement": "The total momentum of a closed system remains constant.",
                "formula": "Σp_initial = Σp_final",
                "conditions": ["Isolated system (no external forces)", "Newton's laws apply"],
                "applications": ["Collisions", "Rocket propulsion", "Particle physics"]
            },
            "newtons_first_law": {
                "statement": "An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction, unless acted upon by an unbalanced force.",
                "formula": "ΣF = 0 ⇒ a = 0",
                "conditions": ["Inertial reference frame"],
                "applications": ["Statics", "Constant velocity motion"]
            },
            "newtons_second_law": {
                "statement": "The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.",
                "formula": "F = ma",
                "conditions": ["Constant mass", "Inertial reference frame"],
                "applications": ["Dynamics", "Force analysis"]
            },
            "newtons_third_law": {
                "statement": "For every action, there is an equal and opposite reaction.",
                "formula": "F_AB = -F_BA",
                "conditions": ["Always applies to force pairs"],
                "applications": ["Tension", "Normal force", "Thrust"]
            },
            "ohms_law": {
                "statement": "The current through a conductor is directly proportional to the voltage across it.",
                "formula": "V = IR",
                "conditions": ["Ohmic materials", "Constant temperature"],
                "applications": ["DC circuits", "Resistor networks"]
            },
            "faraday_law": {
                "statement": "A changing magnetic field induces an electromotive force.",
                "formula": "ℰ = -dΦ/dt",
                "conditions": ["Time-varying magnetic flux"],
                "applications": ["Generators", "Transformers", "Induction"]
            }
        }
    
    def _initialize_misconceptions(self) -> Dict[str, List[str]]:
        """Initialize common physics misconceptions."""
        return {
            "forces_and_motion": [
                "Objects need continuous force to keep moving",
                "Heavier objects fall faster",
                "Force causes motion (not acceleration)",
                "An object can have force without motion"
            ],
            "energy": [
                "Potential energy is stored in objects",
                "Heat and temperature are the same thing",
                "Energy is always conserved in every process"
            ],
            "optics": [
                "Light bends only at interfaces",
                "Lenses work by adding light",
                "The speed of light is always constant in all media"
            ],
            "circuits": [
                "Current gets used up as it flows",
                "Voltage and current are the same thing",
                "Electrons move at the speed of light through wires"
            ]
        }
    
    # ==================== PROBLEM ANALYSIS ====================
    
    def analyze_problem(self, problem: PhysicsProblem) -> Dict[str, Any]:
        """
        Analyze a physics problem and identify the approach.
        
        Args:
            problem: PhysicsProblem to analyze
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "problem_id": problem.problem_id,
            "domain": problem.domain.value,
            "difficulty": problem.difficulty.value,
            "given_quantities": problem.given,
            "unknown_quantities": problem.unknown,
            "concepts": self._identify_concepts(problem),
            "principles": self._identify_principles(problem),
            "formulas_needed": self._suggest_formulas(problem),
            "strategy": self._suggest_strategy(problem),
            "potential_misconceptions": self._check_misconceptions(problem),
            "dimensional_check": self._check_dimensional_consistency(problem)
        }
        
        return analysis
    
    def _identify_concepts(self, problem: PhysicsProblem) -> List[Dict[str, str]]:
        """Identify physics concepts involved in a problem."""
        concepts = []
        description_lower = problem.description.lower()
        
        # Keyword-based concept identification
        concept_keywords = {
            "kinematics": ["position", "velocity", "acceleration", "displacement", "time"],
            "dynamics": ["force", "mass", "weight", "friction", "tension"],
            "energy": ["energy", "work", "power", "kinetic", "potential"],
            "momentum": ["momentum", "collision", "impulse"],
            "waves": ["wave", "frequency", "wavelength", "amplitude", "period"],
            "optics": ["light", "reflection", "refraction", "lens", "mirror"],
            "circuits": ["current", "voltage", "resistance", "power", "circuit"],
            "magnetism": ["magnetic", "field", "force", "induction"]
        }
        
        for concept, keywords in concept_keywords.items():
            if any(kw in description_lower for kw in keywords):
                concepts.append({
                    "concept": concept,
                    "relevance": "high" if sum(1 for kw in keywords if kw in description_lower) > 2 else "medium"
                })
        
        return concepts
    
    def _identify_principles(self, problem: PhysicsProblem) -> List[Dict[str, str]]:
        """Identify physics principles applicable to a problem."""
        principles = []
        description_lower = problem.description.lower()
        
        for principle_id, principle in self._principles.items():
            # Check if principle applies based on keywords
            if "conservation" in description_lower or "conserved" in description_lower:
                if "conservation" in principle_id:
                    principles.append({
                        "principle": principle_id,
                        "statement": principle["statement"]
                    })
            
            if "force" in description_lower and principle_id.startswith("newton"):
                principles.append({
                    "principle": principle_id,
                    "statement": principle["statement"]
                })
            
            if "circuit" in description_lower and "ohms_law" in principle_id:
                principles.append({
                    "principle": principle_id,
                    "statement": principle["statement"]
                })
        
        return principles
    
    def _suggest_formulas(self, problem: PhysicsProblem) -> List[Dict[str, Any]]:
        """Suggest relevant formulas for a problem."""
        suggested = []
        
        for formula in self._formula_registry.list_all_formulas():
            formula_obj = self._formula_registry.get_formula(formula)
            if formula_obj:
                # Check if formula might be relevant
                formula_desc = formula_obj.description.lower()
                problem_desc = problem.description.lower()
                
                relevance = 0
                for given_key in problem.given.keys():
                    if given_key.lower() in formula_desc or given_key.lower() in problem_desc:
                        relevance += 1
                
                if relevance > 0:
                    suggested.append({
                        "formula_id": formula_obj.formula_id,
                        "name": formula_obj.name,
                        "latex": formula_obj.latex,
                        "relevance": "high" if relevance > 2 else "medium"
                    })
        
        return suggested[:5]  # Return top 5 suggestions
    
    def _suggest_strategy(self, problem: PhysicsProblem) -> Dict[str, Any]:
        """Suggest a solution strategy for the problem."""
        strategies = {
            PhysicsDomain.MECHANICS: [
                "Identify known and unknown quantities",
                "Draw a free-body diagram",
                "Apply Newton's second law (F = ma)",
                "Solve for acceleration",
                "Use kinematics equations for motion"
            ],
            PhysicsDomain.OPTICS: [
                "Identify the type of optical system",
                "Draw a ray diagram",
                "Apply Snell's law for refraction",
                "Use lens/mirror equations",
                "Calculate image position and magnification"
            ],
            PhysicsDomain.ELECTROMAGNETISM: [
                "Identify the type of circuit or field",
                "Apply relevant circuit laws (Ohm's, Kirchhoff's)",
                "Calculate equivalent resistance/capacitance",
                "Solve for current, voltage, or power"
            ]
        }
        
        return {
            "domain": problem.domain.value,
            "steps": strategies.get(problem.domain, ["Analyze the problem", "Identify relevant principles", "Apply formulas", "Solve for unknowns"])
        }
    
    def _check_misconceptions(self, problem: PhysicsProblem) -> List[str]:
        """Check for potential misconceptions in a problem."""
        misconceptions = []
        description_lower = problem.description.lower()
        
        for category, items in self._common_misconceptions.items():
            for misconception in items:
                # Check if the problem might lead to this misconception
                if any(keyword in description_lower for keyword in misconception.split()[:2]):
                    misconceptions.append({
                        "category": category,
                        "misconception": misconception,
                        "warning": "Be careful not to fall into this common misconception"
                    })
        
        return misconceptions
    
    def _check_dimensional_consistency(self, problem: PhysicsProblem) -> DimensionalAnalysis:
        """Check dimensional consistency of a problem."""
        # Simplified dimensional analysis
        given = problem.given
        
        # Check for common patterns
        has_length = any(k in given for k in ["position", "distance", "height", "x", "y", "z"])
        has_time = any(k in given for k in ["time", "t"])
        has_mass = any(k in given for k in ["mass", "m"])
        
        if has_length and has_time:
            return DimensionalAnalysis(
                is_consistent=True,
                derived_unit="m/s" if has_length and has_time else "m",
                expected_unit="velocity" if has_length and has_time else "distance",
                check_details=["Length and time dimensions are consistent"]
            )
        
        return DimensionalAnalysis(
            is_consistent=True,
            check_details=["Dimensional analysis pending detailed formula check"]
        )
    
    # ==================== SOLUTION GENERATION ====================
    
    def generate_solution(
        self,
        problem: PhysicsProblem
    ) -> PhysicsSolution:
        """
        Generate a step-by-step solution for a physics problem.
        
        Args:
            problem: PhysicsProblem to solve
            
        Returns:
            Complete PhysicsSolution object
        """
        solution = PhysicsSolution(
            solution_id=f"sol_{problem.problem_id}",
            problem_id=problem.problem_id,
            status=SolutionStatus.SOLVED
        )
        
        # Generate solution based on problem domain and type
        if problem.domain == PhysicsDomain.MECHANICS:
            self._solve_mechanics_problem(problem, solution)
        elif problem.domain == PhysicsDomain.OPTICS:
            self._solve_optics_problem(problem, solution)
        elif problem.domain == PhysicsDomain.ELECTROMAGNETISM:
            self._solve_electromagnetism_problem(problem, solution)
        else:
            self._generate_generic_solution(problem, solution)
        
        # Verify solution
        solution.verification = self._verify_solution(problem, solution)
        
        return solution
    
    def _solve_mechanics_problem(
        self,
        problem: PhysicsProblem,
        solution: PhysicsSolution
    ) -> None:
        """Solve a mechanics problem."""
        given = problem.given
        
        # Check for kinematic problem
        if all(k in given for k in ["initial_velocity", "acceleration", "time"]):
            self._solve_kinematics(given, solution)
        
        # Check for projectile motion
        elif "initial_speed" in given and "launch_angle" in given:
            self._solve_projectile_motion(given, solution)
        
        # Check for energy problem
        elif any(k in given for k in ["mass", "velocity"]) and any(k in given for k in ["height", "potential_energy"]):
            self._solve_energy_problem(given, solution)
        
        # Check for collision problem
        elif all(k in given for k in ["mass1", "mass2", "velocity1", "velocity2"]):
            self._solve_collision(given, solution)
        
        else:
            self._generate_generic_solution(problem, solution)
    
    def _solve_kinematics(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve a kinematics problem."""
        v0 = given.get("initial_velocity", 0)
        a = given.get("acceleration", 0)
        t = given.get("time", 0)
        
        # Step 1: Identify given quantities
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Identify known quantities from the problem",
            variables={
                "v₀ (initial velocity)": v0,
                "a (acceleration)": a,
                "t (time)": t
            },
            explanation="These are the quantities given in the problem statement"
        ))
        
        # Step 2: Select appropriate equation
        solution.steps.append(SolutionStep(
            step_number=2,
            description="Select the kinematic equation for final velocity",
            formula="v = v₀ + at",
            explanation="This equation relates velocity, initial velocity, acceleration, and time"
        ))
        
        # Step 3: Calculate final velocity
        v = v0 + a * t
        solution.steps.append(SolutionStep(
            step_number=3,
            description="Calculate final velocity",
            formula="v = v₀ + at",
            variables={"v₀": v0, "a": a, "t": t},
            result=v,
            unit="m/s",
            explanation=f"Substitute values: v = {v0} + {a} × {t} = {v}"
        ))
        
        # Step 4: Calculate displacement if needed
        if "unknown" in given and "displacement" in str(given):
            d = v0 * t + 0.5 * a * t**2
            solution.steps.append(SolutionStep(
                step_number=4,
                description="Calculate displacement",
                formula="Δx = v₀t + ½at²",
                variables={"v₀": v0, "a": a, "t": t},
                result=d,
                unit="m",
                explanation=f"Substitute values: Δx = {v0} × {t} + 0.5 × {a} × {t}² = {d}"
            ))
        
        solution.final_answers["final_velocity"] = v
        solution.units["final_velocity"] = "m/s"
    
    def _solve_projectile_motion(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve a projectile motion problem."""
        v0 = given.get("initial_speed", 0)
        angle = given.get("launch_angle", 0)
        g = given.get("gravity", 9.81)
        h0 = given.get("initial_height", 0)
        
        # Step 1: Decompose initial velocity
        angle_rad = radians(angle)
        v0x = v0 * cos(angle_rad)
        v0y = v0 * sin(angle_rad)
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Decompose initial velocity into components",
            formula="v₀ₓ = v₀cos(θ), v₀ᵧ = v₀sin(θ)",
            variables={"v₀": v0, "θ": angle},
            explanation=f"Horizontal: {v0} × cos({angle}°) = {v0x:.2f} m/s, Vertical: {v0} × sin({angle}°) = {v0y:.2f} m/s"
        ))
        
        # Step 2: Calculate time of flight
        t_flight = 2 * v0y / g if h0 == 0 else self._calculate_time_of_flight(v0y, g, h0)
        
        solution.steps.append(SolutionStep(
            step_number=2,
            description="Calculate time of flight",
            formula="t = 2v₀ᵧ/g (for level ground)",
            variables={"v₀ᵧ": v0y, "g": g},
            result=t_flight,
            unit="s",
            explanation=f"Time to reach maximum height is v₀ᵧ/g, so total time is 2v₀ᵧ/g = {t_flight:.2f} s"
        ))
        
        # Step 3: Calculate maximum height
        h_max = h0 + (v0y**2) / (2 * g)
        
        solution.steps.append(SolutionStep(
            step_number=3,
            description="Calculate maximum height",
            formula="H = h₀ + v₀ᵧ²/(2g)",
            variables={"h₀": h0, "v₀ᵧ": v0y, "g": g},
            result=h_max,
            unit="m",
            explanation=f"At maximum height, vertical velocity is zero. Using v² = v₀ᵧ² - 2g(H - h₀)"
        ))
        
        # Step 4: Calculate horizontal range
        range_val = v0x * t_flight
        
        solution.steps.append(SolutionStep(
            step_number=4,
            description="Calculate horizontal range",
            formula="R = v₀ₓ × t",
            variables={"v₀ₓ": v0x, "t": t_flight},
            result=range_val,
            unit="m",
            explanation="Horizontal motion is uniform (no acceleration)"
        ))
        
        solution.final_answers = {
            "time_of_flight": t_flight,
            "max_height": h_max,
            "range": range_val,
            "initial_velocity_x": v0x,
            "initial_velocity_y": v0y
        }
        solution.units = {
            "time_of_flight": "s",
            "max_height": "m",
            "range": "m",
            "initial_velocity_x": "m/s",
            "initial_velocity_y": "m/s"
        }
    
    def _solve_energy_problem(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve an energy conservation problem."""
        m = given.get("mass", 0)
        v = given.get("velocity", 0)
        h = given.get("height", 0)
        g = given.get("gravity", 9.81)
        
        # Calculate kinetic energy
        ke = 0.5 * m * v**2
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Calculate kinetic energy",
            formula="K = ½mv²",
            variables={"m": m, "v": v},
            result=ke,
            unit="J",
            explanation="Kinetic energy depends on mass and speed"
        ))
        
        # Calculate potential energy
        pe = m * g * h
        
        solution.steps.append(SolutionStep(
            step_number=2,
            description="Calculate gravitational potential energy",
            formula="U = mgh",
            variables={"m": m, "g": g, "h": h},
            result=pe,
            unit="J",
            explanation="Gravitational potential energy depends on mass, gravity, and height"
        ))
        
        # Total mechanical energy
        total = ke + pe
        
        solution.steps.append(SolutionStep(
            step_number=3,
            description="Calculate total mechanical energy",
            formula="E = K + U",
            variables={"K": ke, "U": pe},
            result=total,
            unit="J",
            explanation="Total mechanical energy is the sum of kinetic and potential energy"
        ))
        
        solution.final_answers = {
            "kinetic_energy": ke,
            "potential_energy": pe,
            "total_energy": total
        }
        solution.units = {
            "kinetic_energy": "J",
            "potential_energy": "J",
            "total_energy": "J"
        }
    
    def _solve_collision(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve a collision problem."""
        m1 = given.get("mass1", 0)
        m2 = given.get("mass2", 0)
        v1 = given.get("velocity1", 0)
        v2 = given.get("velocity2", 0)
        
        # Initial momentum
        p_initial = m1 * v1 + m2 * v2
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Calculate initial total momentum",
            formula="p_initial = m₁v₁ + m₂v₂",
            variables={"m₁": m1, "v₁": v1, "m₂": m2, "v₂": v2},
            result=p_initial,
            unit="kg·m/s",
            explanation="Momentum is conserved in isolated systems"
        ))
        
        # Elastic collision velocities
        if given.get("elastic", True):
            v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
            v2f = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
            
            solution.steps.append(SolutionStep(
                step_number=2,
                description="Calculate final velocities (elastic collision)",
                formula="v₁f = [(m₁-m₂)v₁ + 2m₂v₂]/(m₁+m₂)",
                variables={"m₁": m1, "m₂": m2, "v₁": v1, "v₂": v2},
                result=v1f,
                unit="m/s",
                explanation="For elastic collisions, both momentum and kinetic energy are conserved"
            ))
            
            solution.steps.append(SolutionStep(
                step_number=3,
                description="Calculate final velocity of second object",
                formula="v₂f = [(m₂-m₁)v₂ + 2m₁v₁]/(m₁+m₂)",
                variables={"m₁": m1, "m₂": m2, "v₁": v1, "v₂": v2},
                result=v2f,
                unit="m/s"
            ))
        
        solution.final_answers = {
            "initial_momentum": p_initial,
            "final_velocity_1": v1f if given.get("elastic", True) else None,
            "final_velocity_2": v2f if given.get("elastic", True) else None
        }
        solution.units = {
            "initial_momentum": "kg·m/s",
            "final_velocity_1": "m/s",
            "final_velocity_2": "m/s"
        }
    
    def _solve_optics_problem(
        self,
        problem: PhysicsProblem,
        solution: PhysicsSolution
    ) -> None:
        """Solve an optics problem."""
        given = problem.given
        
        if "refractive_index" in given:
            self._solve_refraction(given, solution)
        elif "focal_length" in given:
            self._solve_lens_problem(given, solution)
        else:
            self._generate_generic_solution(problem, solution)
    
    def _solve_refraction(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve a refraction problem using Snell's law."""
        n1 = given.get("n1", 1.0)
        n2 = given.get("n2", 1.5)
        theta1 = given.get("theta1", 0)
        
        theta1_rad = radians(theta1)
        
        # Snell's law: n1 * sin(theta1) = n2 * sin(theta2)
        sin_theta2 = n1 * sin(theta1_rad) / n2
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Apply Snell's law",
            formula="n₁sin(θ₁) = n₂sin(θ₂)",
            variables={"n₁": n1, "n₂": n2, "θ₁": theta1},
            explanation="Snell's law relates the angles of incidence and refraction to the refractive indices"
        ))
        
        if sin_theta2 <= 1:
            theta2 = degrees(asin(sin_theta2))
            
            solution.steps.append(SolutionStep(
                step_number=2,
                description="Calculate angle of refraction",
                formula="θ₂ = arcsin(n₁sin(θ₁)/n₂)",
                variables={"n₁": n1, "n₂": n2, "θ₁": theta1},
                result=theta2,
                unit="degrees",
                explanation=f"sin(θ₂) = {n1} × sin({theta1}°) / {n2} = {sin_theta2:.4f}"
            ))
            
            solution.final_answers = {"theta2": theta2}
            solution.units = {"theta2": "degrees"}
        else:
            solution.steps.append(SolutionStep(
                step_number=2,
                description="Check for total internal reflection",
                formula="sin(θ₂) > 1",
                variables={"value": sin_theta2},
                result=None,
                explanation=f"Since sin(θ₂) = {sin_theta2:.4f} > 1, total internal reflection occurs"
            ))
            
            solution.status = SolutionStatus.PARTIAL
    
    def _solve_lens_problem(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve a lens problem."""
        f = given.get("focal_length", 0)
        do = given.get("object_distance", 0)
        
        # Lens equation: 1/f = 1/do + 1/di
        di = 1 / (1/f - 1/do) if do != f else float('inf')
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Apply thin lens equation",
            formula="1/f = 1/d₀ + 1/dᵢ",
            variables={"f": f, "d₀": do},
            explanation="The thin lens equation relates focal length, object distance, and image distance"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=2,
            description="Calculate image distance",
            formula="dᵢ = 1/(1/f - 1/d₀)",
            variables={"f": f, "d₀": do},
            result=di if di != float('inf') else None,
            unit="units of distance",
            explanation=f"dᵢ = 1/(1/{f} - 1/{do}) = {di if di != float('inf') else 'infinite'}"
        ))
        
        # Magnification
        if di != float('inf'):
            m = -di / do
            solution.steps.append(SolutionStep(
                step_number=3,
                description="Calculate magnification",
                formula="M = -dᵢ/d₀",
                variables={"dᵢ": di, "d₀": do},
                result=m,
                explanation=f"Magnification is {abs(m):.2f}x, {'inverted' if m < 0 else 'upright'}"
            ))
            
            solution.final_answers = {
                "image_distance": di,
                "magnification": m
            }
            solution.units = {
                "image_distance": "same as distance units",
                "magnification": "unitless"
            }
    
    def _solve_electromagnetism_problem(
        self,
        problem: PhysicsProblem,
        solution: PhysicsSolution
    ) -> None:
        """Solve an electromagnetism problem."""
        given = problem.given
        
        if "resistance" in given and "voltage" in given:
            self._solve_circuit_problem(given, solution)
        elif "charge" in given and "distance" in given:
            self._solve_electrostatics(given, solution)
        else:
            self._generate_generic_solution(problem, solution)
    
    def _solve_circuit_problem(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve a circuit problem using Ohm's law."""
        V = given.get("voltage", 0)
        R = given.get("resistance", 0)
        
        # Ohm's law: V = IR
        I = V / R if R != 0 else 0
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Apply Ohm's law",
            formula="V = IR",
            variables={"V": V, "R": R},
            explanation="Ohm's law relates voltage, current, and resistance"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=2,
            description="Calculate current",
            formula="I = V/R",
            variables={"V": V, "R": R},
            result=I,
            unit="A",
            explanation=f"Current = {V} V / {R} Ω = {I:.4f} A"
        ))
        
        # Power
        P = V * I
        
        solution.steps.append(SolutionStep(
            step_number=3,
            description="Calculate power dissipated",
            formula="P = VI",
            variables={"V": V, "I": I},
            result=P,
            unit="W",
            explanation=f"Power = {V} V × {I:.4f} A = {P:.4f} W"
        ))
        
        solution.final_answers = {
            "current": I,
            "power": P
        }
        solution.units = {
            "current": "A",
            "power": "W"
        }
    
    def _solve_electrostatics(
        self,
        given: Dict[str, Any],
        solution: PhysicsSolution
    ) -> None:
        """Solve an electrostatics problem using Coulomb's law."""
        q1 = given.get("charge1", 0)
        q2 = given.get("charge2", 0)
        r = given.get("distance", 1)
        k = PhysicsConstants.COULOMB_CONSTANT
        
        # Coulomb's law: F = k * q1 * q2 / r^2
        F = k * abs(q1 * q2) / r**2
        
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Apply Coulomb's law",
            formula="F = k|q₁q₂|/r²",
            variables={"k": f"{k:.2e}", "q₁": q1, "q₂": q2, "r": r},
            explanation="Coulomb's law gives the force between two point charges"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=2,
            description="Calculate electrostatic force",
            formula="F = k|q₁q₂|/r²",
            variables={"k": k, "q₁": q1, "q₂": q2, "r": r},
            result=F,
            unit="N",
            explanation=f"F = {k:.2e} × |{q1} × {q2}| / {r}² = {F:.4e} N"
        ))
        
        solution.final_answers = {"force": F}
        solution.units = {"force": "N"}
    
    def _calculate_time_of_flight(
        self,
        v0y: float,
        g: float,
        h0: float
    ) -> float:
        """Calculate time of flight with initial height."""
        # h = h0 + v0y*t - 0.5*g*t^2
        # Solve quadratic: 0.5*g*t^2 - v0y*t - h0 = 0
        a = 0.5 * g
        b = -v0y
        c = -h0
        
        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            t1 = (-b + sqrt(discriminant)) / (2 * a)
            t2 = (-b - sqrt(discriminant)) / (2 * a)
            return max(t1, t2) if t1 > 0 else t2 if t2 > 0 else 0
        
        return 0
    
    def _generate_generic_solution(
        self,
        problem: PhysicsProblem,
        solution: PhysicsSolution
    ) -> None:
        """Generate a generic solution approach."""
        solution.steps.append(SolutionStep(
            step_number=1,
            description="Analyze the problem",
            explanation="Identify the type of problem and relevant physics principles"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=2,
            description="List known quantities",
            variables=problem.given,
            explanation="Extract all given values from the problem statement"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=3,
            description="Identify what to find",
            explanation=f"Unknown quantities: {', '.join(problem.unknown)}"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=4,
            description="Apply relevant formulas",
            explanation="Select appropriate equations based on the physics principles involved"
        ))
        
        solution.steps.append(SolutionStep(
            step_number=5,
            description="Solve for unknowns",
            explanation="Substitute known values and solve for the unknown quantities"
        ))
        
        solution.status = SolutionStatus.NEEDS_REVIEW
    
    # ==================== VERIFICATION ====================
    
    def _verify_solution(
        self,
        problem: PhysicsProblem,
        solution: PhysicsSolution
    ) -> Dict[str, Any]:
        """Verify a physics solution."""
        verification = {
            "is_valid": True,
            "checks": []
        }
        
        # Check 1: All unknowns found
        if solution.final_answers:
            found_count = sum(1 for u in problem.unknown if u in solution.final_answers)
            if found_count < len(problem.unknown):
                verification["checks"].append({
                    "check": "unknowns_found",
                    "status": "warning",
                    "message": f"Found {found_count}/{len(problem.unknown)} unknowns"
                })
                verification["is_valid"] = found_count > 0
            else:
                verification["checks"].append({
                    "check": "unknowns_found",
                    "status": "pass",
                    "message": "All unknowns have been calculated"
                })
        
        # Check 2: Units are consistent
        for var, unit in solution.units.items():
            if not unit or unit == "":
                verification["checks"].append({
                    "check": "units",
                    "status": "warning",
                    "message": f"Missing unit for {var}"
                })
        
        # Check 3: Answers are physically reasonable
        for var, value in solution.final_answers.items():
            if value is None:
                continue
                
            if abs(value) > 1e15:
                verification["checks"].append({
                    "check": "magnitude",
                    "status": "warning",
                    "message": f"{var} = {value:.2e} is very large"
                })
            elif abs(value) < 1e-10 and value != 0:
                verification["checks"].append({
                    "check": "magnitude",
                    "status": "info",
                    "message": f"{var} is essentially zero"
                })
        
        # Check 4: Negative values where inappropriate
        for var, value in solution.final_answers.items():
            if value is None:
                continue
                
            if var in ["mass", "distance", "time", "height"] and value < 0:
                verification["checks"].append({
                    "check": "negative_values",
                    "status": "fail",
                    "message": f"{var} = {value} is negative but should be positive"
                })
                verification["is_valid"] = False
        
        if verification["is_valid"]:
            verification["checks"].append({
                "check": "overall",
                "status": "pass",
                "message": "Solution appears valid"
            })
        
        return verification
    
    # ==================== EXPLANATION GENERATION ====================
    
    def explain_concept(
        self,
        concept: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive explanation of a physics concept.
        
        Args:
            concept: Concept to explain
            context: Optional context for the explanation
            
        Returns:
            Dictionary with explanation components
        """
        # Check if it's a principle
        if concept in self._principles:
            principle = self._principles[concept]
            return {
                "concept": concept,
                "type": "principle",
                "statement": principle["statement"],
                "formula": principle.get("formula", ""),
                "conditions": principle.get("conditions", []),
                "applications": principle.get("applications", [])
            }
        
        # Check if it's a formula
        formula = self._formula_registry.get_formula(concept)
        if formula:
            return {
                "concept": formula.name,
                "type": "formula",
                "description": formula.description,
                "latex": formula.latex,
                "variables": formula.variables,
                "conditions": formula.conditions
            }
        
        # Generic concept explanation
        return {
            "concept": concept,
            "type": "concept",
            "explanation": f"Understanding {concept} requires applying the relevant physics principles.",
            "related_principles": [
                p for p in self._principles.keys()
                if concept.lower() in p.lower() or any(concept.lower() in str(v).lower() 
                for v in self._principles[p].get("applications", []))
            ][:3]
        }
    
    def compare_solutions(
        self,
        solutions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare multiple solution approaches.
        
        Args:
            solutions: List of solution dictionaries
            
        Returns:
            Comparison analysis
        """
        if len(solutions) < 2:
            return {"error": "At least two solutions needed for comparison"}
        
        comparison = {
            "num_solutions": len(solutions),
            "approaches": [],
            "tradeoffs": [],
            "recommendation": None
        }
        
        # Analyze each approach
        for i, sol in enumerate(solutions):
            approach = {
                "solution_id": i,
                "steps_count": sol.get("steps", []).__len__() if isinstance(sol.get("steps"), list) else 0,
                "formulas_used": sol.get("formulas", []).__len__() if isinstance(sol.get("formulas"), list) else 0,
                "assumptions": sol.get("assumptions", [])
            }
            comparison["approaches"].append(approach)
        
        # Identify tradeoffs
        comparison["tradeoffs"] = [
            "Different approaches may have different computational complexity",
            "Some approaches may require more approximations",
            "Choice of approach depends on given information"
        ]
        
        # Recommend best approach
        if comparison["approaches"]:
            best = min(comparison["approaches"], key=lambda x: x["steps_count"])
            comparison["recommendation"] = {
                "solution_id": best["solution_id"],
                "reason": "Fewest steps, most direct approach"
            }
        
        return comparison
    
    def get_similar_problems(
        self,
        problem: PhysicsProblem,
        count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get similar problems for practice.
        
        Args:
            problem: Reference problem
            count: Number of similar problems to return
            
        Returns:
            List of similar problem summaries
        """
        # Generate similar problems based on domain and concepts
        similar = []
        
        template_problems = {
            PhysicsDomain.MECHANICS: [
                {"title": "Kinematics Problem", "difficulty": 1, "type": "motion"},
                {"title": "Force Analysis", "difficulty": 2, "type": "dynamics"},
                {"title": "Energy Conservation", "difficulty": 2, "type": "energy"},
                {"title": "Collision Problem", "difficulty": 3, "type": "momentum"},
                {"title": "Projectile Motion", "difficulty": 2, "type": "kinematics"}
            ],
            PhysicsDomain.OPTICS: [
                {"title": "Refraction Problem", "difficulty": 2, "type": "refraction"},
                {"title": "Lens System", "difficulty": 3, "type": "lenses"},
                {"title": "Mirror Problem", "difficulty": 2, "type": "mirrors"},
                {"title": "Interference", "difficulty": 3, "type": "wave_optics"},
                {"title": "Total Internal Reflection", "difficulty": 2, "type": "refraction"}
            ],
            PhysicsDomain.ELECTROMAGNETISM: [
                {"title": "Circuit Analysis", "difficulty": 2, "type": "circuits"},
                {"title": "Force Between Charges", "difficulty": 2, "type": "electrostatics"},
                {"title": "Magnetic Field", "difficulty": 3, "type": "magnetism"},
                {"title": "Induction Problem", "difficulty": 3, "type": "induction"},
                {"title": "RC Circuit", "difficulty": 2, "type": "circuits"}
            ]
        }
        
        domain_problems = template_problems.get(problem.domain, [])
        similar = [
            {
                "problem_id": f"similar_{i}",
                "title": p["title"],
                "difficulty": p["difficulty"],
                "type": p["type"],
                "domain": problem.domain.value
            }
            for i, p in enumerate(domain_problems[:count])
        ]
        
        return similar
