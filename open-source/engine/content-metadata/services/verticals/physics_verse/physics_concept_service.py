"""
PhysicsVerse Concept Service

This module provides the PhysicsVerse-specific concept service implementation,
extending the base concept service with physics domain functionality including
formula management, unit conversions, physical law verification, and educational
content delivery for mechanics, optics, and electromagnetism.

Licensed under the Apache License, Version 2.0
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

from ....extensions.service_extension_base import (
    ConceptServiceExtension,
    ExtensionContext
)
from .physics_core import (
    Vector2D,
    Vector3D,
    PhysicsState,
    PhysicsConstants,
    UnitConverter,
    PhysicsFormula,
    PhysicsFormulaRegistry,
    calculate_kinematic_motion,
    calculate_projectile_motion,
    calculate_orbit_parameters,
    calculate_shm_parameters,
    calculate_wave_properties,
    calculate_rc_circuit,
    calculate_rlc_circuit
)

logger = logging.getLogger(__name__)


class PhysicsDomain(Enum):
    """Physics domains for categorization."""
    MECHANICS = "mechanics"
    OPTICS = "optics"
    ELECTROMAGNETISM = "electromagnetism"
    THERMODYNAMICS = "thermodynamics"
    WAVE_PHYSICS = "wave_physics"
    MODERN_PHYSICS = "modern_physics"


class MechanicsSubdomain(Enum):
    """Subdomains within mechanics."""
    KINEMATICS = "kinematics"
    DYNAMICS = "dynamics"
    ENERGY = "energy"
    ROTATIONAL_MOTION = "rotational_motion"
    GRAVITATION = "gravitation"
    FLUIDS = "fluids"
    VIBRATIONS = "vibrations"


class OpticsSubdomain(Enum):
    """Subdomains within optics."""
    GEOMETRIC_OPTICS = "geometric_optics"
    WAVE_OPTICS = "wave_optics"
    PHOTOMETRY = "photometry"
    LASER_PHYSICS = "laser_physics"


class ElectromagnetismSubdomain(Enum):
    """Subdomains within electromagnetism."""
    ELECTROSTATICS = "electrostatics"
    CIRCUITS = "circuits"
    MAGNETISM = "magnetism"
    ELECTROMAGNETIC_INDUCTION = "electromagnetic_induction"
    ELECTROMAGNETIC_WAVES = "electromagnetic_waves"


class PhysicsConceptType(Enum):
    """Types of physics concepts."""
    PRINCIPLE = "principle"
    LAW = "law"
    THEOREM = "theorem"
    FORMULA = "formula"
    DEFINITION = "definition"
    PHENOMENON = "phenomenon"
    EXPERIMENT = "experiment"


@dataclass
class PhysicsParameter:
    """
    Represents a physical parameter with value and unit.
    
    Attributes:
        name: Parameter name
        symbol: Mathematical symbol
        value: Numerical value
        unit: Unit string
        uncertainty: Measurement uncertainty
        description: Parameter description
    """
    name: str
    symbol: str
    value: float
    unit: str
    uncertainty: float = 0.0
    description: str = ""


@dataclass
class PhysicsProblem:
    """
    Represents a physics problem for analysis.
    
    Attributes:
        problem_id: Unique identifier
        domain: Physics domain
        subdomain: Specific subdomain
        difficulty: Difficulty level (1-5)
        description: Problem description
        given_parameters: List of given parameters
        unknown_parameters: Parameters to find
        constraints: Physical constraints
        initial_conditions: Initial state conditions
        goal: Problem goal description
    """
    problem_id: str
    domain: PhysicsDomain
    subdomain: str
    difficulty: int
    description: str
    given_parameters: List[PhysicsParameter] = field(default_factory=list)
    unknown_parameters: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    initial_conditions: Dict[str, Any] = field(default_factory=dict)
    goal: str = ""


@dataclass
class PhysicsSolution:
    """
    Represents a solution to a physics problem.
    
    Attributes:
        solution_id: Unique identifier
        problem_id: Reference to problem
        steps: List of solution steps
        formulas_used: List of formulas used
        final_answer: Final numerical answer
        units: Unit of final answer
        verification: Verification results
        alternative_methods: Alternative solution approaches
    """
    solution_id: str
    problem_id: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    formulas_used: List[str] = field(default_factory=list)
    final_answer: float = 0.0
    units: str = ""
    verification: Dict[str, Any] = field(default_factory=dict)
    alternative_methods: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PhysicsConcept:
    """
    Represents a physics concept for educational display.
    
    Attributes:
        concept_id: Unique identifier
        name: Concept name
        concept_type: Type of concept
        domain: Physics domain
        subdomain: Specific subdomain
        description: Concept description
        formula: Associated formula (if applicable)
        variables: Dictionary of variables
        examples: Example problems and solutions
        misconceptions: Common misconceptions
        related_concepts: Related concept IDs
    """
    concept_id: str
    name: str
    concept_type: PhysicsConceptType
    domain: PhysicsDomain
    subdomain: str
    description: str
    formula: Optional[str] = None
    variables: Dict[str, str] = field(default_factory=dict)
    examples: List[Dict[str, Any]] = field(default_factory=list)
    misconceptions: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)


@dataclass
class PhysicsVisualConfig:
    """Configuration for physics visualizations."""
    show_vectors: bool = True
    show_forces: bool = True
    show_trajectories: bool = True
    show_fields: bool = False
    show_grid: bool = True
    scale_factor: float = 1.0
    vector_scale: float = 1.0
    time_scale: float = 1.0


class PhysicsVerseConceptService:
    """
    PhysicsVerse-specific concept service.
    
    This service handles physics concept processing including:
    - Formula management and validation
    - Problem analysis and solution
    - Unit conversion and dimensional analysis
    - Physics concept retrieval and explanation
    - Interactive problem solving
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the PhysicsVerse concept service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._formula_registry = PhysicsFormulaRegistry()
        self._concepts = self._initialize_concepts()
        self._visual_config = PhysicsVisualConfig()
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        if "visual_config" in config:
            self._visual_config = PhysicsVisualConfig(**config["visual_config"])
        logger.info("PhysicsVerseConceptService configured with settings: %s", list(config.keys()))
    
    def _initialize_concepts(self) -> Dict[str, PhysicsConcept]:
        """Initialize the physics concepts database."""
        return {
            # Mechanics Concepts
            "newtons_first_law": PhysicsConcept(
                concept_id="newtons_first_law",
                name="Newton's First Law of Motion",
                concept_type=PhysicsConceptType.LAW,
                domain=PhysicsDomain.MECHANICS,
                subdomain=MechanicsSubdomain.DYNAMICS.value,
                description="An object at rest stays at rest and an object in motion stays in motion with the same speed and direction, unless acted upon by an unbalanced force.",
                formula="ΣF = 0 ⇒ a = 0",
                variables={"ΣF": "net force", "a": "acceleration"},
                examples=[{
                    "scenario": "A book sliding on a table eventually stops",
                    "explanation": "Frictional force provides the unbalanced force that causes deceleration"
                }],
                misconceptions=[
                    "Objects need continuous force to keep moving",
                    "Stationary objects have no forces acting on them"
                ],
                related_concepts=["newtons_second_law", "inertia"]
            ),
            "newtons_second_law": PhysicsConcept(
                concept_id="newtons_second_law",
                name="Newton's Second Law of Motion",
                concept_type=PhysicsConceptType.LAW,
                domain=PhysicsDomain.MECHANICS,
                subdomain=MechanicsSubdomain.DYNAMICS.value,
                description="The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.",
                formula="F = ma",
                variables={"F": "net force", "m": "mass", "a": "acceleration"},
                examples=[{
                    "scenario": "Pushing two shopping carts of different masses",
                    "explanation": "The heavier cart accelerates less for the same push force"
                }],
                misconceptions=[
                    "Heavier objects fall faster",
                    "Force causes motion (not acceleration)"
                ],
                related_concepts=["newtons_first_law", "newtons_third_law", "mass"]
            ),
            "kinetic_energy": PhysicsConcept(
                concept_id="kinetic_energy",
                name="Kinetic Energy",
                concept_type=PhysicsConceptType.DEFINITION,
                domain=PhysicsDomain.MECHANICS,
                subdomain=MechanicsSubdomain.ENERGY.value,
                description="The energy that an object possesses due to its motion. It is defined as one-half the product of mass and the square of velocity.",
                formula="K = ½mv²",
                variables={"K": "kinetic energy", "m": "mass", "v": "speed"},
                examples=[{
                    "problem": "A 2 kg ball moving at 3 m/s",
                    "solution": "K = ½ × 2 × 3² = 9 J"
                }],
                related_concepts=["potential_energy", "work", "momentum"]
            ),
            "projectile_motion": PhysicsConcept(
                concept_id="projectile_motion",
                name="Projectile Motion",
                concept_type=PhysicsConceptType.PHENOMENON,
                domain=PhysicsDomain.MECHANICS,
                subdomain=MechanicsSubdomain.KINEMATICS.value,
                description="The motion of an object thrown or projected into the air, subject to only the acceleration of gravity. The horizontal and vertical motions are independent.",
                formula="x(t) = v₀cos(θ)t, y(t) = v₀sin(θ)t - ½gt²",
                variables={"v₀": "initial speed", "θ": "launch angle", "g": "gravitational acceleration"},
                examples=[{
                    "problem": "A ball thrown at 20 m/s at 45°",
                    "solution": "Range = 20²/g ≈ 40.8 m"
                }],
                misconceptions=[
                    "The fastest path is always the best trajectory",
                    "Gravity affects horizontal motion"
                ],
                related_concepts=["free_fall", "trajectory", "conservation_of_energy"]
            ),
            
            # Optics Concepts
            "snells_law": PhysicsConcept(
                concept_id="snells_law",
                name="Snell's Law of Refraction",
                concept_type=PhysicsConceptType.LAW,
                domain=PhysicsDomain.OPTICS,
                subdomain=OpticsSubdomain.GEOMETRIC_OPTICS.value,
                description="Relates the angles of incidence and refraction when light passes between two media with different refractive indices.",
                formula="n₁sin(θ₁) = n₂sin(θ₂)",
                variables={"n₁": "refractive index of first medium", "θ₁": "angle of incidence", "n₂": "refractive index of second medium", "θ₂": "angle of refraction"},
                examples=[{
                    "problem": "Light enters water (n=1.33) from air (n=1.0) at 30°",
                    "solution": "sin(θ₂) = sin(30°)/1.33 ⇒ θ₂ ≈ 22°"
                }],
                related_concepts=["total_internal_reflection", "critical_angle", "refractive_index"]
            ),
            "lens_maker_equation": PhysicsConcept(
                concept_id="lens_maker_equation",
                name="Lens Maker's Equation",
                concept_type=PhysicsConceptType.FORMULA,
                domain=PhysicsDomain.OPTICS,
                subdomain=OpticsSubdomain.GEOMETRIC_OPTICS.value,
                description="Relates the focal length of a lens to its refractive index and the radii of curvature of its surfaces.",
                formula="1/f = (n-1)(1/R₁ - 1/R₂)",
                variables={"f": "focal length", "n": "refractive index", "R₁": "radius of first surface", "R₂": "radius of second surface"},
                related_concepts=["thin_lens", "focal_point", "magnification"]
            ),
            
            # Electromagnetism Concepts
            "coulombs_law": PhysicsConcept(
                concept_id="coulombs_law",
                name="Coulomb's Law",
                concept_type=PhysicsConceptType.LAW,
                domain=PhysicsDomain.ELECTROMAGNETISM,
                subdomain=ElectromagnetismSubdomain.ELECTROSTATICS.value,
                description="Describes the electrostatic interaction between electrically charged particles. The force is directly proportional to the product of charges and inversely proportional to the square of distance.",
                formula="F = kq₁q₂/r²",
                variables={"F": "electrostatic force", "k": "Coulomb constant", "q₁": "first charge", "q₂": "second charge", "r": "distance"},
                examples=[{
                    "problem": "Two 1 C charges 1 m apart",
                    "solution": "F = 9×10⁹ N (enormous force!)"
                }],
                misconceptions=[
                    "Coulomb's law and gravity are the same type of force",
                    "Electric force always repels"
                ],
                related_concepts=["electric_field", "electric_potential", "superposition"]
            ),
            "ohms_law": PhysicsConcept(
                concept_id="ohms_law",
                name="Ohm's Law",
                concept_type=PhysicsConceptType.LAW,
                domain=PhysicsDomain.ELECTROMAGNETISM,
                subdomain=ElectromagnetismSubdomain.CIRCUITS.value,
                description="States that the current through a conductor between two points is directly proportional to the voltage across the two points, for constant temperature and material properties.",
                formula="V = IR",
                variables={"V": "voltage", "I": "current", "R": "resistance"},
                examples=[{
                    "problem": "A 10 Ω resistor with 5 V across it",
                    "solution": "I = 5/10 = 0.5 A"
                }],
                misconceptions=[
                    "Ohm's law applies to all materials",
                    "Voltage and current are the same thing"
                ],
                related_concepts=["resistance", "power", "circuit_analysis"]
            ),
            "faraday_law": PhysicsConcept(
                concept_id="faraday_law",
                name="Faraday's Law of Induction",
                concept_type=PhysicsConceptType.LAW,
                domain=PhysicsDomain.ELECTROMAGNETISM,
                subdomain=ElectromagnetismSubdomain.ELECTROMAGNETIC_INDUCTION.value,
                description="Describes how a time-varying magnetic field induces an electromotive force (EMF) in a circuit. The induced EMF is equal to the negative rate of change of magnetic flux.",
                formula="ℰ = -dΦ/dt",
                variables={"ℰ": "induced EMF", "Φ": "magnetic flux", "t": "time"},
                examples=[{
                    "scenario": "Moving a magnet through a coil",
                    "explanation": "The changing magnetic flux induces a voltage in the coil"
                }],
                related_concepts=["lenz_law", "magnetic_flux", "transformer"]
            )
        }
    
    # ==================== FORMULA MANAGEMENT ====================
    
    def get_formula(self, formula_id: str) -> Optional[PhysicsFormula]:
        """
        Retrieve a physics formula by ID.
        
        Args:
            formula_id: Unique formula identifier
            
        Returns:
            PhysicsFormula object or None if not found
        """
        return self._formula_registry.get_formula(formula_id)
    
    def get_formulas_by_domain(
        self,
        domain: PhysicsDomain
    ) -> Dict[str, PhysicsFormula]:
        """
        Get all formulas in a physics domain.
        
        Args:
            domain: Physics domain to filter by
            
        Returns:
            Dictionary of formulas
        """
        domain_map = {
            PhysicsDomain.MECHANICS: ["kinematics", "dynamics", "energy"],
            PhysicsDomain.OPTICS: ["optics"],
            PhysicsDomain.ELECTROMAGNETISM: ["electromagnetism"]
        }
        
        categories = domain_map.get(domain, [])
        formulas = {}
        for cat in categories:
            formulas.update(self._formula_registry.get_formulas_by_category(cat))
        
        return formulas
    
    def list_all_formulas(self) -> List[str]:
        """List all available formula IDs."""
        return self._formula_registry.list_all_formulas()
    
    # ==================== CONCEPT RETRIEVAL ====================
    
    def get_concept(self, concept_id: str) -> Optional[PhysicsConcept]:
        """
        Retrieve a physics concept by ID.
        
        Args:
            concept_id: Unique concept identifier
            
        Returns:
            PhysicsConcept object or None if not found
        """
        return self._concepts.get(concept_id)
    
    def search_concepts(
        self,
        query: str,
        domain: Optional[PhysicsDomain] = None
    ) -> List[PhysicsConcept]:
        """
        Search for physics concepts matching a query.
        
        Args:
            query: Search query string
            domain: Optional domain filter
            
        Returns:
            List of matching concepts
        """
        query_lower = query.lower()
        results = []
        
        for concept in self._concepts.values():
            if domain and concept.domain != domain:
                continue
            
            # Check if query matches name, description, or related concepts
            if (query_lower in concept.name.lower() or
                query_lower in concept.description.lower() or
                any(query_lower in rel.lower() for rel in concept.related_concepts)):
                results.append(concept)
        
        return results
    
    def get_concepts_by_domain(
        self,
        domain: PhysicsDomain
    ) -> List[PhysicsConcept]:
        """
        Get all concepts in a physics domain.
        
        Args:
            domain: Physics domain
            
        Returns:
            List of concepts in the domain
        """
        return [c for c in self._concepts.values() if c.domain == domain]
    
    # ==================== UNIT CONVERSION ====================
    
    def convert_units(
        self,
        value: float,
        from_unit: str,
        to_unit: str,
        category: str = "length"
    ) -> float:
        """
        Convert between different units.
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            category: Unit category (length, mass, time, energy)
            
        Returns:
            Converted value
        """
        return UnitConverter.convert(value, from_unit, to_unit, category)
    
    def format_with_units(
        self,
        value: float,
        unit: str,
        precision: int = 4
    ) -> str:
        """
        Format a value with appropriate unit display.
        
        Args:
            value: Numerical value
            unit: Unit string
            precision: Decimal precision
            
        Returns:
            Formatted string with unit
        """
        return f"{value:.{precision}g} {unit}"
    
    # ==================== PHYSICS CALCULATIONS ====================
    
    def calculate_kinematics(
        self,
        initial_velocity: float,
        acceleration: float,
        time: Optional[float] = None,
        final_velocity: Optional[float] = None,
        displacement: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Solve kinematic motion problems.
        
        Args:
            initial_velocity: Initial velocity (m/s)
            acceleration: Acceleration (m/s²)
            time: Time (s) - optional
            final_velocity: Final velocity (m/s) - optional
            displacement: Displacement (m) - optional
            
        Returns:
            Dictionary with all calculated values
        """
        result = {
            "initial_velocity": initial_velocity,
            "acceleration": acceleration
        }
        
        if time is not None:
            result["time"] = time
            result["final_velocity"] = initial_velocity + acceleration * time
            result["displacement"] = (
                initial_velocity * time + 0.5 * acceleration * time**2
            )
        elif final_velocity is not None and time is None:
            # Use v = v₀ + at
            time = (final_velocity - initial_velocity) / acceleration if acceleration != 0 else 0
            result["time"] = time
            result["displacement"] = (
                initial_velocity * time + 0.5 * acceleration * time**2
            )
        elif displacement is not None and time is None:
            # Use d = v₀t + ½at²
            # at² + 2v₀t - 2d = 0
            if acceleration != 0:
                discriminant = initial_velocity**2 + 2 * acceleration * displacement
                if discriminant >= 0:
                    t1 = (-initial_velocity + sqrt(discriminant)) / acceleration
                    t2 = (-initial_velocity - sqrt(discriminant)) / acceleration
                    result["time"] = t1 if t1 >= 0 else t2
                    result["final_velocity"] = initial_velocity + acceleration * result["time"]
                else:
                    result["time"] = None
                    result["error"] = "No real solution for time"
            else:
                if initial_velocity != 0:
                    result["time"] = displacement / initial_velocity
                    result["final_velocity"] = initial_velocity
                else:
                    result["time"] = None
                    result["error"] = "Cannot solve - initial velocity is zero"
        
        return result
    
    def calculate_projectile(
        self,
        initial_speed: float,
        launch_angle: float,
        gravity: float = 9.81,
        initial_height: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate projectile motion parameters.
        
        Args:
            initial_speed: Initial speed (m/s)
            launch_angle: Launch angle (degrees)
            gravity: Gravitational acceleration (m/s²)
            initial_height: Initial height (m)
            
        Returns:
            Dictionary with motion parameters
        """
        angle_rad = radians(launch_angle)
        
        result = {
            "initial_speed": initial_speed,
            "launch_angle": launch_angle,
            "gravity": gravity,
            "horizontal_velocity": initial_speed * cos(angle_rad),
            "vertical_velocity_initial": initial_speed * sin(angle_rad)
        }
        
        # Time of flight
        if gravity != 0:
            result["time_of_flight"] = (
                2 * initial_speed * sin(angle_rad) / gravity
            )
            
            # Maximum height
            result["max_height"] = (
                (initial_speed * sin(angle_rad))**2 / (2 * gravity)
            ) + initial_height
            
            # Range
            result["horizontal_range"] = (
                initial_speed**2 * sin(2 * angle_rad) / gravity
            )
            
            # Time to max height
            result["time_to_max_height"] = (
                initial_speed * sin(angle_rad) / gravity
            )
            
            # Position at any time
            def position_at_time(t):
                return {
                    "x": initial_speed * cos(angle_rad) * t,
                    "y": initial_speed * sin(angle_rad) * t - 0.5 * gravity * t**2 + initial_height
                }
            result["position_at_time"] = position_at_time
        
        return result
    
    def calculate_orbit(
        self,
        central_mass: float,
        orbital_radius: float,
        gravitational_constant: float = 6.67430e-11
    ) -> Dict[str, float]:
        """
        Calculate orbital parameters.
        
        Args:
            central_mass: Mass of central body (kg)
            orbital_radius: Orbital radius (m)
            gravitational_constant: Gravitational constant
            
        Returns:
            Dictionary with orbital parameters
        """
        return calculate_orbit_parameters(
            central_mass,
            orbital_radius,
            gravitational_constant
        )
    
    def calculate_shock_parameters(
        self,
        mass: float,
        spring_constant: float,
        amplitude: float
    ) -> Dict[str, float]:
        """
        Calculate simple harmonic motion parameters.
        
        Args:
            mass: Mass (kg)
            spring_constant: Spring constant (N/m)
            amplitude: Amplitude (m)
            
        Returns:
            Dictionary with SHM parameters
        """
        return calculate_shm_parameters(mass, spring_constant, amplitude)
    
    def calculate_circuit_rc(
        self,
        resistance: float,
        capacitance: float,
        voltage: float
    ) -> Dict[str, float]:
        """
        Calculate RC circuit parameters.
        
        Args:
            resistance: Resistance (Ω)
            capacitance: Capacitance (F)
            voltage: Source voltage (V)
            
        Returns:
            Dictionary with circuit parameters
        """
        return calculate_rc_circuit(resistance, capacitance, voltage)
    
    def calculate_circuit_rlc(
        self,
        resistance: float,
        inductance: float,
        capacitance: float
    ) -> Dict[str, float]:
        """
        Calculate RLC circuit resonant parameters.
        
        Args:
            resistance: Resistance (Ω)
            inductance: Inductance (H)
            capacitance: Capacitance (F)
            
        Returns:
            Dictionary with resonant parameters
        """
        return calculate_rlc_circuit(resistance, inductance, capacitance)
    
    # ==================== PROBLEM SOLVING ====================
    
    def analyze_problem(self, problem: PhysicsProblem) -> PhysicsSolution:
        """
        Analyze and solve a physics problem.
        
        Args:
            problem: PhysicsProblem to solve
            
        Returns:
            PhysicsSolution with steps and answer
        """
        solution = PhysicsSolution(
            solution_id=f"sol_{problem.problem_id}",
            problem_id=problem.problem_id
        )
        
        # Determine which formulas to use based on domain and subdomain
        formulas = self._get_formulas_for_problem(problem)
        
        # Build solution steps
        steps = []
        step_num = 1
        
        for param in problem.given_parameters:
            step = {
                "step": step_num,
                "action": "Identify given parameter",
                "parameter": param.name,
                "value": param.value,
                "unit": param.unit,
                "symbol": param.symbol
            }
            steps.append(step)
            step_num += 1
        
        # Apply physics principles
        step = {
            "step": step_num,
            "action": "Apply physics principle",
            "principle": f"{problem.domain.value} - {problem.subdomain}",
            "formulas": [f.formula_id for f in formulas]
        }
        steps.append(step)
        step_num += 1
        
        # Calculate solution
        for unknown in problem.unknown_parameters:
            calc_result = self._calculate_unknown(problem, unknown, formulas)
            if calc_result:
                solution.final_answer = calc_result.get("value", 0)
                solution.units = calc_result.get("unit", "")
                
                step = {
                    "step": step_num,
                    "action": "Calculate unknown",
                    "unknown": unknown,
                    "calculation": calc_result.get("expression", ""),
                    "result": calc_result.get("value", 0),
                    "unit": calc_result.get("unit", "")
                }
                steps.append(step)
                solution.steps = steps
                solution.formulas_used = [f.formula_id for f in formulas]
        
        # Verify solution
        solution.verification = self._verify_solution(problem, solution)
        
        return solution
    
    def _get_formulas_for_problem(
        self,
        problem: PhysicsProblem
    ) -> List[PhysicsFormula]:
        """Get relevant formulas for a problem."""
        domain_map = {
            PhysicsDomain.MECHANICS: ["kinematics", "dynamics", "energy"],
            PhysicsDomain.OPTICS: ["optics"],
            PhysicsDomain.ELECTROMAGNETISM: ["electromagnetism"]
        }
        
        categories = domain_map.get(problem.domain, [])
        formulas = []
        
        for cat in categories:
            cat_formulas = self._formula_registry.get_formulas_by_category(cat)
            # Simple matching - in practice would use more sophisticated matching
            formulas.extend(list(cat_formulas.values())[:3])
        
        return formulas
    
    def _calculate_unknown(
        self,
        problem: PhysicsProblem,
        unknown: str,
        formulas: List[PhysicsFormula]
    ) -> Optional[Dict[str, Any]]:
        """Calculate an unknown parameter."""
        # Simplified calculation based on problem type
        param_dict = {p.symbol: p.value for p in problem.given_parameters}
        
        if problem.domain == PhysicsDomain.MECHANICS:
            if problem.subdomain == MechanicsSubdomain.KINEMATICS.value:
                if unknown == "displacement" and "initial_velocity" in param_dict:
                    t = param_dict.get("t", 0)
                    a = param_dict.get("a", 0)
                    v0 = param_dict.get("initial_velocity", 0)
                    return {
                        "value": v0 * t + 0.5 * a * t**2,
                        "unit": "m",
                        "expression": "v₀t + ½at²"
                    }
        
        return None
    
    def _verify_solution(
        self,
        problem: PhysicsProblem,
        solution: PhysicsSolution
    ) -> Dict[str, Any]:
        """Verify the physical reasonableness of a solution."""
        verification = {
            "is_physical": True,
            "checks": []
        }
        
        # Check for negative values where inappropriate
        if solution.final_answer < 0:
            if solution.units in ["m", "kg", "J", "s"]:
                verification["is_physical"] = False
                verification["checks"].append({
                    "check": "negative_value",
                    "status": "fail",
                    "message": f"Negative value for {solution.units} may be unphysical"
                })
        
        # Check for reasonable magnitudes
        if abs(solution.final_answer) > 1e15:
            verification["checks"].append({
                "check": "magnitude",
                "status": "warning",
                "message": "Very large value - verify units and calculation"
            })
        
        if solution.final_answer == 0:
            verification["checks"].append({
                "check": "zero_value",
                "status": "info",
                "message": "Result is zero - verify this is expected"
            })
        
        if verification["is_physical"]:
            verification["checks"].append({
                "check": "physical",
                "status": "pass",
                "message": "Solution appears physically reasonable"
            })
        
        return verification
    
    # ==================== VISUALIZATION SUPPORT ====================
    
    def get_visualization_config(self) -> PhysicsVisualConfig:
        """Get the current visualization configuration."""
        return self._visual_config
    
    def set_visualization_config(self, config: PhysicsVisualConfig) -> None:
        """Set the visualization configuration."""
        self._visual_config = config
    
    def get_vector_fields(
        self,
        field_type: str,
        parameters: Dict[str, Any]
    ) -> Callable[[Vector2D], Vector2D]:
        """
        Get a vector field function for visualization.
        
        Args:
            field_type: Type of field (gravity, electric, etc.)
            parameters: Field parameters
            
        Returns:
            Function that returns field vector at a position
        """
        if field_type == "gravity":
            g = parameters.get("g", 9.81)
            direction = parameters.get("direction", Vector2D(0, -1))
            return lambda pos: direction * g
        
        elif field_type == "electric_point":
            Q = parameters.get("charge", 1.0)
            k = PhysicsConstants.COULOMB_CONSTANT
            return lambda pos: Vector2D(
                k * Q * pos.x / pos.magnitude()**3,
                k * Q * pos.y / pos.magnitude()**3
            ) if pos.magnitude() > 0 else Vector2D(0, 0)
        
        elif field_type == "uniform":
            return lambda pos: Vector2D(
                parameters.get("x_component", 0),
                parameters.get("y_component", 0)
            )
        
        return lambda pos: Vector2D(0, 0)
    
    # ==================== EDUCATIONAL CONTENT ====================
    
    def get_misconceptions(self, concept_id: str) -> List[str]:
        """
        Get common misconceptions about a concept.
        
        Args:
            concept_id: Concept identifier
            
        Returns:
            List of misconception strings
        """
        concept = self.get_concept(concept_id)
        return concept.misconceptions if concept else []
    
    def get_examples(self, concept_id: str) -> List[Dict[str, Any]]:
        """
        Get examples for a concept.
        
        Args:
            concept_id: Concept identifier
            
        Returns:
            List of example dictionaries
        """
        concept = self.get_concept(concept_id)
        return concept.examples if concept else []
    
    def get_related_concepts(self, concept_id: str) -> List[PhysicsConcept]:
        """
        Get concepts related to a given concept.
        
        Args:
            concept_id: Concept identifier
            
        Returns:
            List of related PhysicsConcept objects
        """
        concept = self.get_concept(concept_id)
        if not concept:
            return []
        
        related = []
        for rel_id in concept.related_concepts:
            rel_concept = self.get_concept(rel_id)
            if rel_concept:
                related.append(rel_concept)
        
        return related
    
    def explain_concept(self, concept_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive explanation of a concept.
        
        Args:
            concept_id: Concept identifier
            
        Returns:
            Dictionary with explanation components
        """
        concept = self.get_concept(concept_id)
        if not concept:
            return {"error": f"Concept {concept_id} not found"}
        
        return {
            "concept": concept.name,
            "type": concept.concept_type.value,
            "domain": concept.domain.value,
            "subdomain": concept.subdomain,
            "description": concept.description,
            "formula": concept.formula,
            "variables": concept.variables,
            "examples": concept.examples,
            "misconceptions": concept.misconceptions,
            "related_concepts": [
                {"id": c.concept_id, "name": c.name}
                for c in self.get_related_concepts(concept_id)
            ]
        }
