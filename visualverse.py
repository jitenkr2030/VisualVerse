"""
VisualVerse - One Engine, Many Verticals
Main configuration and initialization module.
"""

import os
import sys
from typing import Dict, List, Type
from pathlib import Path

# Import from legacy core structure (migrated to new architecture)
sys.path.insert(0, str(Path(__file__).parent / "engine" / "legacy_core"))

# Mock classes for demo purposes (when Manim is not available)
class MockSceneManager:
    """Mock Scene Manager for demo purposes"""
    def __init__(self):
        pass

class MockRenderEngine:
    """Mock Render Engine for demo purposes"""
    def __init__(self):
        pass

class MockLearningPathGenerator:
    """Mock Learning Path Generator for demo purposes"""
    def generate_path(self, student_progress, concept_map):
        # Mock implementation
        return ["next_concept_1", "next_concept_2", "next_concept_3"]

class VisualVerseEngine:
    """
    Core engine that orchestrates all components of VisualVerse.
    This is the subject-agnostic layer that doesn't know if it's 
    teaching math, physics, or finance.
    """
    
    def __init__(self):
        try:
            # Try to import real components if available
            from schema.base_models import ConceptNode, LessonNode, DependencyGraph
            from manim_wrapper.scene_manager import SceneManager
            from render_queue.render_engine import RenderEngine
            from recommender.learning_path import LearningPathGenerator
            
            self.scene_manager = SceneManager()
            self.render_engine = RenderEngine()
            self.learning_path_generator = LearningPathGenerator()
            self.real_components = True
            
        except (ImportError, ModuleNotFoundError):
            # Use mock components for demo
            print("ℹ️ Using mock components (Manim not available)")
            self.scene_manager = MockSceneManager()
            self.render_engine = MockRenderEngine()
            self.learning_path_generator = MockLearningPathGenerator()
            self.real_components = False
            
        self.plugins = {}
        self.concept_graph = None
        
    def register_plugin(self, plugin_name: str, plugin_class: Type):
        """Register a vertical plugin (MathVerse, PhysicsVerse, etc.)"""
        self.plugins[plugin_name] = plugin_class()
        print(f"✅ Registered plugin: {plugin_name}")
        
    def get_available_subjects(self) -> List[str]:
        """Get list of available subject verticals"""
        return list(self.plugins.keys())
        
    def create_lesson(self, subject: str, lesson_id: str, content: str) -> str:
        """Create a lesson for any subject using the appropriate plugin"""
        if subject not in self.plugins:
            raise ValueError(f"Subject {subject} not available. Available: {self.get_available_subjects()}")
            
        plugin = self.plugins[subject]
        return plugin.create_lesson(lesson_id, content)
        
    def generate_learning_path(self, student_progress: Dict[str, bool], subject: str) -> List[str]:
        """Generate personalized learning path based on student progress"""
        if subject not in self.plugins:
            raise ValueError(f"Subject {subject} not available")
            
        plugin = self.plugins[subject]
        concept_map = plugin.get_concept_map()
        return self.learning_path_generator.generate_path(
            student_progress, concept_map
        )

# Global engine instance
engine = VisualVerseEngine()

def initialize_visualverse():
    """Initialize VisualVerse with all available plugins"""
    print("🚀 Initializing VisualVerse Engine...")
    
    # Import and register plugins (using new platform structure)
    try:
        from platforms.mathverse.math_plugin import MathVersePlugin
        engine.register_plugin("math", MathVersePlugin)
    except ImportError:
        print("⚠️ MathVerse plugin not available")
    
    try:
        from platforms.physicsverse.physics_plugin import PhysicsVersePlugin
        engine.register_plugin("physics", PhysicsVersePlugin)
    except ImportError:
        print("⚠️ PhysicsVerse plugin not available")
    
    try:
        from platforms.algverse.algo_plugin import AlgoVersePlugin
        engine.register_plugin("algorithms", AlgoVersePlugin)
    except ImportError:
        print("⚠️ AlgoVerse plugin not available")
    
    try:
        from platforms.finverse.fin_plugin import FinVersePlugin
        engine.register_plugin("finance", FinVersePlugin)
    except ImportError:
        print("⚠️ FinVerse plugin not available")
    
    try:
        from platforms.chemverse.chem_plugin import ChemVersePlugin
        engine.register_plugin("chemistry", ChemVersePlugin)
    except ImportError:
        print("⚠️ ChemVerse plugin not available")
    
    print(f"✅ VisualVerse initialized with {len(engine.get_available_subjects())} subjects")
    return engine
