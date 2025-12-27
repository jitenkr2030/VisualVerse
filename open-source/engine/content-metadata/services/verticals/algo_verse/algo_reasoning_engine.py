"""
AlgoVerse Reasoning Engine

This module provides comprehensive algorithm analysis and reasoning capabilities for
the AlgoVerse platform. It serves as the intellectual core for algorithm education,
offering complexity analysis, correctness verification, optimization suggestions,
step-by-step explanation generation, and interactive problem-solving assistance.

The reasoning engine is designed to help learners understand not just how algorithms
work, but why they work - providing mathematical foundations, edge case analysis,
and comparative evaluations across different algorithmic approaches.

Key Features:
- Time and space complexity analysis with Big O notation
- Correctness verification through formal reasoning
- Step-by-step algorithm explanation generation
- Optimization suggestions and alternative approaches
- Edge case identification and handling guidance
- Comparative algorithm analysis
- Interactive problem-solving assistance
"""

from typing import Any, Dict, List, Optional, Tuple, Set, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import ast
import copy


class ComplexityClass(Enum):
    """Enumeration of algorithm complexity classes."""
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEARITHMIC = "O(n log n)"
    QUADRATIC = "O(n²)"
    CUBIC = "O(n³)"
    POLYNOMIAL = "O(n^k)"
    EXPONENTIAL = "O(2^n)"
    FACTORIAL = "O(n!)"
    QUASI_LINEAR = "O(n log n)"
    LOG_SQUARED = "O(log² n)"


class AlgorithmCategory(Enum):
    """Enumeration of algorithm categories."""
    SORTING = "sorting"
    SEARCHING = "searching"
    GRAPH = "graph"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    GREEDY = "greedy"
    DIVIDE_AND_CONQUER = "divide_and_conquer"
    BACKTRACKING = "backtracking"
    RECURSION = "recursion"
    DATA_STRUCTURE = "data_structure"


class CorrectnessStatus(Enum):
    """Status of algorithm correctness verification."""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    UNVERIFIED = "unverified"
    HAS_ERRORS = "has_errors"


@dataclass
class ComplexityAnalysis:
    """
    Represents the complexity analysis of an algorithm.
    
    Attributes:
        time_complexity: Best case time complexity
        average_time_complexity: Average case time complexity
        worst_time_complexity: Worst case time complexity
        space_complexity: Space complexity
        auxiliary_space: Extra space used (excluding input)
        time_complexity_class: Complexity class enumeration
        space_complexity_class: Space complexity class enumeration
        factors: List of factors affecting complexity
        explanation: Detailed explanation of the analysis
    """
    time_complexity: str = "O(1)"
    average_time_complexity: str = "O(1)"
    worst_time_complexity: str = "O(1)"
    space_complexity: str = "O(1)"
    auxiliary_space: str = "O(1)"
    time_complexity_class: ComplexityClass = ComplexityClass.CONSTANT
    space_complexity_class: ComplexityClass = ComplexityClass.CONSTANT
    factors: List[str] = field(default_factory=list)
    explanation: str = ""


@dataclass
class CorrectnessVerification:
    """
    Result of algorithm correctness verification.
    
    Attributes:
        status: Overall correctness status
        is_correct: Whether the algorithm is correct
        invariant: Loop invariant or mathematical invariant
        proof_steps: Steps in the correctness proof
        edge_cases: Identified edge cases
        counterexamples: Any found counterexamples
        termination_proof: Proof that the algorithm terminates
        partial_correctness: Proof of partial correctness
        total_correctness: Proof of total correctness
        issues: List of identified issues
        suggestions: List of suggested fixes
    """
    status: CorrectnessStatus = CorrectnessStatus.UNVERIFIED
    is_correct: bool = False
    invariant: Optional[str] = None
    proof_steps: List[str] = field(default_factory=list)
    edge_cases: List[str] = field(default_factory=list)
    counterexamples: List[Dict[str, Any]] = field(default_factory=list)
    termination_proof: str = ""
    partial_correctness: str = ""
    total_correctness: str = ""
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


@dataclass
class OptimizationSuggestion:
    """
    Represents an optimization suggestion for an algorithm.
    
    Attributes:
        suggestion_type: Type of optimization
        description: Detailed description of the optimization
        impact: Expected impact on complexity
        complexity_improvement: From-to complexity improvement
        code_change: Suggested code modification
        tradeoffs: Potential tradeoffs of the optimization
        implementation_difficulty: Difficulty level (1-5)
        benefits: List of benefits
        risks: List of potential risks
    """
    suggestion_type: str = ""
    description: str = ""
    impact: str = ""
    complexity_improvement: Tuple[str, str] = ("", "")
    code_change: Optional[str] = None
    tradeoffs: List[str] = field(default_factory=list)
    implementation_difficulty: int = 1
    benefits: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


@dataclass
class AlgorithmExplanation:
    """
    Complete explanation of an algorithm.
    
    Attributes:
        algorithm_name: Name of the algorithm
        category: Algorithm category
        description: High-level description
        how_it_works: Step-by-step explanation
        key_insights: Important concepts and insights
        mathematical_foundation: Mathematical basis
        intuition: Intuitive explanation
        real_world_applications: Practical applications
        related_algorithms: Related algorithm names
        pseudocode: Pseudocode representation
        when_to_use: Guidance on when to apply
        when_not_to_use: Guidance on when to avoid
    """
    algorithm_name: str = ""
    category: AlgorithmCategory = AlgorithmCategory.SORTING
    description: str = ""
    how_it_works: List[str] = field(default_factory=list)
    key_insights: List[str] = field(default_factory=list)
    mathematical_foundation: str = ""
    intuition: str = ""
    real_world_applications: List[str] = field(default_factory=list)
    related_algorithms: List[str] = field(default_factory=list)
    pseudocode: str = ""
    when_to_use: str = ""
    when_not_to_use: str = ""


@dataclass
class AlgorithmComparison:
    """
    Comparison between multiple algorithms.
    
    Attributes:
        algorithms: Names of algorithms being compared
        comparison_criteria: Criteria used for comparison
        comparison_results: Dictionary of comparisons
        winner: Recommended algorithm for general use
        tradeoffs: General tradeoffs
        recommendations: Specific recommendations for different scenarios
    """
    algorithms: List[str] = field(default_factory=list)
    comparison_criteria: List[str] = field(default_factory=list)
    comparison_results: Dict[str, Dict[str, str]] = field(default_factory=dict)
    winner: str = ""
    tradeoffs: List[str] = field(default_factory=list)
    recommendations: Dict[str, str] = field(default_factory=dict)


