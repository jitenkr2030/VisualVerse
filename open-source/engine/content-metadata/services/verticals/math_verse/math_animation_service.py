"""
MathVerse Animation Service

This module provides the MathVerse-specific animation service implementation,
extending the base animation service with mathematical domain functionality
including function plotting animations, equation solving animations,
integral approximation animations, and mathematical transformation animations.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
import logging

from ....extensions.service_extension_base import ServiceExtension, ExtensionContext

logger = logging.getLogger(__name__)


class AnimationPreset(str, Enum):
    """Pre-defined animation presets for mathematical visualizations."""
    FUNCTION_PLOT = "function-plot"
    EQUATION_SOLVE = "equation-solve"
    INTEGRAL_REVEAL = "integral-reveal"
    TRANSFORMATION = "transformation"
    SEQUENCE_CONVERGE = "sequence-converge"
    SERIES_SUM = "series-sum"
    DERIVATIVE_APPROX = "derivative-approx"
    MATRIX_TRANSFORM = "matrix-transform"


@dataclass
class AnimationKeyframe:
    """A single keyframe in an animation."""
    time_ms: float
    property: str
    value: Any
    easing: str = "linear"


@dataclass
class AnimationConfig:
    """Configuration for mathematical animations."""
    duration_ms: int = 3000
    easing: str = "ease-in-out"
    fps: int = 30
    loop: bool = False
    auto_play: bool = True
    show_controls: bool = True
    resolution: Tuple[int, int] = (800, 600)


@dataclass
class FunctionAnimationParams:
    """Parameters for function animation."""
    functions: List[Dict[str, Any]]
    x_range: Tuple[float, float] = (-10, 10)
    y_range: Optional[Tuple[float, float]] = None
    draw_speed: float = 0.02
    reveal_mode: str = "progressive"  # progressive, simultaneous, wave
    trace_path: bool = True


class MathVerseAnimationService:
    """
    MathVerse-specific animation service.
    
    This service handles mathematical animations including:
    - Function plotting and transformation animations
    - Equation solving step animations
    - Integral approximation animations (Riemann sums)
    - Matrix transformation animations
    - Series and sequence convergence animations
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MathVerse animation service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._presets = self._load_presets()
        self._easings = self._load_easing_functions()
        
    def _load_presets(self) -> Dict[str, Dict[str, Any]]:
        """Load pre-defined animation presets."""
        return {
            AnimationPreset.FUNCTION_PLOT.value: {
                'description': "Animated function plotting with progressive line drawing",
                'default_duration': 3000,
                'easing': 'ease-in-out',
                'features': ['trace', 'axis', 'grid', 'label']
            },
            AnimationPreset.EQUATION_SOLVE.value: {
                'description': "Step-by-step equation solving animation",
                'default_duration': 4000,
                'easing': 'ease-in-out',
                'features': ['steps', 'highlight', 'explain']
            },
            AnimationPreset.INTEGRAL_REVEAL.value: {
                'description': "Riemann sum integral approximation animation",
                'default_duration': 3500,
                'easing': 'linear',
                'features': ['rectangles', 'area', 'sum']
            },
            AnimationPreset.TRANSFORMATION.value: {
                'description': "Geometric transformation animation",
                'default_duration': 2500,
                'easing': 'ease-in-out',
                'features': ['morph', 'trace', 'grid']
            },
            AnimationPreset.SEQUENCE_CONVERGE.value: {
                'description': "Sequence convergence animation",
                'default_duration': 5000,
                'easing': 'ease-out',
                'features': ['terms', 'limit', 'error']
            },
            AnimationPreset.SERIES_SUM.value: {
                'description': "Infinite series partial sum animation",
                'default_duration': 6000,
                'easing': 'ease-out',
                'features': ['partial_sums', 'convergence']
            },
            AnimationPreset.DERIVATIVE_APPROX.value: {
                'description': "Derivative limit definition animation",
                'default_duration': 4000,
                'easing': 'linear',
                'features': ['secant', 'tangent', 'limit']
            },
            AnimationPreset.MATRIX_TRANSFORM.value: {
                'description': "Matrix linear transformation animation",
                'default_duration': 3000,
                'easing': 'ease-in-out',
                'features': ['basis', 'vectors', 'determinant']
            }
        }
    
    def _load_easing_functions(self) -> Dict[str, str]:
        """Load CSS easing function mappings."""
        return {
            'linear': 'linear',
            'ease-in': 'ease-in',
            'ease-out': 'ease-out',
            'ease-in-out': 'ease-in-out',
            'ease-in-quad': 'cubic-bezier(0.55, 0.085, 0.68, 0.53)',
            'ease-out-quad': 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
            'ease-in-out-quad': 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
            'bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        }
    
    def get_animation_presets(self) -> Dict[str, Dict[str, Any]]:
        """
        Get animation presets provided by this service.
        
        Returns:
            Dictionary of preset ID to configuration
        """
        return self._presets
    
    def create_animation(
        self,
        animation_type: str,
        params: Dict[str, Any],
        context: Optional[ExtensionContext] = None
    ) -> Dict[str, Any]:
        """
        Create an animation of the specified type.
        
        Args:
            animation_type: Type of animation
            params: Animation parameters
            context: Optional execution context
            
        Returns:
            Animation configuration
        """
        preset = self._presets.get(animation_type)
        
        if preset is None:
            # Try to match common types
            animation_type = self._resolve_animation_type(animation_type)
        
        # Create animation based on type
        if 'function' in animation_type or 'plot' in animation_type:
            return self._create_function_animation(params)
        elif 'equation' in animation_type or 'solve' in animation_type:
            return self._create_equation_animation(params)
        elif 'integral' in animation_type or 'riemann' in animation_type:
            return self._create_integral_animation(params)
        elif 'transform' in animation_type or 'matrix' in animation_type:
            return self._create_matrix_animation(params)
        elif 'sequence' in animation_type or 'converge' in animation_type:
            return self._create_sequence_animation(params)
        elif 'series' in animation_type or 'sum' in animation_type:
            return self._create_series_animation(params)
        elif 'derivative' in animation_type:
            return self._create_derivative_animation(params)
        else:
            return self._create_default_animation(params)
    
    def _create_function_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a function plotting animation."""
        func_params = FunctionAnimationParams(
            functions=params.get('functions', []),
            x_range=params.get('x_range', (-10, 10)),
            y_range=params.get('y_range'),
            draw_speed=params.get('draw_speed', 0.02),
            reveal_mode=params.get('reveal_mode', 'progressive'),
            trace_path=params.get('trace_path', True)
        )
        
        # Generate keyframes for progressive drawing
        keyframes = self._generate_function_keyframes(func_params)
        
        return {
            'type': 'function-plot',
            'params': {
                'functions': func_params.functions,
                'x_range': func_params.x_range,
                'y_range': func_params.y_range,
                'reveal_mode': func_params.reveal_mode
            },
            'keyframes': keyframes,
            'config': {
                'duration_ms': params.get('duration_ms', 3000),
                'easing': params.get('easing', 'ease-in-out'),
                'fps': params.get('fps', 30)
            },
            'features': self._presets[AnimationPreset.FUNCTION_PLOT.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_equation_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create an equation solving animation."""
        steps = params.get('steps', [])
        
        # Generate keyframes for each solving step
        keyframes = []
        duration_per_step = params.get('duration_ms', 4000) // len(steps) if steps else 1000
        
        for i, step in enumerate(steps):
            keyframes.append(AnimationKeyframe(
                time_ms=i * duration_per_step,
                property='equation_display',
                value=step.get('equation', ''),
                easing='ease-in-out'
            ))
            keyframes.append(AnimationKeyframe(
                time_ms=i * duration_per_step + duration_per_step * 0.3,
                property='highlight',
                value=step.get('focus_terms', []),
                easing='ease-out'
            ))
            keyframes.append(AnimationKeyframe(
                time_ms=i * duration_per_step + duration_per_step * 0.7,
                property='explanation',
                value=step.get('explanation', ''),
                easing='ease-in-out'
            ))
        
        return {
            'type': 'equation-solve',
            'original_equation': params.get('equation', ''),
            'steps': steps,
            'keyframes': [
                {'time_ms': k.time_ms, 'property': k.property, 'value': k.value, 'easing': k.easing}
                for k in keyframes
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 4000),
                'easing': params.get('easing', 'ease-in-out'),
                'show_controls': params.get('show_controls', True)
            },
            'features': self._presets[AnimationPreset.EQUATION_SOLVE.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_integral_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a Riemann sum integral animation."""
        function = params.get('function', 'x^2')
        a = params.get('a', 0)
        b = params.get('b', 2)
        num_rectangles = params.get('num_rectangles', 10)
        
        # Generate rectangle keyframes
        keyframes = []
        dx = (b - a) / num_rectangles
        duration_per_rect = params.get('duration_ms', 3500) // num_rectangles
        
        for i in range(num_rectangles):
            x_left = a + i * dx
            x_mid = x_left + dx / 2
            height = self._evaluate_function(function, x_mid)
            
            keyframes.append(AnimationKeyframe(
                time_ms=i * duration_per_rect,
                property='rectangle',
                value={
                    'index': i,
                    'x': x_left,
                    'width': dx,
                    'height': max(0, height),
                    'area': dx * height if height > 0 else 0
                },
                easing='ease-out'
            ))
        
        # Final sum animation
        total_area = sum(
            (b - a) / num_rectangles * max(0, self._evaluate_function(function, a + (i + 0.5) * (b - a) / num_rectangles))
            for i in range(num_rectangles)
        )
        
        keyframes.append(AnimationKeyframe(
            time_ms=params.get('duration_ms', 3500) - 500,
            property='sum',
            value={'total': total_area, 'exact': self._calculate_integral(function, a, b)},
            easing='ease-out'
        ))
        
        return {
            'type': 'integral-reveal',
            'function': function,
            'bounds': {'a': a, 'b': b},
            'num_rectangles': num_rectangles,
            'method': 'Riemann sum (midpoint)',
            'keyframes': [
                {'time_ms': k.time_ms, 'property': k.property, 'value': k.value, 'easing': k.easing}
                for k in keyframes
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 3500),
                'easing': params.get('easing', 'linear'),
                'show_approximation': True
            },
            'features': self._presets[AnimationPreset.INTEGRAL_REVEAL.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_matrix_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a matrix transformation animation."""
        matrix = params.get('matrix', [[1, 0], [0, 1]])
        show_determinant = params.get('show_determinant', True)
        
        # Calculate determinant
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        # Generate basis vector animation keyframes
        keyframes = [
            AnimationKeyframe(
                time_ms=0,
                property='basis_vectors',
                value={'i': [1, 0], 'j': [0, 1]},
                easing='linear'
            ),
            AnimationKeyframe(
                time_ms=1000,
                property='basis_vectors',
                value={'i': matrix[0], 'j': matrix[1]},
                easing='ease-in-out'
            )
        ]
        
        # Grid transformation
        for t in [0.25, 0.5, 0.75, 1.0]:
            i_vec = [t * m for m in matrix[0]]
            j_vec = [t * m for m in matrix[1]]
            keyframes.append(AnimationKeyframe(
                time_ms=int(1000 + t * 1500),
                property='grid',
                value={'i': i_vec, 'j': j_vec},
                easing='ease-in-out'
            ))
        
        return {
            'type': 'matrix-transform',
            'matrix': matrix,
            'determinant': det if show_determinant else None,
            'keyframes': [
                {'time_ms': k.time_ms, 'property': k.property, 'value': k.value, 'easing': k.easing}
                for k in keyframes
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 3000),
                'easing': params.get('easing', 'ease-in-out'),
                'show_determinant': show_determinant
            },
            'features': self._presets[AnimationPreset.MATRIX_TRANSFORM.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_sequence_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a sequence convergence animation."""
        formula = params.get('formula', '1/n')
        start_n = params.get('start_n', 1)
        terms = params.get('terms', 20)
        
        keyframes = []
        duration_per_term = params.get('duration_ms', 5000) // terms
        
        # Generate sequence terms
        sequence_data = []
        for n in range(start_n, start_n + terms):
            value = self._evaluate_function(formula, n)
            sequence_data.append({'n': n, 'value': value})
        
        for i, data in enumerate(sequence_data):
            keyframes.append(AnimationKeyframe(
                time_ms=i * duration_per_term,
                property='term',
                value=data,
                easing='ease-out'
            ))
        
        # Calculate limit if convergent
        limit = None
        if formula == '1/n' or formula == '1/(n+1)':
            limit = 0
        
        return {
            'type': 'sequence-converge',
            'formula': formula,
            'start_n': start_n,
            'terms': terms,
            'limit': limit,
            'keyframes': [
                {'time_ms': k.time_ms, 'property': k.property, 'value': k.value, 'easing': k.easing}
                for k in keyframes
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 5000),
                'easing': params.get('easing', 'ease-out'),
                'show_limit': True
            },
            'features': self._presets[AnimationPreset.SEQUENCE_CONVERGE.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_series_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create an infinite series partial sum animation."""
        series = params.get('series', '1/2^n')
        num_partials = params.get('num_partials', 10)
        
        keyframes = []
        duration_per_sum = params.get('duration_ms', 6000) // num_partials
        
        # Generate partial sums
        partial_sums = []
        current_sum = 0
        for n in range(num_partials):
            term = self._evaluate_function(series, n + 1)
            current_sum += term
            partial_sums.append({'n': n + 1, 'term': term, 'sum': current_sum})
            
            keyframes.append(AnimationKeyframe(
                time_ms=n * duration_per_sum,
                property='partial_sum',
                value={'n': n + 1, 'term': term, 'sum': current_sum},
                easing='ease-out'
            ))
        
        # Determine convergence
        if series == '1/2^n':
            limit = 1.0
        elif series == '1/n^2':
            limit = math.pi ** 2 / 6
        else:
            limit = None
        
        return {
            'type': 'series-sum',
            'series': series,
            'num_partials': num_partials,
            'limit': limit,
            'keyframes': [
                {'time_ms': k.time_ms, 'property': k.property, 'value': k.value, 'easing': k.easing}
                for k in keyframes
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 6000),
                'easing': params.get('easing', 'ease-out'),
                'show_limit': True
            },
            'features': self._presets[AnimationPreset.SERIES_SUM.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_derivative_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a derivative limit definition animation."""
        function = params.get('function', 'x^2')
        point = params.get('point', 2)
        h_values = params.get('h_values', [1, 0.5, 0.1, 0.01])
        
        keyframes = []
        duration_per_h = params.get('duration_ms', 4000) // len(h_values)
        
        for i, h in enumerate(h_values):
            secant_slope = (self._evaluate_function(function, point + h) - self._evaluate_function(function, point)) / h
            
            keyframes.append(AnimationKeyframe(
                time_ms=i * duration_per_h,
                property='secant',
                value={
                    'h': h,
                    'point': point,
                    'secant_slope': secant_slope,
                    'target_derivative': 2 * point  # derivative of x^2 is 2x
                },
                easing='linear'
            ))
        
        return {
            'type': 'derivative-approx',
            'function': function,
            'point': point,
            'target_derivative': 2 * point,
            'keyframes': [
                {'time_ms': k.time_ms, 'property': k.property, 'value': k.value, 'easing': k.easing}
                for k in keyframes
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 4000),
                'easing': params.get('easing', 'linear'),
                'show_tangent': True
            },
            'features': self._presets[AnimationPreset.DERIVATIVE_APPROX.value]['features'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_default_animation(
        self,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a default animation with simple fade-in."""
        return {
            'type': 'default',
            'keyframes': [
                {'time_ms': 0, 'property': 'opacity', 'value': 0, 'easing': 'ease-in'},
                {'time_ms': 1000, 'property': 'opacity', 'value': 1, 'easing': 'ease-out'}
            ],
            'config': {
                'duration_ms': params.get('duration_ms', 1000),
                'easing': 'ease-in-out'
            },
            'timestamp': datetime.now().isoformat()
        }
    
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
        if animation_type == 'fade':
            return {
                'type': 'fade',
                'duration_ms': 500,
                'keyframes': [
                    {'time_ms': 0, 'property': 'opacity', 'from': 1, 'to': 0},
                    {'time_ms': 500, 'property': 'opacity', 'from': 0, 'to': 1}
                ]
            }
        elif animation_type == 'slide':
            return {
                'type': 'slide',
                'duration_ms': 600,
                'direction': 'horizontal',
                'keyframes': [
                    {'time_ms': 0, 'property': 'transform', 'from': 'translateX(-100%)', 'to': 'translateX(0)'}
                ]
            }
        elif animation_type == 'morph':
            return {
                'type': 'morph',
                'duration_ms': 800,
                'keyframes': [
                    {'time_ms': 0, 'property': 'path', 'from': from_state.get('path'), 'to': to_state.get('path')}
                ]
            }
        else:
            return {
                'type': 'crossfade',
                'duration_ms': 400,
                'keyframes': [
                    {'time_ms': 0, 'property': 'opacity', 'from': 1, 'to': 0.5},
                    {'time_ms': 400, 'property': 'opacity', 'from': 0.5, 'to': 1}
                ]
            }
    
    # Helper methods
    
    def _generate_function_keyframes(
        self,
        params: FunctionAnimationParams
    ) -> List[Dict[str, Any]]:
        """Generate keyframes for function animation."""
        keyframes = []
        
        if params.reveal_mode == 'progressive':
            # Progressive line drawing
            num_points = 200
            points_per_frame = 2
            
            for i in range(0, num_points, points_per_frame):
                points = []
                for j in range(i, min(i + points_per_frame, num_points)):
                    x = params.x_range[0] + (params.x_range[1] - params.x_range[0]) * j / num_points
                    for func in params.functions:
                        y = self._evaluate_function(func.get('expression', ''), x)
                        points.append({'x': x, 'y': y, 'function': func.get('id', 'default')})
                
                keyframes.append({
                    'time_ms': int(i * params.draw_speed * 1000),
                    'property': 'points',
                    'value': points,
                    'easing': 'linear'
                })
        
        return keyframes
    
    def _evaluate_function(self, expression: str, x: float) -> float:
        """Evaluate a function expression at a given x value."""
        try:
            expr = expression.replace('^', '**')
            expr = expr.replace('sin', 'math.sin')
            expr = expr.replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan')
            expr = expr.replace('sqrt', 'math.sqrt')
            expr = expr.replace('log', 'math.log')
            expr = expr.replace('exp', 'math.exp')
            expr = expr.replace('π', 'math.pi')
            
            # Safe evaluation - in production, use a proper math parser
            safe_dict = {'x': x, 'math': math}
            return eval(expr, {"__builtins__": {}}, safe_dict)
        except Exception:
            return 0.0
    
    def _calculate_integral(
        self,
        function: str,
        a: float,
        b: float
    ) -> float:
        """Calculate exact integral (simplified)."""
        # This is a placeholder - use numerical integration in production
        if function == 'x^2' or function == 'x**2':
            return (b ** 3 - a ** 3) / 3
        elif function == 'x':
            return (b ** 2 - a ** 2) / 2
        elif function == '1':
            return b - a
        else:
            return None
    
    def _resolve_animation_type(self, animation_type: str) -> str:
        """Resolve animation type to standard type."""
        type_mappings = {
            'plot': 'function-plot',
            'graph': 'function-plot',
            'solve': 'equation-solve',
            'integral': 'integral-reveal',
            'matrix': 'matrix-transform',
            'sequence': 'sequence-converge',
            'series': 'series-sum',
            'derivative': 'derivative-approx'
        }
        
        for key, value in type_mappings.items():
            if key in animation_type.lower():
                return value
        
        return animation_type


def create_math_animation_service(config: Optional[Dict[str, Any]] = None) -> MathVerseAnimationService:
    """
    Factory function to create a MathVerse animation service.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured MathVerseAnimationService instance
    """
    return MathVerseAnimationService(config)
