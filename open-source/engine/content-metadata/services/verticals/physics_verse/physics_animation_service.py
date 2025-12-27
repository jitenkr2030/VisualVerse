"""
PhysicsVerse Animation Service

This module provides animation capabilities for physics visualizations,
including motion animations, wave propagation, circuit behavior,
and interactive physics simulations with time-based parameter control.

Key Features:
- Motion animations with trajectory tracing
- Wave propagation animations (mechanical and electromagnetic)
- Circuit transient analysis animations
- Orbital motion animations
- Collision and scattering animations
- Time-lapse and slow-motion effects

Licensed under the Apache License, Version 2.0
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from math import sqrt, sin, cos, tan, pi, radians, degrees
import logging
import time

from .physics_core import (
    Vector2D,
    Vector3D,
    PhysicsState,
    PhysicsConstants,
    NumericalIntegrator,
    IntegrationMethod
)

logger = logging.getLogger(__name__)


class AnimationState(Enum):
    """States of an animation."""
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    COMPLETED = "completed"
    REVERSING = "reversing"


class AnimationType(Enum):
    """Types of physics animations."""
    MOTION = "motion"
    TRAJECTORY = "trajectory"
    WAVE = "wave"
    OSCILLATION = "oscillation"
    COLLISION = "collision"
    ORBITAL = "orbital"
    CIRCUIT_TRANSIENT = "circuit_transient"
    FIELD_EVOLUTION = "field_evolution"
    PHASE_CHANGE = "phase_change"


class EasingFunction(Enum):
    """Easing functions for smooth animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    ELASTIC = "elastic"
    BOUNCE = "bounce"


@dataclass
class AnimationKeyframe:
    """
    Represents a keyframe in an animation.
    
    Attributes:
        time: Time at this keyframe (seconds)
        position: Position at this time
        velocity: Velocity at this time
        custom_properties: Additional properties
        easing: Easing function to apply
    """
    time: float
    position: Optional[Vector2D] = None
    velocity: Optional[Vector2D] = None
    custom_properties: Dict[str, Any] = field(default_factory=dict)
    easing: EasingFunction = EasingFunction.LINEAR


@dataclass
class AnimationFrame:
    """
    Represents a single frame in a physics animation.
    
    Attributes:
        frame_number: Sequential frame number
        timestamp: Current animation time
        state: Physics state at this frame
        trail: List of previous positions for trail effect
        metadata: Additional frame information
    """
    frame_number: int
    timestamp: float
    state: PhysicsState
    trail: List[Vector2D] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MotionAnimationConfig:
    """Configuration for motion animations."""
    duration: float = 5.0
    fps: int = 60
    time_scale: float = 1.0
    show_velocity_vector: bool = True
    show_acceleration_vector: bool = True
    show_trail: bool = True
    trail_length: int = 50
    trail_fade: bool = True
    integration_method: IntegrationMethod = IntegrationMethod.SEMI_IMPLICIT_EULAR
    record_frames: bool = True


@dataclass
class WaveAnimationConfig:
    """Configuration for wave animations."""
    amplitude: float = 1.0
    wavelength: float = 1.0
    frequency: float = 1.0
    phase: float = 0.0
    duration: float = 10.0
    fps: int = 30
    show_particles: bool = False
    particle_count: int = 50
    propagation_direction: str = "right"
    wave_type: str = "sine"


@dataclass
class CircuitAnimationConfig:
    """Configuration for circuit animations."""
    time_constant: float = 1.0
    duration: float = 10.0
    fps: int = 30
    show_current_flow: bool = True
    current_indicator: str = "dots"
    show_charging_curve: bool = True
    animation_type: str = "charging"


@dataclass
class PhysicsAnimation:
    """
    Complete physics animation sequence.
    
    Attributes:
        animation_id: Unique identifier
        animation_type: Type of animation
        total_frames: Total number of frames
        frames: List of animation frames
        config: Animation configuration
        metadata: Additional metadata
        duration: Total animation duration
    """
    animation_id: str
    animation_type: AnimationType
    total_frames: int
    frames: List[AnimationFrame]
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0