class AlgoVerseReasoningEngine:
    """
    Comprehensive reasoning engine for algorithm analysis and education.
    
    This engine provides deep analytical capabilities for understanding, verifying,
    and optimizing algorithms. It serves as an intelligent assistant for algorithm
    learning, helping students and developers understand the theoretical and
    practical aspects of algorithm design and analysis.
    
    The engine integrates multiple analysis modules:
    - Complexity Analysis: Time and space complexity determination
    - Correctness Verification: Formal verification of algorithm correctness
    - Optimization Engine: Suggestions for algorithmic improvements
    - Explanation Generator: Educational algorithm explanations
    - Comparison Engine: Comparative analysis of multiple algorithms
    
    Example:
        >>> engine = AlgoVerseReasoningEngine()
        >>> complexity = engine.analyze_complexity("bubble_sort")
        >>> verification = engine.verify_correctness([5, 2, 8, 1])
        >>> explanation = engine.generate_explanation("merge_sort")
    """
    
    def __init__(self):
        """Initialize the reasoning engine with analysis modules."""
        self.config = {}
        self._algorithm_knowledge = self._initialize_algorithm_knowledge()
        self._custom_analyzers: Dict[str, callable] = {}

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        print("AlgoVerseReasoningEngine configured with settings:", list(config.keys()))

    def _initialize_algorithm_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Initialize the knowledge base with algorithm information."""
        return {
            "bubble_sort": {
                "category": AlgorithmCategory.SORTING,
                "time_complexity": {"best": "O(n)", "average": "O(n²)", "worst": "O(n²)"},
                "space_complexity": "O(1)",
                "stability": True,
                "description": "Repeatedly swaps adjacent elements if they are in wrong order",
                "invariant": "After k passes, the last k elements are in their correct positions",
                "how_it_works": [
                    "Compare adjacent elements in the array",
                    "Swap them if they are in the wrong order",
                    "Repeat until no swaps are needed",
                    "Each pass bubbles the largest element to the end"
                ]
            },
            "selection_sort": {
                "category": AlgorithmCategory.SORTING,
                "time_complexity": {"best": "O(n²)", "average": "O(n²)", "worst": "O(n²)"},
                "space_complexity": "O(1)",
                "stability": False,
                "description": "Repeatedly finds the minimum element and places it at the beginning",
                "invariant": "After k iterations, the first k elements are the k smallest elements in sorted order",
                "how_it_works": [
                    "Find the minimum element in the unsorted portion",
                    "Swap it with the first unsorted element",
                    "Repeat with the remaining unsorted portion"
                ]
            },
            "insertion_sort": {
                "category": AlgorithmCategory.SORTING,
                "time_complexity": {"best": "O(n)", "average": "O(n²)", "worst": "O(n²)"},
                "space_complexity": "O(1)",
                "stability": True,
                "description": "Builds the sorted array one element at a time by inserting each element into its correct position",
                "invariant": "The subarray from index 0 to i is always sorted",
                "how_it_works": [
                    "Consider elements one at a time",
                    "Insert each element into its correct position among the sorted elements",
                    "Shift larger elements to the right"
                ]
            },
            "merge_sort": {
                "category": AlgorithmCategory.SORTING,
                "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)"},
                "space_complexity": "O(n)",
                "stability": True,
                "description": "Divide and conquer algorithm that splits the array and merges sorted halves",
                "invariant": "After sorting each half, merging preserves the sorted order",
                "how_it_works": [
                    "Divide the array into two halves",
                    "Recursively sort each half",
                    "Merge the two sorted halves"
                ]
            },
            "quick_sort": {
                "category": AlgorithmCategory.SORTING,
                "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)"},
                "space_complexity": "O(log n)",
                "stability": False,
                "description": "Divide and conquer using a pivot to partition the array",
                "invariant": "Elements to the left of pivot are smaller, elements to the right are larger",
                "how_it_works": [
                    "Choose a pivot element",
                    "Partition the array around the pivot",
                    "Recursively sort the left and right partitions"
                ]
            },
            "heap_sort": {
                "category": AlgorithmCategory.SORTING,
                "time_complexity": {"best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)"},
                "space_complexity": "O(1)",
                "stability": False,
                "description": "Uses a heap data structure to repeatedly extract the maximum element",
                "invariant": "The heap property is maintained at each step",
                "how_it_works": [
                    "Build a max heap from the array",
                    "Repeatedly extract the maximum element",
                    "Place it at the end of the array"
                ]
            },
            "linear_search": {
                "category": AlgorithmCategory.SEARCHING,
                "time_complexity": {"best": "O(1)", "average": "O(n)", "worst": "O(n)"},
                "space_complexity": "O(1)",
                "description": "Sequentially checks each element until the target is found",
                "how_it_works": [
                    "Start from the first element",
                    "Compare each element with the target",
                    "Return position if found, otherwise indicate not found"
                ]
            },
            "binary_search": {
                "category": AlgorithmCategory.SEARCHING,
                "time_complexity": {"best": "O(1)", "average": "O(log n)", "worst": "O(log n)"},
                "space_complexity": "O(1)",
                "description": "Efficiently finds target in sorted array by dividing search space in half",
                "how_it_works": [
                    "Find the middle element of the search range",
                    "Compare with target",
                    "If target is smaller, search left half; otherwise search right half",
                    "Repeat until found or range is empty"
                ]
            },
            "bfs": {
                "category": AlgorithmCategory.GRAPH,
                "time_complexity": {"best": "O(1)", "average": "O(V + E)", "worst": "O(V + E)"},
                "space_complexity": "O(V)",
                "description": "Breadth-first search explores all neighbors at current depth before moving deeper",
                "how_it_works": [
                    "Start from the source node",
                    "Visit all neighbors at current depth",
                    "Add unvisited neighbors to queue",
                    "Repeat until queue is empty"
                ]
            },
            "dfs": {
                "category": AlgorithmCategory.GRAPH,
                "time_complexity": {"best": "O(1)", "average": "O(V + E)", "worst": "O(V + E)"},
                "space_complexity": "O(V)",
                "description": "Depth-first search explores as far as possible before backtracking",
                "how_it_works": [
                    "Start from the source node",
                    "Mark node as visited",
                    "Recursively visit all unvisited neighbors",
                    "Backtrack when no unvisited neighbors remain"
                ]
            },
            "dijkstra": {
                "category": AlgorithmCategory.GRAPH,
                "time_complexity": {"best": "O(E + V log V)", "average": "O(E + V log V)", "worst": "O(E + V log V)"},
                "space_complexity": "O(V)",
                "description": "Finds shortest paths from source to all vertices using greedy approach",
                "how_it_works": [
                    "Initialize distances to infinity except source (0)",
                    "Use priority queue to extract minimum distance vertex",
                    "Relax all outgoing edges from extracted vertex",
                    "Repeat until all vertices are processed"
                ]
            },
            "bellman_ford": {
                "category": AlgorithmCategory.GRAPH,
                "time_complexity": {"best": "O(VE)", "average": "O(VE)", "worst": "O(VE)"},
                "space_complexity": "O(V)",
                "description": "Finds shortest paths using edge relaxation, handles negative weights",
                "how_it_works": [
                    "Initialize all distances to infinity except source",
                    "Relax all edges V-1 times",
                    "Check for negative weight cycles"
                ]
            }
        }
    
    # ==================== COMPLEXITY ANALYSIS ====================
    
    def analyze_complexity(
        self,
        algorithm_name: str,
        custom_code: Optional[str] = None
    ) -> ComplexityAnalysis:
        """
        Analyze the time and space complexity of an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to analyze
            custom_code: Optional custom code for analysis
            
        Returns:
            Complete ComplexityAnalysis object
            
        Raises:
            ValueError: If algorithm is not recognized and no custom code provided
        """
        if algorithm_name.lower() in self._algorithm_knowledge:
            knowledge = self._algorithm_knowledge[algorithm_name.lower()]
            return self._build_complexity_from_knowledge(algorithm_name, knowledge)
        
        if custom_code:
            return self._analyze_code_complexity(custom_code, algorithm_name)
        
        raise ValueError(f"Algorithm '{algorithm_name}' not found in knowledge base")
    
    def _build_complexity_from_knowledge(
        self,
        algorithm_name: str,
        knowledge: Dict[str, Any]
    ) -> ComplexityAnalysis:
        """Build complexity analysis from stored knowledge."""
        time = knowledge.get("time_complexity", {})
        factors = []
        
        if algorithm_name.lower() in ["bubble_sort", "selection_sort", "insertion_sort"]:
            factors = [
                "Number of elements (n)",
                "Initial ordering of elements",
                "Number of comparisons and swaps"
            ]
        elif algorithm_name.lower() in ["merge_sort", "quick_sort", "heap_sort"]:
            factors = [
                "Number of elements (n)",
                "Depth of recursion tree",
                "Cost of merging/partitioning"
            ]
        elif algorithm_name.lower() in ["bfs", "dfs"]:
            factors = [
                "Number of vertices (V)",
                "Number of edges (E)"
            ]
        
        explanation = self._generate_complexity_explanation(algorithm_name, knowledge)
        
        return ComplexityAnalysis(
            time_complexity=time.get("worst", "O(1)"),
            average_time_complexity=time.get("average", "O(1)"),
            worst_time_complexity=time.get("worst", "O(1)"),
            space_complexity=knowledge.get("space_complexity", "O(1)"),
            auxiliary_space=self._calculate_auxiliary_space(knowledge),
            time_complexity_class=self._determine_complexity_class(time.get("average", "O(1)")),
            space_complexity_class=self._determine_complexity_class(knowledge.get("space_complexity", "O(1)")),
            factors=factors,
            explanation=explanation
        )
    
    def _analyze_code_complexity(
        self,
        code: str,
        algorithm_name: str
    ) -> ComplexityAnalysis:
        """Analyze complexity of custom code using static analysis."""
        try:
            tree = ast.parse(code)
            analysis = self._analyze_ast_tree(tree)
            
            explanation = f"Analysis of custom algorithm '{algorithm_name}':\n"
            explanation += f"- Based on code structure analysis:\n"
            explanation += f"- Nested loops increase time complexity\n"
            explanation += f"- Recursive calls affect space complexity\n"
            explanation += f"- Data structure operations contribute to complexity"
            
            return ComplexityAnalysis(
                time_complexity=analysis.get("time", "O(1)"),
                average_time_complexity=analysis.get("time", "O(1)"),
                worst_time_complexity=analysis.get("time", "O(1)"),
                space_complexity=analysis.get("space", "O(1)"),
                auxiliary_space=analysis.get("auxiliary", "O(1)"),
                time_complexity_class=self._determine_complexity_class(analysis.get("time", "O(1)")),
                space_complexity_class=self._determine_complexity_class(analysis.get("space", "O(1)")),
                factors=["Code structure analysis", "Loop nesting", "Recursive calls"],
                explanation=explanation
            )
        except SyntaxError:
            return ComplexityAnalysis(
                time_complexity="O(1)",
                space_complexity="O(1)",
                explanation="Unable to analyze code: syntax error"
            )
    
    def _analyze_ast_tree(self, tree: ast.AST) -> Dict[str, str]:
        """Perform AST-based complexity analysis."""
        max_loop_depth = 0
        has_recursion = False
        has_data_structures = False
        
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                max_loop_depth = max(max_loop_depth, self._get_loop_depth(node))
            if isinstance(node, ast.While):
                max_loop_depth = max(max_loop_depth, self._get_loop_depth(node))
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and child.func.id == node.name:
                        has_recursion = True
        
        time_complexity = self._estimate_time_complexity(max_loop_depth, has_recursion)
        space_complexity = self._estimate_space_complexity(has_recursion, has_data_structures)
        
        return {
            "time": time_complexity,
            "space": space_complexity,
            "auxiliary": space_complexity
        }
    
    def _get_loop_depth(self, node: Union[ast.For, ast.While]) -> int:
        """Calculate nesting depth of a loop."""
        depth = 1
        if isinstance(node.body[0] if node.body else None, (ast.For, ast.While)):
            depth += self._get_loop_depth(node.body[0])
        return depth
    
    def _estimate_time_complexity(self, loop_depth: int, has_recursion: bool) -> str:
        """Estimate time complexity based on analysis."""
        if has_recursion:
            return "O(n log n)" if loop_depth == 1 else "O(2^n)"
        elif loop_depth == 0:
            return "O(1)"
        elif loop_depth == 1:
            return "O(n)"
        elif loop_depth == 2:
            return "O(n²)"
        else:
            return "O(n³)"
    
    def _estimate_space_complexity(self, has_recursion: bool, has_data_structures: bool) -> str:
        """Estimate space complexity based on analysis."""
        if has_recursion:
            return "O(n)"
        elif has_data_structures:
            return "O(n)"
        else:
            return "O(1)"
    
    def _determine_complexity_class(self, complexity: str) -> ComplexityClass:
        """Determine the complexity class from Big O notation."""
        complexity = complexity.upper()
        
        if "O(1)" in complexity:
            return ComplexityClass.CONSTANT
        elif "O(LOG N)" in complexity and "N LOG N" not in complexity:
            return ComplexityClass.LOGARITHMIC
        elif "O(N)" in complexity and "N LOG N" not in complexity:
            return ComplexityClass.LINEAR
        elif "O(N LOG N)" in complexity or "O(N LOG N)" in complexity:
            return ComplexityClass.LINEARITHMIC
        elif "O(N²)" in complexity:
            return ComplexityClass.QUADRATIC
        elif "O(N³)" in complexity:
            return ComplexityClass.CUBIC
        elif "O(2^N)" in complexity:
            return ComplexityClass.EXPONENTIAL
        elif "O(N!)" in complexity:
            return ComplexityClass.FACTORIAL
        else:
            return ComplexityClass.POLYNOMIAL
    
    def _calculate_auxiliary_space(self, knowledge: Dict[str, Any]) -> str:
        """Calculate auxiliary space complexity."""
        space = knowledge.get("space_complexity", "O(1)")
        if space == "O(n)" and knowledge.get("category") == AlgorithmCategory.SORTING:
            return "O(n)"
        return space
    
    def _generate_complexity_explanation(
        self,
        algorithm_name: str,
        knowledge: Dict[str, Any]
    ) -> str:
        """Generate detailed explanation of complexity analysis."""
        time = knowledge.get("time_complexity", {})
        space = knowledge.get("space_complexity", "O(1)")
        category = knowledge.get("category", "").value
        
        explanation = f"""
{algorithm_name.replace('_', ' ').title()} - Complexity Analysis
=============================================

