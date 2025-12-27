"""
ChemVerse Animation Service

This module provides animation services for chemical reactions and molecular
processes in the VisualVerse learning platform. It handles reaction animations,
molecular motion, and time-based visualizations.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from .chem_core import (
    Molecule, Atom, Bond, ChemicalReaction, Vector3D,
    ReactionType, ReactionAnimationConfig
)


class AnimationState(str, Enum):
    """States of animation playback."""
    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


class AnimationEasing(str, Enum):
    """Easing functions for smooth animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"


class ParticleEffectType(str, Enum):
    """Types of particle effects for reactions."""
    SPARK = "spark"
    BUBBLE = "bubble"
    FLASH = "flash"
    SMOKE = "smoke"
    PRECIPITATE = "precipitate"
    GAS_RELEASE = "gas_release"


@dataclass
class AnimationKeyframe:
    """A single keyframe in an animation."""
    time_ms: float
    atom_positions: Dict[str, Vector3D] = field(default_factory=dict)
    bond_changes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    color_changes: Dict[str, Tuple[int, int, int]] = field(default_factory=dict)
    scale_changes: Dict[str, float] = field(default_factory=dict)


@dataclass
class AnimationFrame:
    """A single frame of animation data."""
    time_ms: float
    atom_positions: Dict[str, Vector3D]
    bond_states: Dict[str, Dict[str, Any]]
    particle_effects: List[Dict[str, Any]] = field(default_factory=list)
    camera_position: Vector3D = field(default_factory=lambda: Vector3D(0, 0, 10))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        atoms = {}
        for atom_id, pos in self.atom_positions.items():
            atoms[atom_id] = {"x": pos.x, "y": pos.y, "z": pos.z}
        
        return {
            "time_ms": self.time_ms,
            "atom_positions": atoms,
            "bond_states": self.bond_states,
            "particle_effects": self.particle_effects,
            "camera_position": {
                "x": self.camera_position.x,
                "y": self.camera_position.y,
                "z": self.camera_position.z
            }
        }


@dataclass
class TransitionState:
    """Represents a transition state in a reaction mechanism."""
    name: str
    energy: float
    lifetime_ps: float = 1e-12  # picoseconds
    geometry: Dict[str, Vector3D] = field(default_factory=dict)
    partial_bonds: Dict[str, float] = field(default_factory=dict)


@dataclass
class ReactionAnimation:
    """Complete animation data for a chemical reaction."""
    reaction: ChemicalReaction
    frames: List[AnimationFrame] = field(default_factory=list)
    keyframes: List[AnimationKeyframe] = field(default_factory=list)
    transition_states: List[TransitionState] = field(default_factory=list)
    duration_ms: int = 2000
    state: AnimationState = AnimationState.IDLE
    
    def get_frame_at_time(self, time_ms: float) -> Optional[AnimationFrame]:
        """Get the animation frame at a specific time."""
        if not self.frames:
            return None
        
        for frame in self.frames:
            if abs(frame.time_ms - time_ms) < 1:
                return frame
        return None
    
    def get_progress(self) -> float:
        """Get animation progress as a fraction (0-1)."""
        if self.duration_ms == 0:
            return 1.0
        return min(1.0, self.frames[-1].time_ms / self.duration_ms) if self.frames else 0.0


@dataclass
class MolecularMotion:
    """Represents molecular motion/vibration."""
    atom_id: str
    amplitude: float
    frequency_hz: float
    direction: Vector3D
    motion_type: str = "vibration"
    
    def get_position_at_time(self, base_pos: Vector3D, time_ms: float) -> Vector3D:
        """Get the atom position at a specific time."""
        if self.motion_type == "vibration":
            phase = 2 * 3.14159 * self.frequency_hz * time_ms / 1000
            offset = self.direction * self.amplitude * math.sin(phase)
            return base_pos + offset
        elif self.motion_type == "rotation":
            # Simplified rotation
            return base_pos  # Would need quaternion math for full rotation
        return base_pos


@dataclass
class ParticleEffect:
    """Represents a visual particle effect."""
    effect_type: ParticleEffectType
    position: Vector3D
    velocity: Vector3D
    size: float
    color: Tuple[int, int, int]
    lifetime_ms: float
    start_time_ms: float = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.effect_type.value,
            "position": {"x": self.position.x, "y": self.position.y, "z": self.position.z},
            "velocity": {"x": self.velocity.x, "y": self.velocity.y, "z": self.velocity.z},
            "size": self.size,
            "color": list(self.color),
            "lifetime_ms": self.lifetime_ms,
            "start_time_ms": self.start_time_ms
        }


