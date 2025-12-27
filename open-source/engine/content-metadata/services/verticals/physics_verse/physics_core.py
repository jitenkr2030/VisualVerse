"""
PhysicsVerse Core Math Module

This module provides fundamental mathematical structures and operations for physics
simulations including vector mathematics, complex numbers for wave optics, matrix
operations for linear algebra applications, and numerical integration methods.

Key Features:
- 2D and 3D vector operations with physics-specific methods
- Complex number arithmetic for wave optics simulations
- Matrix operations for linear transformations and circuit analysis
- Numerical integration methods (Euler, Runge-Kutta)
- Physical constants and unit conversions

Licensed under the Apache License, Version 2.0
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from math import sqrt, sin, cos, tan, asin, acos, atan2, pi, exp, log, radians, degrees
import logging

logger = logging.getLogger(__name__)


class VectorOperationType(Enum):
    """Types of vector operations for educational display."""
    ADDITION = "addition"
    SUBTRACTION = "subtraction"
    SCALAR_MULTIPLICATION = "scalar_multiplication"
    DOT_PRODUCT = "dot_product"
    CROSS_PRODUCT = "cross_product"
    PROJECTION = "projection"
    RESOLUTION = "resolution"


class IntegrationMethod(Enum):
    """Numerical integration methods for physics simulations."""
    EULAR = "euler"
    SEMI_IMPLICIT_EULAR = "semi_implicit_euler"
    RUNGE_KUTTA_4 = "runge_kutta_4"
    VERLET = "verlet"
    LEAPFROG = "leapfrog"


@dataclass
class Vector2D:
    """
    2D vector for planar physics simulations.
    
    Attributes:
        x: X component (horizontal)
        y: Y component (vertical)
    """
    x: float = 0.0
    y: float = 0.0
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector addition."""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Vector subtraction."""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        """Scalar multiplication."""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector2D':
        """Scalar division."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector2D':
        """Negation."""
        return Vector2D(-self.x, -self.y)
    
    def __eq__(self, other: object) -> bool:
        """Equality check with tolerance."""
        if not isinstance(other, Vector2D):
            return False
        tolerance = 1e-10
        return abs(self.x - other.x) < tolerance and abs(self.y - other.y) < tolerance
    
    def magnitude(self) -> float:
        """Calculate vector magnitude (length)."""
        return sqrt(self.x**2 + self.y**2)
    
    def magnitude_squared(self) -> float:
        """Calculate squared magnitude (faster than magnitude)."""
        return self.x**2 + self.y**2
    
    def normalize(self) -> 'Vector2D':
        """Return unit vector in same direction."""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return self / mag
    
    def dot(self, other: 'Vector2D') -> float:
        """Dot product with another vector."""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Vector2D') -> float:
        """2D cross product (returns scalar, actually the z-component)."""
        return self.x * other.y - self.y * other.x
    
    def angle(self, other: Optional['Vector2D'] = None) -> float:
        """Calculate angle with another vector or with x-axis."""
        if other is None:
            return atan2(self.y, self.x)
        return acos(self.dot(other) / (self.magnitude() * other.magnitude()))
    
    def rotate(self, angle: float) -> 'Vector2D':
        """Rotate vector by angle (radians)."""
        cos_a = cos(angle)
        sin_a = sin(angle)
        return Vector2D(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def perpendicular(self) -> 'Vector2D':
        """Return perpendicular vector (90° rotation)."""
        return Vector2D(-self.y, self.x)
    
    def project_onto(self, other: 'Vector2D') -> 'Vector2D':
        """Project this vector onto another vector."""
        return other * (self.dot(other) / other.magnitude_squared())
    
    def resolve(self) -> Tuple[float, float]:
        """Resolve into horizontal and vertical components."""
        return (self.x, self.y)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {"x": self.x, "y": self.y}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Vector2D':
        """Create from dictionary."""
        return cls(x=data.get("x", 0), y=data.get("y", 0))
    
    @classmethod
    def from_magnitude_angle(cls, magnitude: float, angle: float) -> 'Vector2D':
        """Create vector from magnitude and angle (radians)."""
        return cls(magnitude * cos(angle), magnitude * sin(angle))
    
    @classmethod
    def zero(cls) -> 'Vector2D':
        """Return zero vector."""
        return cls(0, 0)
    
    @classmethod
    def unit_x(cls) -> 'Vector2D':
        """Return unit vector in x direction."""
        return cls(1, 0)
    
    @classmethod
    def unit_y(cls) -> 'Vector2D':
        """Return unit vector in y direction."""
        return cls(0, 1)


@dataclass
class Vector3D:
    """
    3D vector for spatial physics simulations.
    
    Attributes:
        x: X component
        y: Y component  
        z: Z component
    """
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        """Vector addition."""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        """Vector subtraction."""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        """Scalar multiplication."""
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector3D':
        """Scalar division."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __neg__(self) -> 'Vector3D':
        """Negation."""
        return Vector3D(-self.x, -self.y, -self.z)
    
    def magnitude(self) -> float:
        """Calculate vector magnitude."""
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def magnitude_squared(self) -> float:
        """Calculate squared magnitude."""
        return self.x**2 + self.y**2 + self.z**2
    
    def normalize(self) -> 'Vector3D':
        """Return unit vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return self / mag
    
    def dot(self, other: 'Vector3D') -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """Cross product."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def to_2d(self, projection_plane: str = "xy") -> Vector2D:
        """Project onto 2D plane."""
        if projection_plane == "xy":
            return Vector2D(self.x, self.y)
        elif projection_plane == "xz":
            return Vector2D(self.x, self.z)
        elif projection_plane == "yz":
            return Vector2D(self.y, self.z)
        else:
            return Vector2D(self.x, self.y)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {"x": self.x, "y": self.y, "z": self.z}
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'Vector3D':
        """Create from dictionary."""
        return cls(x=data.get("x", 0), y=data.get("y", 0), z=data.get("z", 0))
    
    @classmethod
    def zero(cls) -> 'Vector3D':
        """Return zero vector."""
        return cls(0, 0, 0)


@dataclass
class Complex:
    """
    Complex number for wave optics and AC circuit analysis.
    
    Attributes:
        real: Real part
        imag: Imaginary part
    """
    real: float = 0.0
    imag: float = 0.0
    
    def __add__(self, other: 'Complex') -> 'Complex':
        """Complex addition."""
        return Complex(self.real + other.real, self.imag + other.imag)
    
    def __sub__(self, other: 'Complex') -> 'Complex':
        """Complex subtraction."""
        return Complex(self.real - other.real, self.imag - other.imag)
    
    def __mul__(self, other: Union['Complex', float]) -> 'Complex':
        """Complex multiplication."""
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real
            )
        else:
            return Complex(self.real * other, self.imag * other)
    
    def __truediv__(self, other: Union['Complex', float]) -> 'Complex':
        """Complex division."""
        if isinstance(other, Complex):
            denom = other.real**2 + other.imag**2
            if denom == 0:
                raise ValueError("Cannot divide by zero")
            return Complex(
                (self.real * other.real + self.imag * other.imag) / denom,
                (self.imag * other.real - self.real * other.imag) / denom
            )
        else:
            if other == 0:
                raise ValueError("Cannot divide by zero")
            return Complex(self.real / other, self.imag / other)
    
    @property
    def magnitude(self) -> float:
        """Magnitude (absolute value)."""
        return sqrt(self.real**2 + self.imag**2)
    
    @property
    def phase(self) -> float:
        """Phase angle in radians."""
        return atan2(self.imag, self.real)
    
    @property
    def conjugate(self) -> 'Complex':
        """Complex conjugate."""
        return Complex(self.real, -self.imag)
    
    def to_polar(self) -> Tuple[float, float]:
        """Convert to polar form (magnitude, phase)."""
        return (self.magnitude, self.phase)
    
    @classmethod
    def from_polar(cls, magnitude: float, phase: float) -> 'Complex':
        """Create from polar form."""
        return cls(magnitude * cos(phase), magnitude * sin(phase))
    
    @classmethod
    def i(cls) -> 'Complex':
        """Return imaginary unit i."""
        return cls(0, 1)
    
    @classmethod
    def exp(cls, theta: float) -> 'Complex':
        """Return e^(i*theta)."""
        return cls(cos(theta), sin(theta))


@dataclass
class Matrix3x3:
    """
    3x3 matrix for 2D transformations and tensor operations.
    
    Attributes:
        elements: 3x3 matrix elements in row-major order
    """
    elements: List[float] = field(default_factory=lambda: [0]*9)
    
    def __getitem__(self, row: int, col: int) -> float:
        """Get element at row, col."""
        return self.elements[row * 3 + col]
    
    def __setitem__(self, row: int, col: int, value: float):
        """Set element at row, col."""
        self.elements[row * 3 + col] = value
    
    def __mul__(self, other: Union['Matrix3x3', Vector2D]) -> Union['Matrix3x3', Vector2D]:
        """Matrix multiplication."""
        if isinstance(other, Vector2D):
            # Matrix-vector multiplication
            return Vector2D(
                self[0,0] * other.x + self[0,1] * other.y + self[0,2],
                self[1,0] * other.x + self[1,1] * other.y + self[1,2]
            )
        else:
            result = Matrix3x3()
            for i in range(3):
                for j in range(3):
                    result[i, j] = sum(
                        self[i, k] * other[k, j] for k in range(3)
                    )
            return result
    
    def determinant(self) -> float:
        """Calculate determinant."""
        return (
            self[0,0] * (self[1,1] * self[2,2] - self[1,2] * self[2,1]) -
            self[0,1] * (self[1,0] * self[2,2] - self[1,2] * self[2,0]) +
            self[0,2] * (self[1,0] * self[2,1] - self[1,1] * self[2,0])
        )
    
    def transpose(self) -> 'Matrix3x3':
        """Return transpose."""
        result = Matrix3x3()
        for i in range(3):
            for j in range(3):
                result[i, j] = self[j, i]
        return result
    
    @classmethod
    def identity(cls) -> 'Matrix3x3':
        """Return identity matrix."""
        m = cls()
        for i in range(3):
            m[i, i] = 1.0
        return m
    
    @classmethod
    def rotation(cls, angle: float) -> 'Matrix3x3':
        """Return 2D rotation matrix."""
        c, s = cos(angle), sin(angle)
        m = cls.identity()
        m[0, 0] = c; m[0, 1] = -s
        m[1, 0] = s; m[1, 1] = c
        return m
    
    @classmethod
    def scale(cls, sx: float, sy: float) -> 'Matrix3x3':
        """Return 2D scale matrix."""
        m = cls.identity()
        m[0, 0] = sx
        m[1, 1] = sy
        return m


@dataclass
class PhysicsState:
    """
    Complete state of a physics system at a given time.
    
    Attributes:
        time: Current simulation time
        positions: Dictionary mapping entity IDs to positions
        velocities: Dictionary mapping entity IDs to velocities
        accelerations: Dictionary mapping entity IDs to accelerations
        additional_properties: For storing angular momentum, energy, etc.
    """
    time: float = 0.0
    positions: Dict[str, Vector2D] = field(default_factory=dict)
    velocities: Dict[str, Vector2D] = field(default_factory=dict)
    accelerations: Dict[str, Vector2D] = field(default_factory=dict)
    additional_properties: Dict[str, Any] = field(default_factory=dict)
    
    def get_velocity_magnitude(self, entity_id: str) -> float:
        """Get speed of an entity."""
        if entity_id in self.velocities:
            return self.velocities[entity_id].magnitude()
        return 0.0
    
    def get_kinetic_energy(self, mass: float, entity_id: str) -> float:
        """Calculate kinetic energy of an entity."""
        v = self.get_velocity_magnitude(entity_id)
        return 0.5 * mass * v**2
    
    def interpolate_to(self, other: 'PhysicsState', t: float) -> 'PhysicsState':
        """Interpolate between two states."""
        return PhysicsState(
            time=self.time + t * (other.time - self.time),
            positions={
                k: self.positions[k] + (other.positions[k] - self.positions[k]) * t
                for k in set(self.positions.keys()) & set(other.positions.keys())
            },
            velocities={
                k: self.velocities[k] + (other.velocities[k] - self.velocities[k]) * t
                for k in set(self.velocities.keys()) & set(other.velocities.keys())
            }
        )


class PhysicsConstants:
    """Physical constants in SI units."""
    # Fundamental constants
    SPEED_OF_LIGHT = 299792458  # m/s
    PLANCK_CONSTANT = 6.62607015e-34  # J·s
    ELEMENTARY_CHARGE = 1.602176634e-19  # C
    GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/(kg·s²)
    BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
    
    # Electromagnetic constants
    VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m (ε₀)
    VACUUM_PERMEABILITY = 1.25663706212e-6  # N/A² (μ₀)
    COULOMB_CONSTANT = 8.987551787e9  # N·m²/C² (k = 1/(4πε₀))
    
    # Mechanical constants
    STANDARD_GRAVITY = 9.80665  # m/s²
    EARTH_MASS = 5.972e24  # kg
    EARTH_RADIUS = 6.371e6  # m
    
    # Optical constants
    REFRACTIVE_INDEX_AIR = 1.0003
    REFRACTIVE_INDEX_WATER = 1.333
    REFRACTIVE_INDEX_GLASS = 1.5


class UnitConverter:
    """Unit conversion utilities for physics calculations."""
    
    # Length conversions (to meters)
    LENGTH_TO_METERS = {
        "m": 1.0,
        "km": 1000.0,
        "cm": 0.01,
        "mm": 0.001,
        "μm": 1e-6,
        "nm": 1e-9,
        "Å": 1e-10,
        "in": 0.0254,
        "ft": 0.3048,
        "mi": 1609.344,
        "AU": 1.496e11,
        "ly": 9.461e15
    }
    
    # Mass conversions (to kilograms)
    MASS_TO_KILOGRAMS = {
        "kg": 1.0,
        "g": 0.001,
        "mg": 1e-6,
        "t": 1000.0,
        "lb": 0.453592,
        "oz": 0.0283495,
        "u": 1.66053906660e-27
    }
    
    # Time conversions (to seconds)
    TIME_TO_SECONDS = {
        "s": 1.0,
        "ms": 1e-3,
        "μs": 1e-6,
        "ns": 1e-9,
        "min": 60.0,
        "h": 3600.0,
        "day": 86400.0,
        "year": 31536000.0
    }
    
    # Energy conversions (to joules)
    ENERGY_TO_JOULES = {
        "J": 1.0,
        "kJ": 1000.0,
        "cal": 4.184,
        "kcal": 4184.0,
        "eV": 1.602176634e-19,
        "kWh": 3.6e6,
        "BTU": 1055.06
    }
    
    @classmethod
    def convert(
        cls,
        value: float,
        from_unit: str,
        to_unit: str,
        category: str = "length"
    ) -> float:
        """Convert value between units."""
        conversion_map = {
            "length": cls.LENGTH_TO_METERS,
            "mass": cls.MASS_TO_KILOGRAMS,
            "time": cls.TIME_TO_SECONDS,
            "energy": cls.ENERGY_TO_JOULES
        }
        
        unit_map = conversion_map.get(category, {})
        
        if from_unit not in unit_map or to_unit not in unit_map:
            raise ValueError(f"Unknown unit: {from_unit} or {to_unit}")
        
        # Convert to base unit, then to target unit
        base_value = value * unit_map[from_unit]
        return base_value / unit_map[to_unit]
    
    @classmethod
    def format_value(cls, value: float, unit: str) -> str:
        """Format value with appropriate SI prefix."""
        if value == 0:
            return f"0 {unit}"
        
        prefixes = {
            1e-24: "y", 1e-21: "z", 1e-18: "a", 1e-15: "f",
            1e-12: "p", 1e-9: "n", 1e-6: "μ", 1e-3: "m",
            1e3: "k", 1e6: "M", 1e9: "G", 1e12: "T", 1e15: "P"
        }
        
        abs_value = abs(value)
        scaled_value = value
        
        for threshold, prefix in sorted(prefixes.items()):
            if abs_value >= threshold:
                scaled_value = value / threshold
                return f"{scaled_value:.4g} {prefix}{unit}"
        
        return f"{value:.4g} {unit}"


class NumericalIntegrator:
    """Numerical integration methods for physics simulations."""
    
    @staticmethod
    def euler(
        state: PhysicsState,
        derivative: callable,
        dt: float
    ) -> PhysicsState:
        """
        Euler integration (first order).
        
        x(t+dt) = x(t) + v(t) * dt
        v(t+dt) = v(t) + a(t) * dt
        """
        new_state = PhysicsState(
            time=state.time + dt,
            positions=state.positions.copy(),
            velocities=state.velocities.copy(),
            accelerations=state.accelerations.copy()
        )
        
        for entity_id in state.positions:
            if entity_id in state.velocities:
                new_state.positions[entity_id] = (
                    state.positions[entity_id] +
                    state.velocities[entity_id] * dt
                )
            if entity_id in state.accelerations:
                new_state.velocities[entity_id] = (
                    state.velocities[entity_id] +
                    state.accelerations[entity_id] * dt
                )
        
        return new_state
    
    @staticmethod
    def semi_implicit_euler(
        state: PhysicsState,
        derivative: callable,
        dt: float
    ) -> PhysicsState:
        """
        Semi-implicit Euler (symplectic, better energy conservation).
        
        v(t+dt) = v(t) + a(t) * dt
        x(t+dt) = x(t) + v(t+dt) * dt
        """
        new_state = PhysicsState(
            time=state.time + dt,
            positions=state.positions.copy(),
            velocities=state.velocities.copy(),
            accelerations=state.accelerations.copy()
        )
        
        # Update velocity first
        for entity_id in state.accelerations:
            if entity_id in state.velocities:
                new_state.velocities[entity_id] = (
                    state.velocities[entity_id] +
                    state.accelerations[entity_id] * dt
                )
        
        # Then update position using new velocity
        for entity_id in new_state.velocities:
            if entity_id in state.positions:
                new_state.positions[entity_id] = (
                    state.positions[entity_id] +
                    new_state.velocities[entity_id] * dt
                )
        
        return new_state
    
    @staticmethod
    def verlet(
        position: Vector2D,
        velocity: Vector2D,
        acceleration: callable,
        dt: float
    ) -> Tuple[Vector2D, Vector2D]:
        """
        Velocity Verlet integration.
        
        x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt²
        v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
        """
        # Half step velocity
        half_vel = velocity + acceleration(position) * (dt / 2)
        
        # Full step position
        new_position = position + half_vel * dt
        
        # Full step velocity
        new_velocity = half_vel + acceleration(new_position) * (dt / 2)
        
        return (new_position, new_velocity)
    
    @staticmethod
    def runge_kutta_4(
        state: PhysicsState,
        derivative: callable,
        dt: float
    ) -> PhysicsState:
        """
        Runge-Kutta 4 integration (fourth order).
        
        Higher accuracy than Euler methods but more computationally expensive.
        """
        k1 = derivative(state)
        
        state2 = PhysicsState(
            time=state.time + dt/2,
            positions={k: state.positions[k] + k1.positions.get(k, Vector2D()) * (dt/2)
                      for k in state.positions},
            velocities={k: state.velocities[k] + k1.velocities.get(k, Vector2D()) * (dt/2)
                       for k in state.velocities}
        )
        k2 = derivative(state2)
        
        state3 = PhysicsState(
            time=state.time + dt/2,
            positions={k: state.positions[k] + k2.positions.get(k, Vector2D()) * (dt/2)
                      for k in state.positions},
            velocities={k: state.velocities[k] + k2.velocities.get(k, Vector2D()) * (dt/2)
                       for k in state.velocities}
        )
        k3 = derivative(state3)
        
        state4 = PhysicsState(
            time=state.time + dt,
            positions={k: state.positions[k] + k3.positions.get(k, Vector2D()) * dt
                      for k in state.positions},
            velocities={k: state.velocities[k] + k3.velocities.get(k, Vector2D()) * dt
                       for k in state.velocities}
        )
        k4 = derivative(state4)
        
        new_state = PhysicsState(
            time=state.time + dt,
            positions={},
            velocities={}
        )
        
        # Combine k values
        for entity_id in state.positions:
            pos_k1 = k1.positions.get(entity_id, Vector2D())
            pos_k2 = k2.positions.get(entity_id, Vector2D())
            pos_k3 = k3.positions.get(entity_id, Vector2D())
            pos_k4 = k4.positions.get(entity_id, Vector2D())
            
            new_state.positions[entity_id] = (
                state.positions[entity_id] +
                (pos_k1 + pos_k2 * 2 + pos_k3 * 2 + pos_k4) * (dt / 6)
            )
        
        for entity_id in state.velocities:
            vel_k1 = k1.velocities.get(entity_id, Vector2D())
            vel_k2 = k2.velocities.get(entity_id, Vector2D())
            vel_k3 = k3.velocities.get(entity_id, Vector2D())
            vel_k4 = k4.velocities.get(entity_id, Vector2D())
            
            new_state.velocities[entity_id] = (
                state.velocities[entity_id] +
                (vel_k1 + vel_k2 * 2 + vel_k3 * 2 + vel_k4) * (dt / 6)
            )
        
        return new_state


@dataclass
class PhysicsFormula:
    """
    Representation of a physics formula for educational display.
    
    Attributes:
        formula_id: Unique identifier
        name: Descriptive name
        latex: LaTeX representation
        description: Explanation of the formula
        variables: Dictionary mapping variable symbols to descriptions
        conditions: Conditions for formula applicability
        example: Example calculation
    """
    formula_id: str
    name: str
    latex: str
    description: str
    variables: Dict[str, str] = field(default_factory=dict)
    conditions: List[str] = field(default_factory=list)
    example: Optional[Dict[str, Any]] = None


class PhysicsFormulaRegistry:
    """Registry of physics formulas organized by category."""
    
    def __init__(self):
        """Initialize the formula registry with common physics formulas."""
        self._formulas = self._initialize_formulas()
    
    def _initialize_formulas(self) -> Dict[str, Dict[str, PhysicsFormula]]:
        """Initialize all physics formulas."""
        return {
            "kinematics": self._create_kinematics_formulas(),
            "dynamics": self._create_dynamics_formulas(),
            "energy": self._create_energy_formulas(),
            "optics": self._create_optics_formulas(),
            "electromagnetism": self._create_electromagnetism_formulas()
        }
    
    def _create_kinematics_formulas(self) -> Dict[str, PhysicsFormula]:
        """Create kinematics formulas."""
        return {
            "velocity_equation": PhysicsFormula(
                formula_id="velocity_equation",
                name="Velocity from Acceleration",
                latex=r"v = v_0 + at",
                description="Calculates final velocity given initial velocity, acceleration, and time",
                variables={"v": "final velocity", "v₀": "initial velocity", "a": "acceleration", "t": "time"},
                conditions=["constant acceleration"]
            ),
            "position_equation_1": PhysicsFormula(
                formula_id="position_equation_1",
                name="Position from Velocity and Time",
                latex=r"x = x_0 + v_0 t + \frac{1}{2}at^2",
                description="Calculates position with constant acceleration",
                variables={"x": "final position", "x₀": "initial position", "v₀": "initial velocity", "a": "acceleration", "t": "time"},
                conditions=["constant acceleration", "straight line motion"]
            ),
            "position_equation_2": PhysicsFormula(
                formula_id="position_equation_2",
                name="Position from Initial and Final Velocity",
                latex=r"x = x_0 + \frac{v^2 - v_0^2}{2a}",
                description="Relates position change to velocities and acceleration",
                variables={"x": "final position", "x₀": "initial position", "v": "final velocity", "v₀": "initial velocity", "a": "acceleration"},
                conditions=["constant acceleration"]
            ),
            "projectile_range": PhysicsFormula(
                formula_id="projectile_range",
                name="Projectile Range",
                latex=r"R = \frac{v_0^2 \sin(2\theta)}{g}",
                description="Calculates horizontal range of a projectile",
                variables={"R": "horizontal range", "v₀": "initial speed", "θ": "launch angle", "g": "gravitational acceleration"},
                conditions=["level ground", "neglect air resistance"]
            ),
            "projectile_max_height": PhysicsFormula(
                formula_id="projectile_max_height",
                name="Maximum Height",
                latex=r"H = \frac{v_0^2 \sin^2(\theta)}{2g}",
                description="Calculates maximum height of a projectile",
                variables={"H": "maximum height", "v₀": "initial speed", "θ": "launch angle", "g": "gravitational acceleration"},
                conditions=["level ground", "neglect air resistance"]
            )
        }
    
    def _create_dynamics_formulas(self) -> Dict[str, PhysicsFormula]:
        """Create dynamics formulas."""
        return {
            "newton_second_law": PhysicsFormula(
                formula_id="newton_second_law",
                name="Newton's Second Law",
                latex=r"\vec{F} = m\vec{a}",
                description="Relates net force to mass and acceleration",
                variables={"F": "net force", "m": "mass", "a": "acceleration"},
                conditions=["inertial frame", "constant mass"]
            ),
            "gravitational_force": PhysicsFormula(
                formula_id="gravitational_force",
                name="Newton's Law of Gravitation",
                latex=r"F = G\frac{m_1 m_2}{r^2}",
                description="Calculates gravitational force between two masses",
                variables={"F": "gravitational force", "G": "gravitational constant", "m₁": "first mass", "m₂": "second mass", "r": "distance"},
                conditions=["point masses", "spherically symmetric"]
            ),
            "weight": PhysicsFormula(
                formula_id="weight",
                name="Weight (Gravitational Force)",
                latex=r"W = mg",
                description="Calculates gravitational force on an object near Earth's surface",
                variables={"W": "weight (force)", "m": "mass", "g": "gravitational acceleration"},
                conditions=["near Earth's surface"]
            ),
            "friction": PhysicsFormula(
                formula_id="friction",
                name="Frictional Force",
                latex=r"f = \mu N",
                description="Calculates frictional force",
                variables={"f": "frictional force", "μ": "coefficient of friction", "N": "normal force"},
                conditions=["maximum static or kinetic friction"}
            ),
            "centripetal_force": PhysicsFormula(
                formula_id="centripetal_force",
                name="Centripetal Force",
                latex=r"F_c = \frac{mv^2}{r} = m\omega^2 r",
                description="Force required for circular motion",
                variables={"F_c": "centripetal force", "m": "mass", "v": "speed", "r": "radius", "ω": "angular velocity"},
                conditions=["uniform circular motion"]
            ),
            "momentum": PhysicsFormula(
                formula_id="momentum",
                name="Linear Momentum",
                latex=r"\vec{p} = m\vec{v}",
                description="Defines momentum as mass times velocity",
                variables={"p": "momentum", "m": "mass", "v": "velocity"},
                conditions=["non-relativistic speeds"]
            )
        }
    
    def _create_energy_formulas(self) -> Dict[str, PhysicsFormula]:
        """Create energy formulas."""
        return {
            "kinetic_energy": PhysicsFormula(
                formula_id="kinetic_energy",
                name="Kinetic Energy",
                latex=r"K = \frac{1}{2}mv^2",
                description="Energy of motion",
                variables={"K": "kinetic energy", "m": "mass", "v": "speed"},
                conditions=["non-relativistic speeds"]
            ),
            "gravitational_potential_energy": PhysicsFormula(
                formula_id="gravitational_potential_energy",
                name="Gravitational Potential Energy",
                latex=r"U_g = mgh",
                description="Potential energy near Earth's surface",
                variables={"U_g": "gravitational potential energy", "m": "mass", "g": "gravitational acceleration", "h": "height"},
                conditions=["near Earth's surface", "constant g"]
            ),
            "spring_potential_energy": PhysicsFormula(
                formula_id="spring_potential_energy",
                name="Spring Potential Energy",
                latex=r"U_s = \frac{1}{2}kx^2",
                description="Potential energy in a compressed or stretched spring",
                variables={"U_s": "spring potential energy", "k": "spring constant", "x": "displacement from equilibrium"},
                conditions=["Hooke's law valid", "ideal spring"]
            ),
            "work": PhysicsFormula(
                formula_id="work",
                name="Work Done by Force",
                latex=r"W = \vec{F} \cdot \vec{d} = Fd\cos\theta",
                description="Work as dot product of force and displacement",
                variables={"W": "work", "F": "force", "d": "displacement", "θ": "angle between force and displacement"},
                conditions=["constant force"]
            ),
            "power": PhysicsFormula(
                formula_id="power",
                name="Power",
                latex=r"P = \frac{W}{t} = Fv\cos\theta",
                description="Rate of doing work",
                variables={"P": "power", "W": "work", "t": "time", "F": "force", "v": "speed", "θ": "angle"},
                conditions=["constant power"]
            ),
            "conservation_mechanical_energy": PhysicsFormula(
                formula_id="conservation_mechanical_energy",
                name="Conservation of Mechanical Energy",
                latex=r"K_1 + U_1 = K_2 + U_2",
                description="Total mechanical energy is conserved in isolated systems",
                variables={"K₁, K₂": "initial and final kinetic energy", "U₁, U₂": "initial and final potential energy"},
                conditions=["no non-conservative forces", "isolated system"]
            )
        }
    
    def _create_optics_formulas(self) -> Dict[str, PhysicsFormula]:
        """Create optics formulas."""
        return {
            "snells_law": PhysicsFormula(
                formula_id="snells_law",
                name="Snell's Law",
                latex=r"n_1\sin\theta_1 = n_2\sin\theta_2",
                description="Relates angles and refractive indices at interface",
                variables={"n₁": "first medium refractive index", "θ₁": "angle of incidence", "n₂": "second medium refractive index", "θ₂": "angle of refraction"},
                conditions=["smooth interface", "monochromatic light"]
            ),
            "lens_maker_equation": PhysicsFormula(
                formula_id="lens_maker_equation",
                name="Lens Maker's Equation",
                latex=r"\frac{1}{f} = (n-1)\left(\frac{1}{R_1} - \frac{1}{R_2}\right)",
                description="Relates focal length to lens parameters",
                variables={"f": "focal length", "n": "refractive index", "R₁": "first surface radius", "R₂": "second surface radius"},
                conditions=["thin lens", "paraxial approximation"]
            ),
            "mirror_equation": PhysicsFormula(
                formula_id="mirror_equation",
                name="Mirror Equation",
                latex=r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}",
                description="Relates object distance, image distance, and focal length",
                variables={"f": "focal length", "d_o": "object distance", "d_i": "image distance"},
                conditions=["paraxial approximation", "spherical mirror"}
            ),
            "magnification": PhysicsFormula(
                formula_id="magnification",
                name="Linear Magnification",
                latex=r"M = -\frac{d_i}{d_o} = \frac{h_i}{h_o}",
                description="Ratio of image size to object size",
                variables={"M": "magnification", "d_i": "image distance", "d_o": "object distance", "h_i": "image height", "h_o": "object height"},
                conditions=["paraxial approximation"]
            ),
            "diffraction_grating": PhysicsFormula(
                formula_id="diffraction_grating",
                name="Diffraction Grating Equation",
                latex=r"d\sin\theta = m\lambda",
                description="Positions of diffraction maxima",
                variables={"d": "grating spacing", "θ": "diffraction angle", "m": "order", "λ": "wavelength"},
                conditions=["far field", "small angles"]
            )
        }
    
    def _create_electromagnetism_formulas(self) -> Dict[str, PhysicsFormula]:
        """Create electromagnetism formulas."""
        return {
            "coulombs_law": PhysicsFormula(
                formula_id="coulombs_law",
                name="Coulomb's Law",
                latex=r"F = k\frac{q_1 q_2}{r^2}",
                description="Force between two point charges",
                variables={"F": "electrostatic force", "k": "Coulomb constant", "q₁": "first charge", "q₂": "second charge", "r": "distance"},
                conditions=["point charges", "stationary charges"]
            ),
            "electric_field_point_charge": PhysicsFormula(
                formula_id="electric_field_point_charge",
                name="Electric Field of Point Charge",
                latex=r"E = k\frac{Q}{r^2}",
                description="Electric field at distance from point charge",
                variables={"E": "electric field magnitude", "k": "Coulomb constant", "Q": "charge", "r": "distance"},
                conditions=["point charge", "test charge negligible"]
            ),
            "electric_potential_point_charge": PhysicsFormula(
                formula_id="electric_potential_point_charge",
                name="Electric Potential of Point Charge",
                latex=r"V = k\frac{Q}{r}",
                description="Electric potential at distance from point charge",
                variables={"V": "electric potential", "k": "Coulomb constant", "Q": "charge", "r": "distance"},
                conditions=["point charge", "reference at infinity"]
            ),
            "ohms_law": PhysicsFormula(
                formula_id="ohms_law",
                name="Ohm's Law",
                latex=r"V = IR",
                description="Relates voltage, current, and resistance",
                variables={"V": "voltage", "I": "current", "R": "resistance"},
                conditions=["ohmic material", "constant temperature"]
            ),
            "power_electrical": PhysicsFormula(
                formula_id="power_electrical",
                name="Electrical Power",
                latex=r"P = IV = I^2 R = \frac{V^2}{R}",
                description="Power dissipated in electrical circuit",
                variables={"P": "power", "I": "current", "V": "voltage", "R": "resistance"},
                conditions=["steady state"]
            ),
            "magnetic_field_wire": PhysicsFormula(
                formula_id="magnetic_field_wire",
                name="Magnetic Field Around Wire",
                latex=r"B = \frac{\mu_0 I}{2\pi r}",
                description="Magnetic field at distance from straight wire",
                variables={"B": "magnetic field", "μ₀": "permeability of free space", "I": "current", "r": "distance"},
                conditions=["infinite straight wire"}
            ),
            "lorentz_force": PhysicsFormula(
                formula_id="lorentz_force",
                name="Lorentz Force",
                latex=r"\vec{F} = q(\vec{E} + \vec{v} \times \vec{B})",
                description="Force on charged particle in electromagnetic field",
                variables={"F": "force", "q": "charge", "E": "electric field", "v": "velocity", "B": "magnetic field"},
                conditions=["non-relativistic"]
            ),
            "faraday_law": PhysicsFormula(
                formula_id="faraday_law",
                name="Faraday's Law of Induction",
                latex=r"\mathcal{E} = -\frac{d\Phi_B}{dt}",
                description="Induced EMF from changing magnetic flux",
                variables={"ℰ": "induced EMF", "Φ_B": "magnetic flux"},
                conditions=["lenz's law included (negative sign)"}
            )
        }
    
    def get_formula(self, formula_id: str) -> Optional[PhysicsFormula]:
        """Get a formula by ID."""
        for category in self._formulas.values():
            if formula_id in category:
                return category[formula_id]
        return None
    
    def get_formulas_by_category(self, category: str) -> Dict[str, PhysicsFormula]:
        """Get all formulas in a category."""
        return self._formulas.get(category, {})
    
    def list_all_formulas(self) -> List[str]:
        """List all formula IDs."""
        return [f"{cat}:{fid}" for cat, formulas in self._formulas.items() 
                for fid in formulas.keys()]


# Physics helper functions
def calculate_kinematic_motion(
    initial_velocity: float,
    acceleration: float,
    time: float
) -> Dict[str, float]:
    """Calculate motion parameters using kinematic equations."""
    final_velocity = initial_velocity + acceleration * time
    displacement = initial_velocity * time + 0.5 * acceleration * time**2
    return {
        "final_velocity": final_velocity,
        "displacement": displacement
    }


def calculate_projectile_motion(
    initial_speed: float,
    launch_angle: float,
    gravity: float = 9.81
) -> Dict[str, float]:
    """Calculate projectile motion parameters."""
    angle_rad = radians(launch_angle)
    time_of_flight = 2 * initial_speed * sin(angle_rad) / gravity
    max_height = (initial_speed * sin(angle_rad))**2 / (2 * gravity)
    horizontal_range = (initial_speed**2 * sin(2 * angle_rad)) / gravity
    max_height_position = (initial_speed * cos(angle_rad)) * (initial_speed * sin(angle_rad) / gravity)
    
    return {
        "time_of_flight": time_of_flight,
        "max_height": max_height,
        "horizontal_range": horizontal_range,
        "horizontal_velocity": initial_speed * cos(angle_rad),
        "vertical_velocity_initial": initial_speed * sin(angle_rad),
        "max_height_x_position": max_height_position
    }


def calculate_orbit_parameters(
    central_mass: float,
    orbital_radius: float,
    gravitational_constant: float = 6.67430e-11
) -> Dict[str, float]:
    """Calculate orbital motion parameters."""
    orbital_velocity = sqrt(gravitational_constant * central_mass / orbital_radius)
    orbital_period = 2 * pi * orbital_radius / orbital_velocity
    angular_velocity = orbital_velocity / orbital_radius
    
    return {
        "orbital_velocity": orbital_velocity,
        "orbital_period": orbital_period,
        "angular_velocity": angular_velocity,
        "centripetal_acceleration": orbital_velocity**2 / orbital_radius
    }


def calculate_shm_parameters(
    mass: float,
    spring_constant: float,
    amplitude: float
) -> Dict[str, float]:
    """Calculate simple harmonic motion parameters."""
    angular_frequency = sqrt(spring_constant / mass)
    period = 2 * pi / angular_frequency
    frequency = 1 / period
    max_velocity = amplitude * angular_frequency
    max_acceleration = amplitude * angular_frequency**2
    
    return {
        "angular_frequency": angular_frequency,
        "period": period,
        "frequency": frequency,
        "max_velocity": max_velocity,
        "max_acceleration": max_acceleration,
        "max_momentum": mass * max_velocity,
        "max_energy": 0.5 * spring_constant * amplitude**2
    }


def calculate_wave_properties(
    frequency: float,
    wavelength: float = None,
    speed: float = None,
    medium_properties: Dict[str, float] = None
) -> Dict[str, float]:
    """Calculate wave properties."""
    result = {"frequency": frequency}
    
    if wavelength and speed is None:
        # Need speed to calculate wavelength relationship
        result["wavelength"] = wavelength
    elif speed and wavelength is None:
        result["wavelength"] = speed / frequency if speed else None
    elif wavelength and speed:
        result["wavelength"] = wavelength
        result["speed"] = speed
        result["frequency"] = speed / wavelength
    else:
        result["wavelength"] = None
        result["speed"] = None
    
    if medium_properties:
        n = medium_properties.get("refractive_index", 1.0)
        if "speed" in result and result["speed"]:
            result["speed_in_medium"] = result["speed"] / n
            result["wavelength_in_medium"] = result["wavelength"] / n if result["wavelength"] else None
    
    return result


def calculate_rc_circuit(
    resistance: float,
    capacitance: float,
    voltage_source: float
) -> Dict[str, float]:
    """Calculate RC circuit charging parameters."""
    time_constant = resistance * capacitance
    max_current = voltage_source / resistance
    max_charge = capacitance * voltage_source
    
    return {
        "time_constant": time_constant,
        "max_current": max_current,
        "max_charge": max_charge,
        "half_life": time_constant * log(2),
        "characteristic_decay": time_constant
    }


def calculate_rlc_circuit(
    resistance: float,
    inductance: float,
    capacitance: float
) -> Dict[str, float]:
    """Calculate RLC circuit resonant properties."""
    resonant_frequency = 1 / sqrt(inductance * capacitance)
    resonant_angular_frequency = 1 / sqrt(inductance * capacitance)
    quality_factor = (1 / resistance) * sqrt(inductance / capacitance)
    bandwidth = resistance / inductance if inductance > 0 else float('inf')
    
    return {
        "resonant_frequency": resonant_frequency,
        "resonant_angular_frequency": resonant_angular_frequency,
        "quality_factor": quality_factor,
        "bandwidth": bandwidth,
        "period": 2 * pi * sqrt(inductance * capacitance)
    }