Time Complexity:
- Best Case: {time.get('best', 'N/A')}
- Average Case: {time.get('average', 'N/A')}
- Worst Case: {time.get('worst', 'N/A')}

Space Complexity: {space}

Category: {category}

Analysis:
"""
        if algorithm_name.lower() == "bubble_sort":
            explanation += """
The best case O(n) occurs when the array is already sorted. In this case,
only one pass is needed to verify that no swaps are required. The worst
case O(n²) occurs when the array is reverse sorted, requiring maximum
comparisons and swaps. The space complexity is O(1) as it sorts in-place.
"""
        elif algorithm_name.lower() == "merge_sort":
            explanation += """
Merge sort consistently achieves O(n log n) time complexity regardless of
input order because it always divides the array in half and merges in
linear time. The O(n) space complexity is for the temporary arrays used
during the merge operation. This makes it suitable for external sorting
where data doesn't fit in memory.
"""
        elif algorithm_name.lower() == "quick_sort":
            explanation += """
Quick sort achieves O(n log n) on average but degrades to O(n²) when the
pivot selection is poor (e.g., already sorted array with first element
as pivot). The space complexity is O(log n) for the recursion stack in
the average case, but can be O(n) in the worst case. Random pivot
selection or median-of-three pivot selection can help avoid worst case.
"""
        elif algorithm_name.lower() == "binary_search":
            explanation += """
