"""
Manim Wrapper for VisualVerse
Provides a simplified, subject-agnostic interface to Manim's rendering capabilities.
"""

import os
import sys
import tempfile
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

# Import Manim after path setup
from manim import *

class SceneManager:
    """
    Main interface to Manim that abstracts away low-level details.
    Provides a simplified API for plugins to create animations
    without directly depending on Manim internals.
    """
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="visualverse_")
        self.render_config = {
            "quality": "m",
            "output_file": "output.mp4",
            "background_color": BLACK
        }
        
    def create_scene(self, scene_config: Dict[str, Any]) -> str:
        """
        Create a Manim scene from configuration.
        
        Args:
            scene_config: Dictionary containing scene configuration
                         - title: Scene title
                         - objects: List of objects to create
                         - animations: List of animations to perform
                         - text of text elements
: List                         - equations: List of LaTeX equations
        
        Returns:
            Path to the rendered video file
        """
        scene_script = self._generate_scene_script(scene_config)
        return self._render_scene(scene_script, scene_config.get("output_name", "scene"))
        
    def create_graph_scene(self, graph_data: Dict[str, Any]) -> str:
        """
        Create a scene specifically for visualizing graphs/networks.
        
        Args:
            graph_data: Dictionary containing graph configuration
                       - nodes: List of node definitions
                       - edges: List of edge definitions  
                       - layout: Layout algorithm to use
                       - highlighting: Nodes/edges to highlight
        
        Returns:
            Path to the rendered video file
        """
        scene_script = self._generate_graph_scene_script(graph_data)
        return self._render_scene(scene_script, graph_data.get("output_name", "graph_scene"))
        
    def create_math_scene(self, math_config: Dict[str, Any]) -> str:
        """
        Create a scene for mathematical visualizations.
        
        Args:
            math_config: Dictionary containing math configuration
                        - functions: Function definitions to plot
                        - equations: LaTeX equations to display
                        - geometric_objects: Shapes and geometric elements
                        - coordinate_system: Axes and grid configuration
        
        Returns:
            Path to the rendered video file
        """
        scene_script = self._generate_math_scene_script(math_config)
        return self._render_scene(scene_script, math_config.get("output_name", "math_scene"))
        
    def create_physics_scene(self, physics_config: Dict[str, Any]) -> str:
        """
        Create a scene for physics simulations.
        
        Args:
            physics_config: Dictionary containing physics configuration
                          - objects: Physical objects and their properties
                          - forces: Forces acting on objects
                          - motion: Motion parameters and trajectories
                          - measurements: Measurement tools and scales
        
        Returns:
            Path to the rendered video file
        """
        scene_script = self._generate_physics_scene_script(physics_config)
        return self._render_scene(scene_script, physics_config.get("output_name", "physics_scene"))
        
    def _generate_scene_script(self, config: Dict[str, Any]) -> str:
        """Generate Manim scene script from configuration"""
        
        script_lines = [
            "from manim import *",
            "",
            f"class {config.get('class_name', 'VisualVerseScene')}(Scene):",
            "    def construct(self):"
        ]
        
        # Add title
        if "title" in config:
            script_lines.append(f'        title = Text("{config["title"]}").scale(1.5)')
            script_lines.append("        self.add(title)")
            script_lines.append("        self.wait(2)")
            script_lines.append("        self.remove(title)")
            script_lines.append("")
            
        # Add text elements
        if "text" in config:
            for i, text_element in enumerate(config["text"]):
                script_lines.append(f'        text_{i} = Text("{text_element}").scale(0.8)')
                script_lines.append(f"        self.add(text_{i})")
                script_lines.append("        self.wait(1)")
                script_lines.append("")
                
        # Add equations
        if "equations" in config:
            for i, equation in enumerate(config["equations"]):
                script_lines.append(f'        eq_{i} = MathTex(r"{equation}").scale(1.2)')
                script_lines.append(f"        self.add(eq_{i})")
                script_lines.append("        self.wait(2)")
                script_lines.append("")
                
        script_lines.append("        self.wait(2)")
        
        return "\n".join(script_lines)
        
    def _generate_graph_scene_script(self, graph_data: Dict[str, Any]) -> str:
        """Generate Manim script for graph visualization"""
        
        script_lines = [
            "from manim import *",
            "from manim import Graph",
            "",
            f"class {graph_data.get('class_name', 'GraphScene')}(Scene):",
            "    def construct(self):"
        ]
        
        # Create nodes
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        if nodes and edges:
            # Create graph structure
            script_lines.append("        # Create graph")
            script_lines.append(f"        nodes = {json.dumps(nodes)}")
            script_lines.append(f"        edges = {json.dumps(edges)}")
            script_lines.append("        ")
            script_lines.append("        # Create graph visualization")
            script_lines.append("        graph = Graph(nodes, edges)")
            script_lines.append("        self.add(graph)")
            script_lines.append("        self.wait(3)")
        else:
            script_lines.append("        # Empty graph scene")
            script_lines.append('        placeholder = Text("Graph visualization")')
            script_lines.append("        self.add(placeholder)")
            script_lines.append("        self.wait(2)")
            
        return "\n".join(script_lines)
        
    def _generate_math_scene_script(self, math_config: Dict[str, Any]) -> str:
        """Generate Manim script for mathematical visualizations"""
        
        script_lines = [
            "from manim import *",
            "import numpy as np",
            "",
            f"class {math_config.get('class_name', 'MathScene')}(Scene):",
            "    def construct(self):"
        ]
        
        # Add coordinate axes if specified
        if math_config.get("show_axes", True):
            script_lines.append("        # Add coordinate system")
            script_lines.append("        axes = Axes()")
            script_lines.append("        self.add(axes)")
            script_lines.append("")
            
        # Add functions
        functions = math_config.get("functions", [])
        for i, func_config in enumerate(functions):
            func_str = func_config.get("function", "x**2")
            color = func_config.get("color", BLUE)
            script_lines.append(f"        # Function {i+1}")
            script_lines.append(f"        graph = FunctionGraph(lambda x: {func_str}, color={color})")
            script_lines.append("        self.add(graph)")
            script_lines.append("        self.wait(1)")
            script_lines.append("")
            
        # Add equations
        equations = math_config.get("equations", [])
        for i, equation in enumerate(equations):
            script_lines.append(f'        eq_{i} = MathTex(r"{equation}").scale(1.2)')
            script_lines.append(f"        self.add(eq_{i})")
            script_lines.append("        self.wait(2)")
            script_lines.append("")
            
        return "\n".join(script_lines)
        
    def _generate_physics_scene_script(self, physics_config: Dict[str, Any]) -> str:
        """Generate Manim script for physics simulations"""
        
        script_lines = [
            "from manim import *",
            "from manim.physics.mechanics import *",
            "",
            f"class {physics_config.get('class_name', 'PhysicsScene')}(Scene):",
            "    def construct(self):"
        ]
        
        # Add objects
        objects = physics_config.get("objects", [])
        for i, obj_config in enumerate(objects):
            obj_type = obj_config.get("type", "circle")
            position = obj_config.get("position", [0, 0, 0])
            color = obj_config.get("color", WHITE)
            size = obj_config.get("size", 1)
            
            script_lines.append(f"        # Object {i+1}")
            if obj_type == "circle":
                script_lines.append(f"        obj_{i} = Circle(radius={size}, color={color}).move_to({position})")
            elif obj_type == "square":
                script_lines.append(f"        obj_{i} = Square(side_length={size*2}, color={color}).move_to({position})")
            else:
                script_lines.append(f"        obj_{i} = Circle(radius={size}, color={color}).move_to({position})")
                
            script_lines.append(f"        self.add(obj_{i})")
            script_lines.append("        self.wait(0.5)")
            script_lines.append("")
            
        script_lines.append("        self.wait(3)")
        
        return "\n".join(script_lines)
        
    def _render_scene(self, scene_script: str, output_name: str) -> str:
        """
        Render a Manim scene script to video.
        
        Args:
            scene_script: The Manim Python script to execute
            output_name: Name for the output file
            
        Returns:
            Path to the rendered video file
        """
        # Create temporary Python file
        temp_script_path = Path(self.temp_dir) / f"{output_name}.py"
        with open(temp_script_path, 'w') as f:
            f.write(scene_script)
        
        # Set up output directory
        output_dir = Path(self.temp_dir) / "renders"
        output_dir.mkdir(exist_ok=True)
        
        # Render using manim
        try:
            # Change to temp directory and run manim
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)
            
            # Use manim command line interface
            import subprocess
            
            cmd = [
                "manim", 
                "-v", "WARNING",
                "--quality", "m",
                "--output_file", output_name,
                str(temp_script_path),
                "Scene"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            os.chdir(original_cwd)
            
            if result.returncode == 0:
                # Find the output file
                media_dir = Path(self.temp_dir) / "media" / "videos" / "720p30"
                output_file = media_dir / f"{output_name}.mp4"
                
                if output_file.exists():
                    # Copy to permanent location
                    final_output = Path(f"/workspace/renders/{output_name}.mp4")
                    final_output.parent.mkdir(exist_ok=True)
                    shutil.copy2(output_file, final_output)
                    return str(final_output)
                    
            print(f"Manim rendering error: {result.stderr}")
            return None
            
        except subprocess.TimeoutExpired:
            print("Manim rendering timed out")
            return None
        except Exception as e:
            print(f"Manim rendering failed: {e}")
            return None
            
    def cleanup(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

class RenderJob:
    """
    Represents a rendering job that can be queued and executed asynchronously.
    """
    
    def __init__(self, job_id: str, scene_config: Dict[str, Any], priority: int = 0):
        self.job_id = job_id
        self.scene_config = scene_config
        self.priority = priority
        self.status = "pending"
        self.result = None
        self.created_at = None
        self.completed_at = None
        
    def execute(self) -> str:
        """Execute the render job"""
        scene_manager = SceneManager()
        self.status = "rendering"
        
        try:
            result_path = scene_manager.create_scene(self.scene_config)
            self.result = result_path
            self.status = "completed"
            return result_path
        except Exception as e:
            self.status = "failed"
            self.result = str(e)
            raise e
        finally:
            scene_manager.cleanup()