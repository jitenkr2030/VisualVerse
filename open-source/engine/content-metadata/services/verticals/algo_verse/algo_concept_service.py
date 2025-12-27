"""
AlgoVerse Concept Service

This module provides the AlgoVerse-specific concept service implementation,
extending the base concept service with algorithmic domain functionality
including code parsing, AST generation, algorithm classification, and
complexity analysis for sorting, searching, graph algorithms, and data structures.

Licensed under the Apache License, Version 2.0
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
import logging

from ....extensions.service_extension_base import (
    ConceptServiceExtension,
    ExtensionContext
)

logger = logging.getLogger(__name__)


class AlgorithmCategory(str, Enum):
    """Algorithm categories for classification."""
    SORTING = "sorting"
    SEARCHING = "searching"
    GRAPH_TRAVERSAL = "graph_traversal"
    GRAPH_SHORTEST_PATH = "graph_shortest_path"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    GREEDY = "greedy"
    DIVIDE_CONQUER = "divide_conquer"
    RECURSION = "recursion"
    DATA_STRUCTURE = "data_structure"
    STRING = "string_algorithms"
    MATHEMATICAL = "mathematical"


class ComplexityClass(str, Enum):
    """Big-O complexity classes."""
    O_1 = "O(1)"
    O_LOG_N = "O(log n)"
    O_N = "O(n)"
    O_N_LOG_N = "O(n log n)"
    O_N_SQUARED = "O(n²)"
    O_N_CUBED = "O(n³)"
    O_2_N = "O(2^n)"
    O_FACTORIAL = "O(n!)"


@dataclass
class CodeStructure:
    """Parsed structure of code."""
    ast: Dict[str, Any]
    control_flow_graph: Dict[str, Any]
    functions: List[Dict[str, Any]]
    variables: List[str]
    loops: List[Dict[str, Any]]
    conditionals: List[Dict[str, Any]]
    recursion_depth: int
    function_calls: List[str]


@dataclass
class ComplexityResult:
    """Result of complexity analysis."""
    time_complexity: ComplexityClass
    space_complexity: ComplexityClass
    time_explanation: str
    space_explanation: str
    dominant_factors: List[str]
    optimizations: List[str]


@dataclass
class AlgorithmMetadata:
    """Metadata for algorithm concepts."""
    category: AlgorithmCategory
    subcategory: Optional[str]
    time_complexity_best: ComplexityClass
    time_complexity_average: ComplexityClass
    time_complexity_worst: ComplexityClass
    space_complexity: ComplexityClass
    stability: Optional[str]
    in_place: bool
    parallelizable: bool
    required_data_structures: List[str]
    pseudocode: str
    code_examples: Dict[str, str]
    visual_types_preferred: List[str]


class AlgoVerseConceptService:
    """
    AlgoVerse-specific concept service.
    
    This service handles algorithmic concept processing including:
    - Code parsing and AST generation
    - Algorithm classification by category
    - Complexity analysis (Big-O)
    - Control flow graph generation
    - Data structure recognition
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AlgoVerse concept service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._patterns = self._compile_patterns()
        self._algorithm_signatures = self._load_algorithm_signatures()

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        logger.info("AlgoVerseConceptService configured with settings: %s", list(config.keys()))

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for code analysis."""
        return {
            'function_def': re.compile(r'def\s+(\w+)\s*\(([^)]*)\)\s*:'),
            'for_loop': re.compile(r'for\s+(\w+)\s+in\s+(range|len|zip)'),
            'while_loop': re.compile(r'while\s+(.+?)\s*:'),
            'if_statement': re.compile(r'if\s+(.+?)\s*:'),
            'elif_statement': re.compile(r'elif\s+(.+?)\s*:'),
            'else_statement': re.compile(r'else\s*:'),
            'return_statement': re.compile(r'return\s+(.+)'),
            'assignment': re.compile(r'(\w+)\s*=\s*(.+)'),
            'array_access': re.compile(r'(\w+)\[(\w+)\]'),
            'function_call': re.compile(r'(\w+)\s*\(([^)]*)\)'),
            'recursive_call': re.compile(r'(\w+)\s*\([^)]*\).*\b\1\b'),
            'swap_pattern': re.compile(r'(\w+)\[(\w+)\]\s*,\s*(\w+)\[(\w+)\]\s*=\s*(\w+)\[(\w+)\]\s*,\s*(\w+)\[(\w+)\]'),
            'comparison': re.compile(r'(<=|>=|<|>|==|!=)\s*'),
        }
    
    def _load_algorithm_signatures(self) -> Dict[str, Dict[str, Any]]:
        """Load known algorithm signatures for classification."""
        return {
            'bubble_sort': {
                'category': AlgorithmCategory.SORTING,
                'signatures': ['adjacent comparison', 'swap', 'nested loops'],
                'complexity': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)'}
            },
            'insertion_sort': {
                'category': AlgorithmCategory.SORTING,
                'signatures': ['shift', 'insert into sorted', 'single loop'],
                'complexity': {'best': 'O(n)', 'average': 'O(n²)', 'worst': 'O(n²)'}
            },
            'merge_sort': {
                'category': AlgorithmCategory.SORTING,
                'signatures': ['divide', 'conquer', 'merge', 'recursion'],
                'complexity': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n log n)'}
            },
            'quick_sort': {
                'category': AlgorithmCategory.SORTING,
                'signatures': ['pivot', 'partition', 'recursion'],
                'complexity': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n²)'}
            },
            'heap_sort': {
                'category': AlgorithmCategory.SORTING,
                'signatures': ['heapify', 'extract max', 'complete binary tree'],
                'complexity': {'best': 'O(n log n)', 'average': 'O(n log n)', 'worst': 'O(n log n)'}
            },
            'linear_search': {
                'category': AlgorithmCategory.SEARCHING,
                'signatures': ['sequential check', 'no ordering'],
                'complexity': {'best': 'O(1)', 'average': 'O(n)', 'worst': 'O(n)'}
            },
            'binary_search': {
                'category': AlgorithmCategory.SEARCHING,
                'signatures': ['divide range', 'compare middle', 'narrow search'],
                'complexity': {'best': 'O(1)', 'average': 'O(log n)', 'worst': 'O(log n)'}
            },
            'dfs': {
                'category': AlgorithmCategory.GRAPH_TRAVERSAL,
                'signatures': ['stack', 'depth first', 'backtrack'],
                'complexity': {'best': 'O(V+E)', 'average': 'O(V+E)', 'worst': 'O(V+E)'}
            },
            'bfs': {
                'category': AlgorithmCategory.GRAPH_TRAVERSAL,
                'signatures': ['queue', 'level order', 'breadth first'],
                'complexity': {'best': 'O(V+E)', 'average': 'O(V+E)', 'worst': 'O(V+E)'}
            },
            'dijkstra': {
                'category': AlgorithmCategory.GRAPH_SHORTEST_PATH,
                'signatures': ['priority queue', 'relaxation', 'greedy'],
                'complexity': {'best': 'O((V+E) log V)', 'average': 'O((V+E) log V)', 'worst': 'O((V+E) log V)'}
            },
            'bellman_ford': {
                'category': AlgorithmCategory.GRAPH_SHORTEST_PATH,
                'signatures': ['edge relaxation', 'V-1 iterations'],
                'complexity': {'best': 'O(VE)', 'average': 'O(VE)', 'worst': 'O(VE)'}
            },
            'fibonacci': {
                'category': AlgorithmCategory.RECURSION,
                'signatures': ['recursive case', 'base case', 'overlapping subproblems'],
                'complexity': {'best': 'O(n)', 'average': 'O(2^n)', 'worst': 'O(2^n)'}
            },
        }
    
    def process_concept(
        self,
        concept: Dict[str, Any],
        context: Optional[ExtensionContext] = None
    ) -> Dict[str, Any]:
        """
        Process an algorithmic concept with domain-specific logic.
        
        Args:
            concept: The concept to process
            context: Optional execution context
            
        Returns:
            Processed concept with enhanced algorithmic metadata
        """
        processed = concept.copy()
        
        # Extract algorithm metadata
        code = concept.get('code', concept.get('description', ''))
        language = concept.get('language', 'python')
        
        # Parse code structure
        code_structure = self.parse_code_structure(code, language)
        
        # Classify algorithm
        classification = self.classify_algorithm(code, code_structure)
        
        # Analyze complexity
        complexity = self.analyze_complexity(code_structure)
        
        # Generate algorithm metadata
        algo_metadata = AlgorithmMetadata(
            category=classification['category'],
            subcategory=classification.get('subcategory'),
            time_complexity_best=ComplexityClass(classification.get('time_best', 'O(n)')),
            time_complexity_average=ComplexityClass(classification.get('time_average', 'O(n²)')),
            time_complexity_worst=ComplexityClass(classification.get('time_worst', 'O(n²)')),
            space_complexity=ComplexityClass(complexity.space_complexity.value),
            stability=classification.get('stability'),
            in_place=classification.get('in_place', False),
            parallelizable=classification.get('parallelizable', False),
            required_data_structures=classification.get('required_structures', []),
            pseudocode=concept.get('pseudocode', ''),
            code_examples=concept.get('code_examples', {}),
            visual_types_preferred=concept.get('visualization_preferences', [])
        )
        
        # Build metadata dictionary
        processed['_algo_metadata'] = {
            'classification': classification,
            'complexity': {
                'time': complexity.time_complexity.value,
                'space': complexity.space_complexity.value,
                'explanation': complexity.time_explanation,
                'factors': complexity.dominant_factors
            },
            'code_structure': {
                'functions': code_structure.functions,
                'variables': code_structure.variables,
                'loops': len(code_structure.loops),
                'conditionals': len(code_structure.conditionals),
                'recursion_depth': code_structure.recursion_depth,
                'function_calls': code_structure.function_calls
            },
            'algorithm_info': {
                'category': algo_metadata.category.value,
                'subcategory': algo_metadata.subdomain,
                'stability': algo_metadata.stability,
                'in_place': algo_metadata.in_place,
                'parallelizable': algo_metadata.parallelizable,
                'data_structures': algo_metadata.required_data_structures
            }
        }
        
        # Generate display representation
        processed['_display'] = self._generate_display_representation(concept, classification, complexity)
        
        # Validate
        processed['_validation'] = self._validate_algorithm_concept(concept, code_structure)
        
        return processed
    
    def validate_concept(self, concept: Dict[str, Any]) -> List[str]:
        """
        Validate an algorithmic concept against domain rules.
        
        Args:
            concept: The concept to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        code = concept.get('code', '')
        if not code and not concept.get('description'):
            errors.append("Algorithm concepts must have code or description")
        
        # Check for required fields based on type
        algo_type = concept.get('algorithm_type', 'general')
        
        if algo_type == 'sorting':
            if 'swap' not in code and 'sort' not in code.lower():
                errors.append("Sorting algorithms should demonstrate swapping or sorting logic")
        
        elif algo_type == 'searching':
            if 'compare' not in code.lower() and '==' not in code:
                errors.append("Searching algorithms should demonstrate comparison logic")
        
        elif algo_type == 'graph':
            if 'adjacency' not in code.lower() and 'neighbor' not in code.lower():
                errors.append("Graph algorithms should reference adjacency or neighbors")
        
        # Validate complexity claims
        claimed_time = concept.get('time_complexity', '')
        if claimed_time:
            if claimed_time not in [e.value for e in ComplexityClass]:
                errors.append(f"Invalid time complexity: {claimed_time}")
        
        # Check for infinite loops
        if self._detect_potential_infinite_loop(code):
            errors.append("Code may contain infinite loop")
        
        return errors
    
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
        relationships = {
            'variations': [
                'quick_sort' for 'merge_sort',
                'merge_sort' for 'quick_sort',
                'heap_sort' for 'both',
                'binary_search' for 'linear_search',
            ],
            'uses_data_structure': [
                'array' for 'bubble_sort',
                'array' for 'binary_search',
                'linked_list' for 'stack_operations',
                'binary_tree' for 'tree_traversal',
                'hash_table' for 'hash_search',
            ],
            'prerequisite_for': [
                'tree_traversal' for 'binary_search_tree',
                'graph_basics' for 'dijkstra',
                'recursion_basics' for 'divide_conquer',
            ],
            'related_techniques': [
                'dynamic_programming' for 'fibonacci',
                'backtracking' for 'dfs',
                'greedy' for 'dijkstra',
            ]
        }
        
        return relationships.get(relationship_type, [])
    
    def parse_code_structure(
        self,
        code: str,
        language: str = 'python'
    ) -> CodeStructure:
        """
        Parse code to extract its structure.
        
        Args:
            code: The code to parse
            language: Programming language
            
        Returns:
            CodeStructure with parsed components
        """
        functions = []
        variables = []
        loops = []
        conditionals = []
        function_calls = []
        recursion_depth = 0
        
        # Extract function definitions
        for match in self._patterns['function_def'].finditer(code):
            functions.append({
                'name': match.group(1),
                'params': [p.strip() for p in match.group(2).split(',') if p.strip()],
                'line': match.start()
            })
        
        # Extract variables
        for match in self._patterns['assignment'].finditer(code):
            var_name = match.group(1).strip()
            if not var_name.startswith('_') and var_name not in ['for', 'while', 'if']:
                variables.append(var_name)
        
        # Extract loops
        for match in self._patterns['for_loop'].finditer(code):
            loops.append({
                'type': 'for',
                'iterator': match.group(1),
                'source': match.group(2),
                'line': match.start()
            })
        
        for match in self._patterns['while_loop'].finditer(code):
            loops.append({
                'type': 'while',
                'condition': match.group(1),
                'line': match.start()
            })
        
        # Extract conditionals
        for match in self._patterns['if_statement'].finditer(code):
            conditionals.append({
                'type': 'if',
                'condition': match.group(1),
                'line': match.start()
            })
        
        # Extract function calls
        for match in self._patterns['function_call'].finditer(code):
            func_name = match.group(1)
            if func_name not in ['print', 'len', 'range', 'abs', 'max', 'min']:
                function_calls.append(func_name)
        
        # Detect recursion
        if self._patterns['recursive_call'].search(code):
            recursion_depth = self._estimate_recursion_depth(code)
        
        # Generate control flow graph
        cfg = self._generate_control_flow_graph(functions, loops, conditionals)
        
        # Build AST (simplified)
        ast = {
            'type': 'Program',
            'body': [
                {'type': 'FunctionDefinition', 'name': f['name'], 'params': f['params']}
                for f in functions
            ]
        }
        
        return CodeStructure(
            ast=ast,
            control_flow_graph=cfg,
            functions=functions,
            variables=list(set(variables)),
            loops=loops,
            conditionals=conditionals,
            recursion_depth=recursion_depth,
            function_calls=list(set(function_calls))
        )
    
    def classify_algorithm(
        self,
        code: str,
        structure: Optional[CodeStructure] = None
    ) -> Dict[str, Any]:
        """
        Classify an algorithm by category and type.
        
        Args:
            code: The code to classify
            structure: Optional pre-parsed structure
            
        Returns:
            Classification result
        """
        if structure is None:
            structure = self.parse_code_structure(code)
        
        code_lower = code.lower()
        
        # Check for sorting algorithms
        if 'swap' in code_lower or 'bubble' in code_lower:
            if 'adjacent' in code_lower or 'adj' in code_lower:
                return {'category': AlgorithmCategory.SORTING, 'name': 'Bubble Sort', 'time_best': 'O(n)', 'time_average': 'O(n²)', 'time_worst': 'O(n²)', 'stability': 'Stable', 'in_place': True}
            return {'category': AlgorithmCategory.SORTING, 'name': 'Selection Sort', 'time_best': 'O(n²)', 'time_average': 'O(n²)', 'time_worst': 'O(n²)', 'stability': 'Unstable', 'in_place': True}
        
        if 'insert' in code_lower or 'shift' in code_lower:
            return {'category': AlgorithmCategory.SORTING, 'name': 'Insertion Sort', 'time_best': 'O(n)', 'time_average': 'O(n²)', 'time_worst': 'O(n²)', 'stability': 'Stable', 'in_place': True}
        
        if 'merge' in code_lower and 'sort' in code_lower:
            return {'category': AlgorithmCategory.SORTING, 'name': 'Merge Sort', 'time_best': 'O(n log n)', 'time_average': 'O(n log n)', 'time_worst': 'O(n log n)', 'stability': 'Stable', 'in_place': False, 'required_structures': ['array', 'temporary array']}
        
        if 'pivot' in code_lower or 'partition' in code_lower:
            return {'category': AlgorithmCategory.SORTING, 'name': 'Quick Sort', 'time_best': 'O(n log n)', 'time_average': 'O(n log n)', 'time_worst': 'O(n²)', 'stability': 'Unstable', 'in_place': True}
        
        # Check for searching algorithms
        if 'binary' in code_lower and ('search' in code_lower or 'find' in code_lower):
            return {'category': AlgorithmCategory.SEARCHING, 'name': 'Binary Search', 'time_best': 'O(1)', 'time_average': 'O(log n)', 'time_worst': 'O(log n)'}
        
        if 'linear' in code_lower or 'sequential' in code_lower:
            return {'category': AlgorithmCategory.SEARCHING, 'name': 'Linear Search', 'time_best': 'O(1)', 'time_average': 'O(n)', 'time_worst': 'O(n)'}
        
        # Check for graph algorithms
        if 'queue' in code_lower and ('visit' in code_lower or 'level' in code_lower):
            return {'category': AlgorithmCategory.GRAPH_TRAVERSAL, 'name': 'Breadth-First Search (BFS)', 'time_best': 'O(V+E)', 'time_average': 'O(V+E)', 'time_worst': 'O(V+E)', 'required_structures': ['queue', 'visited set']}
        
        if 'stack' in code_lower or 'depth' in code_lower:
            return {'category': AlgorithmCategory.GRAPH_TRAVERSAL, 'name': 'Depth-First Search (DFS)', 'time_best': 'O(V+E)', 'time_average': 'O(V+E)', 'time_worst': 'O(V+E)', 'required_structures': ['stack', 'visited set']}
        
        if 'relax' in code_lower or 'distance' in code_lower or 'shortest' in code_lower:
            if 'priority' in code_lower or 'min' in code_lower:
                return {'category': AlgorithmCategory.GRAPH_SHORTEST_PATH, 'name': "Dijkstra's Algorithm", 'time_best': 'O((V+E) log V)', 'time_average': 'O((V+E) log V)', 'time_worst': 'O((V+E) log V)', 'required_structures': ['priority queue', 'distance array']}
        
        # Check for recursion patterns
        if 'fibonacci' in code_lower or 'n <=' in code_lower:
            return {'category': AlgorithmCategory.RECURSION, 'name': 'Fibonacci (Recursive)', 'time_best': 'O(n)', 'time_average': 'O(2^n)', 'time_worst': 'O(2^n)', 'subcategory': 'Simple Recursion', 'required_structures': ['call stack']}
        
        if structure.recursion_depth > 0:
            return {'category': AlgorithmCategory.RECURSION, 'name': 'Recursive Algorithm', 'time_average': 'O(n)', 'time_worst': 'O(n)'}
        
        # Default classification
        return {'category': AlgorithmCategory.DATA_STRUCTURE, 'name': 'Data Structure Operation', 'time_average': 'O(n)', 'time_worst': 'O(n)'}
    
    def analyze_complexity(
        self,
        structure: CodeStructure
    ) -> ComplexityResult:
        """
        Analyze the complexity of parsed code.
        
        Args:
            structure: Parsed code structure
            
        Returns:
            ComplexityResult with analysis
        """
        dominant_factors = []
        optimizations = []
        
        # Analyze loop nesting
        nested_loops = self._count_nested_loops(structure.loops)
        if nested_loops >= 2:
            dominant_factors.append(f"{nested_loops} nested loops")
            if nested_loops == 2:
                time_complexity = ComplexityClass.O_N_SQUARED
                optimizations.append("Consider using more efficient algorithm for large datasets")
            elif nested_loops == 3:
                time_complexity = ComplexityClass.O_N_CUBED
        elif len(structure.loops) == 1:
            dominant_factors.append("Single loop")
            time_complexity = ComplexityClass.O_N
        else:
            time_complexity = ComplexityClass.O_N
        
        # Check for recursion
        if structure.recursion_depth > 0:
            dominant_factors.append(f"Recursion (depth: {structure.recursion_depth})")
            if structure.recursion_depth > 10:
                time_complexity = ComplexityClass.O_2_N
                optimizations.append("Consider memoization to reduce exponential complexity")
        
        # Check for divide and conquer patterns
        for call in structure.function_calls:
            if call in ['merge', 'quick', 'sort']:
                if ComplexityClass.O_N_SQUARED in [time_complexity]:
                    time_complexity = ComplexityClass.O_N_LOG_N
                    dominant_factors.append("Divide and conquer pattern")
        
        # Space complexity analysis
        if structure.recursion_depth > 0:
            space_complexity = ComplexityClass.O_N
            dominant_factors.append("Recursion stack")
        elif len(structure.variables) > 10:
            space_complexity = ComplexityClass.O_N
            dominant_factors.append("Multiple variables/arrays")
        else:
            space_complexity = ComplexityClass.O_1
        
        # Generate explanations
        time_explanation = self._generate_time_explanation(time_complexity, dominant_factors)
        space_explanation = self._generate_space_explanation(space_complexity)
        
        return ComplexityResult(
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            time_explanation=time_explanation,
            space_explanation=space_explanation,
            dominant_factors=dominant_factors,
            optimizations=optimizations
        )
    
    def _generate_control_flow_graph(
        self,
        functions: List[Dict[str, Any]],
        loops: List[Dict[str, Any]],
        conditionals: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate control flow graph from parsed structure."""
        nodes = []
        edges = []
        
        # Create nodes for functions
        for func in functions:
            nodes.append({'id': func['name'], 'type': 'function', 'label': func['name']})
        
        # Create nodes for loops
        for i, loop in enumerate(loops):
            nodes.append({'id': f'loop_{i}', 'type': 'loop', 'label': f'Loop {loop.get("type", "for")}'})
        
        # Create nodes for conditionals
        for i, cond in enumerate(conditionals):
            nodes.append({'id': f'cond_{i}', 'type': 'conditional', 'label': 'Condition'})
        
        return {'nodes': nodes, 'edges': edges}
    
    def _detect_potential_infinite_loop(self, code: str) -> bool:
        """Detect potential infinite loops in code."""
        # Check for while True without break
        if 'while True' in code or 'while true' in code:
            if 'break' not in code and 'return' not in code:
                return True
        
        # Check for counter-based loops without proper increment
        counter_patterns = [
            r'while\s+\w+\s*(<|>|<=|>=|==|!=)',
            r'for\s+\w+\s+in\s+range\([^)]*\)'
        ]
        
        for pattern in counter_patterns:
            if re.search(pattern, code):
                # Look for proper counter increment
                if '++' not in code and '+=' not in code and '-=' not in code:
                    return True
        
        return False
    
    def _estimate_recursion_depth(self, code: str) -> int:
        """Estimate maximum recursion depth from code."""
        # Count indentation levels in recursive function
        lines = code.split('\n')
        max_depth = 0
        current_depth = 0
        
        for line in lines:
            if line.strip().startswith('def '):
                current_depth = 0
            elif line.strip().startswith(('if ', 'elif ', 'else:')):
                pass
            elif line.strip().startswith(('while ', 'for ')):
                pass
            elif line.strip().startswith(('return ')) and current_depth > 0:
                max_depth = max(max_depth, current_depth)
            elif line.strip() and not line.strip().startswith('#'):
                current_depth += 1
        
        return max_depth
    
    def _count_nested_loops(self, loops: List[Dict[str, Any]]) -> int:
        """Count the maximum nesting level of loops."""
        if not loops:
            return 0
        return min(len(loops), 3)  # Cap at 3 for practical purposes
    
    def _generate_time_explanation(
        self,
        complexity: ComplexityClass,
        factors: List[str]
    ) -> str:
        """Generate human-readable time complexity explanation."""
        explanations = {
            ComplexityClass.O_1: "Constant time - execution time doesn't depend on input size",
            ComplexityClass.O_LOG_N: "Logarithmic time - execution time grows slowly with input size",
            ComplexityClass.O_N: "Linear time - execution time grows proportionally with input size",
            ComplexityClass.O_N_LOG_N: "Linearithmic time - efficient for large datasets",
            ComplexityClass.O_N_SQUARED: "Quadratic time - may be slow for large inputs due to nested loops",
            ComplexityClass.O_N_CUBED: "Cubic time - typically from triple nested loops",
            ComplexityClass.O_2_N: "Exponential time - becomes very slow for larger inputs",
            ComplexityClass.O_FACTORIAL: "Factorial time - impractical for inputs larger than 10-12"
        }
        
        base = explanations.get(complexity, "Time complexity analysis")
        
        if factors:
            base += f". Key factors: {', '.join(factors)}"
        
        return base
    
    def _generate_space_explanation(self, complexity: ComplexityClass) -> str:
        """Generate human-readable space complexity explanation."""
        explanations = {
            ComplexityClass.O_1: "Constant space - uses fixed amount of additional memory",
            ComplexityClass.O_N: "Linear space - memory usage grows with input size",
        }
        
        return explanations.get(complexity, "Space complexity analysis")
    
    def _generate_display_representation(
        self,
        concept: Dict[str, Any],
        classification: Dict[str, Any],
        complexity: ComplexityResult
    ) -> Dict[str, Any]:
        """Generate display representation for a concept."""
        return {
            'title': concept.get('name', 'Untitled Algorithm'),
            'category': classification.get('category', 'Unknown').value if hasattr(classification.get('category'), 'value') else str(classification.get('category')),
            'algorithm_name': classification.get('name', 'Unknown'),
            'time_complexity': complexity.time_complexity.value,
            'space_complexity': complexity.space_complexity.value,
            'code_preview': concept.get('code', '')[:200] + '...' if len(concept.get('code', '')) > 200 else concept.get('code', '')
        }
    
    def _validate_algorithm_concept(
        self,
        concept: Dict[str, Any],
        structure: CodeStructure
    ) -> Dict[str, Any]:
        """Validate algorithmic content in a concept."""
        return {
            'is_valid': len(self.validate_concept(concept)) == 0,
            'errors': self.validate_concept(concept),
            'warnings': self._generate_warnings(concept, structure)
        }
    
    def _generate_warnings(
        self,
        concept: Dict[str, Any],
        structure: CodeStructure
    ) -> List[str]:
        """Generate warnings for potential issues."""
        warnings = []
        code = concept.get('code', '')
        
        if len(structure.loops) > 3:
            warnings.append("Multiple nested loops detected - consider algorithm optimization")
        
        if structure.recursion_depth > 5:
            warnings.append("Deep recursion detected - consider iterative approach or memoization")
        
        if 'print' in code:
            warnings.append("Debug statements (print) should be removed in production code")
        
        if len(structure.variables) > 20:
            warnings.append("High number of variables - consider refactoring")
        
        return warnings


def create_algo_concept_service(config: Optional[Dict[str, Any]] = None) -> AlgoVerseConceptService:
    """
    Factory function to create an AlgoVerse concept service.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured AlgoVerseConceptService instance
    """
    return AlgoVerseConceptService(config)