Binary search efficiently reduces the search space by half each iteration.
This leads to O(log n) time complexity because the search space size
decreases exponentially: n, n/2, n/4, n/8, ... until it reaches 1.
The O(1) space complexity comes from using only a few variables.
"""
        
        return explanation.strip()
    
    # ==================== CORRECTNESS VERIFICATION ====================
    
    def verify_correctness(
        self,
        algorithm_name: str,
        test_cases: Optional[List[Dict[str, Any]]] = None,
        custom_code: Optional[str] = None
    ) -> CorrectnessVerification:
        """
        Verify the correctness of an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to verify
            test_cases: Optional list of test cases
            custom_code: Optional custom code for verification
            
        Returns:
            Complete CorrectnessVerification object
        """
        if algorithm_name.lower() in self._algorithm_knowledge:
            return self._verify_known_algorithm(algorithm_name.lower(), test_cases)
        
        if custom_code:
            return self._verify_custom_code(custom_code, test_cases)
        
        return CorrectnessVerification(
            status=CorrectnessStatus.UNVERIFIED,
            issues=["Algorithm not recognized"]
        )
    
    def _verify_known_algorithm(
        self,
        algorithm_name: str,
        test_cases: Optional[List[Dict[str, Any]]] = None
    ) -> CorrectnessVerification:
        """Verify correctness using stored knowledge and invariants."""
        knowledge = self._algorithm_knowledge.get(algorithm_name, {})
        
        edge_cases = self._identify_edge_cases(algorithm_name)
        invariant = knowledge.get("invariant", "")
        
        verification = CorrectnessVerification(
            status=CorrectnessStatus.CORRECT,
            is_correct=True,
            invariant=invariant,
            proof_steps=self._generate_proof_steps(algorithm_name, knowledge),
            edge_cases=edge_cases,
            termination_proof=self._generate_termination_proof(algorithm_name),
            partial_correctness=self._generate_partial_correctness_proof(algorithm_name),
            total_correctness=self._generate_total_correctness_proof(algorithm_name)
        )
        
        if test_cases:
            verification.issues.extend(self._check_test_cases(algorithm_name, test_cases))
            if verification.issues:
                verification.status = CorrectnessStatus.HAS_ERRORS
                verification.is_correct = False
            else:
                verification.status = CorrectnessStatus.CORRECT
                verification.is_correct = True
        
        return verification
    
    def _identify_edge_cases(self, algorithm_name: str) -> List[str]:
        """Identify common edge cases for an algorithm."""
        base_cases = [
            "Empty array/list",
            "Single element array/list",
            "All elements identical",
            "Array with negative numbers (if applicable)",
            "Array with duplicate values (if applicable)"
        ]
        
        algorithm_specific = []
        if algorithm_name in ["bubble_sort", "selection_sort", "insertion_sort", "merge_sort", "quick_sort", "heap_sort"]:
            algorithm_specific = [
                "Already sorted array (best case)",
                "Reverse sorted array (worst case)",
                "Array with maximum size"
            ]
        elif algorithm_name in ["binary_search"]:
            algorithm_specific = [
                "Target at first position",
                "Target at last position",
                "Target not in array",
                "Empty array",
                "Single element array"
            ]
        elif algorithm_name in ["bfs", "dfs"]:
            algorithm_specific = [
                "Empty graph",
                "Single node graph",
                "Disconnected graph",
                "Graph with cycles",
                "Graph with self-loops"
            ]
        
        return base_cases + algorithm_specific
    
    def _generate_proof_steps(
        self,
        algorithm_name: str,
        knowledge: Dict[str, Any]
    ) -> List[str]:
        """Generate steps for correctness proof."""
        steps = []
        
        if algorithm_name == "bubble_sort":
            steps = [
                "Initialization: Before the first pass, no elements are guaranteed to be in their final positions",
                "Maintenance: After k passes, the last k elements are in their correct positions. This holds because each pass places the largest remaining element in its final position",
                "Termination: After n-1 passes, all elements are in their correct positions",
                "Therefore, the algorithm is correct"
            ]
        elif algorithm_name == "binary_search":
            steps = [
                "Initialization: Search range is the entire array [low, high]",
                "Maintenance: If target is found, return. Otherwise, new range [low, mid-1] or [mid+1, high] still contains target if it exists",
                "Termination: Either target is found or low > high, indicating target is not in array"
            ]
        elif algorithm_name == "merge_sort":
            steps = [
                "Base case: Single element array is trivially sorted",
                "Inductive step: Assuming both halves are sorted correctly, the merge step produces a sorted array",
                "Merge correctness: Merging two sorted arrays by always taking the smallest remaining element preserves sorted order"
            ]
        else:
            steps = [
                "Base case verification",
                "Inductive hypothesis assumption",
                "Inductive step proof",
                "Termination condition validation"
            ]
        
        return steps
    
    def _generate_termination_proof(self, algorithm_name: str) -> str:
        """Generate proof that algorithm terminates."""
        termination_proofs = {
            "bubble_sort": "The outer loop runs exactly n-1 times. The inner loop runs at most n-1-i times. Total iterations are bounded by n(n-1)/2, which is finite.",
            "binary_search": "Each iteration either finds the target or reduces the search range by at least half. The range size decreases exponentially and reaches 0 in at most log₂(n) steps.",
            "merge_sort": "The array is divided until subarrays of size 1 are created. The recursion depth is at most log₂(n), and each level performs O(n) work.",
            "quick_sort": "Each recursive call works on a strictly smaller subarray. The recursion depth is bounded by O(log n) on average and O(n) in worst case.",
            "bfs": "The queue processing loop terminates when all reachable vertices are visited. Each vertex is enqueued at most once.",
            "dfs": "Each vertex is visited at most once, and the recursion/iteration count is bounded by the number of vertices.",
            "dijkstra": "The priority queue operations continue until all vertices are processed. Each vertex is extracted exactly once."
        }
        
        return termination_proofs.get(algorithm_name, "Algorithm terminates after finite number of steps.")
    
    def _generate_partial_correctness_proof(self, algorithm_name: str) -> str:
        """Generate partial correctness proof."""
        partial_correctness = {
            "bubble_sort": "If the algorithm terminates, the resulting array is sorted. This follows from the invariant that after each pass, the largest remaining element is in its final position.",
            "binary_search": "If the algorithm terminates, either the target is found at its correct position, or the algorithm correctly determines the target is not present.",
            "merge_sort": "If the algorithm terminates, the array is sorted. This follows from the merge invariant: when merging two sorted subarrays, the result is sorted.",
            "quick_sort": "If the algorithm terminates, the array is sorted. The partition invariant ensures elements left of pivot are smaller and elements right are larger."
        }
        
        return partial_correctness.get(algorithm_name, "Algorithm produces correct output upon termination.")
    
    def _generate_total_correctness_proof(self, algorithm_name: str) -> str:
        """Generate total correctness proof."""
        return f"Total correctness follows from partial correctness (correct output upon termination) and termination proof (algorithm always terminates). For {algorithm_name.replace('_', ' ')}, both conditions have been established."
    
    def _check_test_cases(
        self,
        algorithm_name: str,
        test_cases: List[Dict[str, Any]]
    ) -> List[str]:
        """Check algorithm against test cases."""
        issues = []
        
        for i, test_case in enumerate(test_cases):
            input_data = test_case.get("input", [])
            expected_output = test_case.get("expected", [])
            
            if self._run_test(algorithm_name, input_data) != expected_output:
                issues.append(f"Test case {i+1} failed: input={input_data}, expected={expected_output}")
        
        return issues
    
    def _run_test(self, algorithm_name: str, input_data: Any) -> Any:
        """Run a simple test for the algorithm (placeholder implementation)."""
        # This would be replaced with actual algorithm execution
        return sorted(input_data) if isinstance(input_data, list) else input_data
    
    def _verify_custom_code(
        self,
        code: str,
        test_cases: Optional[List[Dict[str, Any]]] = None
    ) -> CorrectnessVerification:
        """Verify custom code correctness."""
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for common issues
            for node in ast.walk(tree):
                if isinstance(node, ast.For):
                    if not node.body:
                        issues.append("Empty for loop body detected")
                if isinstance(node, ast.While):
                    if not node.body:
                        issues.append("Empty while loop body detected")
            
            if issues:
                return CorrectnessVerification(
                    status=CorrectnessStatus.HAS_ERRORS,
                    is_correct=False,
                    issues=issues,
                    suggestions=["Fix identified code issues and retest"]
                )
            
            return CorrectnessVerification(
                status=CorrectnessStatus.UNVERIFIED,
                is_correct=False,
                proof_steps=["Custom code requires manual verification"],
                edge_cases=["Custom code edge cases not analyzed"],
                issues=[],
                suggestions=["Run comprehensive test suite to verify correctness"]
            )
            
        except SyntaxError as e:
            return CorrectnessVerification(
                status=CorrectnessStatus.INCORRECT,
                is_correct=False,
                issues=[f"Syntax error: {str(e)}"]
            )
    
    # ==================== OPTIMIZATION SUGGESTIONS ====================
    
    def get_optimization_suggestions(
        self,
        algorithm_name: str
    ) -> List[OptimizationSuggestion]:
        """
        Get optimization suggestions for an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to optimize
            
        Returns:
            List of OptimizationSuggestion objects
        """
        suggestions = {
            "bubble_sort": [
                OptimizationSuggestion(
                    suggestion_type="early_termination",
                    description="Add a flag to detect if any swaps occurred in a pass",
                    impact="Best case improves from O(n²) to O(n)",
                    complexity_improvement=("O(n²)", "O(n)"),
                    tradeoffs=["Minor additional memory for flag", "Small overhead per comparison"],
                    implementation_difficulty=1,
                    benefits=["Faster on nearly sorted data", "No downside for worst case"],
                    risks=["None significant"]
                ),
                OptimizationSuggestion(
                    suggestion_type="bidirectional",
                    description="Use cocktail shaker sort (bidirectional bubble sort)",
                    impact="Reduces number of passes needed",
                    complexity_improvement=("O(n²)", "O(n²)"),
                    tradeoffs=["More complex implementation", "Slightly more comparisons"],
                    implementation_difficulty=2,
                    benefits=["Fewer passes on some inputs", "Better cache locality"],
                    risks=["Still O(n²) worst case"]
                )
            ],
            "selection_sort": [
                OptimizationSuggestion(
                    suggestion_type="two_lists",
                    description="Build sorted list from both ends simultaneously",
                    impact="Reduces number of passes by half",
                    complexity_improvement=("O(n²)", "O(n²)"),
                    tradeoffs=["More complex implementation", "May affect stability"],
                    implementation_difficulty=3,
                    benefits=["Fewer passes", "Better constant factors"],
                    risks=["Algorithm complexity increases"]
                )
            ],
            "quick_sort": [
                OptimizationSuggestion(
                    suggestion_type="pivot_selection",
                    description="Use median-of-three pivot selection or random pivot",
                    impact="Worst case probability reduced to nearly zero",
                    complexity_improvement=("O(n²)", "O(n log n)"),
                    tradeoffs=["Slightly more work per partition", "Randomness in timing"],
                    implementation_difficulty=2,
                    benefits=["Avoids worst case on sorted inputs", "More predictable performance"],
                    risks=["Random pivot selection still has small probability of bad case"]
                ),
                OptimizationSuggestion(
                    suggestion_type="tail_recursion",
                    description="Optimize tail recursion for smaller partition",
                    impact="Reduces worst-case space from O(n) to O(log n)",
                    complexity_improvement=("O(n)", "O(log n)"),
                    tradeoffs=["More complex implementation"],
                    implementation_difficulty=3,
                    benefits=["Reduced stack usage", "Better for large inputs"],
                    risks=["None significant"]
                )
            ],
            "binary_search": [
                OptimizationSuggestion(
                    suggestion_type="bitwise",
                    description="Use bitwise operations where possible",
                    impact="Minor constant factor improvement",
                    complexity_improvement=("O(log n)", "O(log n)"),
                    tradeoffs=["May reduce readability"],
                    implementation_difficulty=1,
                    benefits=["Faster on some architectures", "More idiomatic for certain languages"],
                    risks=["Negligible improvement", "Reduced portability"]
                )
            ],
            "dijkstra": [
                OptimizationSuggestion(
                    suggestion_type="fibonacci_heap",
                    description="Use Fibonacci heap for priority queue",
                    impact="Best asymptotic complexity",
                    complexity_improvement=("O(E + V log V)", "O(E + V log V)"),
                    tradeoffs=["High constant factors", "Complex implementation"],
                    implementation_difficulty=5,
                    benefits=["Optimal for sparse graphs"],
                    risks=["Often slower in practice due to constants", "Complex to implement correctly"]
                ),
                OptimizationSuggestion(
                    suggestion_type="early_termination",
                    description="Stop when destination node is extracted",
                    impact="Can significantly reduce work for single-source-single-destination",
                    complexity_improvement=("O(E + V log V)", "O(E + V log V)"),
                    tradeoffs=["Only applicable for single destination"],
                    implementation_difficulty=1,
                    benefits=["Faster for path queries", "No downside for single destinations"],
                    risks=["Not applicable when computing all paths"]
                )
            ]
        }
        
        return suggestions.get(algorithm_name.lower(), [
            OptimizationSuggestion(
                suggestion_type="general",
                description="Review algorithm for potential optimizations specific to your use case",
                impact="Varies based on specific implementation",
                tradeoffs=["Depends on specific optimization"],
                implementation_difficulty=2,
                benefits=["May improve performance"],
                risks=["Requires careful testing"]
            )
        ])
    
    # ==================== EXPLANATION GENERATION ====================
    
    def generate_explanation(
        self,
        algorithm_name: str
    ) -> AlgorithmExplanation:
        """
        Generate comprehensive explanation for an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to explain
            
        Returns:
            Complete AlgorithmExplanation object
        """
        if algorithm_name.lower() not in self._algorithm_knowledge:
            return AlgorithmExplanation(
                algorithm_name=algorithm_name,
                description=f"Algorithm '{algorithm_name}' is not in the knowledge base"
            )
        
        knowledge = self._algorithm_knowledge[algorithm_name.lower()]
        
        return AlgorithmExplanation(
            algorithm_name=algorithm_name,
            category=knowledge.get("category", AlgorithmCategory.SORTING),
            description=knowledge.get("description", ""),
            how_it_works=knowledge.get("how_it_works", []),
            key_insights=self._generate_key_insights(algorithm_name),
            mathematical_foundation=self._generate_mathematical_foundation(algorithm_name),
            intuition=self._generate_intuition(algorithm_name),
            real_world_applications=self._generate_applications(algorithm_name),
            related_algorithms=self._find_related_algorithms(algorithm_name),
            pseudocode=self._generate_pseudocode(algorithm_name),
            when_to_use=self._generate_when_to_use(algorithm_name),
            when_not_to_use=self._generate_when_not_to_use(algorithm_name)
        )
    
    def _generate_key_insights(self, algorithm_name: str) -> List[str]:
        """Generate key insights for an algorithm."""
        insights = {
            "bubble_sort": [
                "Simple but inefficient for large datasets",
                "Named for how elements 'bubble up' to their correct positions",
                "Adaptive: runs in O(n) for nearly sorted data",
                "Stable sort: maintains relative order of equal elements"
            ],
            "merge_sort": [
                "Guaranteed O(n log n) performance regardless of input",
                "Divide and conquer paradigm in its purest form",
                "Requires O(n) additional space",
                "Ideal for external sorting (data too large for memory)"
            ],
            "quick_sort": [
                "Typically fastest in practice despite O(n²) worst case",
                "In-place sorting with O(log n) average space",
                "Choice of pivot dramatically affects performance",
                "Not stable: may change relative order of equal elements"
            ],
            "binary_search": [
                "Exploits sorted property to eliminate half the search space",
                "Number of comparisons equals log₂(n) + 1 in worst case",
                "Cannot be applied to unsorted data without sorting first",
                "Optimal for searching in large sorted datasets"
            ],
            "dijkstra": [
                "Greedy algorithm that always picks the closest unvisited vertex",
                "Cannot handle negative edge weights",
                "Produces shortest path tree from source",
                "Optimal substructure property enables greedy choice"
            ]
        }
        
        return insights.get(algorithm_name.lower(), [
            "Algorithm applies specific problem-solving strategy",
            "Efficiency depends on input characteristics",
            "May have multiple valid implementations",
            "Understanding the intuition helps in optimization"
        ])
    
    def _generate_mathematical_foundation(self, algorithm_name: str) -> str:
        """Generate mathematical foundation for an algorithm."""
        foundations = {
            "bubble_sort": """