class EasingFunction:
    """Collection of easing functions for animations."""
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear easing."""
        return t
    
    @staticmethod
    def ease_in(t: float) -> float:
        """Ease in - starts slow, accelerates."""
        return t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        """Ease out - starts fast, decelerates."""
        return t * (2 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        """Ease in out - slow start and end, fast middle."""
        return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def apply(easing: AnimationEasing, t: float) -> float:
        """Apply an easing function."""
        functions = {
            AnimationEasing.LINEAR: EasingFunction.linear,
            AnimationEasing.EASE_IN: EasingFunction.ease_in,
            AnimationEasing.EASE_OUT: EasingFunction.ease_out,
            AnimationEasing.EASE_IN_OUT: EasingFunction.ease_in_out,
        }
        func = functions.get(easing, EasingFunction.linear)
        return func(t)


class ReactionAnimator:
    """Handles the creation and management of reaction animations."""
    
    def __init__(self, config: ReactionAnimationConfig = None):
        """Initialize the animator with configuration."""
        self.config = config or ReactionAnimationConfig()
    
    def animate_reaction(
        self,
        reaction: ChemicalReaction,
        duration_ms: int = None
    ) -> ReactionAnimation:
        """Create an animation for a chemical reaction."""
        duration = duration_ms or self.config.duration_ms
        
        animation = ReactionAnimation(
            reaction=reaction,
            duration_ms=duration,
            state=AnimationState.IDLE
        )
        
        # Generate frames based on reaction type
        if reaction.reaction_type == ReactionType.SYNTHESIS:
            animation = self._animate_synthesis(reaction, animation, duration)
        elif reaction.reaction_type == ReactionType.DECOMPOSITION:
            animation = self._animate_decomposition(reaction, animation, duration)
        elif reaction.reaction_type == ReactionType.COMBUSTION:
            animation = self._animate_combustion(reaction, animation, duration)
        elif reaction.reaction_type == ReactionType.ACID_BASE:
            animation = self._animate_acid_base(reaction, animation, duration)
        else:
            animation = self._animate_generic(reaction, animation, duration)
        
        return animation
    
    def _animate_synthesis(
        self,
        reaction: ChemicalReaction,
        animation: ReactionAnimation,
        duration: int
    ) -> ReactionAnimation:
        """Animate a synthesis reaction (A + B → AB)."""
        if len(reaction.reactants) < 2:
            return self._animate_generic(reaction, animation, duration)
        
        # Get starting positions of reactants
        start_positions: Dict[str, Vector3D] = {}
        for mol in reaction.reactants:
            for atom in mol.atoms:
                start_positions[atom.id] = atom.position
        
        # Get final positions from products
        end_positions: Dict[str, Vector3D] = {}
        for mol in reaction.products:
            for atom in mol.atoms:
                end_positions[atom.id] = atom.position
        
        # Generate intermediate frames
        num_frames = 30
        frame_duration = duration / num_frames
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_progress = EasingFunction.apply(
                AnimationEasing.EASE_IN_OUT,
                progress
            )
            
            frame_positions: Dict[str, Vector3D] = {}
            bond_states: Dict[str, Dict[str, Any]] = {}
            
            # Interpolate positions
            for atom_id, start_pos in start_positions.items():
                if atom_id in end_positions:
                    end_pos = end_positions[atom_id]
                    frame_positions[atom_id] = Vector3D(
                        start_pos.x + (end_pos.x - start_pos.x) * eased_progress,
                        start_pos.y + (end_pos.y - start_pos.y) * eased_progress,
                        start_pos.z + (end_pos.z - start_pos.z) * eased_progress
                    )
            
            # Add particle effects for bond formation
            if progress > 0.7 and self.config.particle_effects:
                effects = self._create_formation_effects(frame_positions)
            else:
                effects = []
            
            animation.frames.append(AnimationFrame(
                time_ms=i * frame_duration,
                atom_positions=frame_positions,
                bond_states=bond_states,
                particle_effects=effects
            ))
        
        return animation
    
    def _animate_decomposition(
        self,
        reaction: ChemicalReaction,
        animation: ReactionAnimation,
        duration: int
    ) -> ReactionAnimation:
        """Animate a decomposition reaction (AB → A + B)."""
        if len(reaction.reactants) < 1 or len(reaction.products) < 2:
            return self._animate_generic(reaction, animation, duration)
        
        # Start with reactant positions
        start_positions: Dict[str, Vector3D] = {}
        for mol in reaction.reactants:
            for atom in mol.atoms:
                start_positions[atom.id] = atom.position
        
        # End with product positions
        end_positions: Dict[str, Vector3D] = {}
        for mol in reaction.products:
            for atom in mol.atoms:
                end_positions[atom.id] = atom.position
        
        # Generate frames
        num_frames = 30
        frame_duration = duration / num_frames
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            eased_progress = EasingFunction.apply(
                AnimationEasing.EASE_OUT,
                progress
            )
            
            frame_positions: Dict[str, Vector3D] = {}
            bond_states: Dict[str, Dict[str, Any]] = {}
            
            for atom_id, start_pos in start_positions.items():
                if atom_id in end_positions:
                    end_pos = end_positions[atom_id]
                    # Add separation movement
                    separation = progress * 5  # Move apart
                    direction = (end_pos - start_pos).normalize()
                    final_pos = end_pos + direction * separation * eased_progress
                    
                    frame_positions[atom_id] = Vector3D(
                        start_pos.x + (final_pos.x - start_pos.x) * eased_progress,
                        start_pos.y + (final_pos.y - start_pos.y) * eased_progress,
                        start_pos.z + (final_pos.z - start_pos.z) * eased_progress
                    )
            
            # Add breaking effects
            if 0.2 < progress < 0.4 and self.config.particle_effects:
                effects = self._create_breaking_effects(start_positions)
            else:
                effects = []
            
            animation.frames.append(AnimationFrame(
                time_ms=i * frame_duration,
                atom_positions=frame_positions,
                bond_states=bond_states,
                particle_effects=effects
            ))
        
        return animation
    
    def _animate_combustion(
        self,
        reaction: ChemicalReaction,
        animation: ReactionAnimation,
        duration: int
    ) -> ReactionAnimation:
        """Animate a combustion reaction with fire effects."""
        # Start with fuel and oxygen
        start_positions: Dict[str, Vector3D] = {}
        for mol in reaction.reactants:
            for atom in mol.atoms:
                start_positions[atom.id] = atom.position
        
        # Generate frames with fire effects
        num_frames = 30
        frame_duration = duration / num_frames
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            
            frame_positions: Dict[str, Vector3D] = {}
            bond_states: Dict[str, Dict[str, Any]] = {}
            effects: List[Dict[str, Any]] = []
            
            # Interpolate positions (simplified)
            for atom_id, start_pos in start_positions.items():
                # Add vibration for heat effect
                vibration = 0.1 * math.sin(progress * 10)
                frame_positions[atom_id] = Vector3D(
                    start_pos.x + vibration,
                    start_pos.y + vibration,
                    start_pos.z
                )
            
            # Add flame effects
            if 0.3 < progress < 0.9 and self.config.particle_effects:
                for atom_id, pos in frame_positions.items():
                    effects.append(ParticleEffect(
                        effect_type=ParticleEffectType.FLASH,
                        position=pos,
                        velocity=Vector3D(0, 2, 0),
                        size=0.5 * (1 - progress),
                        color=(255, 150 + int(progress * 100), 0),
                        lifetime_ms=500
                    ).to_dict())
            
            animation.frames.append(AnimationFrame(
                time_ms=i * frame_duration,
                atom_positions=frame_positions,
                bond_states=bond_states,
                particle_effects=effects
            ))
        
        return animation
    
    def _animate_acid_base(
        self,
        reaction: ChemicalReaction,
        animation: ReactionAnimation,
        duration: int
    ) -> ReactionAnimation:
        """Animate an acid-base neutralization reaction."""
        # Get all atoms from reactants
        all_atoms: Dict[str, Tuple[Vector3D, str]] = {}
        for mol in reaction.reactants:
            for atom in mol.atoms:
                all_atoms[atom.id] = (atom.position, atom.element_symbol)
        
        num_frames = 30
        frame_duration = duration / num_frames
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            
            frame_positions: Dict[str, Vector3D] = {}
            bond_states: Dict[str, Dict[str, Any]] = {}
            effects: List[Dict[str, Any]] = []
            
            for atom_id, (pos, element) in all_atoms.items():
                # H+ ions move towards OH- or vice versa
                frame_positions[atom_id] = Vector3D(
                    pos.x + math.sin(progress * 3.14) * 0.5,
                    pos.y + math.cos(progress * 3.14) * 0.5,
                    pos.z
                )
            
            # Add flash for neutralization
            if progress > 0.8 and self.config.particle_effects:
                effects.append(ParticleEffect(
                    effect_type=ParticleEffectType.FLASH,
                    position=Vector3D(0, 0, 0),
                    velocity=Vector3D(0, 0, 0),
                    size=2.0,
                    color=(200, 200, 255),
                    lifetime_ms=300
                ).to_dict())
            
            animation.frames.append(AnimationFrame(
                time_ms=i * frame_duration,
                atom_positions=frame_positions,
                bond_states=bond_states,
                particle_effects=effects
            ))
        
        return animation
    
    def _animate_generic(
        self,
        reaction: ChemicalReaction,
        animation: ReactionAnimation,
        duration: int
    ) -> ReactionAnimation:
        """Animate a generic reaction."""
        # Collect all atom positions
        all_positions: Dict[str, Vector3D] = {}
        for mol in reaction.reactants + reaction.products:
            for atom in mol.atoms:
                if atom.id not in all_positions:
                    all_positions[atom.id] = atom.position
        
        # Generate frames with simple interpolation
        num_frames = 20
        frame_duration = duration / num_frames
        
        for i in range(num_frames + 1):
            progress = i / num_frames
            
            frame = AnimationFrame(
                time_ms=i * frame_duration,
                atom_positions=all_positions.copy(),
                bond_states={},
                particle_effects=[]
            )
            animation.frames.append(frame)
        
        return animation
    
    def _create_formation_effects(
        self,
        positions: Dict[str, Vector3D]
    ) -> List[Dict[str, Any]]:
        """Create visual effects for bond formation."""
        effects = []
        for atom_id, pos in list(positions.items())[:5]:
            effects.append(ParticleEffect(
                effect_type=ParticleEffectType.SPARK,
                position=pos,
                velocity=Vector3D(
                    (random() - 0.5) * 2,
                    (random() - 0.5) * 2,
                    (random() - 0.5) * 2
                ),
                size=0.3,
                color=(255, 255, 100),
                lifetime_ms=300
            ).to_dict())
        return effects
    
    def _create_breaking_effects(
        self,
        positions: Dict[str, Vector3D]
    ) -> List[Dict[str, Any]]:
        """Create visual effects for bond breaking."""
        effects = []
        for atom_id, pos in list(positions.items())[:3]:
            effects.append(ParticleEffect(
                effect_type=ParticleEffectType.SMOKE,
                position=pos,
                velocity=Vector3D(
                    (random() - 0.5) * 1,
                    random() * 2,
                    (random() - 0.5) * 1
                ),
                size=0.5,
                color=(150, 150, 150),
                lifetime_ms=500
            ).to_dict())
        return effects


class MolecularDynamics:
    """Simulates molecular motion and vibrations."""
    
    def __init__(self, temperature: float = 298.15):
        """Initialize with temperature in Kelvin."""
        self.temperature = temperature
        self.boltzmann_constant = 1.380649e-23
    
    def get_thermal_vibration(
        self,
        atom: Atom,
        time_ms: float
    ) -> Vector3D:
        """Get thermal vibration offset for an atom."""
        # Calculate vibration amplitude based on temperature
        amplitude = math.sqrt(self.temperature * self.boltzmann_constant / 1000)
        
        # Create vibration based on atom type
        phase1 = 2 * math.pi * random() * time_ms / 1000
        phase2 = 2 * math.pi * random() * time_ms / 1000
        phase3 = 2 * math.pi * random() * time_ms / 1000
        
        return Vector3D(
            amplitude * math.sin(phase1),
            amplitude * math.sin(phase2),
            amplitude * math.sin(phase3)
        )
    
    def simulate_brownian_motion(
        self,
        position: Vector3D,
        time_ms: float,
        diffusion_coefficient: float = 1e-9
    ) -> Vector3D:
        """Simulate Brownian motion for a particle."""
        import random
        step_size = math.sqrt(6 * diffusion_coefficient * time_ms / 1000)
        
        return Vector3D(
            position.x + (random() - 0.5) * step_size,
            position.y + (random() - 0.5) * step_size,
            position.z + (random() - 0.5) * step_size
        )


class ChemVerseAnimationService:
    """
    Service for chemistry animations and molecular motion.
    
    This service provides comprehensive animation capabilities for chemical
    reactions, molecular dynamics, and educational visualizations.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the animation service."""
        self.config = config or {}
        self.animator = ReactionAnimator()
        self.dynamics = MolecularDynamics()
        self._active_animations: Dict[str, ReactionAnimation] = {}
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the service with custom settings."""
        self.config.update(config)
        if "default_duration" in config:
            self._default_duration = config["default_duration"]
    
    def animate_reaction(
        self,
        reaction: ChemicalReaction,
        duration_ms: int = None
    ) -> ReactionAnimation:
        """Create an animation for a chemical reaction."""
        duration = duration_ms or self.config.get("default_duration", 2000)
        animation = self.animator.animate_reaction(reaction, duration)
        self._active_animations[reaction.id] = animation
        return animation
    
    def get_frame(
        self,
        animation: ReactionAnimation,
        time_ms: float
    ) -> Optional[AnimationFrame]:
        """Get a specific frame from an animation."""
        return animation.get_frame_at_time(time_ms)
    
    def get_frame_data(
        self,
        animation: ReactionAnimation,
        time_ms: float
    ) -> Dict[str, Any]:
        """Get frame data for rendering at a specific time."""
        frame = animation.get_frame_at_time(time_ms)
        if frame:
            return frame.to_dict()
        return {"error": "Frame not found"}
    
    def simulate_molecular_motion(
        self,
        molecule: Molecule,
        duration_ms: int,
        temperature: float = 298.15
    ) -> List[AnimationFrame]:
        """Simulate thermal motion of a molecule."""
        self.dynamics.temperature = temperature
        frames = []
        
        num_frames = min(int(duration_ms / 50), 100)  # Max 100 frames
        for i in range(num_frames):
            time_ms = i * 50
            frame_positions: Dict[str, Vector3D] = {}
            
            for atom in molecule.atoms:
                vibration = self.dynamics.get_thermal_vibration(atom, time_ms)
                frame_positions[atom.id] = atom.position + vibration
            
            frames.append(AnimationFrame(
                time_ms=time_ms,
                atom_positions=frame_positions,
                bond_states={},
                particle_effects=[]
            ))
        
        return frames
    
    def create_particle_effect(
        self,
        effect_type: str,
        position: Vector3D,
        duration_ms: float
    ) -> ParticleEffect:
        """Create a particle effect for visualization."""
        return ParticleEffect(
            effect_type=ParticleEffectType(effect_type),
            position=position,
            velocity=Vector3D(0, 1, 0),
            size=0.5,
            color=(255, 255, 255),
            lifetime_ms=duration_ms
        )
    
    def get_energy_profile(
        self,
        reaction: ChemicalReaction
    ) -> Dict[str, Any]:
        """Get energy profile data for a reaction animation."""
        return {
            "reaction_id": reaction.id,
            "reactant_energy": reaction.reactant_energy if hasattr(reaction, 'reactant_energy') else 0,
            "product_energy": reaction.product_energy if hasattr(reaction, 'product_energy') else 0,
            "activation_energy": reaction.activation_energy,
            "delta_h": reaction.delta_h,
            "is_exothermic": reaction.delta_h < 0,
            "transition_state_energy": reaction.reactant_energy + reaction.activation_energy if hasattr(reaction, 'reactant_energy') else None
        }
    
    def export_animation(
        self,
        animation: ReactionAnimation,
        format: str = "json"
    ) -> str:
        """Export animation data in the specified format."""
        frames_data = [frame.to_dict() for frame in animation.frames]
        
        if format == "json":
            return json.dumps({
                "reaction_id": animation.reaction.id,
                "duration_ms": animation.duration_ms,
                "frames": frames_data
            }, indent=2)
        elif format == "dict":
            return {
                "reaction_id": animation.reaction.id,
                "duration_ms": animation.duration_ms,
                "frames": frames_data
            }
        else:
            return str(animation)
    
    def get_animation_status(self, animation: ReactionAnimation) -> Dict[str, Any]:
        """Get the current status of an animation."""
        return {
            "animation_id": animation.reaction.id,
            "state": animation.state.value,
            "progress": animation.get_progress(),
            "duration_ms": animation.duration_ms,
            "frame_count": len(animation.frames)
        }


def create_chem_animation_service(config: dict = None) -> ChemVerseAnimationService:
    """
    Create a ChemVerseAnimationService instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured ChemVerseAnimationService instance
    """
    service = ChemVerseAnimationService(config)
    return service


__all__ = [
    "AnimationState",
    "AnimationEasing",
    "ParticleEffectType",
    "AnimationKeyframe",
    "AnimationFrame",
    "TransitionState",
    "ReactionAnimation",
    "MolecularMotion",
    "ParticleEffect",
    "EasingFunction",
    "ReactionAnimator",
    "MolecularDynamics",
    "ChemVerseAnimationService",
    "create_chem_animation_service"
]
