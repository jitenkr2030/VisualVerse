"""
Service Extension Base Classes for Vertical Platform Features

This module provides the base classes and patterns for extending core services
with domain-specific functionality. Each vertical can extend these services
to add specialized behavior while maintaining compatibility with the core engine.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Type, TypeVar, Generic
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


# ============================================================================
# Extension Registry
# ============================================================================

class ExtensionRegistry:
    """
    Registry for managing service extensions across all verticals.
    
    The registry tracks available extensions, their priorities, and
    dependencies to ensure proper loading order and compatibility.
    """
    
    _instance: Optional['ExtensionRegistry'] = None
    _extensions: Dict[str, Dict[str, Any]] = {}
    _extension_points: Dict[str, List[str]] = {}
    
    def __new__(cls) -> 'ExtensionRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._extensions = {}
            self._extension_points = {}
            self._initialized = True
    
    def register_extension(
        self,
        service_name: str,
        extension_point: str,
        extension_class: Type,
        priority: int = 50,
        config: Optional[Dict[str, Any]] = None,
        dependencies: Optional[List[str]] = None
    ) -> bool:
        """
        Register a service extension.
        
        Args:
            service_name: Name of the service being extended
            extension_point: Specific extension point within the service
            extension_class: Class implementing the extension
            priority: Loading priority (higher loads first)
            config: Extension configuration
            dependencies: Other extensions this depends on
            
        Returns:
            True if registration successful
        """
        key = f"{service_name}.{extension_point}"
        
        self._extensions[key] = {
            'class': extension_class,
            'priority': priority,
            'config': config or {},
            'dependencies': dependencies or [],
            'service_name': service_name,
            'extension_point': extension_point
        }
        
        if service_name not in self._extension_points:
            self._extension_points[service_name] = []
        if extension_point not in self._extension_points[service_name]:
            self._extension_points[service_name].append(extension_point)
        
        logger.info(f"Registered extension: {key} with priority {priority}")
        return True
    
    def get_extension(
        self,
        service_name: str,
        extension_point: str,
        vertical_id: Optional[str] = None
    ) -> Optional[Type]:
        """
        Get the highest-priority extension for a service extension point.
        
        Args:
            service_name: Name of the service
            extension_point: Extension point name
            vertical_id: Optional vertical to filter by
            
        Returns:
            Extension class or None if not found
        """
        key = f"{service_name}.{extension_point}"
        
        if key not in self._extensions:
            return None
        
        ext_info = self._extensions[key]
        return ext_info['class']
    
    def get_all_extensions(self, service_name: str) -> Dict[str, Type]:
        """
        Get all extensions for a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Dictionary of extension points to extension classes
        """
        result = {}
        for key, ext_info in self._extensions.items():
            if ext_info['service_name'] == service_name:
                result[ext_info['extension_point']] = ext_info['class']
        return result
    
    def get_extension_points(self, service_name: str) -> List[str]:
        """
        Get all extension points for a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            List of extension point names
        """
        return self._extension_points.get(service_name, [])
    
    def list_registered(self) -> List[Dict[str, Any]]:
        """
        List all registered extensions.
        
        Returns:
            List of extension information dictionaries
        """
        return [
            {
                'service': info['service_name'],
                'extension_point': info['extension_point'],
                'priority': info['priority'],
                'dependencies': info['dependencies']
            }
            for info in self._extensions.values()
        ]


def get_extension_registry() -> ExtensionRegistry:
    """Get the global extension registry instance."""
    return ExtensionRegistry()


# ============================================================================
# Base Extension Classes
# ============================================================================

class ServiceExtension(ABC):
    """
    Base class for all service extensions.
    
    Extensions provide domain-specific functionality for base services.
    They can override, extend, or completely replace base functionality.
    """
    
    # Extension metadata
    extension_id: str = ""
    extension_version: str = "1.0.0"
    priority: int = 50
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the extension.
        
        Args:
            config: Extension configuration
        """
        self.config = config or {}
        self._initialize()
    
    def _initialize(self) -> None:
        """Override for initialization logic."""
        pass
    
    def get_capabilities(self) -> List[str]:
        """
        Get list of capabilities provided by this extension.
        
        Returns:
            List of capability identifiers
        """
        return []
    
    def validate_config(self) -> bool:
        """
        Validate extension configuration.
        
        Returns:
            True if configuration is valid
        """
        return True
    
    def get_dependencies(self) -> List[str]:
        """
        Get list of extension dependencies.
        
        Returns:
            List of dependency keys
        """
        return []