Bubble sort relies on the principle that if we repeatedly compare and swap
adjacent elements, larger elements will gradually move towards their final
positions. The total number of comparisons in the worst case is the sum
of the first (n-1) natural numbers: n(n-1)/2, which is O(n²).
""",
            "merge_sort": """
Merge sort is based on the divide and conquer paradigm. The recurrence
relation is T(n) = 2T(n/2) + O(n), which solves to O(n log n) using the
master theorem. The O(n) merge step combines two sorted arrays by always
taking the smaller of the two front elements.
""",
            "binary_search": """
Binary search exploits the sorted property through divide and conquer.
Each comparison eliminates half of the remaining search space. After k
comparisons, at most n/2^k elements remain. Solving n/2^k = 1 gives k = log₂(n).
""",
            "dijkstra": """
Dijkstra's algorithm relies on the optimal substructure property: the
shortest path to any vertex must go through one of its neighbors. The greedy
choice property ensures that once a vertex is selected as the closest,
its distance is final and cannot be improved.
""",
            "heap_sort": """
Heap sort builds a binary heap, which is a complete binary tree satisfying
the heap property (parent >= child for max-heap). Building a heap takes O(n)
time, and each extraction takes O(log n) time, giving O(n log n) total.
"""
        }
        
        return foundations.get(algorithm_name.lower(), """