class PhysicsVerseAnimationService:
    """
    PhysicsVerse animation service.
    
    This service handles physics animations including:
    - Motion with trajectory tracing
    - Wave propagation (mechanical and electromagnetic)
    - Circuit transient behavior
    - Orbital motion
    - Collision animations
    - Interactive parameter animations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the PhysicsVerse animation service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._animations: Dict[str, PhysicsAnimation] = {}
        self._current_animation: Optional[PhysicsAnimation] = None
        self._current_frame_index: int = 0
        self._animation_state: AnimationState = AnimationState.IDLE
        self._start_time: float = 0.0
        self._paused_time: float = 0.0
        self._frame_times: List[float] = []
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        logger.info("PhysicsVerseAnimationService configured with settings: %s", list(config.keys()))
    
    # ==================== MOTION ANIMATIONS ====================
    
    def create_motion_animation(
        self,
        initial_position: Vector2D,
        initial_velocity: Vector2D,
        acceleration: Union[Vector2D, Callable[[float, Vector2D], Vector2D]],
        config: Optional[MotionAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create a motion animation with constant or variable acceleration.
        
        Args:
            initial_position: Starting position
            initial_velocity: Starting velocity
            acceleration: Acceleration (constant or function of time and position)
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        anim_config = config or MotionAnimationConfig()
        
        frames = []
        state = PhysicsState(
            time=0.0,
            positions={"obj": initial_position},
            velocities={"obj": initial_velocity}
        )
        
        dt = 1.0 / anim_config.fps
        num_frames = int(anim_config.duration * anim_config.fps * anim_config.time_scale)
        
        trail = []
        
        for i in range(num_frames):
            current_time = i * dt / anim_config.time_scale
            
            # Store frame
            frame = AnimationFrame(
                frame_number=i,
                timestamp=current_time,
                state=PhysicsState(
                    time=current_time,
                    positions=state.positions.copy(),
                    velocities=state.velocities.copy()
                ),
                trail=trail.copy()
            )
            frames.append(frame)
            
            # Update trail
            if anim_config.show_trail:
                trail.append(state.positions["obj"])
                if len(trail) > anim_config.trail_length:
                    trail.pop(0)
            
            # Integrate to next state
            if callable(acceleration):
                # Time-dependent or position-dependent acceleration
                acc = acceleration(current_time, state.positions["obj"])
            else:
                # Constant acceleration
                acc = acceleration
            
            state.accelerations["obj"] = acc
            
            # Use specified integration method
            if anim_config.integration_method == IntegrationMethod.SEMI_IMPLICIT_EULAR:
                state = self._semi_implicit_euler_step(state, dt / anim_config.time_scale)
            elif anim_config.integration_method == IntegrationMethod.RUNGE_KUTTA_4:
                state = self._rk4_step(state, dt / anim_config.time_scale)
            else:
                state = self._euler_step(state, dt / anim_config.time_scale)
        
        animation = PhysicsAnimation(
            animation_id=f"motion_{datetime.now().timestamp()}",
            animation_type=AnimationType.MOTION,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": anim_config.duration,
                "fps": anim_config.fps,
                "time_scale": anim_config.time_scale,
                "integration_method": anim_config.integration_method.value
            },
            metadata={
                "initial_position": initial_position.to_dict(),
                "initial_velocity": initial_velocity.to_dict(),
                "acceleration_type": "callable" if callable(acceleration) else "constant"
            },
            duration=anim_config.duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    def create_projectile_motion_animation(
        self,
        initial_speed: float,
        launch_angle: float,
        initial_height: float = 0.0,
        gravity: float = 9.81,
        config: Optional[MotionAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create a projectile motion animation.
        
        Args:
            initial_speed: Initial speed (m/s)
            launch_angle: Launch angle (degrees)
            initial_height: Initial height (m)
            gravity: Gravitational acceleration (m/s²)
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        angle_rad = radians(launch_angle)
        
        initial_velocity = Vector2D(
            initial_speed * cos(angle_rad),
            initial_speed * sin(angle_rad)
        )
        
        def acceleration_func(t: float, pos: Vector2D) -> Vector2D:
            return Vector2D(0, -gravity)
        
        return self.create_motion_animation(
            initial_position=Vector2D(0, initial_height),
            initial_velocity=initial_velocity,
            acceleration=acceleration_func,
            config=config
        )
    
    def create_shake_motion_animation(
        self,
        equilibrium_position: Vector2D,
        amplitude: Vector2D,
        angular_frequency: float,
        phase: float = 0.0,
        duration: float = 5.0,
        config: Optional[MotionAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create simple harmonic motion animation.
        
        Args:
            equilibrium_position: Center of oscillation
            amplitude: Maximum displacement
            angular_frequency: Angular frequency (rad/s)
            phase: Initial phase
            duration: Animation duration
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        def position_func(t: float) -> Vector2D:
            return equilibrium_position + amplitude * sin(angular_frequency * t + phase)
        
        def velocity_func(t: float) -> Vector2D:
            return amplitude * angular_frequency * cos(angular_frequency * t + phase)
        
        anim_config = config or MotionAnimationConfig()
        frames = []
        
        dt = 1.0 / anim_config.fps
        num_frames = int(duration * anim_config.fps)
        
        for i in range(num_frames):
            t = i * dt
            position = position_func(t)
            velocity = velocity_func(t)
            
            state = PhysicsState(
                time=t,
                positions={"osc": position},
                velocities={"osc": velocity},
                accelerations={"osc": amplitude * (-angular_frequency**2) * sin(angular_frequency * t + phase)}
            )
            
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=state
            )
            frames.append(frame)
        
        animation = PhysicsAnimation(
            animation_id=f"shm_{datetime.now().timestamp()}",
            animation_type=AnimationType.OSCILLATION,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": duration,
                "fps": anim_config.fps,
                "amplitude": amplitude.to_dict(),
                "angular_frequency": angular_frequency
            },
            metadata={
                "equilibrium": equilibrium_position.to_dict(),
                "period": 2 * pi / angular_frequency,
                "frequency": angular_frequency / (2 * pi)
            },
            duration=duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    # ==================== WAVE ANIMATIONS ====================
    
    def create_wave_animation(
        self,
        amplitude: float,
        wavelength: float,
        frequency: float,
        config: Optional[WaveAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create a wave propagation animation.
        
        Args:
            amplitude: Wave amplitude
            wavelength: Wavelength
            frequency: Frequency
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        wave_config = config or WaveAnimationConfig()
        
        frames = []
        k = 2 * pi / wavelength  # Wave number
        omega = 2 * pi * frequency  # Angular frequency
        
        num_points = wave_config.particle_count
        spacing = wavelength / 2
        
        dt = 1.0 / wave_config.fps
        duration = wave_config.duration
        num_frames = int(duration * wave_config.fps)
        
        for i in range(num_frames):
            t = i * dt
            positions = []
            velocities = []
            
            for j in range(num_points):
                x = j * spacing
                displacement = wave_config.amplitude * sin(k * x - omega * t + wave_config.phase)
                positions.append(Vector2D(x, displacement))
                # Vertical velocity
                velocities.append(Vector2D(0, -wave_config.amplitude * omega * cos(k * x - omega * t + wave_config.phase)))
            
            state = PhysicsState(
                time=t,
                positions={f"p_{j}": positions[j] for j in range(num_points)},
                velocities={f"p_{j}": velocities[j] for j in range(num_points)}
            )
            
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=state,
                metadata={
                    "type": wave_config.wave_type,
                    "direction": wave_config.propagation_direction
                }
            )
            frames.append(frame)
        
        animation = PhysicsAnimation(
            animation_id=f"wave_{datetime.now().timestamp()}",
            animation_type=AnimationType.WAVE,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": duration,
                "fps": wave_config.fps,
                "amplitude": amplitude,
                "wavelength": wavelength,
                "frequency": frequency
            },
            metadata={
                "wave_speed": frequency * wavelength,
                "period": 1 / frequency,
                "num_points": num_points
            },
            duration=duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    def create_standing_wave_animation(
        self,
        amplitude: float,
        wavelength: float,
        frequency: float,
        node_positions: List[float],
        antinode_positions: List[float],
        config: Optional[WaveAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create a standing wave animation.
        
        Args:
            amplitude: Maximum amplitude
            wavelength: Wavelength
            frequency: Frequency
            node_positions: Positions of nodes
            antinode_positions: Positions of antinodes
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        wave_config = config or WaveAnimationConfig()
        
        frames = []
        k = 2 * pi / wavelength
        omega = 2 * pi * frequency
        
        dt = 1.0 / wave_config.fps
        num_frames = int(wave_config.duration * wave_config.fps)
        
        # Generate points along the standing wave
        x_min = min(node_positions + antinode_positions) - 0.5 * wavelength
        x_max = max(node_positions + antinode_positions) + 0.5 * wavelength
        num_points = wave_config.particle_count
        
        for i in range(num_frames):
            t = i * dt
            positions = []
            
            for j in range(num_points):
                x = x_min + (x_max - x_min) * j / (num_points - 1)
                displacement = 2 * amplitude * sin(k * x) * cos(omega * t)
                positions.append(Vector2D(x, displacement))
            
            state = PhysicsState(
                time=t,
                positions={f"p_{j}": positions[j] for j in range(num_points)}
            )
            
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=state,
                metadata={
                    "nodes": node_positions,
                    "antinodes": antinode_positions
                }
            )
            frames.append(frame)
        
        animation = PhysicsAnimation(
            animation_id=f"standing_wave_{datetime.now().timestamp()}",
            animation_type=AnimationType.WAVE,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": wave_config.duration,
                "fps": wave_config.fps,
                "amplitude": amplitude,
                "wavelength": wavelength,
                "frequency": frequency
            },
            metadata={
                "type": "standing_wave",
                "harmonic": wavelength / (2 * (x_max - x_min))
            },
            duration=wave_config.duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    # ==================== CIRCUIT ANIMATIONS ====================
    
    def create_rc_charging_animation(
        self,
        voltage: float,
        resistance: float,
        capacitance: float,
        config: Optional[CircuitAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create RC circuit charging animation.
        
        Args:
            voltage: Source voltage
            resistance: Resistance
            capacitance: Capacitance
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        circuit_config = config or CircuitAnimationConfig()
        
        tau = resistance * capacitance  # Time constant
        
        frames = []
        dt = 1.0 / circuit_config.fps
        num_frames = int(circuit_config.duration * circuit_config.fps)
        
        for i in range(num_frames):
            t = i * dt
            
            # Calculate circuit values
            voltage_across_cap = voltage * (1 - exp(-t / tau))
            voltage_across_res = voltage - voltage_across_cap
            current = voltage_across_res / resistance
            charge = capacitance * voltage_across_cap
            power = current * voltage_across_res
            
            state = PhysicsState(
                time=t,
                positions={},
                velocities={},
                additional_properties={
                    "capacitor_voltage": voltage_across_cap,
                    "resistor_voltage": voltage_across_res,
                    "current": current,
                    "charge": charge,
                    "power": power,
                    "energy": 0.5 * capacitance * voltage_across_cap**2
                }
            )
            
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=state,
                metadata={
                    "time_constant": tau,
                    "target_voltage": voltage
                }
            )
            frames.append(frame)
        
        animation = PhysicsAnimation(
            animation_id=f"rc_charging_{datetime.now().timestamp()}",
            animation_type=AnimationType.CIRCUIT_TRANSIENT,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": circuit_config.duration,
                "fps": circuit_config.fps,
                "voltage": voltage,
                "resistance": resistance,
                "capacitance": capacitance
            },
            metadata={
                "time_constant": tau,
                "half_life": tau * 0.693,
                "full_charge_time": 5 * tau
            },
            duration=circuit_config.duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    def create_rl_circuit_animation(
        self,
        voltage: float,
        resistance: float,
        inductance: float,
        config: Optional[CircuitAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create RL circuit current growth animation.
        
        Args:
            voltage: Source voltage
            resistance: Resistance
            inductance: Inductance
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        circuit_config = config or CircuitAnimationConfig()
        
        tau = inductance / resistance  # Time constant
        
        frames = []
        dt = 1.0 / circuit_config.fps
        num_frames = int(circuit_config.duration * circuit_config.fps)
        
        for i in range(num_frames):
            t = i * dt
            
            # Calculate circuit values
            current = (voltage / resistance) * (1 - exp(-t / tau))
            voltage_across_res = current * resistance
            voltage_across_ind = voltage - voltage_across_res
            power = current * voltage
            energy = 0.5 * inductance * current**2
            
            state = PhysicsState(
                time=t,
                additional_properties={
                    "current": current,
                    "inductor_voltage": voltage_across_ind,
                    "resistor_voltage": voltage_across_res,
                    "power": power,
                    "energy": energy
                }
            )
            
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=state,
                metadata={
                    "time_constant": tau,
                    "max_current": voltage / resistance
                }
            )
            frames.append(frame)
        
        animation = PhysicsAnimation(
            animation_id=f"rl_circuit_{datetime.now().timestamp()}",
            animation_type=AnimationType.CIRCUIT_TRANSIENT,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": circuit_config.duration,
                "fps": circuit_config.fps,
                "voltage": voltage,
                "resistance": resistance,
                "inductance": inductance
            },
            metadata={
                "time_constant": tau
            },
            duration=circuit_config.duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    # ==================== ORBITAL ANIMATIONS ====================
    
    def create_orbital_motion_animation(
        self,
        central_mass: float,
        initial_position: Vector2D,
        initial_velocity: Vector2D,
        gravitational_constant: float = 6.67430e-11,
        config: Optional[MotionAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create orbital motion animation.
        
        Args:
            central_mass: Mass of central body
            initial_position: Initial position relative to central body
            initial_velocity: Initial velocity
            gravitational_constant: Gravitational constant
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        anim_config = config or MotionAnimationConfig()
        
        frames = []
        state = PhysicsState(
            time=0.0,
            positions={"satellite": initial_position},
            velocities={"satellite": initial_velocity}
        )
        
        dt = 1.0 / anim_config.fps
        num_frames = int(anim_config.duration * anim_config.fps)
        
        trail = []
        
        for i in range(num_frames):
            t = i * dt
            
            # Calculate gravitational acceleration
            pos = state.positions["satellite"]
            r = pos.magnitude()
            
            if r > 0.001:
                acc_magnitude = gravitational_constant * central_mass / r**2
                acceleration = pos.normalize() * (-acc_magnitude)
            else:
                acceleration = Vector2D(0, 0)
            
            state.accelerations["satellite"] = acceleration
            
            # Store frame
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=PhysicsState(
                    time=t,
                    positions=state.positions.copy(),
                    velocities=state.velocities.copy()
                ),
                trail=trail.copy()
            )
            frames.append(frame)
            
            # Update trail
            if anim_config.show_trail:
                trail.append(state.positions["satellite"])
                if len(trail) > anim_config.trail_length:
                    trail.pop(0)
            
            # Integrate
            state = self._semi_implicit_euler_step(state, dt)
        
        animation = PhysicsAnimation(
            animation_id=f"orbital_{datetime.now().timestamp()}",
            animation_type=AnimationType.ORBITAL,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": anim_config.duration,
                "fps": anim_config.fps,
                "central_mass": central_mass,
                "gravitational_constant": gravitational_constant
            },
            metadata={
                "initial_position": initial_position.to_dict(),
                "initial_velocity": initial_velocity.to_dict()
            },
            duration=anim_config.duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    # ==================== COLLISION ANIMATIONS ====================
    
    def create_collision_animation(
        self,
        mass1: float,
        mass2: float,
        velocity1: Vector2D,
        velocity2: Vector2D,
        position1: Vector2D,
        position2: Vector2D,
        elasticity: float = 1.0,
        config: Optional[MotionAnimationConfig] = None
    ) -> PhysicsAnimation:
        """
        Create collision animation between two objects.
        
        Args:
            mass1: Mass of first object
            mass2: Mass of second object
            velocity1: Initial velocity of first object
            velocity2: Initial velocity of second object
            position1: Initial position of first object
            position2: Initial position of second object
            elasticity: Coefficient of restitution (0-1)
            config: Animation configuration
            
        Returns:
            Complete PhysicsAnimation object
        """
        anim_config = config or MotionAnimationConfig()
        
        frames = []
        state = PhysicsState(
            time=0.0,
            positions={"obj1": position1, "obj2": position2},
            velocities={"obj1": velocity1, "obj2": velocity2}
        )
        
        dt = 1.0 / anim_config.fps
        num_frames = int(anim_config.duration * anim_config.fps)
        
        # Check for collision
        collision_detected = False
        collision_time = None
        radius1 = (3 * mass1 / (4 * pi * 1000))**(1/3) if mass1 > 0 else 0.1
        radius2 = (3 * mass2 / (4 * pi * 1000))**(1/3) if mass2 > 0 else 0.1
        
        for i in range(num_frames):
            t = i * dt
            
            pos1 = state.positions["obj1"]
            pos2 = state.positions["obj2"]
            dist = (pos1 - pos2).magnitude()
            
            # Check collision
            if not collision_detected and dist <= (radius1 + radius2):
                collision_detected = True
                collision_time = t
                
                # Elastic collision response
                v1 = state.velocities["obj1"]
                v2 = state.velocities["obj2"]
                
                # Relative velocity
                v_rel = v1 - v2
                pos_rel = pos1 - pos2
                
                # Only resolve if objects are approaching
                if v_rel.dot(pos_rel) < 0:
                    # Update velocities
                    new_v1 = v1 - (2 * mass2 / (mass1 + mass2)) * (
                        v_rel.dot(pos_rel) / (pos_rel.magnitude()**2)
                    ) * pos_rel * elasticity
                    
                    new_v2 = v2 + (2 * mass1 / (mass1 + mass2)) * (
                        v_rel.dot(pos_rel) / (pos_rel.magnitude()**2)
                    ) * pos_rel * elasticity
                    
                    state.velocities["obj1"] = new_v1
                    state.velocities["obj2"] = new_v2
            
            frame = AnimationFrame(
                frame_number=i,
                timestamp=t,
                state=PhysicsState(
                    time=t,
                    positions=state.positions.copy(),
                    velocities=state.velocities.copy()
                ),
                metadata={
                    "collision_detected": collision_detected,
                    "collision_time": collision_time,
                    "elasticity": elasticity
                }
            )
            frames.append(frame)
            
            # Integrate
            state = self._euler_step(state, dt)
        
        animation = PhysicsAnimation(
            animation_id=f"collision_{datetime.now().timestamp()}",
            animation_type=AnimationType.COLLISION,
            total_frames=num_frames,
            frames=frames,
            config={
                "duration": anim_config.duration,
                "fps": anim_config.fps,
                "mass1": mass1,
                "mass2": mass2,
                "elasticity": elasticity
            },
            metadata={
                "momentum_conserved": True if elasticity == 1.0 else False,
                "kinetic_energy_conserved": True if elasticity == 1.0 else False
            },
            duration=anim_config.duration
        )
        
        self._animations[animation.animation_id] = animation
        return animation
    
    # ==================== ANIMATION CONTROL ====================
    
    def play_animation(self, animation_id: str) -> bool:
        """
        Start playing an animation.
        
        Args:
            animation_id: ID of animation to play
            
        Returns:
            True if successful, False otherwise
        """
        if animation_id not in self._animations:
            return False
        
        self._current_animation = self._animations[animation_id]
        self._current_frame_index = 0
        self._animation_state = AnimationState.PLAYING
        self._start_time = time.time()
        self._frame_times = []
        
        return True
    
    def pause_animation(self) -> None:
        """Pause the current animation."""
        if self._animation_state == AnimationState.PLAYING:
            self._animation_state = AnimationState.PAUSED
            self._paused_time = time.time()
    
    def resume_animation(self) -> None:
        """Resume a paused animation."""
        if self._animation_state == AnimationState.PAUSED:
            self._animation_state = AnimationState.PLAYING
    
    def stop_animation(self) -> None:
        """Stop the current animation."""
        self._animation_state = AnimationState.IDLE
        self._current_animation = None
        self._current_frame_index = 0
    
    def seek_animation(self, timestamp: float) -> Optional[AnimationFrame]:
        """
        Seek to a specific time in the animation.
        
        Args:
            timestamp: Target time in seconds
            
        Returns:
            AnimationFrame at that time, or None if not found
        """
        if not self._current_animation:
            return None
        
        fps = self._current_animation.config.get("fps", 60)
        frame_index = int(timestamp * fps)
        frame_index = max(0, min(frame_index, self._current_animation.total_frames - 1))
        
        self._current_frame_index = frame_index
        return self._current_animation.frames[frame_index]
    
    def get_current_frame(self) -> Optional[AnimationFrame]:
        """
        Get the current animation frame.
        
        Returns:
            Current AnimationFrame, or None if no animation playing
        """
        if not self._current_animation:
            return None
        
        if self._animation_state == AnimationState.IDLE:
            return None
        
        if self._animation_state == AnimationState.PLAYING:
            # Advance frame based on elapsed time
            elapsed = time.time() - self._start_time
            fps = self._current_animation.config.get("fps", 60)
            target_frame = int(elapsed * fps)
            
            if target_frame >= self._current_animation.total_frames:
                self._animation_state = AnimationState.COMPLETED
                return self._current_animation.frames[-1]
            
            self._current_frame_index = target_frame
        
        return self._current_animation.frames[self._current_frame_index]
    
    def get_animation_state(self) -> Dict[str, Any]:
        """
        Get the current animation state.
        
        Returns:
            Dictionary with animation state information
        """
        current_frame = self.get_current_frame()
        
        return {
            "state": self._animation_state.value,
            "animation_id": self._current_animation.animation_id if self._current_animation else None,
            "frame_index": self._current_frame_index,
            "total_frames": self._current_animation.total_frames if self._current_animation else 0,
            "timestamp": current_frame.timestamp if current_frame else 0.0,
            "progress": (
                self._current_frame_index / self._current_animation.total_frames
                if self._current_animation and self._current_animation.total_frames > 0 else 0
            )
        }
    
    # ==================== FRAME EXPORT ====================
    
    def export_frames_to_dict(
        self,
        animation: PhysicsAnimation
    ) -> List[Dict[str, Any]]:
        """
        Export animation frames to dictionaries for serialization.
        
        Args:
            animation: Animation to export
            
        Returns:
            List of frame dictionaries
        """
        export_list = []
        
        for frame in animation.frames:
            frame_dict = {
                "frame_number": frame.frame_number,
                "timestamp": frame.timestamp,
                "metadata": frame.metadata,
                "positions": {
                    k: v.to_dict() for k, v in frame.state.positions.items()
                },
                "velocities": {
                    k: v.to_dict() for k, v in frame.state.velocities.items()
                },
                "trail": [p.to_dict() for p in frame.trail]
            }
            
            # Include additional properties
            if frame.state.additional_properties:
                frame_dict["additional_properties"] = frame.state.additional_properties
            
            export_list.append(frame_dict)
        
        return export_list
    
    def get_animation_info(self, animation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an animation.
        
        Args:
            animation_id: Animation identifier
            
        Returns:
            Dictionary with animation information
        """
        if animation_id not in self._animations:
            return None
        
        animation = self._animations[animation_id]
        
        return {
            "animation_id": animation.animation_id,
            "animation_type": animation.animation_type.value,
            "total_frames": animation.total_frames,
            "duration": animation.duration,
            "fps": animation.config.get("fps", 60),
            "config": animation.config,
            "metadata": animation.metadata
        }
    
    def list_animations(self) -> List[str]:
        """
        List all cached animations.
        
        Returns:
            List of animation IDs
        """
        return list(self._animations.keys())
    
    # ==================== NUMERICAL INTEGRATION ====================
    
    def _euler_step(
        self,
        state: PhysicsState,
        dt: float
    ) -> PhysicsState:
        """Perform Euler integration step."""
        new_state = PhysicsState(
            time=state.time + dt,
            positions=state.positions.copy(),
            velocities=state.velocities.copy()
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
    
    def _semi_implicit_euler_step(
        self,
        state: PhysicsState,
        dt: float
    ) -> PhysicsState:
        """Perform semi-implicit Euler integration step."""
        new_state = PhysicsState(
            time=state.time + dt,
            positions=state.positions.copy(),
            velocities=state.velocities.copy()
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
    
    def _rk4_step(
        self,
        state: PhysicsState,
        dt: float
    ) -> PhysicsState:
        """Perform 4th order Runge-Kutta integration step."""
        def acceleration_at(state: PhysicsState) -> Dict[str, Vector2D]:
            return state.accelerations.copy()
        
        k1 = acceleration_at(state)
        
        state2 = PhysicsState(
            time=state.time + dt/2,
            positions={k: state.positions[k] + state.velocities[k] * (dt/2)
                      for k in state.positions},
            velocities={k: state.velocities[k] + k1.get(k, Vector2D()) * (dt/2)
                       for k in state.velocities}
        )
        k2 = acceleration_at(state2)
        
        state3 = PhysicsState(
            time=state.time + dt/2,
            positions={k: state.positions[k] + state.velocities[k] * (dt/2)
                      for k in state.positions},
            velocities={k: state.velocities[k] + k2.get(k, Vector2D()) * (dt/2)
                       for k in state.velocities}
        )
        k3 = acceleration_at(state3)
        
        state4 = PhysicsState(
            time=state.time + dt,
            positions={k: state.positions[k] + state.velocities[k] * dt
                      for k in state.positions},
            velocities={k: state.velocities[k] + k3.get(k, Vector2D()) * dt
                       for k in state.velocities}
        )
        k4 = acceleration_at(state4)
        
        new_state = PhysicsState(
            time=state.time + dt,
            positions={},
            velocities={}
        )
        
        for entity_id in state.positions:
            pos_k1 = k1.get(entity_id, Vector2D())
            pos_k2 = k2.get(entity_id, Vector2D())
            pos_k3 = k3.get(entity_id, Vector2D())
            pos_k4 = k4.get(entity_id, Vector2D())
            
            new_state.positions[entity_id] = (
                state.positions[entity_id] +
                (pos_k1 + pos_k2 * 2 + pos_k3 * 2 + pos_k4) * (dt / 6)
            )
        
        for entity_id in state.velocities:
            vel_k1 = k1.get(entity_id, Vector2D())
            vel_k2 = k2.get(entity_id, Vector2D())
            vel_k3 = k3.get(entity_id, Vector2D())
            vel_k4 = k4.get(entity_id, Vector2D())
            
            new_state.velocities[entity_id] = (
                state.velocities[entity_id] +
                (vel_k1 + vel_k2 * 2 + vel_k3 * 2 + vel_k4) * (dt / 6)
            )
        
        return new_state