@dataclass
class ExtensionContext:
    """Context passed to extensions during execution."""
    
    vertical_id: str = ""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    locale: str = "en"
    config: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Concept Service Extensions
# ============================================================================

class ConceptServiceExtension(ServiceExtension):
    """
    Base class for concept service extensions.
    
    Extensions can add domain-specific concept processing,
    validation rules, and relationship handling.
    """
    
    @abstractmethod
    def process_concept(self, concept: Dict[str, Any], context: ExtensionContext) -> Dict[str, Any]:
        """
        Process a concept with domain-specific logic.
        
        Args:
            concept: The concept to process
            context: Execution context
            
        Returns:
            Processed concept
        """
        pass
    
    @abstractmethod
    def validate_concept(self, concept: Dict[str, Any]) -> List[str]:
        """
        Validate a concept against domain rules.
        
        Args:
            concept: The concept to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        pass
    
    @abstractmethod
    def get_related_concepts(
        self,
        concept_id: str,
        relationship_type: str
    ) -> List[str]:
        """
        Get related concepts with domain-specific relationships.
        
        Args:
            concept_id: The source concept
            relationship_type: Type of relationship
            
        Returns:
            List of related concept IDs
        """
        pass


class MathConceptServiceExtension(ConceptServiceExtension):
    """MathVerse concept service extension."""
    
    extension_id = "math-concept-service"
    priority = 90
    
    def process_concept(self, concept: Dict[str, Any], context: ExtensionContext) -> Dict[str, Any]:
        # Add math-specific processing
        if 'formula' in concept:
            concept['rendered_formula'] = self._render_formula(concept['formula'])
        return concept
    
    def validate_concept(self, concept: Dict[str, Any]) -> List[str]:
        errors = []
        if concept.get('domain') == 'math':
            if 'difficulty_score' in concept:
                if not 0 <= concept['difficulty_score'] <= 1:
                    errors.append("Difficulty score must be between 0 and 1")
        return errors
    
    def get_related_concepts(
        self,
        concept_id: str,
        relationship_type: str
    ) -> List[str]:
        # Math-specific relationship logic
        return []
    
    def _render_formula(self, formula: str) -> str:
        """Render formula for display."""
        return f"$${formula}$$"


class PhysicsConceptServiceExtension(ConceptServiceExtension):
    """PhysicsVerse concept service extension."""
    
    extension_id = "physics-concept-service"
    priority = 85
    
    def process_concept(self, concept: Dict[str, Any], context: ExtensionContext) -> Dict[str, Any]:
        # Add physics-specific processing
        if 'equation' in concept:
            concept['equation_visualization'] = self._create_equation_viz(concept['equation'])
        return concept
    
    def validate_concept(self, concept: Dict[str, Any]) -> List[str]:
        errors = []
        if concept.get('domain') == 'physics':
            if 'units' not in concept:
                errors.append("Physics concepts must have units defined")
        return errors
    
    def get_related_concepts(
        self,
        concept_id: str,
        relationship_type: str
    ) -> List[str]:
        # Physics-specific relationship logic
        return []
    
    def _create_equation_viz(self, equation: str) -> Dict[str, Any]:
        """Create visualization data for an equation."""
        return {"type": "equation", "content": equation}


class ChemistryConceptServiceExtension(ConceptServiceExtension):
    """ChemVerse concept service extension."""
    
    extension_id = "chemistry-concept-service"
    priority = 85
    
    def process_concept(self, concept: Dict[str, Any], context: ExtensionContext) -> Dict[str, Any]:
        # Add chemistry-specific processing
        if 'molecule' in concept:
            concept['molecule_3d'] = self._create_molecule_data(concept['molecule'])
        return concept
    
    def validate_concept(self, concept: Dict[str, Any]) -> List[str]:
        errors = []
        if concept.get('domain') == 'chemistry':
            if 'formula' in concept:
                if not self._validate_chemical_formula(concept['formula']):
                    errors.append("Invalid chemical formula format")
        return errors
    
    def get_related_concepts(
        self,
        concept_id: str,
        relationship_type: str
    ) -> List[str]:
        # Chemistry-specific relationship logic
        return []
    
    def _validate_chemical_formula(self, formula: str) -> bool:
        """Validate chemical formula format."""
        import re
        return bool(re.match(r'^[A-Z][a-z]?\d*$', formula))
    
    def _create_molecule_data(self, molecule: str) -> Dict[str, Any]:
        """Create 3D molecule data."""
        return {"type": "molecule", "formula": molecule}


# ============================================================================
# Visual Service Extensions
# ============================================================================

class VisualServiceExtension(ServiceExtension):
    """
    Base class for visual service extensions.
    
    Extensions can add domain-specific visualization types,
    rendering logic, and style customization.
    """
    
    @abstractmethod
    def get_visualization_types(self) -> List[str]:
        """
        Get list of visualization types provided by this extension.
        
        Returns:
            List of visualization type identifiers
        """
        pass
    
    @abstractmethod
    def render_visualization(
        self,
        visual_type: str,
        data: Dict[str, Any],
        context: ExtensionContext
    ) -> Dict[str, Any]:
        """
        Render a visualization of the specified type.
        
        Args:
            visual_type: Type of visualization
            data: Data to visualize
            context: Execution context
            
        Returns:
            Rendered visualization data
        """
        pass
    
    @abstractmethod
    def get_default_style(self, visual_type: str) -> Dict[str, Any]:
        """
        Get default styling for a visualization type.
        
        Args:
            visual_type: Type of visualization
            
        Returns:
            Style configuration
        """
        pass


class AlgorithmVisualServiceExtension(VisualServiceExtension):
    """AlgoVerse visual service extension."""
    
    extension_id = "algorithm-visual-service"
    priority = 85
    
    def get_visualization_types(self) -> List[str]:
        return [
            "flowchart",
            "array-layout",
            "node-diagram",
            "tree-layout",
            "sort-animation",
            "search-animation",
            "call-stack",
            "complexity-chart"
        ]
    
    def render_visualization(
        self,
        visual_type: str,
        data: Dict[str, Any],
        context: ExtensionContext
    ) -> Dict[str, Any]:
        # Algorithm-specific rendering logic
        if visual_type == "flowchart":
            return self._render_flowchart(data)
        elif visual_type == "sort-animation":
            return self._render_sort_animation(data)
        return {}
    
    def get_default_style(self, visual_type: str) -> Dict[str, Any]:
        styles = {
            "flowchart": {
                "shape": "rounded",
                "color_scheme": "algorithm-light",
                "font_size": 14
            },
            "sort-animation": {
                "speed": 1.0,
                "color_highlight": "#7c3aed",
                "color_swap": "#ef4444"
            }
        }
        return styles.get(visual_type, {})
    
    def _render_flowchart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render flowchart visualization."""
        return {"type": "flowchart", "nodes": data.get("steps", [])}
    
    def _render_sort_animation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render sorting animation data."""
        return {"type": "sort-animation", "array": data.get("array", [])}


# ============================================================================
# Animation Service Extensions
# ============================================================================

class AnimationServiceExtension(ServiceExtension):
    """
    Base class for animation service extensions.
    
    Extensions can add domain-specific animation types,
    timing functions, and transition effects.
    """
    
    @abstractmethod
    def get_animation_presets(self) -> Dict[str, Dict[str, Any]]:
        """
        Get animation presets provided by this extension.
        
        Returns:
            Dictionary of preset ID to configuration
        """
        pass
    
    @abstractmethod
    def create_animation(
        self,
        animation_type: str,
        params: Dict[str, Any],
        context: ExtensionContext
    ) -> Dict[str, Any]:
        """
        Create an animation of the specified type.
        
        Args:
            animation_type: Type of animation
            params: Animation parameters
            context: Execution context
            
        Returns:
            Animation configuration
        """
        pass
    
    @abstractmethod
    def get_transition(
        self,
        from_state: Dict[str, Any],
        to_state: Dict[str, Any],
        animation_type: str
    ) -> Dict[str, Any]:
        """
        Get transition configuration between states.
        
        Args:
            from_state: Starting state
            to_state: Ending state
            animation_type: Type of transition
            
        Returns:
            Transition configuration
        """
        pass


class FinanceAnimationServiceExtension(AnimationServiceExtension):
    """FinVerse animation service extension."""
    
    extension_id = "finance-animation-service"
    priority = 85
    
    def get_animation_presets(self) -> Dict[str, Dict[str, Any]]:
        return {
            "growth-reveal": {
                "duration_ms": 4000,
                "easing": "ease-in-out",
                "type": "reveal"
            },
            "projection-transition": {
                "duration_ms": 3000,
                "easing": "ease-in-out",
                "type": "transition"
            },
            "scenario-comparison": {
                "duration_ms": 5000,
                "easing": "ease-in-out",
                "type": "comparison"
            }
        }
    
    def create_animation(
        self,
        animation_type: str,
        params: Dict[str, Any],
        context: ExtensionContext
    ) -> Dict[str, Any]:
        if animation_type == "growth-reveal":
            return self._create_growth_reveal(params)
        elif animation_type == "projection-transition":
            return self._create_projection_transition(params)
        return {}
    
    def get_transition(
        self,
        from_state: Dict[str, Any],
        to_state: Dict[str, Any],
        animation_type: str
    ) -> Dict[str, Any]:
        return {
            "from": from_state,
            "to": to_state,
            "type": animation_type,
            "duration_ms": 1000
        }
    
    def _create_growth_reveal(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create growth reveal animation."""
        return {
            "type": "growth-reveal",
            "data_points": params.get("data", []),
            "duration_ms": 4000
        }
    
    def _create_projection_transition(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create projection transition animation."""
        return {
            "type": "projection-transition",
            "historical": params.get("historical", []),
            "projected": params.get("projected", []),
            "duration_ms": 3000
        }


# ============================================================================
# Reasoning Engine Extensions
# ============================================================================

class ReasoningEngineExtension(ServiceExtension):
    """
    Base class for reasoning engine extensions.
    
    Extensions can add domain-specific reasoning strategies,
    step decomposition patterns, and explanation templates.
    """
    
    @abstractmethod
    def get_reasoning_strategies(self) -> List[str]:
        """
        Get reasoning strategies provided by this extension.
        
        Returns:
            List of strategy identifiers
        """
        pass
    
    @abstractmethod
    def decompose_step(
        self,
        step: Dict[str, Any],
        context: ExtensionContext
    ) -> List[Dict[str, Any]]:
        """
        Decompose a reasoning step into sub-steps.
        
        Args:
            step: The step to decompose
            context: Execution context
            
        Returns:
            List of sub-steps
        """
        pass
    
    @abstractmethod
    def generate_explanation(
        self,
        reasoning_type: str,
        data: Dict[str, Any],
        context: ExtensionContext
    ) -> Dict[str, Any]:
        """
        Generate an explanation for a reasoning process.
        
        Args:
            reasoning_type: Type of reasoning
            data: Reasoning data
            context: Execution context
            
        Returns:
            Explanation data
        """
        pass


class MathReasoningEngineExtension(ReasoningEngineExtension):
    """MathVerse reasoning engine extension."""
    
    extension_id = "math-reasoning-engine"
    priority = 90
    
    def get_reasoning_strategies(self) -> List[str]:
        return [
            "direct-proof",
            "proof-by-induction",
            "proof-by-contradiction",
            "algebraic-manipulation",
            "constructive-proof"
        ]
    
    def decompose_step(
        self,
        step: Dict[str, Any],
        context: ExtensionContext
    ) -> List[Dict[str, Any]]:
        if step.get("type") == "proof-step":
            return self._decompose_proof_step(step)
        return [step]
    
    def generate_explanation(
        self,
        reasoning_type: str,
        data: Dict[str, Any],
        context: ExtensionContext
    ) -> Dict[str, Any]:
        templates = {
            "direct-proof": self._template_direct_proof,
            "proof-by-induction": self._template_induction
        }
        
        template = templates.get(reasoning_type, self._template_default)
        return template(data)
    
    def _decompose_proof_step(self, step: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a proof step."""
        return [
            {"type": "assumption", "content": step.get("assumption", "")},
            {"type": "derivation", "content": step.get("derivation", "")},
            {"type": "conclusion", "content": step.get("conclusion", "")}
        ]
    
    def _template_direct_proof(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "direct-proof",
            "steps": data.get("steps", []),
            "explanation": "Starting from given assumptions, we derive the conclusion step by step."
        }
    
    def _template_induction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "induction",
            "base_case": data.get("base_case", ""),
            "inductive_step": data.get("inductive_step", ""),
            "explanation": "We prove the base case, then show that if true for n, it's true for n+1."
        }
    
    def _template_default(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": reasoning_type,
            "explanation": "This reasoning follows standard methodology."
        }