The algorithm is based on fundamental principles of computer science and
mathematics. Its correctness can be proven through induction and its
complexity analyzed using asymptotic notation.
""").strip()
    
    def _generate_intuition(self, algorithm_name: str) -> str:
        """Generate intuitive explanation for an algorithm."""
        intuitions = {
            "bubble_sort": "Imagine air bubbles rising in water - larger bubbles rise faster. Similarly, larger elements 'bubble up' to their correct positions through repeated comparisons and swaps with adjacent elements.",
            "merge_sort": "Think of sorting a deck of cards by repeatedly splitting it in half until you have single cards, then merging pairs back together in sorted order.",
            "quick_sort": "Like organizing books on a shelf by picking a pivot book and placing all smaller books to its left and larger books to its right, then repeating for each section.",
            "binary_search": "Like finding a word in a dictionary by opening to the middle, seeing if your word comes before or after, and repeating until you find it.",
            "insertion_sort": "Like sorting playing cards in your hand - you take one card at a time and insert it into its correct position among the already sorted cards."
        }
        
        return intuitions.get(algorithm_name.lower(), "The algorithm follows a systematic approach to solving the problem efficiently.")
    
    def _generate_applications(self, algorithm_name: str) -> List[str]:
        """Generate real-world applications for an algorithm."""
        applications = {
            "bubble_sort": [
                "Teaching sorting concepts in computer science courses",
                "Small datasets where simplicity is preferred over speed",
                "Detecting small changes in nearly sorted data"
            ],
            "merge_sort": [
                "Sorting large datasets that don't fit in memory (external sorting)",
                "Sorting linked lists (no random access needed)",
                "Inversion count problems",
                "Parallel sorting (subarrays can be sorted independently)"
            ],
            "quick_sort": [
                "General-purpose sorting in libraries (C's qsort, Java's Arrays.sort)",
                "Large datasets where average-case performance matters",
                "In-memory sorting where O(log n) extra space is acceptable"
            ],
            "binary_search": [
                "Searching in sorted databases",
                "Finding values in sorted arrays",
                "Lookup tables and symbol tables",
                "Computer graphics (ray tracing acceleration)"
            ],
            "dijkstra": [
                "GPS navigation systems for shortest path",
                "Network routing protocols",
                "Social network analysis (degrees of separation)",
                "Game AI (pathfinding)"
            ],
            "bfs": [
                "Finding shortest path in unweighted graphs",
                "Web crawlers",
                "Social networking (friend recommendations)",
                "Garbage collection (mark and sweep)"
            ],
            "dfs": [
                "Maze solving",
                "Topological sorting",
                "Detecting cycles in graphs",
                "Solving puzzles (sudoku, crossword)"
            ]
        }
        
        return applications.get(algorithm_name.lower(), ["General algorithm applicable to various problems"])
    
    def _find_related_algorithms(self, algorithm_name: str) -> List[str]:
        """Find related algorithms."""
        related = {
            "bubble_sort": ["cocktail_shaker_sort", "comb_sort", "insertion_sort", "selection_sort"],
            "merge_sort": ["quick_sort", "heap_sort", "natural_merge_sort", "tim_sort"],
            "quick_sort": ["merge_sort", "heap_sort", "introsort", "tim_sort"],
            "binary_search": ["linear_search", "interpolation_search", "exponential_search"],
            "bfs": ["dfs", "dijkstra", "bellman_ford", "a_star"],
            "dfs": ["bfs", "topological_sort", "tarjans_algorithm"],
            "dijkstra": ["bellman_ford", "floyd_warshall", "a_star", "johnsons_algorithm"]
        }
        
        return related.get(algorithm_name.lower(), ["Related algorithms in the same category"])
    
    def _generate_pseudocode(self, algorithm_name: str) -> str:
        """Generate pseudocode for an algorithm."""
        pseudocodes = {
            "bubble_sort": """
