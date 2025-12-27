"""
MathVerse Plugin - Mathematics Education Platform
Provides mathematical animation capabilities and curriculum mapping.
Uses Manim for high-quality mathematical visualizations.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the engine path for imports
engine_path = Path(__file__).parent.parent.parent / "open-source" / "engine"
sys.path.insert(0, str(engine_path))

from plugin_interface import IVerticalPlugin
from schema.base_models import ConceptNode
from legacy_core.manim_wrapper.scene_manager import SceneManager, RenderJob


class MathVersePlugin(IVerticalPlugin):
    """Mathematics-specific plugin for VisualVerse with Manim integration"""
    
    def __init__(self):
        super().__init__()
        self.display_name = "Mathematics"
        self.version = "1.0.0"
        self.subject_id = "mathematics"
        self.scene_manager = SceneManager()
        self.render_queue: Dict[str, RenderJob] = {}
        
    @property
    def plugin_name(self) -> str:
        return "math"
        
    def get_concept_map(self):
        """Return mathematics concepts and dependencies"""
        concepts = {
            "place_value": ConceptNode(
                id="place_value",
                title="Place Value",
                description="Understanding place values in numbers",
                difficulty="beginner",
                prerequisites=[],
                estimated_duration=30
            ),
            "integers": ConceptNode(
                id="integers", 
                title="Integers",
                description="Working with positive and negative numbers",
                difficulty="beginner",
                prerequisites=["place_value"],
                estimated_duration=45
            ),
            "variables": ConceptNode(
                id="variables",
                title="Variables", 
                description="Introduction to algebraic variables",
                difficulty="intermediate",
                prerequisites=["integers"],
                estimated_duration=60
            ),
            "linear_equations": ConceptNode(
                id="linear_equations",
                title="Linear Equations",
                description="Solving linear equations in one variable", 
                difficulty="intermediate",
                prerequisites=["variables"],
                estimated_duration=75
            ),
            "basic_shapes": ConceptNode(
                id="basic_shapes",
                title="Basic Shapes",
                description="Understanding geometric shapes and properties",
                difficulty="beginner", 
                prerequisites=[],
                estimated_duration=40
            ),
            "calculus": ConceptNode(
                id="calculus",
                title="Calculus Fundamentals",
                description="Introduction to limits, derivatives, and integrals",
                difficulty="advanced",
                prerequisites=["linear_equations"],
                estimated_duration=120
            )
        }
        return concepts
        
    def create_lesson(self, lesson_id: str, content: str) -> str:
        """Create math-specific animations using Manim"""
        # Parse content to determine what type of math visualization to create
        math_config = self._parse_math_content(content)
        return self.scene_manager.create_math_scene(math_config)
        
    def create_math_visualization(
        self,
        functions: List[Dict[str, Any]],
        equations: List[str],
        title: str = "Math Visualization",
        show_axes: bool = True
    ) -> str:
        """
        Create a mathematical visualization with functions and equations.
        
        Args:
            functions: List of function configurations with 'function' key (e.g., "x**2")
            equations: List of LaTeX equations to display
            title: Title for the visualization
            show_axes: Whether to show coordinate axes
            
        Returns:
            Path to the rendered video file
        """
        config = {
            "class_name": f"MathVerse{title.replace(' ', '')}",
            "title": title,
            "functions": functions,
            "equations": equations,
            "show_axes": show_axes,
            "output_name": f"math_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_math_scene(config)
        
    def create_function_graph(
        self,
        function: str,
        x_range: tuple = (-5, 5),
        color: str = "BLUE"
    ) -> str:
        """
        Create a visualization of a single function graph.
        
        Args:
            function: Python function string (e.g., "x**2")
            x_range: Tuple of (min_x, max_x)
            color: Color for the graph line
            
        Returns:
            Path to the rendered video file
        """
        config = {
            "class_name": f"FunctionGraph_{function.replace('**', 'pow').replace('*', 'mul')}",
            "functions": [{"function": function, "color": color}],
            "equations": [],
            "show_axes": True,
            "output_name": f"function_{function}"
        }
        return self.scene_manager.create_math_scene(config)
        
    def create_geometric_scene(
        self,
        shapes: List[Dict[str, Any]],
        title: str = "Geometric Shapes"
    ) -> str:
        """
        Create a scene with geometric shapes.
        
        Args:
            shapes: List of shape configurations with 'type', 'position', 'color', 'size'
            title: Title for the scene
            
        Returns:
            Path to the rendered video file
        """
        # Convert geometric shapes to a physics-like scene for Manim
        config = {
            "class_name": f"GeometricScene_{title.replace(' ', '')}",
            "objects": shapes,
            "output_name": f"geometric_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_physics_scene(config)
        
    def queue_render_job(
        self,
        job_id: str,
        scene_config: Dict[str, Any],
        priority: int = 0
    ) -> str:
        """
        Queue a rendering job for asynchronous processing.
        
        Args:
            job_id: Unique identifier for the job
            scene_config: Scene configuration dictionary
            priority: Job priority (higher = processed first)
            
        Returns:
            Job ID
        """
        job = RenderJob(job_id, scene_config, priority)
        self.render_queue[job_id] = job
        return job_id
        
    def get_render_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a render job.
        
        Args:
            job_id: ID of the job to check
            
        Returns:
            Dictionary with job status information
        """
        if job_id not in self.render_queue:
            return {"status": "not_found", "error": f"Job {job_id} not found"}
            
        job = self.render_queue[job_id]
        return {
            "job_id": job.job_id,
            "status": job.status,
            "result": job.result,
            "priority": job.priority
        }
        
    def get_subject_specific_objects(self):
        """Return Manim objects for mathematics"""
        return {
            "coordinate_plane": {
                "description": "2D coordinate system",
                "manim_class": "Axes",
                "parameters": {"x_range": [-10, 10], "y_range": [-10, 10]}
            },
            "function_graph": {
                "description": "Graph plotting capabilities",
                "manim_class": "FunctionGraph",
                "parameters": {"func": lambda x: x**2, "color": "BLUE"}
            },
            "geometric_shapes": {
                "description": "Mathematical shapes and constructions",
                "manim_classes": ["Circle", "Square", "Triangle", "Line", "Arrow"]
            },
            "equations": {
                "description": "Mathematical equations and formulas",
                "manim_class": "MathTex",
                "parameters": {"tex_string": "E = mc^2"}
            },
            "3d_surfaces": {
                "description": "3D surface plots",
                "manim_class": "ParametricSurface",
                "parameters": {}
            }
        }
        
    def validate_content(self, content: str) -> bool:
        """Validate mathematics content"""
        # Check for math content indicators
        math_indicators = ['+', '-', '*', '/', '=', 'function', 'equation', 'graph', 'theorem']
        content_lower = content.lower()
        
        math_count = sum(1 for indicator in math_indicators if indicator in content_lower)
        return len(content.strip()) > 10 and math_count >= 1
        
    def _parse_math_content(self, content: str) -> Dict[str, Any]:
        """
        Parse math content to extract visualization configuration.
        
        Args:
            content: The math content string
            
        Returns:
            Configuration dictionary for Manim scene
        """
        config = {
            "class_name": "MathVerseLesson",
            "title": "Mathematics Lesson",
            "functions": [],
            "equations": [],
            "show_axes": True
        }
        
        # Extract function patterns like "f(x) = x^2" or "y = sin(x)"
        import re
        
        # Find equations in LaTeX format
        latex_patterns = re.findall(r'\$.*?\$', content)
        for latex in latex_patterns:
            config["equations"].append(latex.strip('$'))
            
        # Simple function detection
        if 'x^2' in content or 'x**2' in content:
            config["functions"].append({"function": "x**2", "color": "BLUE"})
        if 'x^3' in content or 'x**3' in content:
            config["functions"].append({"function": "x**3", "color": "RED"})
        if 'sin' in content.lower():
            config["functions"].append({"function": "np.sin(x)", "color": "GREEN"})
        if 'cos' in content.lower():
            config["functions"].append({"function": "np.cos(x)", "color": "YELLOW"})
            
        return config
        
    def cleanup(self):
        """Clean up resources"""
        self.scene_manager.cleanup()
        self.render_queue.clear()
