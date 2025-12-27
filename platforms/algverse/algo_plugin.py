"""
AlgoVerse Plugin - Computer Science Education Platform
Provides algorithm visualization capabilities and curriculum mapping.
Uses Manim for algorithm animations and visualizations.
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


class AlgoVersePlugin(IVerticalPlugin):
    """Computer Science Algorithm-specific plugin for VisualVerse with Manim integration"""
    
    def __init__(self):
        super().__init__()
        self.display_name = "Computer Science"
        self.version = "1.0.0"
        self.subject_id = "computer_science"
        self.scene_manager = SceneManager()
        self.render_queue: Dict[str, RenderJob] = {}
        
    @property
    def plugin_name(self) -> str:
        return "algorithms"
        
    def get_concept_map(self):
        """Return CS concepts and dependencies"""
        concepts = {
            "data_structures": ConceptNode(
                id="data_structures",
                title="Data Structures",
                description="Basic data structures like arrays, lists, trees",
                difficulty="beginner",
                prerequisites=[],
                estimated_duration=90
            ),
            "sorting": ConceptNode(
                id="sorting",
                title="Sorting Algorithms",
                description="Various sorting algorithms and their complexity",
                difficulty="intermediate",
                prerequisites=["data_structures"],
                estimated_duration=75
            ),
            "searching": ConceptNode(
                id="searching",
                title="Searching Algorithms",
                description="Linear and binary search algorithms",
                difficulty="beginner",
                prerequisites=["data_structures"],
                estimated_duration=60
            )
        }
        return concepts
        
    def create_lesson(self, lesson_id: str, content: str) -> str:
        """Create algorithm-specific animations using Manim"""
        graph_config = self._parse_algorithm_content(content)
        return self.scene_manager.create_graph_scene(graph_config)
        
    def create_algorithm_visualization(
        self,
        nodes: List[str],
        edges: List[tuple],
        layout: str = "spring",
        title: str = "Algorithm Visualization",
        highlighting: List[str] = None
    ) -> str:
        """
        Create a visualization of an algorithm or data structure.
        
        Args:
            nodes: List of node labels
            edges: List of (source, target) tuples representing connections
            layout: Layout algorithm to use (spring, circular, shell)
            title: Title for the visualization
            highlighting: List of nodes/edges to highlight
            
        Returns:
            Path to the rendered video file
        """
        graph_data = {
            "class_name": f"AlgoVerse{title.replace(' ', '')}",
            "nodes": nodes,
            "edges": edges,
            "layout": layout,
            "highlighting": highlighting or [],
            "output_name": f"algo_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_graph_scene(graph_data)
        
    def create_sorting_animation(
        self,
        array: List[int],
        algorithm: str = "bubble",
        title: str = "Sorting Animation"
    ) -> str:
        """
        Create a sorting algorithm animation.
        
        Args:
            array: List of integers to sort
            algorithm: Sorting algorithm to visualize
            title: Title for the animation
            
        Returns:
            Path to the rendered video file
        """
        # Convert sorting to a graph visualization
        nodes = [str(x) for x in array]
        edges = []
        
        for i in range(len(array) - 1):
            edges.append((str(array[i]), str(array[i + 1])))
            
        return self.create_algorithm_visualization(
            nodes=nodes,
            edges=edges,
            layout="linear",
            title=title,
            highlighting=[]
        )
        
    def create_tree_visualization(
        self,
        tree_data: Dict[str, Any],
        title: str = "Tree Structure"
    ) -> str:
        """
        Create a tree data structure visualization.
        
        Args:
            tree_data: Tree structure with 'root' and 'children'
            title: Title for the visualization
            
        Returns:
            Path to the rendered video file
        """
        nodes = []
        edges = []
        
        def traverse(node, parent=None):
            node_id = str(node.get('value', len(nodes)))
            nodes.append(node_id)
            if parent:
                edges.append((str(parent), node_id))
            for child in node.get('children', []):
                traverse(child, node.get('value'))
                
        traverse(tree_data)
        return self.create_algorithm_visualization(nodes, edges, "tree", title)
        
    def queue_render_job(
        self,
        job_id: str,
        scene_config: Dict[str, Any],
        priority: int = 0
    ) -> str:
        """Queue a rendering job for asynchronous processing."""
        job = RenderJob(job_id, scene_config, priority)
        self.render_queue[job_id] = job
        return job_id
        
    def get_render_status(self, job_id: str) -> Dict[str, Any]:
        """Get the status of a render job."""
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
        """Return Manim objects for CS"""
        return {
            "code_blocks": {
                "description": "Syntax-highlighted code representations",
                "manim_class": "Text"
            },
            "data_structures": {
                "description": "Visual tree and graph structures",
                "manim_classes": ["Circle", "Line", "Arrow"]
            },
            "algorithm_flow": {
                "description": "Flowchart and step-by-step visualizations",
                "manim_classes": ["Rectangle", "Arrow", "Text"]
            },
            "complexity_charts": {
                "description": "Big-O notation and performance graphs",
                "manim_classes": ["Axes", "Line", "Text"]
            },
            "arrays": {
                "description": "Array element visualizations",
                "manim_classes": ["Rectangle", "Text"]
            }
        }
        
    def validate_content(self, content: str) -> bool:
        """Validate CS content"""
        cs_indicators = ['algorithm', 'sort', 'search', 'tree', 'graph', 'array', 'complexity']
        content_lower = content.lower()
        cs_count = sum(1 for indicator in cs_indicators if indicator in content_lower)
        return len(content.strip()) > 10 and cs_count >= 1
        
    def _parse_algorithm_content(self, content: str) -> Dict[str, Any]:
        """Parse algorithm content to extract visualization configuration."""
        config = {
            "class_name": "AlgoVerseLesson",
            "nodes": [],
            "edges": [],
            "output_name": "algorithm_lesson"
        }
        
        # Simple parsing - look for common patterns
        if 'array' in content.lower():
            import re
            array_match = re.search(r'\[(.*?)\]', content)
            if array_match:
                array_str = array_match.group(1)
                array = [int(x.strip()) for x in array_str.split(',') if x.strip().isdigit()]
                config["nodes"] = [str(x) for x in array]
                
        if not config["nodes"]:
            # Default nodes
            config["nodes"] = ["1", "2", "3", "4", "5"]
            
        return config
        
    def cleanup(self):
        """Clean up resources"""
        self.scene_manager.cleanup()
        self.render_queue.clear()