procedure bubbleSort(A: array of items)
    n = length(A)
    for i from 0 to n-1 do
        swapped = false
        for j from 0 to n-i-2 do
            if A[j] > A[j+1] then
                swap(A[j], A[j+1])
                swapped = true
            end if
        end for
        if not swapped then
            break
        end if
    end for
end procedure
""",
            "merge_sort": """
procedure mergeSort(A: array of items)
    if length(A) <= 1 then
        return A
    end if
    
    mid = length(A) / 2
    left = mergeSort(A[0:mid])
    right = mergeSort(A[mid:length(A)])
    
    return merge(left, right)
end procedure

procedure merge(left, right: arrays)
    result = empty array
    i = 0, j = 0
    
    while i < length(left) and j < length(right) do
        if left[i] <= right[j] then
            append left[i] to result
            i = i + 1
        else
            append right[j] to result
            j = j + 1
        end if
    end while
    
    append remaining elements of left to result
    append remaining elements of right to result
    
    return result
end procedure
""",
            "binary_search": """
procedure binarySearch(A: sorted array, target: value)
    low = 0
    high = length(A) - 1
    
    while low <= high do
        mid = (low + high) / 2
        
        if A[mid] == target then
            return mid
        else if A[mid] < target then
            low = mid + 1
        else
            high = mid - 1
        end if
    end while
    
    return -1  // not found
end procedure
""",
            "bfs": """
procedure bfs(G: graph, s: source vertex)
    create empty queue Q
    create empty set visited
    enqueue s into Q
    add s to visited
    
    while Q is not empty do
        v = dequeue Q
        process(v)
        
        for each neighbor u of v do
            if u not in visited then
                add u to visited
                enqueue u into Q
            end if
        end for
    end while
