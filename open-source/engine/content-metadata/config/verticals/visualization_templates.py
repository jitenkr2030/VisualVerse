"""
Visualization Template Framework for Vertical Platform Features

This module provides the framework for defining, customizing, and rendering
visualization templates across different verticals with domain-specific hooks.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json


# ============================================================================
# Template Types
# ============================================================================

class TemplateCategory(str, Enum):
    """Categories of visualization templates"""
    DIAGRAM = "diagram"
    CHART = "chart"
    ANIMATION = "animation"
    INTERACTIVE = "interactive"
    SIMULATION = "simulation"
    FLOWCHART = "flowchart"
    GRAPH = "graph"
    THREE_D = "3d-model"


class CustomizationScope(str, Enum):
    """Scope of customization available for a template"""
    FULL = "full"           # All aspects can be customized
    LIMITED = "limited"     # Only specific aspects can be customized
    FIXED = "fixed"         # Template is fixed, no customization


@dataclass
class CustomizationHook:
    """
    Defines a point of customization in a visualization template.
    
    Customization hooks allow verticals to inject domain-specific
    behavior while maintaining template structure.
    """
    hook_id: str
    name: str
    description: str
    scope: CustomizationScope
    default_value: Any
    allowed_values: Optional[List[Any]] = None
    validator: Optional[Callable[[Any], bool]] = None
    domain_specific: bool = False


@dataclass
class TemplateComponent:
    """
    A component within a visualization template.
    
    Templates are composed of multiple components that can be
    independently customized and rendered.
    """
    component_id: str
    name: str
    component_type: str
    position: Dict[str, int]  # x, y, width, height
    style: Dict[str, Any] = field(default_factory=dict)
    behavior: Dict[str, Any] = field(default_factory=dict)
    children: List['TemplateComponent'] = field(default_factory=list)


@dataclass
class VisualizationTemplate:
    """
    A visualization template definition.
    
    Templates define the structure and behavior for visualizations,
    with customization hooks for domain-specific adaptations.
    """
    template_id: str
    name: str
    category: TemplateCategory
    renderer: str
    
    # Template structure
    components: List[TemplateComponent] = field(default_factory=list)
    layout: Dict[str, Any] = field(default_factory=dict)
    
    # Customization
    customization_hooks: Dict[str, CustomizationHook] = field(default_factory=dict)
    customization_scope: CustomizationScope = CustomizationScope.LIMITED
    
    # Domain
    primary_domain: Optional[str] = None
    supported_domains: List[str] = field(default_factory=list)
    
    # Technical
    output_format: str = "canvas"
    capabilities: List[str] = field(default_factory=list)
    requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    version: str = "1.0.0"
    author: str = "VisualVerse"


# ============================================================================
# Template Registry
# ============================================================================

class TemplateRegistry:
    """
    Registry for managing visualization templates.
    
    The registry tracks available templates, their customization options,
    and domain-specific adaptations.
    """
    
    _instance: Optional['TemplateRegistry'] = None
    _templates: Dict[str, VisualizationTemplate] = {}
    _customizations: Dict[str, Dict[str, Any]] = {}
    
    def __new__(cls) -> 'TemplateRegistry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._templates = {}
            self._customizations = {}
            self._initialized = True
    
    def register_template(self, template: VisualizationTemplate) -> bool:
        """
        Register a visualization template.
        
        Args:
            template: The template to register
            
        Returns:
            True if registration successful
        """
        if template.template_id in self._templates:
            return False
        
        self._templates[template.template_id] = template
        return True
    
    def get_template(self, template_id: str) -> Optional[VisualizationTemplate]:
        """
        Get a template by ID.
        
        Args:
            template_id: The template identifier
            
        Returns:
            Template or None if not found
        """
        return self._templates.get(template_id)
    
    def list_templates(self, domain: Optional[str] = None) -> List[str]:
        """
        List available templates.
        
        Args:
            domain: Optional domain filter
            
        Returns:
            List of template IDs
        """
        if domain is None:
            return list(self._templates.keys())
        
        return [
            tid for tid, t in self._templates.items()
            if domain in t.supported_domains or t.primary_domain == domain
        ]
    
    def register_customization(
        self,
        template_id: str,
        vertical_id: str,
        customizations: Dict[str, Any]
    ) -> bool:
        """
        Register domain-specific customizations for a template.
        
        Args:
            template_id: Template to customize
            vertical_id: Vertical providing customizations
            customizations: Customization values
            
        Returns:
            True if registration successful
        """
        key = f"{template_id}.{vertical_id}"
        self._customizations[key] = customizations
        return True
    
    def get_customization(
        self,
        template_id: str,
        vertical_id: str
    ) -> Dict[str, Any]:
        """
        Get customizations for a template from a vertical.
        
        Args:
            template_id: Template identifier
            vertical_id: Vertical identifier
            
        Returns:
            Customization dictionary or empty
        """
        key = f"{template_id}.{vertical_id}"
        return self._customizations.get(key, {})


def get_template_registry() -> TemplateRegistry:
    """Get the global template registry instance."""
    return TemplateRegistry()


# ============================================================================
# Template Builder
# ============================================================================

class TemplateBuilder:
    """
    Builder for creating visualization templates.
    
    The builder provides a fluent interface for constructing templates
    with proper structure and customization hooks.
    """
    
    def __init__(self, template_id: str, name: str, category: TemplateCategory):
        self._template = VisualizationTemplate(
            template_id=template_id,
            name=name,
            category=category,
            renderer=""
        )
    
    def renderer(self, renderer: str) -> 'TemplateBuilder':
        """Set the renderer for this template."""
        self._template.renderer = renderer
        return self
    
    def output_format(self, output_format: str) -> 'TemplateBuilder':
        """Set the output format."""
        self._template.output_format = output_format
        return self
    
    def primary_domain(self, domain: str) -> 'TemplateBuilder':
        """Set the primary domain."""
        self._template.primary_domain = domain
        self._template.supported_domains.append(domain)
        return self
    
    def add_supported_domain(self, domain: str) -> 'TemplateBuilder':
        """Add a supported domain."""
        if domain not in self._template.supported_domains:
            self._template.supported_domains.append(domain)
        return self
    
    def add_capability(self, capability: str) -> 'TemplateBuilder':
        """Add a capability."""
        if capability not in self._template.capabilities:
            self._template.capabilities.append(capability)
        return self
    
    def add_component(self, component: TemplateComponent) -> 'TemplateBuilder':
        """Add a component to the template."""
        self._template.components.append(component)
        return self
    
    def add_customization_hook(
        self,
        hook_id: str,
        name: str,
        description: str,
        default_value: Any,
        scope: CustomizationScope = CustomizationScope.LIMITED,
        domain_specific: bool = False
    ) -> 'TemplateBuilder':
        """Add a customization hook."""
        hook = CustomizationHook(
            hook_id=hook_id,
            name=name,
            description=description,
            scope=scope,
            default_value=default_value,
            domain_specific=domain_specific
        )
        self._template.customization_hooks[hook_id] = hook
        return self
    
    def layout(self, layout: Dict[str, Any]) -> 'TemplateBuilder':
        """Set the layout configuration."""
        self._template.layout = layout
        return self
    
    def requirements(self, requirements: Dict[str, Any]) -> 'TemplateBuilder':
        """Set template requirements."""
        self._template.requirements = requirements
        return self
    
    def version(self, version: str) -> 'TemplateBuilder':
        """Set template version."""
        self._template.version = version
        return self
    
    def build(self) -> VisualizationTemplate:
        """Build and return the template."""
        return self._template


# ============================================================================
# Template Renderer
# ============================================================================

class TemplateRenderer:
    """
    Renders visualization templates with customization.
    
    The renderer applies customizations from verticals and generates
    the final visualization configuration.
    """
    
    def __init__(self):
        self._registry = get_template_registry()
        self._custom_renders: Dict[str, Callable] = {}
    
    def register_custom_renderer(
        self,
        template_id: str,
        renderer_func: Callable
    ) -> None:
        """
        Register a custom renderer for a template.
        
        Args:
            template_id: Template to render
            renderer_func: Rendering function
        """
        self._custom_renders[template_id] = renderer_func
    
    def render(
        self,
        template_id: str,
        data: Dict[str, Any],
        vertical_id: Optional[str] = None,
        customizations: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Render a template with data and customizations.
        
        Args:
            template_id: Template to render
            data: Data to visualize
            vertical_id: Optional vertical for domain-specific rendering
            customizations: Optional explicit customizations
            
        Returns:
            Rendered visualization configuration
        """
        template = self._registry.get_template(template_id)
        if template is None:
            raise ValueError(f"Template not found: {template_id}")
        
        # Get customizations
        effective_customizations = customizations or {}
        if vertical_id:
            vertical_customizations = self._registry.get_customization(
                template_id, vertical_id
            )
            effective_customizations = {
                **vertical_customizations,
                **effective_customizations
            }
        
        # Check for custom renderer
        if template_id in self._custom_renders:
            return self._custom_renders[template_id](
                template, data, effective_customizations
            )
        
        # Default rendering
        return self._default_render(template, data, effective_customizations)
    
    def _default_render(
        self,
        template: VisualizationTemplate,
        data: Dict[str, Any],
        customizations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Default template rendering logic."""
        return {
            "template_id": template.template_id,
            "renderer": template.renderer,
            "output_format": template.output_format,
            "data": data,
            "customizations": customizations,
            "components": self._render_components(
                template.components,
                data,
                customizations
            ),
            "capabilities": template.capabilities
        }
    
    def _render_components(
        self,
        components: List[TemplateComponent],
        data: Dict[str, Any],
        customizations: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Render template components."""
        rendered = []
        for comp in components:
            rendered.append({
                "component_id": comp.component_id,
                "name": comp.name,
                "type": comp.component_type,
                "style": self._apply_customizations(comp.style, customizations),
                "behavior": comp.behavior,
                "children": self._render_components(
                    comp.children, data, customizations
                )
            })
        return rendered
    
    def _apply_customizations(
        self,
        base_style: Dict[str, Any],
        customizations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply customizations to a style."""
        result = {**base_style}
        for key, value in customizations.items():
            if key in result:
                result[key] = value
        return result


def get_template_renderer() -> TemplateRenderer:
    """Get a template renderer instance."""
    return TemplateRenderer()


# ============================================================================
# Pre-built Templates
# ============================================================================

def create_chart_template(
    template_id: str,
    name: str,
    chart_type: str
) -> VisualizationTemplate:
    """Create a standard chart template."""
    return (
        TemplateBuilder(template_id, name, TemplateCategory.CHART)
        .renderer(chart_type)
        .output_format("canvas")
        .add_capability("interactive")
        .add_capability("responsive")
        .add_customization_hook(
            "colors",
            "Color Scheme",
            "Color scheme for the chart",
            {"primary": "#2563eb", "secondary": "#3b82f6"},
            CustomizationScope.FULL,
            domain_specific=True
        )
        .add_customization_hook(
            "animation",
            "Animation",
            "Chart animation settings",
            {"duration_ms": 1000, "easing": "ease-in-out"},
            CustomizationScope.LIMITED
        )
        .add_customization_hook(
            "labels",
            "Labels",
            "Label configuration",
            {"show": True, "position": "auto"},
            CustomizationScope.LIMITED
        )
        .build()
    )


def create_animation_template(
    template_id: str,
    name: str,
    animation_type: str
) -> VisualizationTemplate:
    """Create a standard animation template."""
    return (
        TemplateBuilder(template_id, name, TemplateCategory.ANIMATION)
        .renderer(animation_type)
        .output_format("webgl")
        .add_capability("animated")
        .add_capability("interactive")
        .add_customization_hook(
            "duration_ms",
            "Duration",
            "Animation duration in milliseconds",
            3000,
            CustomizationScope.LIMITED
        )
        .add_customization_hook(
            "easing",
            "Easing",
            "Animation easing function",
            "ease-in-out",
            CustomizationScope.LIMITED
        )
        .add_customization_hook(
            "style",
            "Visual Style",
            "Animation visual style",
            {"colors": [], "shapes": []},
            CustomizationScope.FULL,
            domain_specific=True
        )
        .build()
    )


def create_diagram_template(
    template_id: str,
    name: str,
    diagram_type: str
) -> VisualizationTemplate:
    """Create a standard diagram template."""
    return (
        TemplateBuilder(template_id, name, TemplateCategory.DIAGRAM)
        .renderer(diagram_type)
        .output_format("svg")
        .add_capability("accessible")
        .add_capability("responsive")
        .add_customization_hook(
            "theme",
            "Theme",
            "Diagram theme",
            "light",
            CustomizationScope.FULL,
            domain_specific=True
        )
        .add_customization_hook(
            "layout",
            "Layout",
            "Diagram layout",
            {"type": "auto", "direction": "horizontal"},
            CustomizationScope.LIMITED
        )
        .build()
    )
