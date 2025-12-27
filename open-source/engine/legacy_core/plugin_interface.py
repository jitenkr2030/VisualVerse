"""
Base Plugin Interface for VisualVerse Verticals
All subject-specific plugins must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from core.schema.base_models import ConceptMap, ConceptNode, LessonNode

class IVerticalPlugin(ABC):
    """
    Interface that all VisualVerse vertical plugins must implement.
    This ensures consistency across different subject areas.
    """
    
    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Name of the plugin (e.g., 'math', 'physics')"""
        pass
        
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name (e.g., 'Mathematics', 'Physics')"""
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass
        
    @abstractmethod
    def get_available_syllabi(self) -> Dict[str, str]:
        """
        Get available curriculum standards/syllabi for this subject.
        
        Returns:
            Dictionary mapping syllabus_id to syllabus_name
            e.g., {'cbse': 'CBSE (India)', 'icse': 'ICSE (India)', 'university': 'University Level'}
        """
        pass
        
    @abstractmethod
    def get_syllabus(self, syllabus_id: str) -> Dict[str, Any]:
        """
        Get the complete syllabus for a specific curriculum standard.
        
        Args:
            syllabus_id: ID of the syllabus to retrieve
            
        Returns:
            Dictionary containing syllabus structure
        """
        pass
        
    @abstractmethod
    def get_concept_map(self) -> Dict[str, ConceptNode]:
        """
        Get the complete concept map for this subject.
        
        Returns:
            Dictionary mapping concept_id to ConceptNode
        """
        pass
        
    @abstractmethod
    def create_lesson(self, lesson_id: str, content: str) -> str:
        """
        Create a lesson using this subject's specific logic.
        
        Args:
            lesson_id: Unique identifier for the lesson
            content: Lesson content and configuration
            
        Returns:
            Path to the rendered lesson video or lesson data
        """
        pass
        
    @abstractmethod
    def get_subject_specific_objects(self) -> Dict[str, Any]:
        """
        Get subject-specific Manim objects and utilities.
        
        Returns:
            Dictionary of available objects, utilities, and templates
        """
        pass
        
    @abstractmethod
    def validate_concept(self, concept_data: Dict[str, Any]) -> bool:
        """
        Validate that concept data is valid for this subject.
        
        Args:
            concept_data: Concept data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
        
    def get_learning_objectives_template(self) -> Dict[str, List[str]]:
        """
        Get subject-specific learning objectives templates.
        
        Returns:
            Dictionary mapping concept types to suggested learning objectives
        """
        return {
            "basic": ["Understand the fundamental concept", "Apply to simple examples"],
            "intermediate": ["Apply concepts to complex problems", "Connect to other topics"],
            "advanced": ["Analyze and synthesize", "Create original solutions"]
        }
        
    def get_assessment_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Get subject-specific assessment templates.
        
        Returns:
            Dictionary of assessment templates for different concept types
        """
        return {
            "multiple_choice": {
                "type": "multiple_choice",
                "default_options": 4,
                "difficulty_levels": ["basic", "intermediate", "advanced"]
            },
            "problem_solving": {
                "type": "problem_solving",
                "steps": ["analyze", "plan", "execute", "verify"],
                "scoring_rubric": "detailed"
            }
        }
        
    def get_visual_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Get subject-specific visual animation templates.
        
        Returns:
            Dictionary of visual templates for common concepts
        """
        # Import enhanced templates
        from core.templates.enhanced_templates import get_subject_templates
        return get_subject_templates(self.plugin_name)
        
    def preprocess_content(self, content: str) -> str:
        """
        Preprocess content specific to this subject.
        Can be overridden by plugins for subject-specific text processing.
        
        Args:
            raw_content: Raw content input
            
        Returns:
            Processed content
        """
        return content
        
    def get_difficulty_adjustment(self, base_difficulty: str, student_profile: Dict[str, Any]) -> str:
        """
        Adjust difficulty based on student profile for this subject.
        
        Args:
            base_difficulty: Base difficulty level
            student_profile: Student learning profile
            
        Returns:
            Adjusted difficulty level
        """
        # Default implementation - can be overridden by plugins
        return base_difficulty
        
    def get_prerequisite_suggestions(self, concept_type: str) -> List[str]:
        """
        Get suggested prerequisites for a concept type.
        
        Args:
            concept_type: Type of concept
            
        Returns:
            List of suggested prerequisite concepts
        """
        return []

class PluginRegistry:
    """
    Registry for managing VisualVerse plugins.
    """
    
    def __init__(self):
        self._plugins: Dict[str, IVerticalPlugin] = {}
        
    def register_plugin(self, plugin: IVerticalPlugin):
        """Register a plugin"""
        self._plugins[plugin.plugin_name] = plugin
        print(f"✅ Registered plugin: {plugin.display_name} v{plugin.version}")
        
    def get_plugin(self, plugin_name: str) -> Optional[IVerticalPlugin]:
        """Get a plugin by name"""
        return self._plugins.get(plugin_name)
        
    def get_all_plugins(self) -> Dict[str, IVerticalPlugin]:
        """Get all registered plugins"""
        return self._plugins.copy()
        
    def get_available_subjects(self) -> List[str]:
        """Get list of available subject names"""
        return list(self._plugins.keys())
        
    def get_plugin_info(self) -> Dict[str, Dict[str, str]]:
        """Get information about all registered plugins"""
        info = {}
        for name, plugin in self._plugins.items():
            info[name] = {
                "name": plugin.display_name,
                "version": plugin.version,
                "plugin_name": plugin.plugin_name
            }
        return info
        
    def validate_all_plugins(self) -> Dict[str, bool]:
        """Validate all registered plugins"""
        validation_results = {}
        for name, plugin in self._plugins.items():
            try:
                # Test basic plugin functionality
                syllabi = plugin.get_available_syllabi()
                concept_map = plugin.get_concept_map()
                objects = plugin.get_subject_specific_objects()
                
                validation_results[name] = True
                print(f"✅ Plugin {name} validation passed")
                
            except Exception as e:
                validation_results[name] = False
                print(f"❌ Plugin {name} validation failed: {e}")
                
        return validation_results

# Global plugin registry
plugin_registry = PluginRegistry()