end procedure
"""
        }
        
        return pseudocodes.get(algorithm_name.lower(), "Pseudocode not available for this algorithm")
    
    def _generate_when_to_use(self, algorithm_name: str) -> str:
        """Generate guidance on when to use the algorithm."""
        guidance = {
            "bubble_sort": "Use for very small arrays (< 20 elements) or when simplicity is more important than performance. Good for nearly sorted data where it achieves O(n) complexity.",
            "merge_sort": "Use when guaranteed O(n log n) performance is needed, for external sorting, when sorting linked lists, or when stability is required.",
            "quick_sort": "Use as the default sorting algorithm for general-purpose use. Ideal when average-case performance matters more than worst-case, and O(log n) extra space is acceptable.",
            "binary_search": "Use whenever you need to search in sorted data. Essential for large datasets where O(log n) search time is required.",
            "dijkstra": "Use for finding shortest paths in graphs with non-negative edge weights. Ideal for road networks, routing, and pathfinding problems.",
            "bfs": "Use when you need the shortest path in an unweighted graph, or when you want to explore all nodes at the current depth before going deeper."
        }
        
        return guidance.get(algorithm_name.lower(), "Use when the algorithm's characteristics match your problem requirements.")
    
    def _generate_when_not_to_use(self, algorithm_name: str) -> str:
        """Generate guidance on when not to use the algorithm."""
        guidance = {
            "bubble_sort": "Do not use for large arrays as O(n²) complexity will be too slow. Consider merge sort, heap sort, or quick sort instead.",
            "merge_sort": "Do not use when O(1) space complexity is required (in-place sorting needed). Consider heap sort or quick sort for in-place alternatives.",
            "quick_sort": "Do not use when worst-case performance must be guaranteed or when sorting stable order is required. Consider merge sort or heap sort instead.",
            "binary_search": "Do not use on unsorted data without first sorting it. For unsorted data, linear search may be faster if only searching once.",
            "dijkstra": "Do not use when edges have negative weights (use Bellman-Ford instead). For single-source single-destination, A* may be more efficient.",
            "bfs": "Do not use when you need the longest path (use DFS) or when memory is constrained (BFS uses O(V) space for queue)."
        }
        
        return guidance.get(algorithm_name.lower(), "Consider alternative algorithms if your use case differs from the algorithm's strengths.")
    
    # ==================== ALGORITHM COMPARISON ====================
    
    def compare_algorithms(
        self,
        algorithm_names: List[str],
        criteria: Optional[List[str]] = None
    ) -> AlgorithmComparison:
        """
        Compare multiple algorithms across various criteria.
        
        Args:
            algorithm_names: List of algorithm names to compare
            criteria: List of comparison criteria
            
        Returns:
            Complete AlgorithmComparison object
        """
        criteria = criteria or ["time_complexity", "space_complexity", "stability", "use_cases"]
        
        comparison_results = {}
        for name in algorithm_names:
            if name.lower() in self._algorithm_knowledge:
                knowledge = self._algorithm_knowledge[name.lower()]
                comparison_results[name] = {
                    "time_complexity": knowledge.get("time_complexity", {}).get("average", "N/A"),
                    "space_complexity": knowledge.get("space_complexity", "N/A"),
                    "stability": "Yes" if knowledge.get("stability") else "No",
                    "category": knowledge.get("category", "").value
                }
        
        winner = self._determine_comparison_winner(algorithm_names, criteria)
        tradeoffs = self._generate_comparison_tradeoffs(algorithm_names)
        recommendations = self._generate_comparison_recommendations(algorithm_names)
        
        return AlgorithmComparison(
            algorithms=algorithm_names,
            comparison_criteria=criteria,
            comparison_results=comparison_results,
            winner=winner,
            tradeoffs=tradeoffs,
            recommendations=recommendations
        )
    
    def _determine_comparison_winner(
        self,
        algorithm_names: List[str],
        criteria: List[str]
    ) -> str:
        """Determine the overall winner of the comparison."""
        scores = {name: 0 for name in algorithm_names}
        
        complexity_preference = {
            "O(1)": 5,
            "O(log n)": 4,
            "O(n)": 3,
            "O(n log n)": 2,
            "O(n²)": 1,
            "O(n³)": 0,
            "O(2^n)": -1
        }
        
        for name in algorithm_names:
            if name.lower() in self._algorithm_knowledge:
                knowledge = self._algorithm_knowledge[name.lower()]
                
                if "time_complexity" in criteria:
                    avg_time = knowledge.get("time_complexity", {}).get("average", "O(1)")
                    scores[name] += complexity_preference.get(avg_time, 1)
                
                if "space_complexity" in criteria:
                    space = knowledge.get("space_complexity", "O(1)")
                    scores[name] += complexity_preference.get(space, 2)
        
        if scores:
            return max(scores, key=scores.get)
        return ""
    
    def _generate_comparison_tradeoffs(self, algorithm_names: List[str]) -> List[str]:
        """Generate general tradeoffs between algorithms."""
        tradeoffs = []
        
        if all(name.lower() in ["bubble_sort", "selection_sort", "insertion_sort"] for name in algorithm_names):
            tradeoffs = [
                "All three are O(n²) but with different characteristics",
                "Bubble and insertion sort are stable; selection sort is not",
                "Insertion sort is best for nearly sorted data (O(n) best case)",
                "Selection sort makes minimum number of swaps (O(n))",
                "Consider data characteristics when choosing"
            ]
        
        elif all(name.lower() in ["merge_sort", "quick_sort", "heap_sort"] for name in algorithm_names):
            tradeoffs = [
                "All achieve O(n log n) average case",
                "Merge sort is stable; quick sort and heap sort are not",
                "Merge sort uses O(n) extra space; heap sort uses O(1)",
                "Quick sort has best cache locality but O(n²) worst case",
                "Heap sort has worst-case O(n log n) but poor cache locality"
            ]
        
        elif all(name.lower() in ["bfs", "dfs"] for name in algorithm_names):
            tradeoffs = [
                "Both traverse all vertices: O(V + E)",
                "BFS uses queue (O(V) space); DFS uses stack (O(V) space)",
                "BFS finds shortest path in unweighted graphs",
                "DFS is more memory-efficient for deep graphs",
                "Choice depends on what you need to find"
            ]
        
        else:
            tradeoffs = [
                "Algorithm choice depends on specific requirements",
                "Consider time complexity, space complexity, and data characteristics",
                "No single algorithm is best for all situations"
            ]
        
        return tradeoffs
    
    def _generate_comparison_recommendations(self, algorithm_names: List[str]) -> Dict[str, str]:
        """Generate specific recommendations for different scenarios."""
        recommendations = {
            "general": "Choose based on your specific requirements for time, space, and stability.",
            "small_data": "For small datasets, simpler algorithms like insertion sort may be faster due to lower overhead.",
            "large_data": "For large datasets, prefer O(n log n) algorithms. Consider merge sort for stability needs.",
            "memory_constrained": "Use in-place algorithms like heap sort or quick sort when memory is limited."
        }
        
        if set(algorithm_names) & {"bubble_sort", "selection_sort", "insertion_sort"}:
            recommendations.update({
                "nearly_sorted": "Use insertion sort for nearly sorted data - achieves O(n) best case",
                "minimum_swaps": "Use selection sort if minimizing swaps is important (only O(n) swaps)"
            })
        
        if set(algorithm_names) & {"merge_sort", "quick_sort", "heap_sort"}:
            recommendations.update({
                "stability_needed": "Use merge sort if you need stable sorting",
                "average_performance": "Quick sort typically has the best average performance",
                "worst_case_guarantee": "Heap sort guarantees O(n log n) worst case"
            })
        
        if set(algorithm_names) & {"bfs", "dfs"}:
            recommendations.update({
                "shortest_path": "Use BFS for shortest path in unweighted graphs",
                "deep_exploration": "Use DFS when you want to explore as deep as possible",
                "memory_efficient": "DFS is often more memory-efficient for deep graphs"
            })
        
        return recommendations
    
    # ==================== INTERACTIVE PROBLEM SOLVING ====================
    
    def analyze_problem(
        self,
        problem_description: str,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a problem and suggest appropriate algorithmic approaches.
        
        Args:
            problem_description: Description of the problem to solve
            constraints: Problem constraints (size, time, space requirements)
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        problem_lower = problem_description.lower()
        
        analysis = {
            "problem_type": self._classify_problem(problem_lower),
            "suggested_algorithms": [],
            "complexity_considerations": "",
            "approach": ""
        }
        
        # Classify problem and suggest algorithms
        if "sort" in problem_lower:
            analysis["problem_type"] = "sorting"
            analysis["suggested_algorithms"] = self._suggest_sorting_algorithm(constraints)
            analysis["approach"] = "Determine which sorting algorithm best fits your data characteristics and constraints."
        
        elif "search" in problem_lower or "find" in problem_lower:
            analysis["problem_type"] = "searching"
            analysis["suggested_algorithms"] = ["binary_search", "linear_search", "ternary_search"]
            analysis["approach"] = "Binary search requires sorted data. For unsorted data, consider sorting first or using linear search."
        
        elif "shortest path" in problem_lower or "path" in problem_lower:
            analysis["problem_type"] = "graph_shortest_path"
            analysis["suggested_algorithms"] = self._suggest_path_algorithm(constraints)
            analysis["approach"] = "Consider whether edges have weights, whether they're positive, and if you need single-source or all-pairs."
        
        elif "travers" in problem_lower:
            analysis["problem_type"] = "graph_traversal"
            analysis["suggested_algorithms"] = ["bfs", "dfs"]
            analysis["approach"] = "Choose BFS for shortest path in unweighted graphs, DFS for exploration and cycle detection."
        
        return analysis
    
    def _classify_problem(self, problem: str) -> str:
        """Classify a problem based on its description."""
        classifications = {
            "sort": "sorting",
            "search": "searching",
            "find": "searching",
            "shortest": "shortest_path",
            "path": "graph_path",
            "travers": "graph_traversal",
            "minimum": "optimization",
            "maximum": "optimization",
            "graph": "graph",
            "tree": "tree"
        }
        
        for key, value in classifications.items():
            if key in problem:
                return value
        
        return "general"
    
    def _suggest_sorting_algorithm(
        self,
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Suggest sorting algorithms based on constraints."""
        suggestions = []
        constraints = constraints or {}
        
        size = constraints.get("size", "medium")
        stability = constraints.get("stability", False)
        space_constraint = constraints.get("space", "unlimited")
        
        if size == "small":
            suggestions = ["insertion_sort", "bubble_sort"]
        elif size == "large":
            if stability:
                suggestions = ["merge_sort", "timsort"]
            else:
                suggestions = ["quick_sort", "heap_sort", "introsort"]
        else:
            suggestions = ["merge_sort", "quick_sort", "timsort"]
        
        if space_constraint == "low":
            suggestions = [s for s in suggestions if s in ["heap_sort", "quick_sort", "insertion_sort"]]
        
        return suggestions
    
    def _suggest_path_algorithm(
        self,
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Suggest path-finding algorithms based on constraints."""
        constraints = constraints or {}
        has_negative = constraints.get("negative_weights", False)
        single_source = constraints.get("single_source", True)
        
        if has_negative:
            return ["bellman_ford", "johnsons_algorithm"]
        elif single_source:
            return ["dijkstra", "a_star", "bellman_ford"]
        else:
            return ["floyd_warshall", "johnsons_algorithm"]
    
    # ==================== UTILITY METHODS ====================
    
    def get_algorithm_info(
        self,
        algorithm_name: str
    ) -> Dict[str, Any]:
        """
        Get all available information about an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm
            
        Returns:
            Dictionary with all algorithm information
        """
        if algorithm_name.lower() not in self._algorithm_knowledge:
            return {"error": f"Algorithm '{algorithm_name}' not found"}
        
        knowledge = self._algorithm_knowledge[algorithm_name.lower()]
        
        return {
            "basic_info": knowledge,
            "complexity": self.analyze_complexity(algorithm_name),
            "explanation": self.generate_explanation(algorithm_name),
            "optimizations": self.get_optimization_suggestions(algorithm_name),
            "correctness": self.verify_correctness(algorithm_name)
        }
    
    def register_custom_algorithm(
        self,
        name: str,
        info: Dict[str, Any]
    ) -> None:
        """
        Register a custom algorithm in the knowledge base.
        
        Args:
            name: Unique name for the algorithm
            info: Algorithm information dictionary
        """
        self._algorithm_knowledge[name.lower()] = info
    
    def get_supported_algorithms(self) -> Dict[str, List[str]]:
        """
        Get list of all supported algorithms organized by category.
        
        Returns:
            Dictionary mapping categories to algorithm names
        """
        categorized = {}
        for name, info in self._algorithm_knowledge.items():
            category = info.get("category", AlgorithmCategory.SORTING).value
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(name)
        
        return categorized
