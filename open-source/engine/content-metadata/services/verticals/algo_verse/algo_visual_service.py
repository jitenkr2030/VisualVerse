"""
AlgoVerse Visual Service

This module provides the AlgoVerse-specific visual service implementation,
extending the base visual service with algorithmic domain functionality
including flowchart generation, data structure visualization, code highlighting,
and complexity chart rendering.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import math
import logging

from ....extensions.service_extension_base import (
    VisualServiceExtension,
    ExtensionContext
)

logger = logging.getLogger(__name__)


class VisualType(str, Enum):
    """AlgoVerse visualization types."""
    FLOWCHART = "flowchart"
    ARRAY_LAYOUT = "array-layout"
    NODE_DIAGRAM = "node-diagram"
    TREE_LAYOUT = "tree-layout"
    GRAPH_LAYOUT = "graph-layout"
    CODE_HIGHLIGHT = "code-highlight"
    CALL_STACK = "call-stack"
    SORT_ANIMATION = "sort-animation"
    SEARCH_ANIMATION = "search-animation"
    DFS_ANIMATION = "dfs-animation"
    BFS_ANIMATION = "bfs-animation"
    COMPLEXITY_CHART = "complexity-chart"
    STEP_DIAGRAM = "step-diagram"


@dataclass
class FlowchartConfig:
    """Configuration for flowchart generation."""
    direction: str = "vertical"  # vertical, horizontal
    node_style: str = "rounded"  # rounded, rectangular, diamond
    arrow_style: str = "standard"  # standard, curved, straight
    show_line_numbers: bool = True
    highlight_path: Optional[List[str]] = None


@dataclass
class ArrayLayoutConfig:
    """Configuration for array visualization."""
    cell_width: int = 60
    cell_height: int = 40
    spacing: int = 10
    show_indices: bool = True
    highlight_values: Optional[Dict[int, str]] = None
    color_scheme: str = "default"


@dataclass
class TreeLayoutConfig:
    """Configuration for tree visualization."""
    layout_type: str = "tidy"  # tidy, radial, dendrogram
    node_radius: int = 20
    level_height: int = 80
    sibling_spacing: int = 40
    orientation: str = "top-down"  # top-down, left-right


@dataclass
class GraphLayoutConfig:
    """Configuration for graph visualization."""
    layout_type: str = "force-directed"  # force-directed, circular, grid, hierarchical
    node_radius: int = 25
    edge_length: int = 100
    directed: bool = True
    show_weights: bool = True
    highlight_path: Optional[List[int]] = None


@dataclass
class CodeHighlightConfig:
    """Configuration for code syntax highlighting."""
    language: str = "python"
    show_line_numbers: bool = True
    highlight_lines: Optional[List[int]] = None
    current_line: Optional[int] = None
    theme: str = "default"  # default, dark, high-contrast


class AlgoVerseVisualService:
    """
    AlgoVerse-specific visual service.
    
    This service handles algorithmic visualization including:
    - Flowchart generation from code
    - Data structure visualization (arrays, trees, graphs, linked lists)
    - Code syntax highlighting with execution highlighting
    - Call stack visualization
    - Complexity chart rendering
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AlgoVerse visual service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._renderers = self._initialize_renderers()
        self._color_schemes = self._load_color_schemes()
        self._syntax_rules = self._load_syntax_rules()

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        logger.info("AlgoVerseVisualService configured with settings: %s", list(config.keys()))

    def _initialize_renderers(self) -> Dict[str, Any]:
        """Initialize visualization renderers."""
        return {
            VisualType.FLOWCHART: self._render_flowchart,
            VisualType.ARRAY_LAYOUT: self._render_array_layout,
            VisualType.NODE_DIAGRAM: self._render_node_diagram,
            VisualType.TREE_LAYOUT: self._render_tree_layout,
            VisualType.GRAPH_LAYOUT: self._render_graph_layout,
            VisualType.CODE_HIGHLIGHT: self._render_code_highlight,
            VisualType.CALL_STACK: self._render_call_stack,
            VisualType.COMPLEXITY_CHART: self._render_complexity_chart,
            VisualType.SORT_ANIMATION: self._render_sort_animation,
            VisualType.SEARCH_ANIMATION: self._render_search_animation,
            VisualType.DFS_ANIMATION: self._render_traversal_animation,
            VisualType.BFS_ANIMATION: self._render_traversal_animation,
        }
    
    def _load_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Load available color schemes."""
        return {
            'default': {
                'primary': '#7c3aed',
                'secondary': '#8b5cf6',
                'accent': '#06b6d4',
                'background': '#ffffff',
                'text': '#374151',
                'highlight': '#fcd34d',
                'visited': '#22c55e',
                'processing': '#f59e0b',
                'error': '#ef4444',
                'success': '#22c55e',
                'code_keyword': '#7c3aed',
                'code_string': '#059669',
                'code_comment': '#9ca3af',
                'code_function': '#2563eb',
            },
            'dark': {
                'primary': '#a78bfa',
                'secondary': '#c4b5fd',
                'accent': '#22d3ee',
                'background': '#1e1e1e',
                'text': '#e5e7eb',
                'highlight': '#fcd34d',
                'visited': '#4ade80',
                'processing': '#fbbf24',
                'error': '#f87171',
                'success': '#4ade80',
                'code_keyword': '#c084fc',
                'code_string': '#34d399',
                'code_comment': '#6b7280',
                'code_function': '#60a5fa',
            },
            'high-contrast': {
                'primary': '#000000',
                'secondary': '#333333',
                'accent': '#0066cc',
                'background': '#ffffff',
                'text': '#000000',
                'highlight': '#ff9900',
                'visited': '#008000',
                'processing': '#ff6600',
                'error': '#cc0000',
                'success': '#008000',
                'code_keyword': '#0000cc',
                'code_string': '#008000',
                'code_comment': '#666666',
                'code_function': '#0000cc',
            }
        }
    
    def _load_syntax_rules(self) -> Dict[str, Dict[str, str]]:
        """Load syntax highlighting rules for different languages."""
        return {
            'python': {
                'keywords': ['def', 'if', 'elif', 'else', 'for', 'while', 'return', 'import', 'from', 'class', 'try', 'except', 'finally', 'with', 'as', 'pass', 'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None', 'lambda', 'yield', 'global', 'nonlocal'],
                'string_delimiters': ['"', "'", '"""', "'''"],
                'comment': '#',
                'function_definition': r'def\s+(\w+)\s*\('
            },
            'javascript': {
                'keywords': ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'class', 'import', 'export', 'default', 'try', 'catch', 'finally', 'throw', 'new', 'this', 'super', 'extends', 'async', 'await', 'true', 'false', 'null', 'undefined'],
                'string_delimiters': ['"', "'", '`'],
                'comment': '//',
                'function_definition': r'function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*\('
            },
            'java': {
                'keywords': ['public', 'private', 'protected', 'class', 'interface', 'extends', 'implements', 'static', 'final', 'void', 'int', 'long', 'double', 'float', 'boolean', 'char', 'byte', 'short', 'if', 'else', 'for', 'while', 'return', 'new', 'this', 'super', 'try', 'catch', 'finally', 'throw', 'throws', 'import', 'package', 'true', 'false', 'null'],
                'string_delimiters': ['"', "'"],
                'comment': '//',
                'function_definition': r'(public|private|protected|static|\s)+\s+[\w<>\[\]]+\s+(\w+)\s*\('
            }
        }
    
    def get_visualization_types(self) -> List[str]:
        """
        Get list of visualization types provided by this service.
        
        Returns:
            List of visualization type identifiers
        """
        return [e.value for e in VisualType]
    
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
        try:
            vtype = VisualType(visual_type)
        except ValueError:
            logger.warning(f"Unknown visual type: {visual_type}")
            return {
                'error': f'Unknown visual type: {visual_type}',
                'available_types': self.get_visualization_types()
            }
        
        renderer = self._renderers.get(vtype)
        
        if renderer is None:
            return {'error': f'No renderer for type: {visual_type}'}
        
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
            VisualType.FLOWCHART.value: {
                'direction': 'vertical',
                'node_style': 'rounded',
                'arrow_style': 'standard',
                'show_line_numbers': True,
            },
            VisualType.ARRAY_LAYOUT.value: {
                'cell_width': 60,
                'cell_height': 40,
                'spacing': 10,
                'show_indices': True,
                'color_scheme': 'default',
            },
            VisualType.TREE_LAYOUT.value: {
                'layout_type': 'tidy',
                'node_radius': 20,
                'level_height': 80,
                'sibling_spacing': 40,
                'orientation': 'top-down',
            },
            VisualType.GRAPH_LAYOUT.value: {
                'layout_type': 'force-directed',
                'node_radius': 25,
                'edge_length': 100,
                'directed': True,
                'show_weights': True,
            },
            VisualType.CODE_HIGHLIGHT.value: {
                'language': 'python',
                'show_line_numbers': True,
                'theme': 'default',
            },
            VisualType.CALL_STACK.value: {
                'max_frames': 10,
                'show_args': True,
                'animation_speed': 'normal',
            },
            VisualType.COMPLEXITY_CHART.value: {
                'show_labels': True,
                'log_scale': True,
                'comparisons': True,
            }
        }
        
        return style_map.get(visual_type, {})
    
    def _render_flowchart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a flowchart from code or control flow graph."""
        cfg = data.get('control_flow_graph', {})
        config = FlowchartConfig(
            direction=data.get('direction', 'vertical'),
            node_style=data.get('node_style', 'rounded'),
            show_line_numbers=data.get('show_line_numbers', True)
        )
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Extract nodes and edges
        nodes = cfg.get('nodes', [])
        edges = cfg.get('edges', [])
        
        # Generate flowchart nodes with positions
        positioned_nodes = self._layout_flowchart_nodes(
            nodes, config.direction, config.node_style
        )
        
        # Process edges with path information
        processed_edges = []
        for edge in edges:
            processed_edges.append({
                'from': edge.get('from'),
                'to': edge.get('to'),
                'label': edge.get('label', ''),
                'style': {
                    'stroke': colors['primary'],
                    'arrow': config.arrow_style
                }
            })
        
        return {
            'type': 'flowchart',
            'config': {
                'direction': config.direction,
                'node_style': config.node_style,
                'show_line_numbers': config.show_line_numbers
            },
            'nodes': positioned_nodes,
            'edges': processed_edges,
            'colors': colors,
            'dimensions': self._calculate_flowchart_dimensions(positioned_nodes, processed_edges),
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_array_layout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render an array visualization."""
        array = data.get('array', [])
        config = ArrayLayoutConfig(
            cell_width=data.get('cell_width', 60),
            cell_height=data.get('cell_height', 40),
            spacing=data.get('spacing', 10),
            show_indices=data.get('show_indices', True),
            color_scheme=data.get('color_scheme', 'default')
        )
        
        colors = self._color_schemes.get(config.color_scheme, self._color_schemes['default'])
        highlight_map = data.get('highlight_values', {})
        
        # Generate cell positions
        cells = []
        for i, value in enumerate(array):
            cell = {
                'index': i,
                'value': value,
                'x': i * (config.cell_width + config.spacing),
                'y': 0,
                'width': config.cell_width,
                'height': config.cell_height,
                'color': highlight_map.get(i, colors['primary']),
                'state': data.get('states', {}).get(i, 'default')  # default, comparing, swapping, sorted
            }
            cells.append(cell)
        
        total_width = len(array) * (config.cell_width + config.spacing) - config.spacing
        total_height = config.cell_height + 30 if config.show_indices else config.cell_height
        
        return {
            'type': 'array-layout',
            'config': {
                'cell_width': config.cell_width,
                'cell_height': config.cell_height,
                'spacing': config.spacing,
                'show_indices': config.show_indices,
                'color_scheme': config.color_scheme
            },
            'cells': cells,
            'total_size': {'width': total_width, 'height': total_height},
            'colors': colors,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_node_diagram(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a node-link diagram for linked lists or general graphs."""
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
        config = data.get('config', {})
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Calculate node positions (simple circular layout)
        positioned_nodes = []
        center_x = 400
        center_y = 300
        radius = min(250, 200 / (len(nodes) ** 0.5) * 10)
        
        for i, node in enumerate(nodes):
            angle = (2 * math.pi * i) / len(nodes) - math.pi / 2
            positioned_nodes.append({
                'id': node.get('id', i),
                'label': node.get('label', str(i)),
                'value': node.get('value'),
                'x': center_x + radius * math.cos(angle),
                'y': center_y + radius * math.sin(angle),
                'radius': 25,
                'color': colors['primary'],
                'next': node.get('next')  # For linked lists
            })
        
        # Process edges
        processed_edges = []
        for edge in edges:
            processed_edges.append({
                'from': edge.get('from'),
                'to': edge.get('to'),
                'directed': edge.get('directed', True),
                'weight': edge.get('weight'),
                'style': {
                    'stroke': colors['primary'],
                    'arrow': 'standard'
                }
            })
        
        return {
            'type': 'node-diagram',
            'nodes': positioned_nodes,
            'edges': processed_edges,
            'colors': colors,
            'dimensions': {'width': 800, 'height': 600},
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_tree_layout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a tree visualization."""
        tree_data = data.get('tree', {})
        config = TreeLayoutConfig(
            layout_type=data.get('layout_type', 'tidy'),
            node_radius=data.get('node_radius', 20),
            level_height=data.get('level_height', 80),
            sibling_spacing=data.get('sibling_spacing', 40),
            orientation=data.get('orientation', 'top-down')
        )
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Build tree structure
        nodes = []
        edges = []
        
        def traverse_tree(node: Dict[str, Any], x: float, y: float, level: int, siblings: List) -> Tuple[float, List]:
            node_id = node.get('id', len(nodes))
            nodes.append({
                'id': node_id,
                'label': str(node.get('value', node.get('id', ''))),
                'x': x,
                'y': y,
                'radius': config.node_radius,
                'color': colors['primary'],
                'level': level
            })
            
            children = node.get('children', [])
            if not children:
                return x, siblings
            
            child_count = len(children)
            subtree_width = (child_count - 1) * config.sibling_spacing * 10
            start_x = x - subtree_width / 2
            
            for i, child in enumerate(children):
                child_x = start_x + i * config.sibling_spacing * 10
                child_y = y + config.level_height
                new_siblings, _ = traverse_tree(child, child_x, child_y, level + 1, siblings)
                
                edges.append({
                    'from': node_id,
                    'to': child.get('id', len(nodes)),
                    'style': {'stroke': colors['primary']}
                })
            
            return x, children
        
        traverse_tree(tree_data, 400, 50, 0, [])
        
        return {
            'type': 'tree-layout',
            'config': {
                'layout_type': config.layout_type,
                'node_radius': config.node_radius,
                'level_height': config.level_height,
                'sibling_spacing': config.sibling_spacing,
                'orientation': config.orientation
            },
            'nodes': nodes,
            'edges': edges,
            'colors': colors,
            'dimensions': {'width': 800, 'height': max(600, len(nodes) * 50)},
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_graph_layout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a graph visualization."""
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
        config = GraphLayoutConfig(
            layout_type=data.get('layout_type', 'force-directed'),
            node_radius=data.get('node_radius', 25),
            directed=data.get('directed', True),
            show_weights=data.get('show_weights', True),
            highlight_path=data.get('highlight_path')
        )
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Calculate positions based on layout type
        if config.layout_type == 'circular':
            positions = self._circular_layout(nodes, 300, 300, 250)
        else:
            positions = self._force_directed_layout(nodes, edges, 400, 300, 800, 600)
        
        positioned_nodes = []
        for i, node in enumerate(nodes):
            pos = positions.get(i, {'x': 400, 'y': 300})
            is_highlighted = config.highlight_path and i in config.highlight_path
            positioned_nodes.append({
                'id': i,
                'label': node.get('label', str(i)),
                'x': pos['x'],
                'y': pos['y'],
                'radius': config.node_radius,
                'color': colors['highlight'] if is_highlighted else colors['primary'],
                'state': 'highlighted' if is_highlighted else 'default'
            })
        
        processed_edges = []
        for edge in edges:
            from_pos = positions.get(edge.get('from', 0), {'x': 400, 'y': 300})
            to_pos = positions.get(edge.get('to', 0), {'x': 400, 'y': 300})
            processed_edges.append({
                'from': edge.get('from', 0),
                'to': edge.get('to', 0),
                'from_x': from_pos['x'],
                'from_y': from_pos['y'],
                'to_x': to_pos['x'],
                'to_y': to_pos['y'],
                'weight': edge.get('weight'),
                'directed': config.directed,
                'style': {'stroke': colors['primary']}
            })
        
        return {
            'type': 'graph-layout',
            'config': {
                'layout_type': config.layout_type,
                'node_radius': config.node_radius,
                'directed': config.directed,
                'show_weights': config.show_weights
            },
            'nodes': positioned_nodes,
            'edges': processed_edges,
            'colors': colors,
            'dimensions': {'width': 800, 'height': 600},
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_code_highlight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render syntax-highlighted code."""
        code = data.get('code', '')
        config = CodeHighlightConfig(
            language=data.get('language', 'python'),
            show_line_numbers=data.get('show_line_numbers', True),
            highlight_lines=data.get('highlight_lines'),
            current_line=data.get('current_line'),
            theme=data.get('theme', 'default')
        )
        
        colors = self._color_schemes.get(config.theme, self._color_schemes['default'])
        rules = self._syntax_rules.get(config.language, self._syntax_rules['python'])
        
        # Parse and highlight code
        lines = code.split('\n')
        highlighted_lines = []
        
        for i, line in enumerate(lines):
            line_num = i + 1
            is_highlighted = (
                config.highlight_lines and line_num in config.highlight_lines
            ) or line_num == config.current_line
            
            tokens = self._tokenize_line(line, config.language, rules)
            highlighted_lines.append({
                'line_number': line_num,
                'content': line,
                'tokens': tokens,
                'is_highlighted': is_highlighted,
                'highlight_reason': data.get('highlight_reasons', {}).get(line_num)
            })
        
        return {
            'type': 'code-highlight',
            'config': {
                'language': config.language,
                'show_line_numbers': config.show_line_numbers,
                'theme': config.theme
            },
            'lines': highlighted_lines,
            'total_lines': len(lines),
            'colors': colors,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_call_stack(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a call stack visualization."""
        frames = data.get('frames', [])
        max_frames = data.get('max_frames', 10)
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Limit frames
        display_frames = frames[-max_frames:] if len(frames) > max_frames else frames
        
        stack_frames = []
        for i, frame in enumerate(display_frames):
            stack_frames.append({
                'index': i,
                'function': frame.get('function', 'anonymous'),
                'line': frame.get('line', 0),
                'args': frame.get('args', {}),
                'local_vars': frame.get('local_vars', {}),
                'is_active': frame.get('is_active', i == len(display_frames) - 1),
                'depth': len(frames) - max_frames + i
            })
        
        return {
            'type': 'call-stack',
            'frames': stack_frames,
            'total_depth': len(frames),
            'max_displayed': max_frames,
            'colors': colors,
            'dimensions': {'width': 400, 'height': min(len(display_frames) * 60 + 40, 600)},
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_complexity_chart(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render a complexity comparison chart."""
        complexities = data.get('complexities', [])
        config = data.get('config', {})
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Prepare chart data
        chart_data = []
        for comp in complexities:
            chart_data.append({
                'name': comp.get('name', 'Unknown'),
                'time_complexity': comp.get('time_complexity', 'O(n)'),
                'space_complexity': comp.get('space_complexity', 'O(n)'),
                'n_10': comp.get('operations_at_n10', 0),
                'n_100': comp.get('operations_at_n100', 0),
                'n_1000': comp.get('operations_at_n1000', 0),
                'color': colors['primary']
            })
        
        # Complexity curve points for visualization
        curves = self._generate_complexity_curves()
        
        return {
            'type': 'complexity-chart',
            'data': chart_data,
            'curves': curves,
            'config': {
                'show_labels': config.get('show_labels', True),
                'log_scale': config.get('log_scale', True),
                'comparisons': config.get('comparisons', True)
            },
            'colors': colors,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_sort_animation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render sorting animation data."""
        array = data.get('array', [])
        sort_type = data.get('sort_type', 'bubble')
        steps = data.get('steps', [])
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        # Generate animation frames
        frames = []
        for i, step in enumerate(steps):
            frames.append({
                'frame': i,
                'array': step.get('array', array),
                'highlight': step.get('highlight', []),
                'swap': step.get('swap'),
                'compare': step.get('compare'),
                'description': step.get('description', f'Step {i}'),
                'duration_ms': data.get('duration_per_frame', 500)
            })
        
        return {
            'type': 'sort-animation',
            'sort_type': sort_type,
            'initial_array': array,
            'frames': frames,
            'total_frames': len(frames),
            'config': {
                'duration_per_frame': data.get('duration_per_frame', 500),
                'show_comparisons': True,
                'show_swaps': True
            },
            'colors': colors,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_search_animation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render searching animation data."""
        array = data.get('array', [])
        target = data.get('target')
        search_type = data.get('search_type', 'linear')
        steps = data.get('steps', [])
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        frames = []
        for i, step in enumerate(steps):
            frames.append({
                'frame': i,
                'index': step.get('index'),
                'value': step.get('value'),
                'checked': step.get('checked', []),
                'found': step.get('found', False),
                'description': step.get('description', f'Checking index {step.get("index", i)}'),
                'duration_ms': data.get('duration_per_frame', 500)
            })
        
        return {
            'type': 'search-animation',
            'search_type': search_type,
            'target': target,
            'initial_array': array,
            'frames': frames,
            'total_frames': len(frames),
            'found_at': next((f['index'] for f in frames if f.get('found')), None),
            'colors': colors,
            'timestamp': datetime.now().isoformat()
        }
    
    def _render_traversal_animation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Render graph traversal animation (DFS/BFS)."""
        graph = data.get('graph', {})
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        traversal_type = data.get('traversal_type', 'dfs')
        steps = data.get('steps', [])
        
        colors = self._color_schemes.get(data.get('color_scheme', 'default'), self._color_schemes['default'])
        
        frames = []
        for i, step in enumerate(steps):
            frames.append({
                'frame': i,
                'visited': step.get('visited', []),
                'current': step.get('current'),
                'queue': step.get('queue', []),  # For BFS
                'stack': step.get('stack', []),  # For DFS
                'frontier': step.get('frontier', []),
                'description': step.get('description', f'Step {i}'),
                'duration_ms': data.get('duration_per_frame', 1000)
            })
        
        return {
            'type': f'{traversal_type}-animation',
            'nodes': nodes,
            'edges': edges,
            'traversal_type': traversal_type,
            'frames': frames,
            'total_frames': len(frames),
            'order': data.get('order', []),
            'colors': colors,
            'timestamp': datetime.now().isoformat()
        }
    
    # Helper methods
    
    def _layout_flowchart_nodes(
        self,
        nodes: List[Dict[str, Any]],
        direction: str,
        node_style: str
    ) -> List[Dict[str, Any]]:
        """Layout flowchart nodes in specified direction."""
        positioned = []
        y_offset = 50
        x_offset = 400
        spacing = 80 if direction == 'vertical' else 120
        
        for i, node in enumerate(nodes):
            if direction == 'vertical':
                positioned.append({
                    'id': node.get('id', i),
                    'label': node.get('label', f'Node {i}'),
                    'type': node.get('type', 'process'),
                    'x': x_offset,
                    'y': y_offset + i * spacing,
                    'width': 120,
                    'height': 50,
                    'style': node_style
                })
            else:
                positioned.append({
                    'id': node.get('id', i),
                    'label': node.get('label', f'Node {i}'),
                    'type': node.get('type', 'process'),
                    'x': x_offset + i * spacing,
                    'y': y_offset,
                    'width': 120,
                    'height': 50,
                    'style': node_style
                })
        
        return positioned
    
    def _calculate_flowchart_dimensions(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Calculate flowchart dimensions."""
        if not nodes:
            return {'width': 800, 'height': 600}
        
        max_x = max(n.get('x', 0) + n.get('width', 120) for n in nodes)
        max_y = max(n.get('y', 0) + n.get('height', 50) for n in nodes)
        
        return {'width': max(max_x + 50, 800), 'height': max(max_y + 50, 600)}
    
    def _circular_layout(
        self,
        nodes: List[Dict[str, Any]],
        center_x: float,
        center_y: float,
        radius: float
    ) -> Dict[int, Dict[str, float]]:
        """Calculate circular positions for nodes."""
        positions = {}
        n = len(nodes)
        if n == 0:
            return positions
        
        for i in range(n):
            angle = (2 * math.pi * i) / n - math.pi / 2
            positions[i] = {
                'x': center_x + radius * math.cos(angle),
                'y': center_y + radius * math.sin(angle)
            }
        
        return positions
    
    def _force_directed_layout(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        center_x: float,
        center_y: float,
        width: float,
        height: float
    ) -> Dict[int, Dict[str, float]]:
        """Calculate force-directed layout positions."""
        positions = {}
        n = len(nodes)
        
        if n == 0:
            return positions
        
        # Initialize positions
        for i in range(n):
            positions[i] = {
                'x': center_x + (hash(str(i)) % 200 - 100),
                'y': center_y + (hash(str(i) + 'y') % 200 - 100)
            }
        
        # Simple iteration to spread nodes
        for _ in range(50):
            for i in range(n):
                force_x, force_y = 0, 0
                
                # Repulsion between all nodes
                for j in range(n):
                    if i != j:
                        dx = positions[i]['x'] - positions[j]['x']
                        dy = positions[i]['y'] - positions[j]['y']
                        dist = max(0.1, (dx ** 2 + dy ** 2) ** 0.5)
                        force_x += dx / dist * 10
                        force_y += dy / dist * 10
                
                # Attraction along edges
                for edge in edges:
                    for node_idx in [edge.get('from'), edge.get('to')]:
                        if node_idx == i:
                            other = edge.get('to') if node_idx == edge.get('from') else edge.get('from')
                            if other in positions:
                                dx = positions[other]['x'] - positions[i]['x']
                                dy = positions[other]['y'] - positions[i]['y']
                                force_x += dx * 0.01
                                force_y += dy * 0.01
                
                positions[i]['x'] += force_x * 0.1
                positions[i]['y'] += force_y * 0.1
        
        return positions
    
    def _tokenize_line(
        self,
        line: str,
        language: str,
        rules: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Tokenize a line of code for syntax highlighting."""
        tokens = []
        
        # Split by keywords
        for keyword in rules.get('keywords', []):
            if keyword in line:
                tokens.append({'type': 'keyword', 'value': keyword})
        
        # Find strings
        for delim in rules.get('string_delimiters', []):
            pattern = f'{delim}.*?{delim}'
            matches = re.findall(pattern, line)
            for match in matches:
                tokens.append({'type': 'string', 'value': match})
        
        # Find comments
        comment = rules.get('comment', '#')
        if comment in line:
            idx = line.index(comment)
            tokens.append({'type': 'comment', 'value': line[idx:]})
        
        return tokens
    
    def _generate_complexity_curves(self) -> Dict[str, List[Dict[str, float]]]:
        """Generate curve points for complexity visualization."""
        n_values = [1, 10, 50, 100, 500, 1000]
        
        curves = {
            'O(1)': [{'n': n, 'ops': 1} for n in n_values],
            'O(log n)': [{'n': n, 'ops': math.log2(n) if n > 0 else 0} for n in n_values],
            'O(n)': [{'n': n, 'ops': n} for n in n_values],
            'O(n log n)': [{'n': n, 'ops': n * math.log2(n) if n > 0 else 0} for n in n_values],
            'O(n²)': [{'n': n, 'ops': n ** 2} for n in n_values],
        }
        
        return curves


def create_algo_visual_service(config: Optional[Dict[str, Any]] = None) -> AlgoVerseVisualService:
    """
    Factory function to create an AlgoVerse visual service.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured AlgoVerseVisualService instance
    """
    return AlgoVerseVisualService(config)
