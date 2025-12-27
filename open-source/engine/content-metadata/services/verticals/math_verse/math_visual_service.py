"""
MathVerse Visual Service

This module provides the MathVerse-specific visual service implementation,
extending the base visual service with mathematical domain functionality
including equation rendering, function graphing, proof visualization,
and mathematical diagram generation.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import math
import logging

from ....extensions.service_extension_base import (
    VisualServiceExtension,
    ExtensionContext
)

logger = logging.getLogger(__name__)


@dataclass
class EquationRenderConfig:
    """Configuration for equation rendering."""
    font_size: int = 24
    color: str = "#1e293b"
    background_color: str = "transparent"
    padding: int = 10
    display_mode: bool = True
    LaTeX: bool = True


@dataclass
class GraphConfig:
    """Configuration for function graphing."""
    width: int = 800
    height: int = 600
    x_range: Tuple[float, float] = (-10, 10)
    y_range: Tuple[float, float] = (-10, 10)
    grid: bool = True
    axes: bool = True
    legend: bool = True
    animation: bool = True
    animation_duration: int = 1000
    color_scheme: str = "default"
    points_resolution: int = 200


@dataclass
class ProofVisualConfig:
    """Configuration for proof visualization."""
    style: str = "step-by-step"
    show_connections: bool = True
    animation: bool = True
    color_highlight: str = "#3b82f6"
    color_normal: str = "#64748b"
    color_conclusion: str = "#22c55e"


class MathVerseVisualService:
    """
    MathVerse-specific visual service.
    
    This service handles mathematical visualization including:
    - Equation layout and rendering
    - Function graphing (2D and 3D)
    - Proof step visualization
    - Matrix transformations
    - Probability distribution charts
    - Riemann sum animations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MathVerse visual service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._renderers = self._initialize_renderers()
        self._color_schemes = self._load_color_schemes()
        
    def _initialize_renderers(self) -> Dict[str, Any]:
        """Initialize visualization renderers."""
        return {
            'equation': self._render_equation,
            'graph': self._render_graph,
            'proof': self._render_proof,
            'matrix': self._render_matrix,
            'distribution': self._render_distribution,
            'integral': self._render_integral,
            'logic': self._render_logic_flow,
        }
    
    def _load_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Load available color schemes."""
        return {
            'default': {
                'primary': '#2563eb',
                'secondary': '#3b82f6',
                'accent': '#f59e0b',
                'text': '#1e293b',
                'grid': '#e2e8f0',
                'axis': '#64748b',
                'positive': '#22c55e',
                'negative': '#ef4444',
            },
            'dark': {
                'primary': '#60a5fa',
                'secondary': '#93c5fd',
                'accent': '#fbbf24',
                'text': '#e2e8f0',
                'grid': '#334155',
                'axis': '#94a3b8',
                'positive': '#4ade80',
                'negative': '#f87171',
            },
            'high-contrast': {
                'primary': '#000000',
                'secondary': '#333333',
                'accent': '#ff6600',
                'text': '#000000',
                'grid': '#cccccc',
                'axis': '#000000',
                'positive': '#008000',
                'negative': '#cc0000',
            }
        }
    
    def get_visualization_types(self) -> List[str]:
        """
        Get list of visualization types provided by this service.
        
        Returns:
            List of visualization type identifiers
        """
        return [
            'equation-layout',
            'parabola-animation',
            'graph-function',
            'proof-step',
            'matrix-transformation',
            'riemann-sum',
            'distribution-bar',
            'logic-flow',
            'exponential-growth',
            'polynomial-graph',
            'trigonometric',
            'calculus-animation'
        ]
    
    def render_visualization(
        self,
        visual_type: str,
        data: Dict[str, Any],
        context: Optional[ExtensionContext] = None
    ) -> Dict[str, Any]:
        """
        Render a visualization of the specified type.
        
        Args:
            visual_type: Type of visualization
            data: Data to visualize
            context: Optional execution context
            
        Returns:
            Rendered visualization data
        """
        renderer = self._renderers.get(visual_type)
        
        if renderer is None:
            logger.warning(f"No renderer found for visual type: {visual_type}")
            return {
                'error': f'Unknown visual type: {visual_type}',
                'available_types': self.get_visualization_types()
            }
        
        try:
            return renderer(data)
        except Exception as e:
            logger.error(f"Rendering failed for {visual_type}: {e}")
            return {'error': str(e)}
    
    def get_default_style(self, visual_type: str) -> Dict[str, Any]:
        """
        Get default styling for a visualization type.
        
        Args:
            visual_type: Type of visualization
            
        Returns:
            Style configuration
        """
        style_map = {
            'equation-layout': {
                'font_size': 24,
                'color': '#1e293b',
                'display_mode': True,
                'LaTeX': True,
            },
            'graph-function': {
                'width': 800,
                'height': 600,
                'grid': True,
                'animation': True,
                'color_scheme': 'default',
            },
            'proof-step': {
                'style': 'step-by-step',
                'show_connections': True,
                'animation': True,
                'color_highlight': '#3b82f6',
            },
            'matrix-transformation': {
                'animation': True,
                'show_determinant': True,
                'transform_animation': True,
            },
            'riemann-sum': {
                'animation': True,
                'show_approximation': True,
                'num_rectangles': 10,
            },
            'distribution-bar': {
                'show_mean': True,
                'show_std': True,
                'animation': True,
            },
        }
        
        return style_map.get(visual_type, {})
    
    def render_equation(
        self,
        equation: str,
        variables: Optional[Dict[str, float]] = None,
        config: Optional[EquationRenderConfig] = None
    ) -> Dict[str, Any]:
        """
        Render an equation with optional variable substitution.
        
        Args:
            equation: The equation to render
            variables: Optional variable values for evaluation
            config: Rendering configuration
            
        Returns:
            Rendered equation data
        """
        if config is None:
            config = EquationRenderConfig()
        
        # Process LaTeX
        latex = self._process_latex(equation)
        
        # Calculate if variables provided
        result = None
        if variables:
            result = self._evaluate_equation(equation, variables)
        
        return {
            'type': 'equation',
            'input_equation': equation,
            'latex': latex,
            'rendered': True,
            'config': {
                'font_size': config.font_size,
                'color': config.color,
                'display_mode': config.display_mode,
            },
            'evaluation': result,
            'timestamp': datetime.now().isoformat()
        }
    
    def render_function_graph(
        self,
        functions: List[Dict[str, Any]],
        config: Optional[GraphConfig] = None
    ) -> Dict[str, Any]:
        """
        Render a graph of one or more functions.
        
        Args:
            functions: List of function definitions to plot
            config: Graph configuration
            
        Returns:
            Graph visualization data
        """
        if config is None:
            config = GraphConfig()
        
        colors = self._color_schemes.get(config.color_scheme, self._color_schemes['default'])
        
        # Generate plot points for each function
        plot_data = []
        for i, func in enumerate(functions):
            points = self._generate_function_points(
                func,
                config.x_range,
                config.y_range,
                config.points_resolution
            )
            plot_data.append({
                'function_id': func.get('id', f'func_{i}'),
                'expression': func.get('expression'),
                'points': points,
                'color': func.get('color', colors['primary']),
                'label': func.get('label', f'f{i+1}(x)')
            })
        
        return {
            'type': 'function-graph',
            'config': {
                'width': config.width,
                'height': config.height,
                'x_range': config.x_range,
                'y_range': config.y_range,
                'grid': config.grid,
                'axes': config.axes,
                'legend': config.legend,
            },
            'colors': colors,
            'plot_data': plot_data,
            'animation': {
                'enabled': config.animation,
                'duration_ms': config.animation_duration,
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def render_proof(
        self,
        proof_steps: List[Dict[str, Any]],
        config: Optional[ProofVisualConfig] = None
    ) -> Dict[str, Any]:
        """
        Render a proof as a visual step-by-step diagram.
        
        Args:
            proof_steps: List of proof steps
            config: Visualization configuration
            
        Returns:
            Proof visualization data
        """
        if config is None:
            config = ProofVisualConfig()
        
        # Process steps into visual nodes
        nodes = []
        edges = []
        
        for i, step in enumerate(proof_steps):
            node = {
                'id': f'step_{i}',
                'type': step.get('type', 'step'),
                'content': step.get('description', ''),
                'label': f'Step {i+1}',
                'style': {
                    'fill': config.color_highlight if step.get('type') == 'conclusion' else config.color_normal,
                    'stroke': config.color_highlight if step.get('type') == 'conclusion' else config.color_normal,
                }
            }
            nodes.append(node)
            
            # Create edges between steps
            if i > 0 and config.show_connections:
                edges.append({
                    'from': f'step_{i-1}',
                    'to': f'step_{i}',
                    'type': 'arrow',
                    'style': {'stroke': config.color_normal}
                })
        
        return {
            'type': 'proof-visualization',
            'config': {
                'style': config.style,
                'show_connections': config.show_connections,
                'animation': config.animation,
                'colors': {
                    'highlight': config.color_highlight,
                    'normal': config.color_normal,
                    'conclusion': config.color_conclusion,
                }
            },
            'nodes': nodes,
            'edges': edges,
            'step_count': len(proof_steps),
            'proof_type': proof_steps[0].get('proof_type', 'direct') if proof_steps else None,
            'timestamp': datetime.now().isoformat()
        }
    
    def render_matrix(
        self,
        matrix: List[List[float]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Render a matrix with optional transformation visualization.
        
        Args:
            matrix: 2D list representing the matrix
            config: Rendering configuration
            
        Returns:
            Matrix visualization data
        """
        config = config or {}
        
        # Calculate properties
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        determinant = self._calculate_determinant(matrix) if rows == cols else None
        
        # Generate transformation data if 2x2 or 3x3
        transformation = None
        if rows == 2 and cols == 2:
            transformation = self._compute_2d_transformation(matrix)
        elif rows == 3 and cols == 3:
            transformation = self._compute_3d_transformation(matrix)
        
        return {
            'type': 'matrix',
            'matrix': matrix,
            'dimensions': {'rows': rows, 'columns': cols},
            'determinant': determinant,
            'eigenvalues': self._calculate_eigenvalues(matrix) if rows == cols else None,
            'transformation': transformation,
            'config': {
                'show_determinant': config.get('show_determinant', True),
                'show_eigenvalues': config.get('show_eigenvalues', False),
                'animate_transform': config.get('animate_transform', True),
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def render_distribution(
        self,
        distribution_type: str,
        params: Dict[str, float],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Render a probability distribution chart.
        
        Args:
            distribution_type: Type of distribution
            params: Distribution parameters (e.g., mean, std for normal)
            config: Rendering configuration
            
        Returns:
            Distribution visualization data
        """
        config = config or {}
        
        if distribution_type == 'normal':
            data = self._generate_normal_distribution(params)
        elif distribution_type == 'binomial':
            data = self._generate_binomial_distribution(params)
        elif distribution_type == 'poisson':
            data = self._generate_poisson_distribution(params)
        else:
            return {'error': f'Unknown distribution type: {distribution_type}'}
        
        return {
            'type': 'distribution',
            'distribution_type': distribution_type,
            'parameters': params,
            'data': data,
            'config': {
                'show_mean': config.get('show_mean', True),
                'show_std': config.get('show_std', True),
                'animation': config.get('animation', True),
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def render_integral_visualization(
        self,
        function: str,
        a: float,
        b: float,
        num_rectangles: int = 10,
        animation: bool = True
    ) -> Dict[str, Any]:
        """
        Render a Riemann sum visualization for definite integrals.
        
        Args:
            function: Function to integrate
            a: Lower bound
            b: Upper bound
            num_rectangles: Number of rectangles for approximation
            animation: Whether to animate the visualization
            
        Returns:
            Integral visualization data
        """
        # Generate rectangle data
        rectangles = []
        dx = (b - a) / num_rectangles
        
        for i in range(num_rectangles):
            x_left = a + i * dx
            x_mid = x_left + dx / 2
            height = self._evaluate_function_at(function, x_mid)
            
            rectangles.append({
                'id': i,
                'x': x_left,
                'width': dx,
                'height': max(0, height),
                'method': 'midpoint',
                'area': dx * height if height > 0 else 0
            })
        
        # Calculate approximation
        total_area = sum(r['area'] for r in rectangles)
        
        return {
            'type': 'integral-visualization',
            'function': function,
            'bounds': {'a': a, 'b': b},
            'method': 'Riemann sum (midpoint)',
            'num_rectangles': num_rectangles,
            'rectangle_width': dx,
            'approximation': total_area,
            'rectangles': rectangles,
            'animation': {
                'enabled': animation,
                'duration_ms': 2000,
                'reveal_order': 'left-to-right'
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def render_logic_flow(
        self,
        logical_structure: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Render a logical flow diagram for proof structures.
        
        Args:
            logical_structure: Logical structure to visualize
            config: Rendering configuration
            
        Returns:
            Logic flow visualization data
        """
        config = config or {}
        
        nodes = []
        edges = []
        
        # Process assumptions
        assumptions = logical_structure.get('assumptions', [])
        for i, assumption in enumerate(assumptions):
            nodes.append({
                'id': f'assumption_{i}',
                'type': 'assumption',
                'content': assumption,
                'layer': 0,
                'position': i
            })
        
        # Process deductions
        deductions = logical_structure.get('deductions', [])
        for i, deduction in enumerate(deductions):
            nodes.append({
                'id': f'deduction_{i}',
                'type': 'deduction',
                'content': deduction,
                'layer': 1,
                'position': i,
                'depends_on': deduction.get('depends_on', [])
            })
            
            # Create edges
            for dep in deduction.get('depends_on', []):
                edges.append({
                    'from': dep,
                    'to': f'deduction_{i}',
                    'type': 'implication'
                })
        
        # Process conclusion
        if 'conclusion' in logical_structure:
            nodes.append({
                'id': 'conclusion',
                'type': 'conclusion',
                'content': logical_structure['conclusion'],
                'layer': 2,
                'position': 0
            })
            
            # Connect last deductions to conclusion
            for i in range(len(deductions)):
                edges.append({
                    'from': f'deduction_{len(deductions)-1}',
                    'to': 'conclusion',
                    'type': 'implication'
                })
        
        return {
            'type': 'logic-flow',
            'config': {
                'direction': config.get('direction', 'horizontal'),
                'show_labels': config.get('show_labels', True),
            },
            'nodes': nodes,
            'edges': edges,
            'layers': ['Assumptions', 'Deductions', 'Conclusion'],
            'timestamp': datetime.now().isoformat()
        }
    
    # Helper methods
    
    def _process_latex(self, equation: str) -> str:
        """Process equation into LaTeX format."""
        # Ensure proper LaTeX formatting
        if not equation.startswith('$$'):
            if '\\' in equation or '_' in equation or '^' in equation:
                return f'$${equation}$$'
        return equation
    
    def _evaluate_equation(
        self,
        equation: str,
        variables: Dict[str, float]
    ) -> Optional[float]:
        """Evaluate equation with given variable values."""
        try:
            # Simple evaluation - in production, use a proper math parser
            expr = equation
            for var, value in variables.items():
                expr = expr.replace(var, str(value))
            return eval(expr)
        except Exception:
            return None
    
    def _generate_function_points(
        self,
        func: Dict[str, Any],
        x_range: Tuple[float, float],
        y_range: Tuple[float, float],
        resolution: int
    ) -> List[Dict[str, float]]:
        """Generate points for plotting a function."""
        expression = func.get('expression')
        points = []
        
        x_step = (x_range[1] - x_range[0]) / resolution
        
        for i in range(resolution + 1):
            x = x_range[0] + i * x_step
            y = self._evaluate_function_at(expression, x)
            
            # Clamp y to y_range
            if y_range:
                y = max(y_range[0], min(y_range[1], y))
            
            points.append({'x': x, 'y': y})
        
        return points
    
    def _evaluate_function_at(self, expression: str, x: float) -> float:
        """Evaluate a function expression at a specific x value."""
        try:
            # Simple evaluation - use a proper math parser in production
            expr = expression.replace('x', f'({x})')
            expr = expr.replace('^', '**')
            return eval(expr)
        except Exception:
            return 0.0
    
    def _calculate_determinant(self, matrix: List[List[float]]) -> float:
        """Calculate determinant of a square matrix."""
        n = len(matrix)
        if n != len(matrix[0]):
            return None
        
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        elif n == 3:
            return (
                matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
                - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
                + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
            )
        else:
            # Use numpy or similar for larger matrices
            return None
    
    def _calculate_eigenvalues(self, matrix: List[List[float]]) -> List[float]:
        """Calculate eigenvalues of a matrix."""
        # Simplified - use numpy in production
        n = len(matrix)
        if n == 2:
            a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
            trace = a + d
            det = a * d - b * c
            discriminant = trace ** 2 - 4 * det
            if discriminant >= 0:
                return [(trace + discriminant ** 0.5) / 2, (trace - discriminant ** 0.5) / 2]
            else:
                return [trace / 2, trace / 2]
        return []
    
    def _compute_2d_transformation(self, matrix: List[List[float]]) -> Dict[str, Any]:
        """Compute 2D transformation data from 2x2 matrix."""
        return {
            'type': 'linear',
            'matrix': matrix,
            'determinant': self._calculate_determinant(matrix),
            'basis_vectors': {
                'i_hat': {'x': matrix[0][0], 'y': matrix[0][1]},
                'j_hat': {'x': matrix[1][0], 'y': matrix[1][1]}
            }
        }
    
    def _compute_3d_transformation(self, matrix: List[List[float]]) -> Dict[str, Any]:
        """Compute 3D transformation data from 3x3 matrix."""
        return {
            'type': 'linear',
            'matrix': matrix,
            'determinant': self._calculate_determinant(matrix),
        }
    
    def _generate_normal_distribution(
        self,
        params: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate normal distribution data."""
        mean = params.get('mean', 0)
        std = params.get('std', 1)
        
        points = []
        x = mean - 4 * std
        while x <= mean + 4 * std:
            y = (1 / (std * math.sqrt(2 * math.pi))) * math.exp(
                -0.5 * ((x - mean) / std) ** 2
            )
            points.append({'x': x, 'y': y})
            x += std / 10
        
        return {
            'type': 'normal',
            'mean': mean,
            'std': std,
            'points': points,
            'cdf': self._generate_normal_cdf(mean, std)
        }
    
    def _generate_normal_cdf(self, mean: float, std: float) -> List[Dict[str, float]]:
        """Generate normal CDF data."""
        points = []
        x = mean - 4 * std
        while x <= mean + 4 * std:
            y = 0.5 * (1 + math.erf((x - mean) / (std * math.sqrt(2))))
            points.append({'x': x, 'y': y})
            x += std / 10
        return points
    
    def _generate_binomial_distribution(
        self,
        params: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate binomial distribution data."""
        n = int(params.get('n', 10))
        p = params.get('p', 0.5)
        
        points = []
        for k in range(n + 1):
            # Calculate binomial probability
            coeff = math.comb(n, k)
            prob = coeff * (p ** k) * ((1 - p) ** (n - k))
            points.append({'x': k, 'y': prob})
        
        return {
            'type': 'binomial',
            'n': n,
            'p': p,
            'points': points,
            'mean': n * p,
            'variance': n * p * (1 - p)
        }
    
    def _generate_poisson_distribution(
        self,
        params: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate Poisson distribution data."""
        lambda_param = params.get('lambda', 5)
        
        points = []
        k = 0
        prob = math.exp(-lambda_param) * (lambda_param ** k) / math.factorial(k)
        while prob > 0.0001:
            points.append({'x': k, 'y': prob})
            k += 1
            prob = math.exp(-lambda_param) * (lambda_param ** k) / math.factorial(k)
        
        return {
            'type': 'poisson',
            'lambda': lambda_param,
            'points': points,
            'mean': lambda_param,
            'variance': lambda_param
        }


def create_math_visual_service(config: Optional[Dict[str, Any]] = None) -> MathVerseVisualService:
    """
    Factory function to create a MathVerse visual service.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured MathVerseVisualService instance
    """
    return MathVerseVisualService(config)
