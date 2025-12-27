"""
PhysicsVerse Visual Service

This module provides the PhysicsVerse-specific visual service implementation,
extending the base visual service with physics domain functionality for
rendering simulations, diagrams, graphs, and interactive visualizations
of mechanics, optics, and electromagnetism phenomena.

Key Features:
- Vector field visualization (electric, magnetic, gravitational)
- Motion trajectory plotting with velocity/acceleration vectors
- Optical ray tracing for lenses, mirrors, and prisms
- Circuit diagram rendering
- Graph plotting (position-time, velocity-time, energy graphs)
- 3D to 2D projection for spatial physics

Licensed under the Apache License, Version 2.0
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from math import sqrt, sin, cos, tan, atan2, pi, radians, degrees
import logging

from ....extensions.service_extension_base import (
    VisualServiceExtension,
    ExtensionContext
)
from .physics_core import (
    Vector2D,
    Vector3D,
    Complex,
    PhysicsState
)

logger = logging.getLogger(__name__)


class PhysicsVisualType(Enum):
    """Types of physics visualizations."""
    TRAJECTORY = "trajectory"
    VECTOR_FIELD = "vector_field"
    RAY_DIAGRAM = "ray_diagram"
    CIRCUIT_DIAGRAM = "circuit_diagram"
    ENERGY_GRAPH = "energy_graph"
    PHASE_SPACE = "phase_space"
    FIELD_LINES = "field_lines"
    WAVE_PATTERN = "wave_pattern"
    SPECTRUM = "spectrum"
    OPTICAL_BENCH = "optical_bench"


class VectorDisplayType(Enum):
    """Types of vector displays."""
    ARROW = "arrow"
    COMPONENTS = "components"
    MAGNITUDE_ONLY = "magnitude_only"
    DYNAMIC = "dynamic"


class ColorScheme(Enum):
    """Color schemes for physics visualizations."""
    BLUEPRINT = "blueprint"
    LAB = "lab"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    RAINBOW = "rainbow"


@dataclass
class VectorStyle:
    """Style configuration for vector display."""
    color: str = "#3b82f6"
    line_width: float = 2.0
    arrowhead_size: float = 10.0
    show_components: bool = False
    component_colors: Tuple[str, str] = ("#ef4444", "#22c55e")
    label_format: str = "default"
    scale_factor: float = 1.0


@dataclass
class GraphConfig:
    """Configuration for graph plotting."""
    x_label: str = "x"
    y_label: str = "y"
    title: str = ""
    x_range: Tuple[float, float] = (-10, 10)
    y_range: Tuple[float, float] = (-10, 10)
    show_grid: bool = True
    grid_color: str = "#e5e7eb"
    axis_color: str = "#374151"
    data_colors: List[str] = field(default_factory=lambda: ["#3b82f6", "#ef4444", "#22c55e"])
    line_width: float = 2.0
    show_points: bool = False
    point_radius: float = 4.0
    legend_position: str = "upper_right"


@dataclass
class FieldVisualConfig:
    """Configuration for field visualizations."""
    field_type: str = "electric"
    density: int = 20
    arrow_length: float = 15.0
    color_gradient: bool = True
    magnitude_colormap: str = "viridis"
    show_equipotential: bool = False
    equipotential_spacing: float = 1.0
    3d_projection: Optional[str] = None


@dataclass
class CircuitVisualConfig:
    """Configuration for circuit diagram visualization."""
    component_spacing: int = 80
    wire_style: str = "straight"
    show_values: bool = True
    value_position: str = "below"
    battery_symbol: str = "long"
    inductor_symbol: str = "coil"
    show_current: bool = False
    current_animation: bool = True


@dataclass
class OpticalConfig:
    """Configuration for optical system visualization."""
    lens_type: str = "convex"
    mirror_type: str = "concave"
    show_principal_rays: bool = True
    show_focal_points: bool = True
    show_image_rays: bool = True
    ray_color: str = "#fbbf24"
    image_style: str = "solid"
    scale_factor: float = 1.0


@dataclass
class PhysicsVisualization:
    """
    Represents a complete physics visualization.
    
    Attributes:
        visualization_id: Unique identifier
        visual_type: Type of visualization
        width: Canvas width in pixels
        height: Canvas height in pixels
        elements: List of visual elements
        annotations: List of text annotations
        config: Visualization configuration
        metadata: Additional metadata
    """
    visualization_id: str
    visual_type: PhysicsVisualType
    width: int
    height: int
    elements: List[Dict[str, Any]] = field(default_factory=list)
    annotations: List[Dict[str, Any]] = field(default_factory=list)
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PhysicsVerseVisualService:
    """
    PhysicsVerse-specific visual service.
    
    This service handles physics visualization including:
    - Vector field rendering (electric, magnetic, gravitational)
    - Motion trajectory plotting with vectors
    - Optical ray tracing and lens diagrams
    - Circuit diagram rendering
    - Real-time graph plotting
    - Interactive physics simulations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the PhysicsVerse visual service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._color_schemes = self._initialize_color_schemes()
        self._symbol_library = self._initialize_symbol_library()
        self._default_style = VectorStyle()
    
    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        logger.info("PhysicsVerseVisualService configured with settings: %s", list(config.keys()))
    
    def _initialize_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Initialize available color schemes."""
        return {
            "blueprint": {
                "background": "#1e3a5f",
                "grid": "#2d5a87",
                "primary": "#60a5fa",
                "secondary": "#93c5fd",
                "accent": "#fcd34d",
                "text": "#ffffff",
                "positive": "#22c55e",
                "negative": "#ef4444"
            },
            "lab": {
                "background": "#ffffff",
                "grid": "#e5e7eb",
                "primary": "#3b82f6",
                "secondary": "#6366f1",
                "accent": "#8b5cf6",
                "text": "#1f2937",
                "positive": "#16a34a",
                "negative": "#dc2626"
            },
            "dark": {
                "background": "#111827",
                "grid": "#374151",
                "primary": "#60a5fa",
                "secondary": "#a78bfa",
                "accent": "#fbbf24",
                "text": "#f9fafb",
                "positive": "#34d399",
                "negative": "#f87171"
            },
            "high_contrast": {
                "background": "#000000",
                "grid": "#333333",
                "primary": "#ffffff",
                "secondary": "#ffff00",
                "accent": "#00ffff",
                "text": "#ffffff",
                "positive": "#00ff00",
                "negative": "#ff0000"
            }
        }
    
    def _initialize_symbol_library(self) -> Dict[str, str]:
        """Initialize symbol library for physics notation."""
        return {
            "force": "F",
            "velocity": "v",
            "acceleration": "a",
            "position": "r",
            "momentum": "p",
            "energy": "E",
            "mass": "m",
            "charge": "q",
            "field": "B",
            "potential": "V",
            "current": "I",
            "resistance": "R",
            "capacitance": "C",
            "inductance": "L",
            "frequency": "f",
            "wavelength": "λ",
            "period": "T",
            "omega": "ω",
            "theta": "θ",
            "phi": "φ",
            "alpha": "α",
            "beta": "β",
            "gamma": "γ",
            "delta": "Δ",
            "sum": "Σ",
            "integral": "∫",
            "nabla": "∇",
            "partial": "∂",
            "infinity": "∞"
        }
    
    # ==================== TRAJECTORY VISUALIZATION ====================
    
    def create_trajectory_visualization(
        self,
        trajectories: List[Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> PhysicsVisualization:
        """
        Create a trajectory visualization for motion.
        
        Args:
            trajectories: List of trajectory dictionaries with position data
            config: Optional configuration
            
        Returns:
            PhysicsVisualization object
        """
        viz_config = config or {}
        width = viz_config.get("width", 800)
        height = viz_config.get("height", 600)
        
        elements = []
        
        # Convert world coordinates to screen coordinates
        scale = self._calculate_scale(trajectories, width, height)
        
        for i, trajectory in enumerate(trajectories):
            positions = trajectory.get("positions", [])
            color = trajectory.get("color", self._color_schemes["lab"]["primary"])
            
            # Create path elements
            path_points = []
            for pos in positions:
                screen_pos = self._world_to_screen(pos, scale, width, height)
                path_points.append([screen_pos.x, screen_pos.y])
            
            if len(path_points) > 1:
                elements.append({
                    "type": "path",
                    "points": path_points,
                    "stroke": color,
                    "stroke_width": 2,
                    "fill": "none"
                })
            
            # Add velocity vectors at key points
            if trajectory.get("show_vectors", True):
                velocity_vectors = trajectory.get("velocities", [])
                for j, vel in enumerate(velocity_vectors):
                    if j % viz_config.get("vector_interval", 5) == 0:
                        pos = positions[j]
                        screen_pos = self._world_to_screen(pos, scale, width, height)
                        vector_element = self._create_vector_element(
                            screen_pos, vel, scale, VectorStyle(color=color)
                        )
                        elements.append(vector_element)
            
            # Add start and end markers
            if positions:
                start_screen = self._world_to_screen(positions[0], scale, width, height)
                end_screen = self._world_to_screen(positions[-1], scale, width, height)
                
                elements.append({
                    "type": "circle",
                    "cx": start_screen.x,
                    "cy": start_screen.y,
                    "r": 5,
                    "fill": color,
                    "stroke": "none"
                })
                elements.append({
                    "type": "circle",
                    "cx": end_screen.x,
                    "cy": end_screen.y,
                    "r": 6,
                    "fill": "none",
                    "stroke": color,
                    "stroke_width": 2
                })
        
        # Add grid if configured
        if viz_config.get("show_grid", True):
            grid_elements = self._create_grid_elements(scale, width, height)
            elements.extend(grid_elements)
        
        # Add axes
        elements.extend(self._create_axes_elements(scale, width, height))
        
        return PhysicsVisualization(
            visualization_id=f"trajectory_{datetime.now().timestamp()}",
            visual_type=PhysicsVisualType.TRAJECTORY,
            width=width,
            height=height,
            elements=elements,
            config=viz_config,
            metadata={"type": "trajectory", "num_trajectories": len(trajectories)}
        )
    
    def create_vector_field_visualization(
        self,
        field_function: Callable[[Vector2D], Vector2D],
        bounds: Tuple[float, float, float, float],
        config: Optional[Dict[str, Any]] = None
    ) -> PhysicsVisualization:
        """
        Create a vector field visualization.
        
        Args:
            field_function: Function that returns field vector at a position
            bounds: (x_min, x_max, y_min, y_max) in world coordinates
            config: Optional configuration
            
        Returns:
            PhysicsVisualization object
        """
        viz_config = config or {}
        width = viz_config.get("width", 800)
        height = viz_config.get("height", 600)
        density = viz_config.get("density", 20)
        
        elements = []
        
        x_min, x_max, y_min, y_max = bounds
        x_step = (x_max - x_min) / density
        y_step = (y_max - y_min) / density
        
        # Calculate scale
        world_width = x_max - x_min
        world_height = y_max - y_min
        scale_x = width / world_width
        scale_y = height / world_height
        scale = min(scale_x, scale_y)
        
        # Generate vector field
        for i in range(density + 1):
            for j in range(density + 1):
                x = x_min + i * x_step
                y = y_min + j * y_step
                position = Vector2D(x, y)
                
                field_vector = field_function(position)
                magnitude = field_vector.magnitude()
                
                if magnitude > 0.001:  # Skip near-zero vectors
                    screen_pos = Vector2D(
                        (x - x_min) * scale_x,
                        height - (y - y_min) * scale_y
                    )
                    
                    # Normalize and scale for display
                    display_length = min(viz_config.get("arrow_length", 20), 40)
                    display_vector = field_vector.normalize() * display_length
                    
                    # Color based on magnitude
                    max_mag = viz_config.get("max_magnitude", 10)
                    normalized_mag = min(magnitude / max_mag, 1.0)
                    color = self._get_colormap_color(normalized_mag, viz_config.get("colormap", "viridis"))
                    
                    elements.append(self._create_vector_element(
                        screen_pos, display_vector, Vector2D(1, 1),
                        VectorStyle(color=color, arrowhead_size=8)
                    ))
        
        return PhysicsVisualization(
            visualization_id=f"vector_field_{datetime.now().timestamp()}",
            visual_type=PhysicsVisualType.VECTOR_FIELD,
            width=width,
            height=height,
            elements=elements,
            config=viz_config,
            metadata={"type": "vector_field", "bounds": bounds, "density": density}
        )
    
    # ==================== OPTICAL VISUALIZATION ====================
    
    def create_ray_diagram(
        self,
        optical_elements: List[Dict[str, Any]],
        rays: List[Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> PhysicsVisualization:
        """
        Create an optical ray diagram visualization.
        
        Args:
            optical_elements: List of optical elements (lenses, mirrors, etc.)
            rays: List of light rays
            config: Optional configuration
            
        Returns:
            PhysicsVisualization object
        """
        viz_config = config or {}
        width = viz_config.get("width", 800)
        height = viz_config.get("height", 600)
        
        elements = []
        annotations = []
        
        # Center of optical axis
        center_y = height // 2
        optical_axis_y = center_y
        
        # Draw optical axis
        elements.append({
            "type": "line",
            "x1": 0,
            "y1": optical_axis_y,
            "x2": width,
            "y2": optical_axis_y,
            "stroke": "#9ca3af",
            "stroke_width": 1,
            "stroke_dasharray": "5,5"
        })
        
        # Draw optical elements
        for elem in optical_elements:
            elem_type = elem.get("type", "lens")
            position = elem.get("position", Vector2D(width // 2, center_y))
            screen_x = position.x
            screen_y = position.y
            
            if elem_type == "lens":
                # Draw lens symbol
                lens_type = elem.get("lens_type", "convex")
                focal_length = elem.get("focal_length", 100)
                
                if lens_type == "convex":
                    # Biconvex lens
                    elements.append({
                        "type": "path",
                        "d": f"M {screen_x} {screen_y - 60} "
                             f"Q {screen_x + 20} {screen_y} {screen_x} {screen_y + 60} "
                             f"Q {screen_x - 20} {screen_y} {screen_x} {screen_y - 60}",
                        "fill": "none",
                        "stroke": "#3b82f6",
                        "stroke_width": 3
                    })
                else:
                    # Concave lens
                    elements.append({
                        "type": "path",
                        "d": f"M {screen_x} {screen_y - 60} "
                             f"Q {screen_x - 15} {screen_y} {screen_x} {screen_y + 60} "
                             f"Q {screen_x + 15} {screen_y} {screen_x} {screen_y - 60}",
                        "fill": "none",
                        "stroke": "#3b82f6",
                        "stroke_width": 3
                    })
                
                # Draw focal points
                if viz_config.get("show_focal_points", True):
                    for sign in [-1, 1]:
                        focal_x = screen_x + sign * focal_length
                        elements.append({
                            "type": "circle",
                            "cx": focal_x,
                            "cy": screen_y,
                            "r": 4,
                            "fill": "#ef4444",
                            "stroke": "none"
                        })
                        annotations.append({
                            "text": "F",
                            "x": focal_x,
                            "y": screen_y - 15,
                            "font_size": 12,
                            "fill": "#ef4444"
                        })
                
                # Label
                annotations.append({
                    "text": f"f = {focal_length}px",
                    "x": screen_x + 10,
                    "y": screen_y - 70,
                    "font_size": 11,
                    "fill": "#6b7280"
                })
            
            elif elem_type == "mirror":
                # Draw mirror symbol
                mirror_type = elem.get("mirror_type", "concave")
                radius = elem.get("radius", 100)
                
                if mirror_type == "concave":
                    elements.append({
                        "type": "path",
                        "d": f"M {screen_x} {screen_y - 80} "
                             f"A {radius} {radius} 0 0 0 {screen_x} {screen_y + 80}",
                        "fill": "none",
                        "stroke": "#3b82f6",
                        "stroke_width": 3
                    })
                else:
                    elements.append({
                        "type": "path",
                        "d": f"M {screen_x} {screen_y - 80} "
                             f"A {radius} {radius} 0 0 1 {screen_x} {screen_y + 80}",
                        "fill": "none",
                        "stroke": "#3b82f6",
                        "stroke_width": 3
                    })
            
            elif elem_type == "prism":
                # Draw triangular prism
                height_prism = elem.get("height", 80)
                elements.append({
                    "type": "path",
                    "d": f"M {screen_x} {screen_y - height_prism} "
                         f"L {screen_x + height_prism * 0.866} {screen_y + height_prism * 0.5} "
                         f"L {screen_x - height_prism * 0.866} {screen_y + height_prism * 0.5} Z",
                    "fill": "rgba(147, 197, 253, 0.3)",
                    "stroke": "#3b82f6",
                    "stroke_width": 2
                })
        
        # Draw rays
        for ray in rays:
            origin = ray.get("origin", Vector2D(0, center_y))
            direction = ray.get("direction", Vector2D(1, 0))
            color = ray.get("color", viz_config.get("ray_color", "#fbbf24"))
            
            # Convert to screen coordinates
            start_x = origin.x
            start_y = height - origin.y if hasattr(origin, 'y') else center_y
            end_x = start_x + direction.x * 200
            end_y = start_y - direction.y * 200
            
            elements.append({
                "type": "line",
                "x1": start_x,
                "y1": start_y,
                "x2": end_x,
                "y2": end_y,
                "stroke": color,
                "stroke_width": 2
            })
            
            # Arrowhead
            self._add_arrowhead(elements, start_x, start_y, end_x, end_y, color)
        
        return PhysicsVisualization(
            visualization_id=f"ray_diagram_{datetime.now().timestamp()}",
            visual_type=PhysicsVisualType.RAY_DIAGRAM,
            width=width,
            height=height,
            elements=elements,
            annotations=annotations,
            config=viz_config,
            metadata={"type": "optical", "num_elements": len(optical_elements), "num_rays": len(rays)}
        )
    
    # ==================== CIRCUIT VISUALIZATION ====================
    
    def create_circuit_diagram(
        self,
        components: List[Dict[str, Any]],
        connections: List[Tuple[str, str]],
        config: Optional[Dict[str, Any]] = None
    ) -> PhysicsVisualization:
        """
        Create a circuit diagram visualization.
        
        Args:
            components: List of circuit components
            connections: List of (component_id, node_id) connections
            config: Optional configuration
            
        Returns:
            PhysicsVisualization object
        """
        viz_config = config or {}
        width = viz_config.get("width", 800)
        height = viz_config.get("height", 600)
        
        elements = []
        annotations = []
        
        spacing = viz_config.get("component_spacing", 80)
        
        # Position components in a simple layout
        component_positions = {}
        for i, comp in enumerate(components):
            comp_id = comp.get("id", f"c{i}")
            comp_type = comp.get("type", "resistor")
            
            x = 100 + (i % 4) * spacing
            y = 100 + (i // 4) * spacing
            component_positions[comp_id] = Vector2D(x, y)
            
            # Draw component symbol
            symbol_elements = self._create_component_symbol(
                comp_type, Vector2D(x, y), comp, viz_config
            )
            elements.extend(symbol_elements)
            
            # Add value annotation
            if viz_config.get("show_values", True):
                value = comp.get("value", "")
                unit = comp.get("unit", "")
                if value:
                    annotations.append({
                        "text": f"{value} {unit}",
                        "x": x,
                        "y": y + 25,
                        "font_size": 11,
                        "fill": "#374151",
                        "anchor": "middle"
                    })
        
        # Draw connections (wires)
        for conn in connections:
            if len(conn) >= 2:
                comp_a, comp_b = conn[0], conn[1]
                if comp_a in component_positions and comp_b in component_positions:
                    pos_a = component_positions[comp_a]
                    pos_b = component_positions[comp_b]
                    
                    elements.append({
                        "type": "line",
                        "x1": pos_a.x,
                        "y1": pos_a.y,
                        "x2": pos_b.x,
                        "y2": pos_b.y,
                        "stroke": "#374151",
                        "stroke_width": 2
                    })
        
        # Add ground symbols if present
        for comp in components:
            if comp.get("ground", False):
                pos = component_positions.get(comp.get("id"))
                if pos:
                    ground_elements = self._create_ground_symbol(pos)
                    elements.extend(ground_elements)
        
        return PhysicsVisualization(
            visualization_id=f"circuit_{datetime.now().timestamp()}",
            visual_type=PhysicsVisualType.CIRCUIT_DIAGRAM,
            width=width,
            height=height,
            elements=elements,
            annotations=annotations,
            config=viz_config,
            metadata={"type": "circuit", "num_components": len(components)}
        )
    
    def _create_component_symbol(
        self,
        comp_type: str,
        position: Vector2D,
        component: Dict[str, Any],
        config: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Create SVG elements for a circuit component symbol."""
        elements = []
        x, y = position.x, position.y
        
        if comp_type == "resistor":
            elements.append({
                "type": "path",
                "d": f"M {x - 15} {y} L {x - 10} {y - 8} L {x - 5} {y + 8} L {x} {y - 8} L {x + 5} {y + 8} L {x + 10} {y - 8} L {x + 15} {y}",
                "fill": "none",
                "stroke": "#374151",
                "stroke_width": 2
            })
        
        elif comp_type == "capacitor":
            elements.append({
                "type": "line",
                "x1": x - 10,
                "y1": y - 15,
                "x2": x - 10,
                "y2": y + 15,
                "stroke": "#374151",
                "stroke_width": 2
            })
            elements.append({
                "type": "line",
                "x1": x + 10,
                "y1": y - 15,
                "x2": x + 10,
                "y2": y + 15,
                "stroke": "#374151",
                "stroke_width": 2
            })
        
        elif comp_type == "inductor":
            inductor_symbol = config.get("inductor_symbol", "coil")
            if inductor_symbol == "coil":
                elements.append({
                    "type": "path",
                    "d": f"M {x - 15} {y} Q {x - 10} {y - 10} {x - 5} {y} "
                         f"Q {x} {y + 10} {x + 5} {y} Q {x + 10} {y - 10} {x + 15} {y}",
                    "fill": "none",
                    "stroke": "#374151",
                    "stroke_width": 2
                })
        
        elif comp_type == "battery":
            battery_symbol = config.get("battery_symbol", "long")
            if battery_symbol == "long":
                elements.append({
                    "type": "line",
                    "x1": x - 15,
                    "y1": y - 8,
                    "x2": x + 15,
                    "y2": y - 8,
                    "stroke": "#374151",
                    "stroke_width": 2
                })
                elements.append({
                    "type": "line",
                    "x1": x - 5,
                    "y1": y + 8,
                    "x2": x + 5,
                    "y2": y + 8,
                    "stroke": "#374151",
                    "stroke_width": 4
                })
            else:
                elements.append({
                    "type": "line",
                    "x1": x - 10,
                    "y1": y - 5,
                    "x2": x + 10,
                    "y2": y - 5,
                    "stroke": "#374151",
                    "stroke_width": 2
                })
                elements.append({
                    "type": "line",
                    "x1": x - 5,
                    "y1": y + 5,
                    "x2": x + 5,
                    "y2": y + 5,
                    "stroke": "#374151",
                    "stroke_width": 4
                })
        
        elif comp_type == "switch":
            elements.append({
                "type": "line",
                "x1": x - 15,
                "y1": y - 10,
                "x2": x,
                "y2": y - 10,
                "stroke": "#374151",
                "stroke_width": 2
            })
            is_closed = component.get("closed", False)
            if is_closed:
                elements.append({
                    "type": "line",
                    "x1": x,
                    "y1": y - 10,
                    "x2": x + 15,
                    "y2": y,
                    "stroke": "#374151",
                    "stroke_width": 2
                })
            else:
                elements.append({
                    "type": "line",
                    "x1": x,
                    "y1": y - 10,
                    "x2": x + 15,
                    "y2": y - 10,
                    "stroke": "#374151",
                    "stroke_width": 2
                })
        
        elif comp_type == "voltage_source":
            elements.append({
                "type": "circle",
                "cx": x,
                "cy": y,
                "r": 15,
                "fill": "none",
                "stroke": "#374151",
                "stroke_width": 2
            })
            annotations.append({
                "text": "V",
                "x": x,
                "y": y + 4,
                "font_size": 12,
                "fill": "#374151",
                "anchor": "middle"
            })
        
        # Terminals
        elements.append({
            "type": "circle",
            "cx": x - 15,
            "cy": y,
            "r": 3,
            "fill": "#374151",
            "stroke": "none"
        })
        elements.append({
            "type": "circle",
            "cx": x + 15,
            "cy": y,
            "r": 3,
            "fill": "#374151",
            "stroke": "none"
        })
        
        return elements
    
    def _create_ground_symbol(self, position: Vector2D) -> List[Dict[str, Any]]:
        """Create SVG elements for ground symbol."""
        x, y = position.x, position.y
        return [
            {
                "type": "line",
                "x1": x - 15,
                "y1": y,
                "x2": x + 15,
                "y2": y,
                "stroke": "#374151",
                "stroke_width": 2
            },
            {
                "type": "line",
                "x1": x - 10,
                "y1": y + 8,
                "x2": x + 10,
                "y2": y + 8,
                "stroke": "#374151",
                "stroke_width": 2
            },
            {
                "type": "line",
                "x1": x - 5,
                "y1": y + 16,
                "x2": x + 5,
                "y2": y + 16,
                "stroke": "#374151",
                "stroke_width": 2
            }
        ]
    
    # ==================== GRAPH PLOTTING ====================
    
    def create_energy_graph(
        self,
        data: Dict[str, List[Tuple[float, float]]],
        config: Optional[GraphConfig] = None
    ) -> PhysicsVisualization:
        """
        Create an energy vs. time graph.
        
        Args:
            data: Dictionary mapping energy types to (time, value) tuples
            config: Graph configuration
            
        Returns:
            PhysicsVisualization object
        """
        graph_config = config or GraphConfig()
        width = 800
        height = 600
        
        elements = []
        annotations = []
        
        # Calculate data ranges
        all_times = []
        all_values = []
        for series in data.values():
            for t, v in series:
                all_times.append(t)
                all_values.append(v)
        
        if not all_times:
            return PhysicsVisualization(
                visualization_id=f"energy_graph_{datetime.now().timestamp()}",
                visual_type=PhysicsVisualType.ENERGY_GRAPH,
                width=width,
                height=height
            )
        
        t_min, t_max = min(all_times), max(all_times)
        v_min, v_max = min(all_values), max(all_values)
        
        # Add padding
        t_range = t_max - t_min or 1
        v_range = v_max - v_min or 1
        t_min -= t_range * 0.1
        t_max += t_range * 0.1
        v_min -= v_range * 0.1
        v_max += v_range * 0.1
        
        # Scale functions
        scale_x = (width - 100) / (t_max - t_min)
        scale_y = (height - 100) / (v_max - v_min)
        
        # Draw axes
        origin_x = 60
        origin_y = height - 50
        
        # Y-axis
        elements.append({
            "type": "line",
            "x1": origin_x,
            "y1": 50,
            "x2": origin_x,
            "y2": origin_y,
            "stroke": graph_config.axis_color,
            "stroke_width": 2
        })
        
        # X-axis
        elements.append({
            "type": "line",
            "x1": origin_x,
            "y1": origin_y,
            "x2": width - 40,
            "y2": origin_y,
            "stroke": graph_config.axis_color,
            "stroke_width": 2
        })
        
        # Axis labels
        annotations.append({
            "text": graph_config.x_label,
            "x": width - 30,
            "y": origin_y + 15,
            "font_size": 12,
            "fill": graph_config.axis_color
        })
        annotations.append({
            "text": graph_config.y_label,
            "x": origin_x - 10,
            "y": 40,
            "font_size": 12,
            "fill": graph_config.axis_color,
            "anchor": "end"
        })
        
        # Grid
        if graph_config.show_grid:
            for t in [t_min, t_max]:
                x = origin_x + (t - t_min) * scale_x
                elements.append({
                    "type": "line",
                    "x1": x,
                    "y1": 50,
                    "x2": x,
                    "y2": origin_y,
                    "stroke": graph_config.grid_color,
                    "stroke_width": 1
                })
            for v in [v_min, v_max]:
                y = origin_y - (v - v_min) * scale_y
                elements.append({
                    "type": "line",
                    "x1": origin_x,
                    "y1": y,
                    "x2": width - 40,
                    "y2": y,
                    "stroke": graph_config.grid_color,
                    "stroke_width": 1
                })
        
        # Plot data series
        colors = graph_config.data_colors
        for i, (energy_type, series) in enumerate(data.items()):
            if len(series) < 2:
                continue
            
            color = colors[i % len(colors)]
            path_points = []
            
            for t, v in series:
                x = origin_x + (t - t_min) * scale_x
                y = origin_y - (v - v_min) * scale_y
                path_points.append([x, y])
            
            elements.append({
                "type": "path",
                "d": "M " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in path_points),
                "fill": "none",
                "stroke": color,
                "stroke_width": graph_config.line_width
            })
            
            # Legend entry
            legend_y = 70 + i * 25
            elements.append({
                "type": "line",
                "x1": origin_x + 10,
                "y1": legend_y,
                "x2": origin_x + 40,
                "y2": legend_y,
                "stroke": color,
                "stroke_width": 3
            })
            annotations.append({
                "text": energy_type,
                "x": origin_x + 50,
                "y": legend_y + 4,
                "font_size": 11,
                "fill": "#374151"
            })
        
        return PhysicsVisualization(
            visualization_id=f"energy_graph_{datetime.now().timestamp()}",
            visual_type=PhysicsVisualType.ENERGY_GRAPH,
            width=width,
            height=height,
            elements=elements,
            annotations=annotations,
            config={"title": graph_config.title},
            metadata={"type": "graph", "data_series": list(data.keys())}
        )
    
    # ==================== HELPER METHODS ====================
    
    def _calculate_scale(
        self,
        trajectories: List[Dict[str, Any]],
        width: int,
        height: int
    ) -> Vector2D:
        """Calculate coordinate scale from world to screen."""
        all_positions = []
        for traj in trajectories:
            all_positions.extend(traj.get("positions", []))
        
        if not all_positions:
            return Vector2D(1, 1)
        
        min_x = min(p.x if hasattr(p, 'x') else p[0] for p in all_positions)
        max_x = max(p.x if hasattr(p, 'x') else p[0] for p in all_positions)
        min_y = min(p.y if hasattr(p, 'y') else p[1] for p in all_positions)
        max_y = max(p.y if hasattr(p, 'y') else p[1] for p in all_positions)
        
        world_width = max_x - min_x or 1
        world_height = max_y - min_y or 1
        
        scale_x = (width - 100) / world_width
        scale_y = (height - 100) / world_height
        
        return Vector2D(scale_x, scale_y)
    
    def _world_to_screen(
        self,
        position: Vector2D,
        scale: Vector2D,
        width: int,
        height: int
    ) -> Vector2D:
        """Convert world coordinates to screen coordinates."""
        return Vector2D(
            50 + position.x * scale.x,
            height - 50 - position.y * scale.y
        )
    
    def _create_vector_element(
        self,
        position: Vector2D,
        vector: Vector2D,
        scale: Vector2D,
        style: VectorStyle
    ) -> Dict[str, Any]:
        """Create a vector visualization element."""
        magnitude = vector.magnitude()
        if magnitude < 0.001:
            return {"type": "circle", "cx": position.x, "cy": position.y, "r": 3, "fill": style.color}
        
        # Scale the vector
        display_vector = vector * style.scale_factor
        end_pos = position + display_vector
        
        elements = {
            "type": "vector",
            "start_x": position.x,
            "start_y": position.y,
            "end_x": end_pos.x,
            "end_y": end_pos.y,
            "color": style.color,
            "line_width": style.line_width,
            "arrowhead_size": style.arrowhead_size
        }
        
        # Add component vectors if requested
        if style.show_components:
            elements["components"] = {
                "x": {
                    "start_x": position.x,
                    "start_y": position.y,
                    "end_x": end_pos.x,
                    "end_y": position.y,
                    "color": style.component_colors[0]
                },
                "y": {
                    "start_x": end_pos.x,
                    "start_y": position.y,
                    "end_x": end_pos.x,
                    "end_y": end_pos.y,
                    "color": style.component_colors[1]
                }
            }
        
        return elements
    
    def _create_grid_elements(
        self,
        scale: Vector2D,
        width: int,
        height: int
    ) -> List[Dict[str, Any]]:
        """Create grid elements for background."""
        elements = []
        grid_spacing = 50
        
        # Vertical lines
        for x in range(50, width, grid_spacing):
            elements.append({
                "type": "line",
                "x1": x,
                "y1": 50,
                "x2": x,
                "y2": height - 50,
                "stroke": "#e5e7eb",
                "stroke_width": 1
            })
        
        # Horizontal lines
        for y in range(50, height, grid_spacing):
            elements.append({
                "type": "line",
                "x1": 50,
                "y1": y,
                "x2": width - 50,
                "y2": y,
                "stroke": "#e5e7eb",
                "stroke_width": 1
            })
        
        return elements
    
    def _create_axes_elements(
        self,
        scale: Vector2D,
        width: int,
        height: int
    ) -> List[Dict[str, Any]]:
        """Create axes elements."""
        elements = []
        
        # X-axis
        elements.append({
            "type": "line",
            "x1": 50,
            "y1": height - 50,
            "x2": width - 50,
            "y2": height - 50,
            "stroke": "#374151",
            "stroke_width": 2
        })
        
        # Y-axis
        elements.append({
            "type": "line",
            "x1": 50,
            "y1": 50,
            "x2": 50,
            "y2": height - 50,
            "stroke": "#374151",
            "stroke_width": 2
        })
        
        # Origin label
        elements.append({
            "type": "text",
            "x": 40,
            "y": height - 40,
            "text": "O",
            "font_size": 12,
            "fill": "#6b7280"
        })
        
        return elements
    
    def _get_colormap_color(
        self,
        value: float,
        colormap: str
    ) -> str:
        """Get color from colormap based on value (0-1)."""
        if colormap == "viridis":
            colors = [
                (0.267004, 0.004874, 0.329415),
                (0.282327, 0.140926, 0.457517),
                (0.253935, 0.265254, 0.529983),
                (0.206756, 0.371758, 0.553117),
                (0.163625, 0.471133, 0.558148),
                (0.127568, 0.566949, 0.550556),
                (0.134692, 0.658636, 0.517649),
                (0.266941, 0.748751, 0.440573),
                (0.477504, 0.821444, 0.318195),
                (0.741388, 0.873449, 0.149561),
                (0.993248, 0.906157, 0.143936)
            ]
        else:
            colors = [
                (0.5, 0.5, 1.0),
                (0.0, 0.5, 1.0),
                (0.0, 1.0, 0.5),
                (1.0, 1.0, 0.0),
                (1.0, 0.5, 0.0),
                (1.0, 0.0, 0.0)
            ]
        
        idx = int(value * (len(colors) - 1))
        idx = min(idx, len(colors) - 1)
        r, g, b = colors[idx]
        
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    
    def _add_arrowhead(
        self,
        elements: List[Dict[str, Any]],
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str
    ) -> None:
        """Add arrowhead to a line."""
        angle = atan2(y2 - y1, x2 - x1)
        arrow_size = 10
        
        p1x = x2 - arrow_size * cos(angle - pi/6)
        p1y = y2 - arrow_size * sin(angle - pi/6)
        p2x = x2 - arrow_size * cos(angle + pi/6)
        p2y = y2 - arrow_size * sin(angle + pi/6)
        
        elements.append({
            "type": "path",
            "d": f"M {x2} {y2} L {p1x} {p1y} L {p2x} {p2y} Z",
            "fill": color,
            "stroke": "none"
        })
    
    # ==================== UTILITY METHODS ====================
    
    def get_symbol(self, symbol_id: str) -> str:
        """
        Get a physics symbol for display.
        
        Args:
            symbol_id: Symbol identifier
            
        Returns:
            Unicode symbol string
        """
        return self._symbol_library.get(symbol_id, symbol_id)
    
    def create_wave_visualization(
        self,
        amplitude: float,
        wavelength: float,
        frequency: float,
        phase: float = 0.0,
        config: Optional[Dict[str, Any]] = None
    ) -> PhysicsVisualization:
        """
        Create a wave visualization.
        
        Args:
            amplitude: Wave amplitude
            wavelength: Wavelength
            frequency: Frequency
            phase: Initial phase
            config: Optional configuration
            
        Returns:
            PhysicsVisualization object
        """
        viz_config = config or {}
        width = viz_config.get("width", 800)
        height = viz_config.get("height", 400)
        
        elements = []
        annotations = []
        
        center_y = height // 2
        k = 2 * pi / wavelength  # Wave number
        omega = 2 * pi * frequency  # Angular frequency
        
        # Generate wave path
        path_points = []
        for x in range(50, width - 50):
            t = viz_config.get("time", 0)
            y = center_y + amplitude * sin(k * (x - 50) - omega * t + phase)
            path_points.append([x, y])
        
        elements.append({
            "type": "path",
            "d": "M " + " L ".join(f"{p[0]},{p[1]:.1f}" for p in path_points),
            "fill": "none",
            "stroke": viz_config.get("color", "#3b82f6"),
            "stroke_width": 2
        })
        
        # Add labels
        annotations.append({
            "text": f"λ = {wavelength}",
            "x": width - 100,
            "y": 30,
            "font_size": 12,
            "fill": "#374151"
        })
        annotations.append({
            "text": f"A = {amplitude}",
            "x": width - 100,
            "y": 50,
            "font_size": 12,
            "fill": "#374151"
        })
        
        return PhysicsVisualization(
            visualization_id=f"wave_{datetime.now().timestamp()}",
            visual_type=PhysicsVisualType.WAVE_PATTERN,
            width=width,
            height=height,
            elements=elements,
            annotations=annotations,
            config=viz_config,
            metadata={"type": "wave", "amplitude": amplitude, "wavelength": wavelength}
        )
    
    def export_visualization(
        self,
        visualization: PhysicsVisualization,
        format: str = "svg"
    ) -> str:
        """
        Export a visualization to specified format.
        
        Args:
            visualization: PhysicsVisualization to export
            format: Export format (svg, json)
            
        Returns:
            Exported visualization as string
        """
        if format == "json":
            import json
            return json.dumps({
                "visualization_id": visualization.visualization_id,
                "visual_type": visualization.visual_type.value,
                "width": visualization.width,
                "height": visualization.height,
                "elements": visualization.elements,
                "annotations": visualization.annotations,
                "config": visualization.config,
                "metadata": visualization.metadata
            }, indent=2)
        
        # Default to SVG
        return self._visualization_to_svg(visualization)
    
    def _visualization_to_svg(self, visualization: PhysicsVisualization) -> str:
        """Convert visualization to SVG string."""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{visualization.width}" height="{visualization.height}">'
        ]
        
        # Add background
        svg_parts.append(
            f'<rect width="100%" height="100%" fill="white"/>'
        )
        
        # Add elements
        for elem in visualization.elements:
            elem_type = elem.get("type", "line")
            
            if elem_type == "line":
                svg_parts.append(
                    f'<line x1="{elem["x1"]}" y1="{elem["y1"]}" x2="{elem["x2"]}" y2="{elem["y2"]}" '
                    f'stroke="{elem.get("stroke", "#000")}" stroke-width="{elem.get("stroke_width", 1)}"'
                    f'{f" stroke-dasharray=\"{elem.get("stroke_dasharray", "")}\"" if elem.get("stroke_dasharray") else ""}/>'
                )
            elif elem_type == "circle":
                svg_parts.append(
                    f'<circle cx="{elem["cx"]}" cy="{elem["cy"]}" r="{elem["r"]}" '
                    f'fill="{elem.get("fill", "none")}" stroke="{elem.get("stroke", "none")}"/>'
                )
            elif elem_type == "path":
                svg_parts.append(
                    f'<path d="{elem["d"]}" fill="{elem.get("fill", "none")}" '
                    f'stroke="{elem.get("stroke", "#000")}" stroke-width="{elem.get("stroke_width", 1)}"/>'
                )
            elif elem_type == "text":
                svg_parts.append(
                    f'<text x="{elem["x"]}" y="{elem["y"]}" '
                    f'fill="{elem.get("fill", "#000")}" font-size="{elem.get("font_size", 12)}"'
                    f'{f" text-anchor=\"{elem.get("anchor", "start")}\"" if elem.get("anchor") else ""}>'
                    f'{elem["text"]}</text>'
                )
        
        svg_parts.append('</svg>')
        return "\n".join(svg_parts)
