"""
ChemVerse Plugin - Chemistry Education Platform
Provides chemistry visualization capabilities and curriculum mapping.
Uses Manim for molecular and reaction visualizations.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the engine path for imports
engine_path = Path(__file__).parent.parent.parent / "open-source" / "engine"
sys.path.insert(0, str(engine_path))

from plugin_interface import IVerticalPlugin
from schema.base_models import ConceptNode
from legacy_core.manim_wrapper.scene_manager import SceneManager, RenderJob


class ChemVersePlugin(IVerticalPlugin):
    """Chemistry-specific plugin for VisualVerse with Manim integration"""
    
    def __init__(self):
        super().__init__()
        self.display_name = "Chemistry"
        self.version = "1.0.0"
        self.subject_id = "chemistry"
        self.scene_manager = SceneManager()
        self.render_queue: Dict[str, RenderJob] = {}
        
    @property
    def plugin_name(self) -> str:
        return "chemistry"
        
    def get_concept_map(self):
        """Return chemistry concepts and dependencies"""
        concepts = {
            "atomic_structure": ConceptNode(
                id="atomic_structure",
                title="Atomic Structure",
                description="Understanding protons, neutrons, and electrons",
                difficulty="beginner",
                prerequisites=[],
                estimated_duration=60
            ),
            "chemical_bonds": ConceptNode(
                id="chemical_bonds",
                title="Chemical Bonds",
                description="Ionic, covalent, and metallic bonding",
                difficulty="intermediate",
                prerequisites=["atomic_structure"],
                estimated_duration=90
            ),
            "reaction_mechanisms": ConceptNode(
                id="reaction_mechanisms",
                title="Reaction Mechanisms",
                description="Step-by-step chemical reaction processes",
                difficulty="advanced",
                prerequisites=["chemical_bonds"],
                estimated_duration=120
            )
        }
        return concepts
        
    def create_lesson(self, lesson_id: str, content: str) -> str:
        """Create chemistry-specific animations using Manim"""
        config = self._parse_chemistry_content(content)
        return self.scene_manager.create_scene(config)
        
    def create_molecular_visualization(
        self,
        atoms: List[Dict[str, Any]],
        bonds: List[tuple],
        title: str = "Molecular Structure"
    ) -> str:
        """
        Create a molecular structure visualization.
        
        Args:
            atoms: List of atoms with 'element', 'position', 'color', 'size'
            bonds: List of (atom_index1, atom_index2) tuples for bonds
            title: Title for the visualization
            
        Returns:
            Path to the rendered video file
        """
        # Convert molecular structure to graph visualization
        nodes = [f"{atom.get('element', 'C')}{i}" for i, atom in enumerate(atoms)]
        edges = []
        
        for bond in bonds:
            if len(bond) == 2:
                edges.append((nodes[bond[0]], nodes[bond[1]]))
                
        graph_config = {
            "class_name": f"ChemVerse{title.replace(' ', '')}",
            "nodes": nodes,
            "edges": edges,
            "output_name": f"molecule_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_graph_scene(graph_config)
        
    def create_reaction_animation(
        self,
        reactants: List[str],
        products: List[str],
        equation: str,
        title: str = "Chemical Reaction"
    ) -> str:
        """
        Create a chemical reaction animation.
        
        Args:
            reactants: List of reactant molecules
            products: List of product molecules
            equation: LaTeX equation of the reaction
            title: Title for the animation
            
        Returns:
            Path to the rendered video file
        """
        config = {
            "class_name": f"Reaction{title.replace(' ', '')}",
            "title": title,
            "text": [f"Reactants: {', '.join(reactants)}", f"Products: {', '.join(products)}"],
            "equations": [equation],
            "output_name": f"reaction_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_scene(config)
        
    def create_periodic_table_highlight(
        self,
        element_group: List[str],
        title: str = "Periodic Table"
    ) -> str:
        """
        Create a periodic table group highlight visualization.
        
        Args:
            element_group: List of element symbols to highlight
            title: Title for the visualization
            
        Returns:
            Path to the rendered video file
        """
        config = {
            "class_name": f"PeriodicTable{title.replace(' ', '')}",
            "title": title,
            "text": [f"Group Elements: {', '.join(element_group)}"],
            "equations": [],
            "output_name": f"periodic_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_scene(config)
        
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
        """Return Manim objects for chemistry"""
        return {
            "molecular_models": {
                "description": "3D molecular structure representations",
                "manim_classes": ["Circle", "Line"]
            },
            "reaction_diagrams": {
                "description": "Chemical equation and mechanism visualizations",
                "manim_classes": ["Text", "MathTex", "Arrow"]
            },
            "periodic_table": {
                "description": "Interactive periodic table elements",
                "manim_classes": ["Rectangle", "Text"]
            },
            "energy_diagrams": {
                "description": "Reaction energy profiles and thermodynamics",
                "manim_classes": ["Axes", "Line", "Text"]
            },
            "atomic_orbitals": {
                "description": "Electron orbital visualizations",
                "manim_classes": ["Circle", "Dot"]
            }
        }
        
    def validate_content(self, content: str) -> bool:
        """Validate chemistry content"""
        chem_indicators = ['atom', 'molecule', 'reaction', 'bond', 'element', 'periodic']
        content_lower = content.lower()
        chem_count = sum(1 for indicator in chem_indicators if indicator in content_lower)
        return len(content.strip()) > 10 and chem_count >= 1
        
    def _parse_chemistry_content(self, content: str) -> Dict[str, Any]:
        """Parse chemistry content to extract visualization configuration."""
        config = {
            "class_name": "ChemVerseLesson",
            "title": "Chemistry Lesson",
            "text": [],
            "equations": [],
            "output_name": "chemistry_lesson"
        }
        
        # Extract LaTeX equations
        import re
        latex_patterns = re.findall(r'\$.*?\$', content)
        for latex in latex_patterns:
            config["equations"].append(latex.strip('$'))
            
        return config
        
    def cleanup(self):
        """Clean up resources"""
        self.scene_manager.cleanup()
        self.render_queue.clear()