# ============================================================================
# Vertical Loader
# ============================================================================

class VerticalLoader:
    """
    Loads and initializes vertical configurations.
    
    The loader processes vertical configuration files, registers
    service extensions, and prepares visualization templates.
    """
    
    def __init__(self):
        self._verticals: Dict[str, Dict[str, Any]] = {}
        self._registry = get_extension_registry()
    
    def load_vertical(self, config_path: str) -> bool:
        """
        Load a vertical configuration from file.
        
        Args:
            config_path: Path to vertical configuration file
            
        Returns:
            True if loading successful
        """
        import json
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            vertical_id = config['id']
            self._verticals[vertical_id] = config
            
            # Register service extensions
            self._register_extensions(vertical_id, config)
            
            logger.info(f"Loaded vertical: {vertical_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to load vertical from {config_path}: {e}")
            return False
    
    def _register_extensions(
        self,
        vertical_id: str,
        config: Dict[str, Any]
    ) -> None:
        """Register service extensions from vertical configuration."""
        extensions = config.get('service_extensions', {})
        
        for service_name, ext_config in extensions.items():
            class_path = ext_config.get('class_path', '')
            module = ext_config.get('module', '')
            priority = ext_config.get('priority', 50)
            
            # Extract class name from path
            class_name = class_path.split('.')[-1]
            
            # Import and register
            try:
                # This would dynamically import the class in a real implementation
                extension_point = f"{vertical_id}.{service_name}"
                logger.info(f"Would register: {extension_point} -> {class_path}")
            except Exception as e:
                logger.warning(f"Could not register extension {class_path}: {e}")
    
    def get_vertical(self, vertical_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a loaded vertical configuration.
        
        Args:
            vertical_id: The vertical identifier
            
        Returns:
            Vertical configuration or None
        """
        return self._verticals.get(vertical_id)
    
    def list_verticals(self) -> List[str]:
        """
        List all loaded verticals.
        
        Returns:
            List of vertical identifiers
        """
        return list(self._verticals.keys())


def get_vertical_loader() -> VerticalLoader:
    """Get the vertical loader instance."""
    return VerticalLoader()
