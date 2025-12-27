"""
Extended Visual Metadata Models for Vertical Platform Features

This module extends the base visual_meta.py with domain-specific visualization
types for all verticals: MathVerse, PhysicsVerse, ChemVerse, AlgoVerse, and FinVerse.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum
import uuid


# ============================================================================
# Domain Enums
# ============================================================================

class MathVisualType(str, Enum):
    """Math-specific visualization types"""
    EQUATION_LAYOUT = "equation-layout"
    PARABOLA_ANIMATION = "parabola-animation"
    GRAPH_FUNCTION = "graph-function"
    PROOF_STEP = "proof-step"
    MATRIX_TRANSFORMATION = "matrix-transformation"
    RIEMANN_SUM = "riemann-sum"
    DISTRIBUTION_BAR = "distribution-bar"
    LOGIC_FLOW = "logic-flow"
    EXPONENTIAL_GROWTH = "exponential-growth"
    POLYNOMIAL_GRAPH = "polynomial-graph"
    TRIGONOMETRIC = "trigonometric"
    CALCULUS_ANIMATION = "calculus-animation"


class PhysicsVisualType(str, Enum):
    """Physics-specific visualization types"""
    MOTION_TIMELINE = "motion-timeline"
    TRAJECTORY_ANIMATION = "trajectory-animation"
    FORCE_DIAGRAM = "force-diagram"
    VECTOR_FIELD = "vector-field"
    RAY_DIAGRAM = "ray-diagram"
    LENS_RAY_TRACE = "lens-ray-trace"
    WAVE_INTERFERENCE = "wave-interference"
    ENERGY_BAR = "energy-bar"
    FIELD_LINE_3D = "field-line-3d"
    PARTICLE_SIMULATION = "particle-simulation"
    CIRCUIT_DIAGRAM = "circuit-diagram"
    WAVE_PROPAGATION = "wave-propagation"


class ChemistryVisualType(str, Enum):
    """Chemistry-specific visualization types"""
    ATOM_MODEL = "atom-model"
    MOLECULE_3D = "molecule-3d"
    BALL_STICK = "ball-stick"
    SPACE_FILL = "space-fill"
    ORBITAL_3D = "orbital-3d"
    ORBITAL_DIAGRAM = "orbital-diagram"
    REACTION_ANIMATION = "reaction-animation"
    MECHANISM_FLOW = "mechanism-flow"
    ENERGY_PROFILE = "energy-profile"
    VSEPR_MODEL = "vsepr-model"
    LEWIS_STRUCTURE = "lewis-structure"
    CRYSTAL_3D = "crystal-3d"
    ELECTRON_TRANSFER = "electron-transfer"


class AlgorithmVisualType(str, Enum):
    """Algorithm-specific visualization types"""
    FLOWCHART = "flowchart"
    ARRAY_LAYOUT = "array-layout"
    NODE_DIAGRAM = "node-diagram"
    TREE_LAYOUT = "tree-layout"
    SORT_ANIMATION = "sort-animation"
    SEARCH_ANIMATION = "search-animation"
    GRAPH_LAYOUT = "graph-layout"
    CALL_STACK = "call-stack"
    COMPLEXITY_CHART = "complexity-chart"
    CODE_HIGHLIGHT = "code-highlight"
    STEP_DIAGRAM = "step-diagram"
    DFS_ANIMATION = "dfs-animation"
    BFS_ANIMATION = "bfs-animation"


class FinanceVisualType(str, Enum):
    """Finance-specific visualization types"""
    TIMELINE_CASHFLOW = "timeline-cashflow"
    COMPOUND_GROWTH = "compound-growth"
    STOCK_CHART = "stock-chart"
    YIELD_CURVE = "yield-curve"
    RISK_SCATTER = "risk-scatter"
    FRONTIER_CURVE = "frontier-curve"
    DCF_TIMELINE = "dcf-timeline"
    SCENARIO_CHART = "scenario-chart"
    VAR_DISTRIBUTION = "var-distribution"
    CASHFLOW_CHART = "cashflow-chart"
    SUPPLY_DEMAND_GRAPH = "supply-demand-graph"
    CORRELATION_PLOT = "correlation-plot"


class VerticalDomain(str, Enum):
    """Supported vertical domains"""
    MATH = "math"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    ALGORITHM = "algorithm"
    FINANCE = "finance"


class AnimationStyle(str, Enum):
    """Animation style presets for visualizations"""
    SMOOTH = "smooth"
    STEP_BY_STEP = "step-by-step"
    FAST_FORWARD = "fast-forward"
    PAUSABLE = "pausable"
    INTERACTIVE = "interactive"
    REAL_TIME = "real-time"


class ColorSchemeType(str, Enum):
    """Color scheme categories"""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high-contrast"
    COLORBLIND_FRIENDLY = "colorblind-friendly"
    DOMAIN_SPECIFIC = "domain-specific"


# ============================================================================
# Extended Asset Models
# ============================================================================

class VisualizationTemplate(BaseModel):
    """
    Defines a visualization template that can be customized for different domains.
    
    Templates provide the structure and behavior for visualizations, with
    customization hooks for domain-specific adaptations.
    """
    
    id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Display name of the template")
    description: Optional[str] = Field(None, description="Template description")
    
    # Template categorization
    domain: VerticalDomain = Field(..., description="Primary domain for this template")
    category: str = Field(..., description="Visualization category")
    
    # Technical specifications
    renderer: str = Field(..., description="Renderer identifier")
    output_format: str = Field(default="canvas", description="Output format (canvas, svg, webgl)")
    
    # Customization hooks
    customization_points: Dict[str, Any] = Field(
        default_factory=dict,
        description="Points of customization in the template"
    )
    
    # Style presets
    default_animation_style: AnimationStyle = Field(
        default=AnimationStyle.SMOOTH,
        description="Default animation style"
    )
    
    # Layout configuration
    aspect_ratio: Optional[str] = Field(None, description="Preferred aspect ratio (e.g., '16:9')")
    responsive_breakpoints: List[int] = Field(
        default_factory=lambda: [320, 768, 1024, 1920],
        description="Responsive breakpoints"
    )
    
    # Capabilities
    capabilities: List[str] = Field(
        default_factory=list,
        description="List of supported capabilities"
    )
    
    # Domain-specific configuration
    domain_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Domain-specific configuration"
    )
    
    # Metadata
    version: str = Field(default="1.0.0", description="Template version")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class DomainColorScheme(BaseModel):
    """
    Defines color schemes for visualizations, with domain-specific adaptations.
    """
    
    id: str = Field(..., description="Unique scheme identifier")
    name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Scheme description")
    
    # Domain applicability
    domain: VerticalDomain = Field(..., description="Primary domain")
    theme_type: ColorSchemeType = Field(..., description="Theme category")
    
    # Color definitions
    colors: Dict[str, str] = Field(..., description="Color definitions (hex codes)")
    
    # Semantic colors
    semantic_colors: Dict[str, str] = Field(
        default_factory=dict,
        description="Semantic color mappings (positive, negative, neutral, etc.)"
    )
    
    # Domain-specific adaptations
    domain_overrides: Dict[str, Dict[str, str]] = Field(
        default_factory=dict,
        description="Domain-specific color overrides"
    )
    
    # Accessibility
    contrast_ratio: Optional[float] = Field(
        None,
        ge=1.0,
        le=21.0,
        description="WCAG contrast ratio"
    )
    is_accessible: bool = Field(default=True, description="Meets accessibility standards")


class VisualStylePreset(BaseModel):
    """
    Pre-defined visual style presets for different educational contexts.
    """
    
    id: str = Field(..., description="Unique preset identifier")
    name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Preset description")
    
    # Style components
    color_scheme_id: str = Field(..., description="Associated color scheme")
    typography: Dict[str, Any] = Field(default_factory=dict, description="Typography settings")
    spacing: Dict[str, Any] = Field(default_factory=dict, description="Spacing settings")
    shapes: Dict[str, Any] = Field(default_factory=dict, description="Shape definitions")
    
    # Animation defaults
    animation_defaults: Dict[str, Any] = Field(
        default_factory=dict,
        description="Default animation settings"
    )
    
    # Domain
    domain: Optional[VerticalDomain] = Field(None, description="Target domain")
    use_case: Optional[str] = Field(None, description="Use case context")


# ============================================================================
# Service Extension Models
# ============================================================================

class ServiceExtensionConfig(BaseModel):
    """
    Configuration for extending base services with domain-specific functionality.
    """
    
    class_path: str = Field(..., description="Python class path for the extension")
    module: str = Field(..., description="Module containing the extension class")
    
    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict, description="Extension configuration")
    
    # Lifecycle
    priority: int = Field(default=50, ge=0, le=100, description="Loading priority")
    dependencies: List[str] = Field(default_factory=list, description="Extension dependencies")
    
    # Status
    is_active: bool = Field(default=True, description="Whether extension is active")
    version: str = Field(default="1.0.0", description="Extension version")


class ServiceExtensionPoint(BaseModel):
    """
    Defines where and how base services can be extended.
    """
    
    service_name: str = Field(..., description="Name of the service being extended")
    extension_point: str = Field(..., description="Specific extension point within the service")
    description: str = Field(..., description="Description of the extension point")
    
    # Extension requirements
    required_capabilities: List[str] = Field(
        default_factory=list,
        description="Required capabilities for extensions"
    )
    
    # Default implementation
    default_extension: Optional[ServiceExtensionConfig] = Field(
        None,
        description="Default extension if none specified"
    )
    
    # Available extensions
    available_extensions: Dict[str, ServiceExtensionConfig] = Field(
        default_factory=dict,
        description="Available extension implementations"
    )


# ============================================================================
# Vertical Configuration Models
# ============================================================================

class VerticalConfigMetadata(BaseModel):
    """Metadata for vertical configurations"""
    
    author: str = Field(default="VisualVerse Platform", description="Configuration author")
    created_at: datetime = Field(default_factory=datetime.now, description="Created timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Updated timestamp")
    tags: List[str] = Field(default_factory=list, description="Configuration tags")
    license: str = Field(default="proprietary", description="License type")
    version: str = Field(default="1.0.0", description="Configuration version")


class VerticalDomainConfig(BaseModel):
    """Configuration for a knowledge domain within a vertical"""
    
    id: str = Field(..., description="Domain identifier")
    name: str = Field(..., description="Domain display name")
    description: Optional[str] = Field(None, description="Domain description")
    
    # Topics within this domain
    topics: List[Dict[str, Any]] = Field(default_factory=list, description="Domain topics")
    
    # Target audience
    target_audience: Dict[str, Any] = Field(
        default_factory=dict,
        description="Target audience specification
    )
    
    # Prerequisites
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisite domains")


class VerticalConfig(BaseModel):
    """
    Complete configuration for a vertical platform.
    
    This model encapsulates all configuration needed to enable a vertical,
    including domains, visualization types, service extensions, and templates.
    """
    
    # Identification
    id: str = Field(..., description="Vertical identifier (kebab-case)")
    name: str = Field(..., description="Vertical display name")
    code: str = Field(..., description="Vertical code (CamelCase)")
    version: str = Field(default="1.0.0", description="Configuration version")
    
    # Description
    description: str = Field(..., description="Vertical description")
    engine_version: str = Field(default="1.0.0", description="Required engine version")
    
    # Domain configurations
    domains: List[VerticalDomainConfig] = Field(
        default_factory=list,
        description="Knowledge domains covered"
    )
    
    # Visualization types specific to this vertical
    visualization_types: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Domain-specific visualization types"
    )
    
    # Service extensions
    service_extensions: Dict[str, ServiceExtensionConfig] = Field(
        default_factory=dict,
        description="Service extensions"
    )
    
    # Visualization templates
    visualization_templates: Dict[str, Any] = Field(
        default_factory=dict,
        description="Visualization template configuration"
    )
    
    # Curriculum templates
    curriculum_templates: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Curriculum templates"
    )
    
    # Metadata
    metadata: VerticalConfigMetadata = Field(
        default_factory=VerticalConfigMetadata,
        description="Configuration metadata"
    )


# ============================================================================
# Feature Toggle Models
# ============================================================================

class FeatureToggle(BaseModel):
    """Feature toggle for vertical-specific features"""
    
    feature_id: str = Field(..., description="Unique feature identifier")
    name: str = Field(..., description="Feature name")
    description: Optional[str] = Field(None, description="Feature description")
    
    # Toggle status
    is_enabled: bool = Field(default=False, description="Whether feature is enabled")
    rollout_percentage: int = Field(default=0, ge=0, le=100, description="Rollout percentage")
    
    # Targeting
    vertical_ids: List[str] = Field(default_factory=list, description="Applicable verticals")
    user_segments: List[str] = Field(default_factory=list, description="Target user segments")
    
    # Dependencies
    depends_on: List[str] = Field(default_factory=list, description="Dependent features")
    
    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict, description="Feature configuration")


# ============================================================================
# Layout Pattern Models
# ============================================================================

class LayoutPattern(BaseModel):
    """
    Defines a layout pattern for visualizations.
    """
    
    id: str = Field(..., description="Unique pattern identifier")
    name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Pattern description")
    
    # Layout specification
    template_id: str = Field(..., description="Associated template ID")
    aspect_ratio: str = Field(default="16:9", description="Aspect ratio")
    
    # Breakpoints
    responsive_breakpoints: List[int] = Field(
        default_factory=lambda: [320, 768, 1024, 1920],
        description="Responsive breakpoints"
    )
    
    # Components
    components: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Layout components"
    )
    
    # Domain
    domain: Optional[VerticalDomain] = Field(None, description="Target domain")


# ============================================================================
# Utility Functions
# ============================================================================

def get_domain_visual_types(domain: VerticalDomain) -> List[str]:
    """
    Get all visualization types for a specific domain.
    
    Args:
        domain: The vertical domain
        
    Returns:
        List of visualization type identifiers
    """
    type_mapping = {
        VerticalDomain.MATH: [e.value for e in MathVisualType],
        VerticalDomain.PHYSICS: [e.value for e in PhysicsVisualType],
        VerticalDomain.CHEMISTRY: [e.value for e in ChemistryVisualType],
        VerticalDomain.ALGORITHM: [e.value for e in AlgorithmVisualType],
        VerticalDomain.FINANCE: [e.value for e in FinanceVisualType],
    }
    return type_mapping.get(domain, [])


def create_domain_color_scheme(
    domain: VerticalDomain,
    theme: ColorSchemeType,
    base_colors: Dict[str, str]
) -> DomainColorScheme:
    """
    Create a color scheme for a specific domain.
    
    Args:
        domain: The vertical domain
        theme: The color theme type
        base_colors: Base color definitions
        
    Returns:
        Configured DomainColorScheme
    """
    # Domain-specific color adaptations
    domain_overrides = {
        VerticalDomain.MATH: {
            "primary": base_colors.get("primary", "#2563eb"),
            "secondary": base_colors.get("secondary", "#3b82f6"),
            "accent": base_colors.get("accent", "#f59e0b"),
        },
        VerticalDomain.PHYSICS: {
            "primary": base_colors.get("primary", "#dc2626"),
            "secondary": base_colors.get("secondary", "#ef4444"),
            "accent": base_colors.get("accent", "#3b82f6"),
        },
        VerticalDomain.CHEMISTRY: {
            "primary": base_colors.get("primary", "#059669"),
            "secondary": base_colors.get("secondary", "#10b981"),
            "accent": base_colors.get("accent", "#8b5cf6"),
        },
        VerticalDomain.ALGORITHM: {
            "primary": base_colors.get("primary", "#7c3aed"),
            "secondary": base_colors.get("secondary", "#8b5cf6"),
            "accent": base_colors.get("accent", "#06b6d4"),
        },
        VerticalDomain.FINANCE: {
            "primary": base_colors.get("primary", "#0d6efd"),
            "secondary": base_colors.get("secondary", "#198754"),
            "accent": base_colors.get("accent", "#dc3545"),
        },
    }
    
    return DomainColorScheme(
        id=f"{domain.value}-{theme.value}",
        name=f"{domain.value.title()} {theme.title()} Scheme",
        domain=domain,
        theme_type=theme,
        colors=base_colors,
        domain_overrides=domain_overrides
    )


def validate_visualization_config(
    visual_type: str,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate and normalize visualization configuration.
    
    Args:
        visual_type: The visualization type
        config: Configuration to validate
        
    Returns:
        Validated and normalized configuration
    """
    # Default configuration for each visualization type
    defaults = {
        "duration_ms": 3000,
        "easing": "ease-in-out",
        "responsive": True,
        "interactive": False,
        "animated": True,
    }
    
    # Merge defaults with provided config
    validated = {**defaults, **config}
    
    # Type-specific validations
    if "animation" in visual_type:
        if "duration_ms" not in config:
            validated["duration_ms"] = 3000
    
    if "chart" in visual_type:
        validated["interactive"] = True
    
    if "3d" in visual_type:
        validated["renderer"] = "webgl"
    
    return validated
