"""
AlgoVerse Animation Service

This module provides animation frame generation capabilities for algorithmic visualizations.
It handles step-by-step animation frames for sorting, searching, and traversal algorithms,
enabling the creation of dynamic, educational animations that illustrate how algorithms work.

The service generates frame-by-frame representations of algorithm execution, capturing
the state of data structures at each critical step. These frames can then be rendered
into smooth animations by the visualization layer.

Key Features:
- Sorting algorithm animations (bubble sort, selection sort, insertion sort, merge sort, quicksort, heap sort)
- Graph traversal animations (BFS, DFS)
- Tree traversal animations (pre-order, in-order, post-order, level-order)
- Search algorithm animations (binary search, linear search)
- Custom algorithm animation support
- Frame state tracking and metadata
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import copy


class AnimationType(Enum):
    """Enumeration of supported animation types for algorithm visualization."""
    SORTING = "sorting"
    GRAPH_TRAVERSAL = "graph_traversal"
    TREE_TRAVERSAL = "tree_traversal"
    SEARCH = "search"
    CUSTOM = "custom"


class SortingAlgorithm(Enum):
    """Enumeration of supported sorting algorithms for animation."""
    BUBBLE_SORT = "bubble_sort"
    SELECTION_SORT = "selection_sort"
    INSERTION_SORT = "insertion_sort"
    MERGE_SORT = "merge_sort"
    QUICK_SORT = "quick_sort"
    HEAP_SORT = "heap_sort"
    RADIX_SORT = "radix_sort"
    SHELL_SORT = "shell_sort"


class GraphTraversalType(Enum):
    """Enumeration of supported graph traversal algorithms."""
    BFS = "bfs"
    DFS = "dfs"
    DIJKSTRA = "dijkstra"
    BELLMAN_FORD = "bellman_ford"


class TreeTraversalType(Enum):
    """Enumeration of supported tree traversal algorithms."""
    PRE_ORDER = "pre_order"
    IN_ORDER = "in_order"
    POST_ORDER = "post_order"
    LEVEL_ORDER = "level_order"


class ElementState(Enum):
    """State of an element during animation."""
    DEFAULT = "default"
    COMPARING = "comparing"
    SWAPPING = "swapping"
    ACTIVE = "active"
    COMPLETED = "completed"
    FOUND = "found"
    NOT_FOUND = "not_found"


@dataclass
class AnimationFrame:
    """
    Represents a single frame in an algorithm animation.
    
    Attributes:
        frame_number: Sequential number of this frame in the animation
        data_state: Current state of the data being animated
        highlighted_indices: List of indices currently being highlighted
        element_states: Mapping of indices to their visual states
        message: Description of what operation is being performed
        metadata: Additional frame-specific information
        timestamp: Relative timestamp within the animation sequence
    """
    frame_number: int
    data_state: List[Any]
    highlighted_indices: List[int] = field(default_factory=list)
    element_states: Dict[int, ElementState] = field(default_factory=dict)
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = 0.0


@dataclass
class GraphAnimationFrame:
    """
    Represents a frame in a graph traversal animation.
    
    Attributes:
        frame_number: Sequential number of this frame
        visited_nodes: Set of nodes that have been visited
        current_node: Node currently being processed
        edge_states: Mapping of edges to their states
        node_states: Mapping of nodes to their visual states
        queue_state: Current state of the BFS queue or DFS stack
        message: Description of the current operation
        metadata: Additional frame-specific information
    """
    frame_number: int
    visited_nodes: List[Any] = field(default_factory=list)
    current_node: Optional[Any] = None
    edge_states: Dict[Tuple[Any, Any], ElementState] = field(default_factory=dict)
    node_states: Dict[Any, ElementState] = field(default_factory=dict)
    queue_state: List[Any] = field(default_factory=list)
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TreeAnimationFrame:
    """
    Represents a frame in a tree traversal animation.
    
    Attributes:
        frame_number: Sequential number of this frame
        visited_nodes: List of nodes that have been visited in order
        current_node: Node currently being processed
        path: Current path from root to current node
        node_states: Mapping of nodes to their visual states
        message: Description of the traversal step
        metadata: Additional frame-specific information
    """
    frame_number: int
    visited_nodes: List[Any] = field(default_factory=list)
    current_node: Optional[Any] = None
    path: List[Any] = field(default_factory=list)
    node_states: Dict[Any, ElementState] = field(default_factory=dict)
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnimationSequence:
    """
    Container for a complete animation sequence.
    
    Attributes:
        animation_type: Type of animation being performed
        algorithm_name: Name of the algorithm being animated
        total_frames: Total number of frames in the sequence
        frames: List of animation frames
        initial_data: Original input data before animation
        complexity_info: Time and space complexity information
        metadata: Additional animation metadata
    """
    animation_type: AnimationType
    algorithm_name: str
    total_frames: int
    frames: List[Union[AnimationFrame, GraphAnimationFrame, TreeAnimationFrame]]
    initial_data: Any
    complexity_info: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AlgoVerseAnimationService:
    """
    Service for generating algorithm animation frames.
    
    This service provides comprehensive animation generation capabilities for
    various algorithmic concepts including sorting, searching, graph traversals,
    and tree traversals. Each animation sequence captures the complete state
    progression of the algorithm, enabling the creation of educational animations.
    
    The service is designed to be extensible, allowing for custom algorithm
    animations to be added through a plugin architecture.
    
    Example:
        >>> service = AlgoVerseAnimationService()
        >>> frames = service.create_sorting_frames([5, 2, 8, 1, 9], "bubble_sort")
        >>> sequence = service.assemble_animation_sequence(frames, AnimationType.SORTING, "bubble_sort")
    """
    
    def __init__(self):
        """Initialize the animation service with default configuration."""
        self.config = {}
        self._frame_counter = 0
        self._custom_algorithms: Dict[str, callable] = {}

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the service with provided settings.
        
        Args:
            config: Configuration dictionary with service settings
        """
        self.config.update(config)
        print("AlgoVerseAnimationService configured with settings:", list(config.keys()))

    def reset_frame_counter(self) -> None:
        """Reset the frame counter for a new animation sequence."""
        self._frame_counter = 0
    
    def _next_frame_number(self) -> int:
        """Get the next frame number in the sequence."""
        self._frame_counter += 1
        return self._frame_counter
    
    def _create_base_frame(
        self,
        data: List[Any],
        message: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AnimationFrame:
        """
        Create a base animation frame with common attributes.
        
        Args:
            data: Current state of the data
            message: Description of the current operation
            metadata: Additional frame-specific information
            
        Returns:
            A new AnimationFrame instance
        """
        return AnimationFrame(
            frame_number=self._next_frame_number(),
            data_state=copy.deepcopy(data),
            message=message,
            metadata=metadata or {}
        )
    
    # ==================== SORTING ANIMATIONS ====================
    
    def create_sorting_frames(
        self,
        data: List[Union[int, float]],
        algorithm: Union[str, SortingAlgorithm],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """
        Generate animation frames for sorting algorithms.
        
        Creates a complete sequence of frames showing each step of the sorting
        process, including comparisons, swaps, and element state changes.
        
        Args:
            data: List of comparable elements to sort
            algorithm: Sorting algorithm to animate (name or enum)
            custom_comparator: Optional custom comparison function
            
        Returns:
            List of AnimationFrame objects representing the sorting process
            
        Raises:
            ValueError: If the algorithm is not supported
        """
        if isinstance(algorithm, str):
            try:
                algorithm = SortingAlgorithm(algorithm.lower())
            except ValueError:
                raise ValueError(f"Unsupported sorting algorithm: {algorithm}")
        
        # Create a deep copy to avoid modifying original data
        working_data = copy.deepcopy(data)
        frames = []
        
        # Add initial state frame
        initial_frame = self._create_base_frame(
            working_data,
            message=f"Starting {algorithm.value.replace('_', ' ').title()} on array of size {len(working_data)}",
            metadata={"phase": "initial"}
        )
        frames.append(initial_frame)
        
        # Generate algorithm-specific frames
        if algorithm == SortingAlgorithm.BUBBLE_SORT:
            frames.extend(self._animate_bubble_sort(working_data, custom_comparator))
        elif algorithm == SortingAlgorithm.SELECTION_SORT:
            frames.extend(self._animate_selection_sort(working_data, custom_comparator))
        elif algorithm == SortingAlgorithm.INSERTION_SORT:
            frames.extend(self._animate_insertion_sort(working_data, custom_comparator))
        elif algorithm == SortingAlgorithm.MERGE_SORT:
            frames.extend(self._animate_merge_sort(working_data, custom_comparator))
        elif algorithm == SortingAlgorithm.QUICK_SORT:
            frames.extend(self._animate_quick_sort(working_data, custom_comparator))
        elif algorithm == SortingAlgorithm.HEAP_SORT:
            frames.extend(self._animate_heap_sort(working_data, custom_comparator))
        elif algorithm == SortingAlgorithm.RADIX_SORT:
            frames.extend(self._animate_radix_sort(working_data))
        elif algorithm == SortingAlgorithm.SHELL_SORT:
            frames.extend(self._animate_shell_sort(working_data, custom_comparator))
        else:
            raise ValueError(f"Algorithm not yet implemented: {algorithm}")
        
        # Add final state frame
        final_frame = self._create_base_frame(
            working_data,
            message=f"Sorting complete! Array is now sorted in ascending order.",
            metadata={"phase": "final"}
        )
        # Mark all elements as completed
        for i in range(len(working_data)):
            final_frame.element_states[i] = ElementState.COMPLETED
        final_frame.highlighted_indices = list(range(len(working_data)))
        frames.append(final_frame)
        
        return frames
    
    def _animate_bubble_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for bubble sort animation."""
        frames = []
        n = len(data)
        comparator = custom_comparator or (lambda a, b: a > b)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Comparison frame
                comp_frame = self._create_base_frame(
                    data,
                    message=f"Comparing elements at indices {j} ({data[j]}) and {j+1} ({data[j+1]})",
                    metadata={"phase": "comparison", "indices": [j, j + 1]}
                )
                comp_frame.highlighted_indices = [j, j + 1]
                comp_frame.element_states[j] = ElementState.COMPARING
                comp_frame.element_states[j + 1] = ElementState.COMPARING
                frames.append(comp_frame)
                
                # Swap if needed
                if comparator(data[j], data[j + 1]):
                    # Swap frame
                    swap_frame = self._create_base_frame(
                        data,
                        message=f"Swapping {data[j]} and {data[j+1]} because {'a > b' if not custom_comparator else 'custom condition'}",
                        metadata={"phase": "swap", "indices": [j, j + 1]}
                    )
                    swap_frame.highlighted_indices = [j, j + 1]
                    swap_frame.element_states[j] = ElementState.SWAPPING
                    swap_frame.element_states[j + 1] = ElementState.SWAPPING
                    frames.append(swap_frame)
                    
                    # Perform swap
                    data[j], data[j + 1] = data[j + 1], data[j]
                    
                    # After swap frame
                    after_swap = self._create_base_frame(
                        data,
                        message=f"Swap complete. Array state after swap.",
                        metadata={"phase": "after_swap", "indices": [j, j + 1]}
                    )
                    after_swap.highlighted_indices = [j, j + 1]
                    frames.append(after_swap)
            
            # Mark the last element of this pass as sorted
            sorted_frame = self._create_base_frame(
                data,
                message=f"Pass {i + 1} complete. Element at index {n - i - 1} is now in correct position.",
                metadata={"phase": "pass_complete", "sorted_index": n - i - 1}
            )
            sorted_frame.element_states[n - i - 1] = ElementState.COMPLETED
            frames.append(sorted_frame)
        
        return frames
    
    def _animate_selection_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for selection sort animation."""
        frames = []
        n = len(data)
        comparator = custom_comparator or (lambda a, b: a > b)
        
        for i in range(n):
            min_idx = i
            
            # Find minimum element in unsorted portion
            find_min_frame = self._create_base_frame(
                data,
                message=f"Starting pass {i + 1}. Finding minimum element in unsorted portion.",
                metadata={"phase": "find_min", "start_index": i}
            )
            find_min_frame.highlighted_indices = list(range(i, n))
            find_min_frame.element_states[i] = ElementState.ACTIVE
            frames.append(find_min_frame)
            
            for j in range(i + 1, n):
                # Comparison with current minimum
                comp_frame = self._create_base_frame(
                    data,
                    message=f"Comparing {data[j]} with current minimum {data[min_idx]}",
                    metadata={"phase": "compare_min", "indices": [j, min_idx]}
                )
                comp_frame.highlighted_indices = [min_idx, j]
                comp_frame.element_states[min_idx] = ElementState.ACTIVE
                comp_frame.element_states[j] = ElementState.COMPARING
                frames.append(comp_frame)
                
                if comparator(data[min_idx], data[j]):
                    min_idx = j
                    
                    # New minimum found
                    new_min_frame = self._create_base_frame(
                        data,
                        message=f"New minimum found! Index {min_idx} contains {data[min_idx]}",
                        metadata={"phase": "new_min", "min_index": min_idx}
                    )
                    new_min_frame.highlighted_indices = [min_idx]
                    new_min_frame.element_states[min_idx] = ElementState.ACTIVE
                    frames.append(new_min_frame)
            
            # Swap if minimum is not in correct position
            if min_idx != i:
                swap_frame = self._create_base_frame(
                    data,
                    message=f"Swapping minimum element {data[min_idx]} with element at index {i} ({data[i]})",
                    metadata={"phase": "swap", "indices": [i, min_idx]}
                )
                swap_frame.highlighted_indices = [i, min_idx]
                swap_frame.element_states[i] = ElementState.SWAPPING
                swap_frame.element_states[min_idx] = ElementState.SWAPPING
                frames.append(swap_frame)
                
                data[i], data[min_idx] = data[min_idx], data[i]
                
                after_swap = self._create_base_frame(
                    data,
                    message="Swap complete.",
                    metadata={"phase": "after_swap", "indices": [i, min_idx]}
                )
                after_swap.highlighted_indices = [i]
                after_swap.element_states[i] = ElementState.COMPLETED
                frames.append(after_swap)
            else:
                # Element already in correct position
                correct_frame = self._create_base_frame(
                    data,
                    message=f"Element at index {i} is already in correct position.",
                    metadata={"phase": "correct_position", "index": i}
                )
                correct_frame.element_states[i] = ElementState.COMPLETED
                frames.append(correct_frame)
        
        return frames
    
    def _animate_insertion_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for insertion sort animation."""
        frames = []
        comparator = custom_comparator or (lambda a, b: a > b)
        
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            
            # Start inserting element
            insert_frame = self._create_base_frame(
                data,
                message=f"Inserting element {key} into sorted portion of array.",
                metadata={"phase": "insert_start", "key_index": i, "key_value": key}
            )
            insert_frame.highlighted_indices = list(range(i))
            insert_frame.element_states[i] = ElementState.ACTIVE
            frames.append(insert_frame)
            
            # Move elements greater than key
            while j >= 0 and comparator(data[j], key):
                # Shift frame
                shift_frame = self._create_base_frame(
                    data,
                    message=f"Shifting element {data[j]} to the right to make space for {key}",
                    metadata={"phase": "shift", "from_index": j, "to_index": j + 1}
                )
                shift_frame.highlighted_indices = [j, j + 1, i]
                shift_frame.element_states[j] = ElementState.SWAPPING
                shift_frame.element_states[j + 1] = ElementState.SWAPPING
                frames.append(shift_frame)
                
                data[j + 1] = data[j]
                
                after_shift = self._create_base_frame(
                    data,
                    message="Shift complete. Continuing to find correct position.",
                    metadata={"phase": "after_shift", "position": j}
                )
                after_shift.highlighted_indices = list(range(j + 1, i + 1))
                frames.append(after_shift)
                
                j -= 1
            
            data[j + 1] = key
            
            # Insertion complete
            insert_complete = self._create_base_frame(
                data,
                message=f"Inserted {key} at index {j + 1}. First {i + 1} elements are now sorted.",
                metadata={"phase": "insert_complete", "final_position": j + 1}
            )
            insert_complete.highlighted_indices = list(range(i + 1))
            for k in range(i + 1):
                insert_complete.element_states[k] = ElementState.COMPLETED
            frames.append(insert_complete)
        
        return frames
    
    def _animate_merge_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for merge sort animation."""
        frames = []
        
        def merge_sort_helper(arr: List[Union[int, float]], left: int, right: int):
            if left >= right:
                return
            
            mid = (left + right) // 2
            
            # Divide step
            divide_frame = self._create_base_frame(
                arr if left == 0 else data,
                message=f"Dividing: Working on subarray [{left}..{right}], splitting at midpoint {mid}",
                metadata={"phase": "divide", "left": left, "right": right, "mid": mid}
            )
            divide_frame.highlighted_indices = list(range(left, right + 1))
            frames.append(divide_frame)
            
            # Sort left half
            merge_sort_helper(arr if left == 0 else data, left, mid)
            
            # Sort right half
            merge_sort_helper(arr if left == 0 else data, mid + 1, right)
            
            # Merge step
            self._animate_merge(
                data if left == 0 else arr,
                left, mid, right,
                frames
            )
        
        merge_sort_helper(data, 0, len(data) - 1)
        return frames
    
    def _animate_merge(
        self,
        arr: List[Union[int, float]],
        left: int,
        mid: int,
        right: int,
        frames: List[AnimationFrame]
    ) -> None:
        """Generate frames for merge operation in merge sort."""
        # Create copies of both halves
        left_half = arr[left:mid + 1].copy()
        right_half = arr[mid + 1:right + 1].copy()
        
        # Merge frame
        merge_start = self._create_base_frame(
            arr,
            message=f"Merging sorted subarrays [{left}..{mid}] and [{mid + 1}..{right}]",
            metadata={"phase": "merge_start", "left": left, "mid": mid, "right": right}
        )
        merge_start.highlighted_indices = list(range(left, right + 1))
        frames.append(merge_start)
        
        i = j = 0
        k = left
        
        while i < len(left_half) and j < len(right_half):
            # Comparison frame
            comp_frame = self._create_base_frame(
                arr,
                message=f"Comparing {left_half[i]} (from left) with {right_half[j]} (from right)",
                metadata={"phase": "merge_compare", "left_val": left_half[i], "right_val": right_half[j]}
            )
            comp_frame.highlighted_indices = [left + i, mid + 1 + j]
            comp_frame.element_states[left + i] = ElementState.COMPARING
            comp_frame.element_states[mid + 1 + j] = ElementState.COMPARING
            frames.append(comp_frame)
            
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                placed_frame = self._create_base_frame(
                    arr,
                    message=f"Placing {left_half[i]} at index {k}",
                    metadata={"phase": "merge_place", "value": left_half[i], "position": k}
                )
                placed_frame.highlighted_indices = [k]
                placed_frame.element_states[k] = ElementState.COMPLETED
                frames.append(placed_frame)
                i += 1
            else:
                arr[k] = right_half[j]
                placed_frame = self._create_base_frame(
                    arr,
                    message=f"Placing {right_half[j]} at index {k}",
                    metadata={"phase": "merge_place", "value": right_half[j], "position": k}
                )
                placed_frame.highlighted_indices = [k]
                placed_frame.element_states[k] = ElementState.COMPLETED
                frames.append(placed_frame)
                j += 1
            k += 1
        
        # Place remaining elements from left half
        while i < len(left_half):
            arr[k] = left_half[i]
            remaining_frame = self._create_base_frame(
                arr,
                message=f"Placing remaining element {left_half[i]} at index {k}",
                metadata={"phase": "merge_remaining", "value": left_half[i], "position": k}
            )
            remaining_frame.highlighted_indices = [k]
            remaining_frame.element_states[k] = ElementState.COMPLETED
            frames.append(remaining_frame)
            i += 1
            k += 1
        
        # Place remaining elements from right half
        while j < len(right_half):
            arr[k] = right_half[j]
            remaining_frame = self._create_base_frame(
                arr,
                message=f"Placing remaining element {right_half[j]} at index {k}",
                metadata={"phase": "merge_remaining", "value": right_half[j], "position": k}
            )
            remaining_frame.highlighted_indices = [k]
            remaining_frame.element_states[k] = ElementState.COMPLETED
            frames.append(remaining_frame)
            j += 1
            k += 1
        
        # Merge complete
        merge_complete = self._create_base_frame(
            arr,
            message=f"Merge complete. Subarray [{left}..{right}] is now sorted.",
            metadata={"phase": "merge_complete", "left": left, "right": right}
        )
        merge_complete.highlighted_indices = list(range(left, right + 1))
        for idx in range(left, right + 1):
            merge_complete.element_states[idx] = ElementState.COMPLETED
        frames.append(merge_complete)
    
    def _animate_quick_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for quick sort animation."""
        frames = []
        
        def quick_sort_helper(arr: List[Union[int, float]], low: int, high: int):
            if low < high:
                # Partitioning step
                pivot_frame = self._create_base_frame(
                    arr,
                    message=f"Partitioning subarray [{low}..{high}]. Choosing pivot.",
                    metadata={"phase": "partition_start", "low": low, "high": high}
                )
                pivot_frame.highlighted_indices = list(range(low, high + 1))
                pivot_frame.element_states[high] = ElementState.ACTIVE  # Using last element as pivot
                frames.append(pivot_frame)
                
                pivot_idx = self._animate_partition(arr, low, high, frames)
                
                # Recursively sort partitions
                quick_sort_helper(arr, low, pivot_idx - 1)
                quick_sort_helper(arr, pivot_idx + 1, high)
        
        quick_sort_helper(data, 0, len(data) - 1)
        return frames
    
    def _animate_partition(
        self,
        arr: List[Union[int, float]],
        low: int,
        high: int,
        frames: List[AnimationFrame]
    ) -> int:
        """Generate frames for partition operation in quick sort."""
        pivot = arr[high]
        i = low - 1
        
        # Pivot selection frame
        pivot_info = self._create_base_frame(
            arr,
            message=f"Using {pivot} as pivot. Partitioning elements relative to pivot.",
            metadata={"phase": "pivot_selection", "pivot": pivot, "pivot_index": high}
        )
        pivot_info.highlighted_indices = [high]
        pivot_info.element_states[high] = ElementState.ACTIVE
        frames.append(pivot_info)
        
        for j in range(low, high):
            # Compare with pivot
            comp_frame = self._create_base_frame(
                arr,
                message=f"Comparing {arr[j]} with pivot {pivot}",
                metadata={"phase": "pivot_compare", "value": arr[j], "pivot": pivot}
            )
            comp_frame.highlighted_indices = [j, high]
            comp_frame.element_states[j] = ElementState.COMPARING
            comp_frame.element_states[high] = ElementState.ACTIVE
            frames.append(comp_frame)
            
            if arr[j] <= pivot:
                i += 1
                
                if i != j:
                    # Swap
                    swap_frame = self._create_base_frame(
                        arr,
                        message=f"Element {arr[j]} <= pivot {pivot}. Swapping with element at index {i}.",
                        metadata={"phase": "pivot_swap", "indices": [i, j]}
                    )
                    swap_frame.highlighted_indices = [i, j]
                    swap_frame.element_states[i] = ElementState.SWAPPING
                    swap_frame.element_states[j] = ElementState.SWAPPING
                    frames.append(swap_frame)
                    
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    after_swap = self._create_base_frame(
                        arr,
                        message="Swap complete.",
                        metadata={"phase": "after_pivot_swap"}
                    )
                    after_swap.highlighted_indices = list(range(low, i + 1))
                    frames.append(after_swap)
            else:
                not_moved = self._create_base_frame(
                    arr,
                    message=f"Element {arr[j]} > pivot {pivot}. Keeping it in the right partition.",
                    metadata={"phase": "pivot_not_moved", "value": arr[j]}
                )
                not_moved.highlighted_indices = [j]
                frames.append(not_moved)
        
        # Final swap to place pivot
        if i + 1 != high:
            final_swap = self._create_base_frame(
                arr,
                message=f"Placing pivot {pivot} in correct position at index {i + 1}",
                metadata={"phase": "final_pivot_swap", "pivot_index": i + 1}
            )
            final_swap.highlighted_indices = [i + 1, high]
            final_swap.element_states[i + 1] = ElementState.SWAPPING
            final_swap.element_states[high] = ElementState.SWAPPING
            frames.append(final_swap)
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
        
        pivot_placed = self._create_base_frame(
            arr,
            message=f"Pivot {pivot} is now in its final position at index {i + 1}.",
            metadata={"phase": "pivot_placed", "final_position": i + 1}
        )
        pivot_placed.highlighted_indices = [i + 1]
        pivot_placed.element_states[i + 1] = ElementState.COMPLETED
        frames.append(pivot_placed)
        
        return i + 1
    
    def _animate_heap_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for heap sort animation."""
        frames = []
        n = len(data)
        
        # Build max heap
        build_heap_frame = self._create_base_frame(
            data,
            message="Building max heap from the array.",
            metadata={"phase": "build_heap"}
        )
        build_heap_frame.highlighted_indices = list(range(n))
        frames.append(build_heap_frame)
        
        for i in range(n // 2 - 1, -1, -1):
            self._animate_heapify(data, n, i, frames)
        
        # Extract elements from heap
        extract_frame = self._create_base_frame(
            data,
            message="Max heap built. Starting to extract elements in sorted order.",
            metadata={"phase": "extract_start"}
        )
        frames.append(extract_frame)
        
        for i in range(n - 1, 0, -1):
            # Swap root (max element) with last element
            swap_frame = self._create_base_frame(
                data,
                message=f"Swapping root (max element {data[0]}) with element at index {i}",
                metadata={"phase": "heap_swap", "indices": [0, i]}
            )
            swap_frame.highlighted_indices = [0, i]
            swap_frame.element_states[0] = ElementState.SWAPPING
            swap_frame.element_states[i] = ElementState.SWAPPING
            frames.append(swap_frame)
            
            data[0], data[i] = data[i], data[0]
            
            after_swap = self._create_base_frame(
                data,
                message=f"Element {data[i]} is now in its final sorted position.",
                metadata={"phase": "heap_extract", "position": i}
            )
            after_swap.highlighted_indices = list(range(i, n))
            after_swap.element_states[i] = ElementState.COMPLETED
            frames.append(after_swap)
            
            # Heapify the reduced heap
            self._animate_heapify(data, i, 0, frames)
        
        final_frame = self._create_base_frame(
            data,
            message="Heap sort complete. Array is sorted in ascending order.",
            metadata={"phase": "complete"}
        )
        for i in range(n):
            final_frame.element_states[i] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_heapify(
        self,
        arr: List[Union[int, float]],
        n: int,
        i: int,
        frames: List[AnimationFrame]
    ) -> None:
        """Generate frames for heapify operation."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        heapify_frame = self._create_base_frame(
            arr,
            message=f"Heapifying subtree rooted at index {i} with value {arr[i]}",
            metadata={"phase": "heapify_start", "index": i}
        )
        heapify_frame.highlighted_indices = [i]
        if left < n:
            heapify_frame.highlighted_indices.append(left)
        if right < n:
            heapify_frame.highlighted_indices.append(right)
        frames.append(heapify_frame)
        
        # Compare with left child
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        # Compare with right child
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            # Swap
            swap_frame = self._create_base_frame(
                arr,
                message=f"Swapping {arr[i]} with {arr[largest]} to maintain heap property",
                metadata={"phase": "heapify_swap", "indices": [i, largest]}
            )
            swap_frame.highlighted_indices = [i, largest]
            swap_frame.element_states[i] = ElementState.SWAPPING
            swap_frame.element_states[largest] = ElementState.SWAPPING
            frames.append(swap_frame)
            
            arr[i], arr[largest] = arr[largest], arr[i]
            
            # Recursively heapify affected sub-tree
            self._animate_heapify(arr, n, largest, frames)
    
    def _animate_radix_sort(
        self,
        data: List[Union[int, float]]
    ) -> List[AnimationFrame]:
        """Generate frames for radix sort animation."""
        frames = []
        
        if not data:
            return frames
        
        max_val = max(data)
        num_digits = len(str(int(max_val)))
        
        for d in range(num_digits):
            digit_frame = self._create_base_frame(
                data,
                message=f"Sorting by digit at position {d} (1's place = {d == 0}, 10's place = {d == 1}, etc.)",
                metadata={"phase": "digit_start", "digit_position": d}
            )
            frames.append(digit_frame)
            
            # Counting sort by digit
            output = [0] * len(data)
            count = [0] * 10
            
            # Count occurrences
            for num in data:
                digit = (num // (10 ** d)) % 10
                count[digit] += 1
            
            count_frame = self._create_base_frame(
                data,
                message=f"Digit counts: {dict(enumerate(count))}",
                metadata={"phase": "count_digits", "counts": count}
            )
            frames.append(count_frame)
            
            # Calculate positions
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            position_frame = self._create_base_frame(
                data,
                message=f"Cumulative counts (positions): {count}",
                metadata={"phase": "cumulative_counts", "counts": count}
            )
            frames.append(position_frame)
            
            # Build output array
            for i in range(len(data) - 1, -1, -1):
                digit = (data[i] // (10 ** d)) % 10
                output[count[digit] - 1] = data[i]
                count[digit] -= 1
                
                place_frame = self._create_base_frame(
                    output,
                    message=f"Placing {data[i]} (digit {digit}) at position {count[digit]}",
                    metadata={"phase": "place", "value": data[i], "digit": digit}
                )
                place_frame.highlighted_indices = [count[digit]]
                frames.append(place_frame)
            
            data[:] = output[:]
            
            digit_complete = self._create_base_frame(
                data,
                message=f"Pass complete for digit position {d}. Current state: {data}",
                metadata={"phase": "digit_complete"}
            )
            frames.append(digit_complete)
        
        final_frame = self._create_base_frame(
            data,
            message="Radix sort complete!",
            metadata={"phase": "complete"}
        )
        for i in range(len(data)):
            final_frame.element_states[i] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_shell_sort(
        self,
        data: List[Union[int, float]],
        custom_comparator: Optional[callable] = None
    ) -> List[AnimationFrame]:
        """Generate frames for shell sort animation."""
        frames = []
        n = len(data)
        gap = n // 2
        pass_num = 1
        comparator = custom_comparator or (lambda a, b: a > b)
        
        while gap > 0:
            gap_frame = self._create_base_frame(
                data,
                message=f"Shell sort pass {pass_num}: Using gap of {gap}",
                metadata={"phase": "gap_start", "gap": gap, "pass": pass_num}
            )
            gap_frame.highlighted_indices = list(range(0, n, gap))
            frames.append(gap_frame)
            
            for i in range(gap, n):
                temp = data[i]
                j = i
                
                insert_frame = self._create_base_frame(
                    data,
                    message=f"Inserting element {temp} at index {i} into gap-sorted subarray",
                    metadata={"phase": "gap_insert", "value": temp, "index": i, "gap": gap}
                )
                insert_frame.highlighted_indices = list(range(i % gap, i + 1, gap))
                insert_frame.element_states[i] = ElementState.ACTIVE
                frames.append(insert_frame)
                
                while j >= gap and comparator(data[j - gap], temp):
                    shift_frame = self._create_base_frame(
                        data,
                        message=f"Shifting {data[j - gap]} to make space for {temp}",
                        metadata={"phase": "gap_shift", "from": j - gap, "to": j}
                    )
                    shift_frame.highlighted_indices = [j - gap, j]
                    shift_frame.element_states[j - gap] = ElementState.SWAPPING
                    shift_frame.element_states[j] = ElementState.SWAPPING
                    frames.append(shift_frame)
                    
                    data[j] = data[j - gap]
                    j -= gap
                
                data[j] = temp
                
                after_insert = self._create_base_frame(
                    data,
                    message=f"Inserted {temp} at index {j}. Subarray with gap {gap} remains sorted.",
                    metadata={"phase": "gap_insert_complete"}
                )
                after_insert.highlighted_indices = list(range(j, i + 1, gap))
                frames.append(after_insert)
            
            gap //= 2
            pass_num += 1
        
        final_frame = self._create_base_frame(
            data,
            message="Shell sort complete!",
            metadata={"phase": "complete"}
        )
        for i in range(len(data)):
            final_frame.element_states[i] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    # ==================== GRAPH TRAVERSAL ANIMATIONS ====================
    
    def create_graph_traversal_frames(
        self,
        graph: Dict[Any, List[Any]],
        start_node: Any,
        traversal_type: Union[str, GraphTraversalType]
    ) -> List[GraphAnimationFrame]:
        """
        Generate animation frames for graph traversal algorithms.
        
        Args:
            graph: Adjacency list representation of the graph
            start_node: Starting node for traversal
            traversal_type: Type of graph traversal (BFS, DFS, Dijkstra, Bellman-Ford)
            
        Returns:
            List of GraphAnimationFrame objects
            
        Raises:
            ValueError: If the traversal type is not supported
        """
        if isinstance(traversal_type, str):
            try:
                traversal_type = GraphTraversalType(traversal_type.lower())
            except ValueError:
                raise ValueError(f"Unsupported graph traversal type: {traversal_type}")
        
        if traversal_type == GraphTraversalType.BFS:
            return self._animate_bfs(graph, start_node)
        elif traversal_type == GraphTraversalType.DFS:
            return self._animate_dfs(graph, start_node)
        elif traversal_type == GraphTraversalType.DIJKSTRA:
            return self._animate_dijkstra(graph, start_node)
        elif traversal_type == GraphTraversalType.BELLMAN_FORD:
            return self._animate_bellman_ford(graph, start_node)
        else:
            raise ValueError(f"Algorithm not yet implemented: {traversal_type}")
    
    def _animate_bfs(
        self,
        graph: Dict[Any, List[Any]],
        start_node: Any
    ) -> List[GraphAnimationFrame]:
        """Generate frames for BFS traversal animation."""
        frames = []
        visited = set()
        queue = []
        
        # Initial frame
        init_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            queue_state=[],
            message=f"Starting BFS from node {start_node}",
            metadata={"phase": "init", "start_node": start_node}
        )
        init_frame.node_states[start_node] = ElementState.ACTIVE
        frames.append(init_frame)
        
        # Add start node to queue
        visited.add(start_node)
        queue.append(start_node)
        
        queue_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            queue_state=queue.copy(),
            message=f"Added {start_node} to queue. Visited set: {visited}",
            metadata={"phase": "enqueue", "node": start_node}
        )
        queue_frame.node_states[start_node] = ElementState.ACTIVE
        frames.append(queue_frame)
        
        while queue:
            current = queue.pop(0)
            
            # Process current node
            process_frame = GraphAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=list(visited),
                current_node=current,
                queue_state=queue.copy(),
                message=f"Processing node {current} from front of queue",
                metadata={"phase": "process", "current": current}
            )
            for node in visited:
                process_frame.node_states[node] = ElementState.COMPLETED
            process_frame.node_states[current] = ElementState.ACTIVE
            frames.append(process_frame)
            
            # Mark as visited (if not already in visited list)
            if current not in frames[-1].visited_nodes:
                frames[-1].visited_nodes.append(current)
            
            # Explore neighbors
            neighbors = graph.get(current, [])
            neighbors_frame = GraphAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=list(visited),
                current_node=current,
                queue_state=queue.copy(),
                message=f"Node {current} has neighbors: {neighbors}",
                metadata={"phase": "explore", "neighbors": neighbors}
            )
            for node in visited:
                neighbors_frame.node_states[node] = ElementState.COMPLETED
            neighbors_frame.node_states[current] = ElementState.ACTIVE
            for neighbor in neighbors:
                if neighbor not in visited:
                    neighbors_frame.edge_states[(current, neighbor)] = ElementState.COMPARING
                    neighbors_frame.node_states[neighbor] = ElementState.COMPARING
            frames.append(neighbors_frame)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
                    # Mark edge as traversed
                    edge_traversed = GraphAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=list(visited),
                        current_node=current,
                        queue_state=queue.copy(),
                        message=f"Traversed edge ({current}, {neighbor}). Added {neighbor} to queue.",
                        metadata={"phase": "traverse", "edge": (current, neighbor), "neighbor": neighbor}
                    )
                    for node in visited:
                        edge_traversed.node_states[node] = ElementState.COMPLETED
                    edge_traversed.node_states[current] = ElementState.COMPLETED
                    edge_traversed.edge_states[(current, neighbor)] = ElementState.ACTIVE
                    edge_traversed.node_states[neighbor] = ElementState.ACTIVE
                    frames.append(edge_traversed)
        
        # Final frame
        final_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=list(visited),
            current_node=None,
            queue_state=queue.copy(),
            message=f"BFS complete! Visited nodes in order: {list(visited)}",
            metadata={"phase": "complete"}
        )
        for node in visited:
            final_frame.node_states[node] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_dfs(
        self,
        graph: Dict[Any, List[Any]],
        start_node: Any
    ) -> List[GraphAnimationFrame]:
        """Generate frames for DFS traversal animation."""
        frames = []
        visited = set()
        stack = [start_node]
        
        # Initial frame
        init_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            queue_state=stack.copy(),
            message=f"Starting DFS from node {start_node}",
            metadata={"phase": "init", "start_node": start_node}
        )
        init_frame.node_states[start_node] = ElementState.ACTIVE
        frames.append(init_frame)
        
        def dfs_visit(node: Any):
            visited.add(node)
            
            # Process node
            process_frame = GraphAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=list(visited),
                current_node=node,
                queue_state=stack.copy(),
                message=f"Visiting node {node} from stack",
                metadata={"phase": "visit", "node": node}
            )
            for v in visited:
                process_frame.node_states[v] = ElementState.COMPLETED
            process_frame.node_states[node] = ElementState.ACTIVE
            frames.append(process_frame)
            
            neighbors = graph.get(node, [])
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
                    
                    # Show stack push
                    push_frame = GraphAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=list(visited),
                        current_node=node,
                        queue_state=stack.copy(),
                        message=f"Pushed {neighbor} to stack. Exploring from {node} to {neighbor}.",
                        metadata={"phase": "push", "neighbor": neighbor, "from": node}
                    )
                    for v in visited:
                        push_frame.node_states[v] = ElementState.COMPLETED
                    push_frame.node_states[node] = ElementState.COMPLETED
                    push_frame.edge_states[(node, neighbor)] = ElementState.ACTIVE
                    push_frame.node_states[neighbor] = ElementState.ACTIVE
                    frames.append(push_frame)
                    
                    dfs_visit(neighbor)
                    
                    # Backtrack
                    backtrack_frame = GraphAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=list(visited),
                        current_node=node,
                        queue_state=stack.copy(),
                        message=f"Backtracking to node {node} after exploring {neighbor}",
                        metadata={"phase": "backtrack", "from": neighbor, "to": node}
                    )
                    for v in visited:
                        backtrack_frame.node_states[v] = ElementState.COMPLETED
                    backtrack_frame.node_states[neighbor] = ElementState.COMPLETED
                    frames.append(backtrack_frame)
        
        while stack:
            node = stack.pop()
            if node not in visited:
                dfs_visit(node)
        
        # Final frame
        final_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=list(visited),
            current_node=None,
            queue_state=[],
            message=f"DFS complete! Visited nodes: {list(visited)}",
            metadata={"phase": "complete"}
        )
        for node in visited:
            final_frame.node_states[node] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_dijkstra(
        self,
        graph: Dict[Any, List[Tuple[Any, int]]],
        start_node: Any
    ) -> List[GraphAnimationFrame]:
        """Generate frames for Dijkstra's algorithm animation."""
        frames = []
        
        # Initialize distances
        dist = {node: float('inf') for node in graph}
        dist[start_node] = 0
        visited = set()
        
        # Initial frame
        init_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            queue_state=[],
            message=f"Starting Dijkstra's algorithm from node {start_node}. Initial distances: {dist}",
            metadata={"phase": "init", "start_node": start_node, "distances": dist}
        )
        init_frame.node_states[start_node] = ElementState.ACTIVE
        frames.append(init_frame)
        
        import heapq
        pq = [(0, start_node)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            # Process node
            process_frame = GraphAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=list(visited),
                current_node=current,
                queue_state=[n for _, n in pq],
                message=f"Processing node {current} with distance {current_dist}",
                metadata={"phase": "process", "node": current, "distance": current_dist}
            )
            for node in visited:
                process_frame.node_states[node] = ElementState.COMPLETED
            process_frame.node_states[current] = ElementState.ACTIVE
            frames.append(process_frame)
            
            neighbors = graph.get(current, [])
            
            for neighbor, weight in neighbors:
                if neighbor in visited:
                    continue
                
                new_dist = current_dist + weight
                
                # Compare distances
                comp_frame = GraphAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=list(visited),
                    current_node=current,
                    queue_state=[n for _, n in pq],
                    message=f"Checking edge ({current}, {neighbor}) with weight {weight}. Current distance to {neighbor}: {dist[neighbor]}, new distance: {new_dist}",
                    metadata={"phase": "compare", "edge": (current, neighbor), "weight": weight}
                )
                for node in visited:
                    comp_frame.node_states[node] = ElementState.COMPLETED
                comp_frame.node_states[current] = ElementState.COMPLETED
                comp_frame.edge_states[(current, neighbor)] = ElementState.COMPARING
                comp_frame.node_states[neighbor] = ElementState.COMPARING
                frames.append(comp_frame)
                
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    
                    update_frame = GraphAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=list(visited),
                        current_node=current,
                        queue_state=[n for _, n in pq],
                        message=f"Updated distance to {neighbor}: {new_dist}. Adding to priority queue.",
                        metadata={"phase": "update", "node": neighbor, "new_distance": new_dist}
                    )
                    for node in visited:
                        update_frame.node_states[node] = ElementState.COMPLETED
                    update_frame.node_states[current] = ElementState.COMPLETED
                    update_frame.edge_states[(current, neighbor)] = ElementState.ACTIVE
                    update_frame.node_states[neighbor] = ElementState.ACTIVE
                    frames.append(update_frame)
                    
                    heapq.heappush(pq, (new_dist, neighbor))
                else:
                    skip_frame = GraphAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=list(visited),
                        current_node=current,
                        queue_state=[n for _, n in pq],
                        message=f"No update needed. Current distance to {neighbor} is better.",
                        metadata={"phase": "skip", "node": neighbor}
                    )
                    for node in visited:
                        skip_frame.node_states[node] = ElementState.COMPLETED
                    skip_frame.node_states[current] = ElementState.COMPLETED
                    frames.append(skip_frame)
        
        # Final frame
        final_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=list(visited),
            current_node=None,
            queue_state=[],
            message=f"Dijkstra's algorithm complete! Shortest distances: {dist}",
            metadata={"phase": "complete", "distances": dist}
        )
        for node in visited:
            final_frame.node_states[node] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_bellman_ford(
        self,
        graph: Dict[Any, List[Tuple[Any, int]]],
        start_node: Any
    ) -> List[GraphAnimationFrame]:
        """Generate frames for Bellman-Ford algorithm animation."""
        frames = []
        
        # Get all nodes
        nodes = set(graph.keys())
        for neighbors in graph.values():
            for neighbor, _ in neighbors:
                nodes.add(neighbor)
        
        # Initialize distances
        dist = {node: float('inf') for node in nodes}
        dist[start_node] = 0
        
        # Initial frame
        init_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            queue_state=[],
            message=f"Starting Bellman-Ford algorithm from node {start_node}",
            metadata={"phase": "init", "start_node": start_node}
        )
        init_frame.node_states[start_node] = ElementState.ACTIVE
        frames.append(init_frame)
        
        # Relaxation passes
        for i in range(len(nodes) - 1):
            pass_frame = GraphAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=[],
                current_node=None,
                queue_state=[],
                message=f"Relaxation pass {i + 1} of {len(nodes) - 1}",
                metadata={"phase": "pass", "pass_number": i + 1}
            )
            frames.append(pass_frame)
            
            relaxations = 0
            for node in nodes:
                for neighbor, weight in graph.get(node, []):
                    if dist[node] != float('inf') and dist[node] + weight < dist[neighbor]:
                        relax_frame = GraphAnimationFrame(
                            frame_number=self._next_frame_number(),
                            visited_nodes=[],
                            current_node=node,
                            queue_state=[],
                            message=f"Relaxing edge ({node}, {neighbor}): {dist[node]} + {weight} < {dist[neighbor]}. Updating {neighbor} to {dist[node] + weight}.",
                            metadata={"phase": "relax", "edge": (node, neighbor), "weight": weight, "old_dist": dist[neighbor], "new_dist": dist[node] + weight}
                        )
                        relax_frame.node_states[node] = ElementState.ACTIVE
                        relax_frame.node_states[neighbor] = ElementState.ACTIVE
                        relax_frame.edge_states[(node, neighbor)] = ElementState.ACTIVE
                        frames.append(relax_frame)
                        
                        dist[neighbor] = dist[node] + weight
                        relaxations += 1
            
            if relaxations == 0:
                no_relax = GraphAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=[],
                    current_node=None,
                    queue_state=[],
                    message=f"No relaxations in pass {i + 1}. Distances may be optimal.",
                    metadata={"phase": "no_relax", "pass": i + 1}
                )
                frames.append(no_relax)
        
        # Final frame
        final_frame = GraphAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            queue_state=[],
            message=f"Bellman-Ford complete! Shortest distances: {dist}",
            metadata={"phase": "complete", "distances": dist}
        )
        for node in nodes:
            final_frame.node_states[node] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    # ==================== TREE TRAVERSAL ANIMATIONS ====================
    
    def create_tree_traversal_frames(
        self,
        tree: Dict[str, Any],
        traversal_type: Union[str, TreeTraversalType]
    ) -> List[TreeAnimationFrame]:
        """
        Generate animation frames for tree traversal algorithms.
        
        Args:
            tree: Tree represented as a nested dictionary with 'value', 'left', 'right' keys
            traversal_type: Type of tree traversal (pre-order, in-order, post-order, level-order)
            
        Returns:
            List of TreeAnimationFrame objects
            
        Raises:
            ValueError: If the traversal type is not supported
        """
        if isinstance(traversal_type, str):
            try:
                traversal_type = TreeTraversalType(traversal_type.lower().replace('-', '_'))
            except ValueError:
                raise ValueError(f"Unsupported tree traversal type: {traversal_type}")
        
        if traversal_type == TreeTraversalType.PRE_ORDER:
            return self._animate_pre_order(tree)
        elif traversal_type == TreeTraversalType.IN_ORDER:
            return self._animate_in_order(tree)
        elif traversal_type == TreeTraversalType.POST_ORDER:
            return self._animate_post_order(tree)
        elif traversal_type == TreeTraversalType.LEVEL_ORDER:
            return self._animate_level_order(tree)
        else:
            raise ValueError(f"Algorithm not yet implemented: {traversal_type}")
    
    def _animate_pre_order(
        self,
        tree: Optional[Dict[str, Any]]
    ) -> List[TreeAnimationFrame]:
        """Generate frames for pre-order traversal animation."""
        frames = []
        visited = []
        path = []
        
        def pre_order_helper(node: Optional[Dict[str, Any]], current_path: List[str]):
            if node is None:
                return
            
            value = node['value']
            visited.append(value)
            path = current_path + [value]
            
            # Visit node
            visit_frame = TreeAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=visited.copy(),
                current_node=value,
                path=path,
                message=f"Pre-order: Visiting node {value}. Current path: {' -> '.join(path)}",
                metadata={"phase": "visit", "value": value, "traversal": "pre-order"}
            )
            visit_frame.node_states[value] = ElementState.ACTIVE
            for v in visited[:-1]:
                visit_frame.node_states[v] = ElementState.COMPLETED
            frames.append(visit_frame)
            
            # Visit left subtree
            if node.get('left'):
                left_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=value,
                    path=path,
                    message=f"Traversing left subtree of {value}",
                    metadata={"phase": "left", "parent": value}
                )
                left_frame.node_states[value] = ElementState.ACTIVE
                for v in visited[:-1]:
                    left_frame.node_states[v] = ElementState.COMPLETED
                frames.append(left_frame)
                
                pre_order_helper(node['left'], path)
            
            # Visit right subtree
            if node.get('right'):
                right_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=value,
                    path=path,
                    message=f"Traversing right subtree of {value}",
                    metadata={"phase": "right", "parent": value}
                )
                right_frame.node_states[value] = ElementState.ACTIVE
                for v in visited:
                    right_frame.node_states[v] = ElementState.COMPLETED
                frames.append(right_frame)
                
                pre_order_helper(node['right'], path)
        
        # Initial frame
        init_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            path=[],
            message="Starting pre-order traversal (Root -> Left -> Right)",
            metadata={"phase": "init", "traversal": "pre-order"}
        )
        frames.append(init_frame)
        
        pre_order_helper(tree, [])
        
        # Final frame
        final_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=visited,
            current_node=None,
            path=[],
            message=f"Pre-order traversal complete! Visit order: {' -> '.join(map(str, visited))}",
            metadata={"phase": "complete", "order": visited}
        )
        for v in visited:
            final_frame.node_states[v] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_in_order(
        self,
        tree: Optional[Dict[str, Any]]
    ) -> List[TreeAnimationFrame]:
        """Generate frames for in-order traversal animation."""
        frames = []
        visited = []
        path = []
        
        def in_order_helper(node: Optional[Dict[str, Any]], current_path: List[str]):
            if node is None:
                return
            
            # Visit left subtree first
            if node.get('left'):
                left_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=node['value'],
                    path=current_path + [node['value']],
                    message=f"Going to left subtree of {node['value']}",
                    metadata={"phase": "left", "parent": node['value']}
                )
                left_frame.node_states[node['value']] = ElementState.ACTIVE
                frames.append(left_frame)
                
                in_order_helper(node['left'], current_path + [node['value']])
            
            # Visit node
            value = node['value']
            visited.append(value)
            path = current_path + [value]
            
            visit_frame = TreeAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=visited.copy(),
                current_node=value,
                path=path,
                message=f"In-order: Visiting node {value}. This is in sorted order for BST.",
                metadata={"phase": "visit", "value": value, "traversal": "in-order"}
            )
            visit_frame.node_states[value] = ElementState.ACTIVE
            for v in visited[:-1]:
                visit_frame.node_states[v] = ElementState.COMPLETED
            frames.append(visit_frame)
            
            # Visit right subtree
            if node.get('right'):
                right_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=value,
                    path=path,
                    message=f"Going to right subtree of {value}",
                    metadata={"phase": "right", "parent": value}
                )
                right_frame.node_states[value] = ElementState.ACTIVE
                for v in visited:
                    right_frame.node_states[v] = ElementState.COMPLETED
                frames.append(right_frame)
                
                in_order_helper(node['right'], path)
        
        # Initial frame
        init_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            path=[],
            message="Starting in-order traversal (Left -> Root -> Right)",
            metadata={"phase": "init", "traversal": "in-order"}
        )
        frames.append(init_frame)
        
        in_order_helper(tree, [])
        
        # Final frame
        final_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=visited,
            current_node=None,
            path=[],
            message=f"In-order traversal complete! Visit order: {' -> '.join(map(str, visited))}",
            metadata={"phase": "complete", "order": visited}
        )
        for v in visited:
            final_frame.node_states[v] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_post_order(
        self,
        tree: Optional[Dict[str, Any]]
    ) -> List[TreeAnimationFrame]:
        """Generate frames for post-order traversal animation."""
        frames = []
        visited = []
        path = []
        
        def post_order_helper(node: Optional[Dict[str, Any]], current_path: List[str]):
            if node is None:
                return
            
            # Visit left subtree
            if node.get('left'):
                left_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=node['value'],
                    path=current_path + [node['value']],
                    message=f"Processing left subtree of {node['value']}",
                    metadata={"phase": "left", "parent": node['value']}
                )
                left_frame.node_states[node['value']] = ElementState.ACTIVE
                frames.append(left_frame)
                
                post_order_helper(node['left'], current_path + [node['value']])
            
            # Visit right subtree
            if node.get('right'):
                right_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=node['value'],
                    path=current_path + [node['value']],
                    message=f"Processing right subtree of {node['value']}",
                    metadata={"phase": "right", "parent": node['value']}
                )
                right_frame.node_states[node['value']] = ElementState.ACTIVE
                for v in visited:
                    right_frame.node_states[v] = ElementState.COMPLETED
                frames.append(right_frame)
                
                post_order_helper(node['right'], current_path + [node['value']])
            
            # Visit node
            value = node['value']
            visited.append(value)
            path = current_path + [value]
            
            visit_frame = TreeAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=visited.copy(),
                current_node=value,
                path=path,
                message=f"Post-order: All children processed. Now visiting node {value}.",
                metadata={"phase": "visit", "value": value, "traversal": "post-order"}
            )
            visit_frame.node_states[value] = ElementState.ACTIVE
            for v in visited[:-1]:
                visit_frame.node_states[v] = ElementState.COMPLETED
            frames.append(visit_frame)
        
        # Initial frame
        init_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            path=[],
            message="Starting post-order traversal (Left -> Right -> Root)",
            metadata={"phase": "init", "traversal": "post-order"}
        )
        frames.append(init_frame)
        
        post_order_helper(tree, [])
        
        # Final frame
        final_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=visited,
            current_node=None,
            path=[],
            message=f"Post-order traversal complete! Visit order: {' -> '.join(map(str, visited))}",
            metadata={"phase": "complete", "order": visited}
        )
        for v in visited:
            final_frame.node_states[v] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    def _animate_level_order(
        self,
        tree: Optional[Dict[str, Any]]
    ) -> List[TreeAnimationFrame]:
        """Generate frames for level-order (BFS) traversal animation."""
        from collections import deque
        
        frames = []
        visited = []
        
        if tree is None:
            # Initial frame for empty tree
            init_frame = TreeAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=[],
                current_node=None,
                path=[],
                message="Starting level-order traversal (Breadth-first)",
                metadata={"phase": "init", "traversal": "level-order"}
            )
            frames.append(init_frame)
            
            final_frame = TreeAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=[],
                current_node=None,
                path=[],
                message="Tree is empty. Level-order traversal complete.",
                metadata={"phase": "complete"}
            )
            frames.append(final_frame)
            return frames
        
        queue = deque([tree])
        
        # Initial frame
        init_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=[],
            current_node=None,
            path=[],
            message="Starting level-order traversal (Breadth-first, by levels)",
            metadata={"phase": "init", "traversal": "level-order frames.append(init_frame"}
        )
       )
        
        level = 0
        while queue:
            level_size = len(queue)
            level_nodes = []
            
            level_frame = TreeAnimationFrame(
                frame_number=self._next_frame_number(),
                visited_nodes=visited.copy(),
                current_node=None,
                path=[],
                message=f"Processing level {level} with {level_size} nodes",
                metadata={"phase": "level", "level": level, "level_size": level_size}
            )
            for node in visited:
                level_frame.node_states[node] = ElementState.COMPLETED
            frames.append(level_frame)
            
            for _ in range(level_size):
                node = queue.popleft()
                value = node['value']
                visited.append(value)
                level_nodes.append(value)
                
                # Visit node
                visit_frame = TreeAnimationFrame(
                    frame_number=self._next_frame_number(),
                    visited_nodes=visited.copy(),
                    current_node=value,
                    path=[],
                    message=f"Visiting node {value} at level {level}",
                    metadata={"phase": "visit", "value": value, "level": level}
                )
                visit_frame.node_states[value] = ElementState.ACTIVE
                for v in visited[:-1]:
                    visit_frame.node_states[v] = ElementState.COMPLETED
                frames.append(visit_frame)
                
                # Add children to queue
                if node.get('left'):
                    queue.append(node['left'])
                    child_frame = TreeAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=visited.copy(),
                        current_node=value,
                        path=[],
                        message=f"Adding left child of {value} to queue",
                        metadata={"phase": "add_child", "parent": value, "child_position": "left"}
                    )
                    child_frame.node_states[value] = ElementState.ACTIVE
                    for v in visited:
                        child_frame.node_states[v] = ElementState.COMPLETED
                    frames.append(child_frame)
                
                if node.get('right'):
                    queue.append(node['right'])
                    child_frame = TreeAnimationFrame(
                        frame_number=self._next_frame_number(),
                        visited_nodes=visited.copy(),
                        current_node=value,
                        path=[],
                        message=f"Adding right child of {value} to queue",
                        metadata={"phase": "add_child", "parent": value, "child_position": "right"}
                    )
                    child_frame.node_states[value] = ElementState.ACTIVE
                    for v in visited:
                        child_frame.node_states[v] = ElementState.COMPLETED
                    frames.append(child_frame)
            
            level += 1
        
        # Final frame
        final_frame = TreeAnimationFrame(
            frame_number=self._next_frame_number(),
            visited_nodes=visited,
            current_node=None,
            path=[],
            message=f"Level-order traversal complete! Visit order: {' -> '.join(map(str, visited))}",
            metadata={"phase": "complete", "order": visited}
        )
        for v in visited:
            final_frame.node_states[v] = ElementState.COMPLETED
        frames.append(final_frame)
        
        return frames
    
    # ==================== SEARCH ANIMATIONS ====================
    
    def create_search_frames(
        self,
        data: List[Union[int, float]],
        target: Union[int, float],
        algorithm: str = "binary"
    ) -> List[AnimationFrame]:
        """
        Generate animation frames for search algorithms.
        
        Args:
            data: Sorted list of elements to search
            target: Target value to find
            algorithm: Search algorithm to use ("linear" or "binary")
            
        Returns:
            List of AnimationFrame objects
            
        Raises:
            ValueError: If the algorithm is not supported
        """
        if algorithm.lower() == "linear":
            return self._animate_linear_search(data, target)
        elif algorithm.lower() == "binary":
            return self._animate_binary_search(data, target)
        else:
            raise ValueError(f"Unsupported search algorithm: {algorithm}")
    
    def _animate_linear_search(
        self,
        data: List[Union[int, float]],
        target: Union[int, float]
    ) -> List[AnimationFrame]:
        """Generate frames for linear search animation."""
        frames = []
        
        # Initial frame
        init_frame = self._create_base_frame(
            data,
            message=f"Starting linear search for target value {target}",
            metadata={"phase": "init", "target": target}
        )
        init_frame.element_states[0] = ElementState.ACTIVE
        frames.append(init_frame)
        
        for i, element in enumerate(data):
            # Compare frame
            if element == target:
                found_frame = self._create_base_frame(
                    data,
                    message=f"Found target {target} at index {i}!",
                    metadata={"phase": "found", "target": target, "index": i}
                )
                found_frame.highlighted_indices = [i]
                found_frame.element_states[i] = ElementState.FOUND
                frames.append(found_frame)
                break
            else:
                not_match = self._create_base_frame(
                    data,
                    message=f"Element at index {i} is {element}, not the target {target}",
                    metadata={"phase": "compare", "index": i, "value": element}
                )
                not_match.highlighted_indices = [i]
                not_match.element_states[i] = ElementState.COMPARING
                frames.append(not_match)
        else:
            # Not found
            not_found = self._create_base_frame(
                data,
                message=f"Target {target} not found in the array",
                metadata={"phase": "not_found", "target": target}
            )
            not_found.element_states[len(data) - 1] = ElementState.NOT_FOUND
            frames.append(not_found)
        
        return frames
    
    def _animate_binary_search(
        self,
        data: List[Union[int, float]],
        target: Union[int, float]
    ) -> List[AnimationFrame]:
        """Generate frames for binary search animation."""
        frames = []
        left, right = 0, len(data) - 1
        
        # Initial frame
        init_frame = self._create_base_frame(
            data,
            message=f"Starting binary search for target {target} in sorted array",
            metadata={"phase": "init", "target": target}
        )
        init_frame.highlighted_indices = [left, right]
        init_frame.element_states[left] = ElementState.ACTIVE
        init_frame.element_states[right] = ElementState.ACTIVE
        frames.append(init_frame)
        
        while left <= right:
            mid = (left + right) // 2
            
            # Mid calculation
            mid_frame = self._create_base_frame(
                data,
                message=f"Search range: [{left}, {right}]. Calculating middle index: ({left} + {right}) // 2 = {mid}",
                metadata={"phase": "mid_calc", "left": left, "right": right, "mid": mid}
            )
            mid_frame.highlighted_indices = [left, right]
            mid_frame.element_states[left] = ElementState.ACTIVE
            mid_frame.element_states[right] = ElementState.ACTIVE
            frames.append(mid_frame)
            
            # Compare with mid
            comp_frame = self._create_base_frame(
                data,
                message=f"Comparing target {target} with middle element data[{mid}] = {data[mid]}",
                metadata={"phase": "compare", "mid": mid, "mid_value": data[mid]}
            )
            comp_frame.highlighted_indices = [mid, left, right]
            comp_frame.element_states[mid] = ElementState.COMPARING
            comp_frame.element_states[left] = ElementState.ACTIVE
            comp_frame.element_states[right] = ElementState.ACTIVE
            frames.append(comp_frame)
            
            if data[mid] == target:
                # Found!
                found_frame = self._create_base_frame(
                    data,
                    message=f"Found target {target} at index {mid}!",
                    metadata={"phase": "found", "index": mid, "value": data[mid]}
                )
                found_frame.highlighted_indices = [mid]
                found_frame.element_states[mid] = ElementState.FOUND
                frames.append(found_frame)
                break
            elif data[mid] < target:
                # Search right half
                right_search = self._create_base_frame(
                    data,
                    message=f"{data[mid]} < {target}. Target must be in right half. New search range: [{mid + 1}, {right}]",
                    metadata={"phase": "right_half", "mid": mid, "new_left": mid + 1, "right": right}
                )
                right_search.highlighted_indices = list(range(mid + 1, right + 1))
                right_search.element_states[mid] = ElementState.COMPLETED
                for i in range(mid + 1, right + 1):
                    if i == mid + 1:
                        right_search.element_states[i] = ElementState.ACTIVE
                frames.append(right_search)
                left = mid + 1
            else:
                # Search left half
                left_search = self._create_base_frame(
                    data,
                    message=f"{data[mid]} > {target}. Target must be in left half. New search range: [{left}, {mid - 1}]",
                    metadata={"phase": "left_half", "mid": mid, "left": left, "new_right": mid - 1}
                )
                left_search.highlighted_indices = list(range(left, mid))
                left_search.element_states[mid] = ElementState.COMPLETED
                for i in range(left, mid):
                    if i == mid - 1:
                        left_search.element_states[i] = ElementState.ACTIVE
                frames.append(left_search)
                right = mid - 1
        else:
            # Not found
            not_found = self._create_base_frame(
                data,
                message=f"Target {target} not found in the array",
                metadata={"phase": "not_found", "target": target}
            )
            frames.append(not_found)
        
        return frames
    
    # ==================== CUSTOM ALGORITHM SUPPORT ====================
    
    def register_custom_algorithm(
        self,
        name: str,
        frame_generator: callable
    ) -> None:
        """
        Register a custom algorithm for animation generation.
        
        Args:
            name: Unique name for the custom algorithm
            frame_generator: Function that takes input data and returns animation frames
        """
        self._custom_algorithms[name] = frame_generator
    
    def create_custom_animation(
        self,
        algorithm_name: str,
        data: Any,
        **kwargs
    ) -> List[AnimationFrame]:
        """
        Generate animation frames for a registered custom algorithm.
        
        Args:
            algorithm_name: Name of the registered custom algorithm
            data: Input data for the algorithm
            **kwargs: Additional arguments to pass to the custom algorithm
            
        Returns:
            List of AnimationFrame objects
            
        Raises:
            ValueError: If the algorithm is not registered
        """
        if algorithm_name not in self._custom_algorithms:
            raise ValueError(f"Custom algorithm '{algorithm_name}' not registered")
        
        return self._custom_algorithms[algorithm_name](data, **kwargs)
    
    # ==================== SEQUENCE ASSEMBLY ====================
    
    def assemble_animation_sequence(
        self,
        frames: List[Union[AnimationFrame, GraphAnimationFrame, TreeAnimationFrame]],
        animation_type: AnimationType,
        algorithm_name: str,
        initial_data: Any,
        complexity_info: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AnimationSequence:
        """
        Assemble a complete animation sequence from generated frames.
        
        Args:
            frames: List of animation frames
            animation_type: Type of animation
            algorithm_name: Name of the algorithm
            initial_data: Original input data
            complexity_info: Optional time/space complexity information
            metadata: Optional additional metadata
            
        Returns:
            Complete AnimationSequence object
        """
        # Update frame timestamps
        frame_duration = 0.5  # seconds per frame
        for i, frame in enumerate(frames):
            frame.timestamp = i * frame_duration
        
        return AnimationSequence(
            animation_type=animation_type,
            algorithm_name=algorithm_name,
            total_frames=len(frames),
            frames=frames,
            initial_data=initial_data,
            complexity_info=complexity_info or {},
            metadata=metadata or {}
        )
    
    # ==================== UTILITY METHODS ====================
    
    def get_supported_algorithms(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of all supported algorithms by category.
        
        Returns:
            Dictionary mapping algorithm categories to lists of algorithm names
        """
        return {
            "sorting": [algo.value for algo in SortingAlgorithm],
            "graph_traversal": [algo.value for algo in GraphTraversalType],
            "tree_traversal": [algo.value for algo in TreeTraversalType],
            "search": ["linear", "binary"],
            "custom": list(self._custom_algorithms.keys())
        }
    
    def get_algorithm_complexity(
        self,
        algorithm_name: str
    ) -> Optional[Dict[str, str]]:
        """
        Get time and space complexity information for an algorithm.
        
        Args:
            algorithm_name: Name of the algorithm
            
        Returns:
            Dictionary with 'time' and 'space' complexity, or None if not found
        """
        complexities = {
            "bubble_sort": {"time": "O(n²)", "space": "O(1)"},
            "selection_sort": {"time": "O(n²)", "space": "O(1)"},
            "insertion_sort": {"time": "O(n²)", "space": "O(1)"},
            "merge_sort": {"time": "O(n log n)", "space": "O(n)"},
            "quick_sort": {"time": "O(n log n)", "space": "O(log n)"},
            "heap_sort": {"time": "O(n log n)", "space": "O(1)"},
            "radix_sort": {"time": "O(nk)", "space": "O(n + k)"},
            "shell_sort": {"time": "O(n log n) - O(n²)", "space": "O(1)"},
            "bfs": {"time": "O(V + E)", "space": "O(V)"},
            "dfs": {"time": "O(V + E)", "space": "O(V)"},
            "dijkstra": {"time": "O((V + E) log V)", "space": "O(V)"},
            "bellman_ford": {"time": "O(VE)", "space": "O(V)"},
            "pre_order": {"time": "O(n)", "space": "O(h)"},
            "in_order": {"time": "O(n)", "space": "O(h)"},
            "post_order": {"time": "O(n)", "space": "O(h)"},
            "level_order": {"time": "O(n)", "space": "O(n)"},
            "linear": {"time": "O(n)", "space": "O(1)"},
            "binary": {"time": "O(log n)", "space": "O(1)"},
        }
        
        return complexities.get(algorithm_name.lower())
    
    def export_frames_to_dict(
        self,
        frames: List[Union[AnimationFrame, GraphAnimationFrame, TreeAnimationFrame]]
    ) -> List[Dict[str, Any]]:
        """
        Export animation frames to a list of dictionaries for serialization.
        
        Args:
            frames: List of animation frames to export
            
        Returns:
            List of dictionaries representing the frames
        """
        export_list = []
        for frame in frames:
            frame_dict = {
                "frame_number": frame.frame_number,
                "message": frame.message,
                "timestamp": frame.timestamp,
                "metadata": frame.metadata,
            }
            
            if isinstance(frame, AnimationFrame):
                frame_dict.update({
                    "data_state": frame.data_state,
                    "highlighted_indices": frame.highlighted_indices,
                    "element_states": {str(k): v.value for k, v in frame.element_states.items()}
                })
            elif isinstance(frame, GraphAnimationFrame):
                frame_dict.update({
                    "visited_nodes": frame.visited_nodes,
                    "current_node": frame.current_node,
                    "edge_states": {f"{k[0]}-{k[1]}": v.value for k, v in frame.edge_states.items()},
                    "node_states": {str(k): v.value for k, v in frame.node_states.items()},
                    "queue_state": frame.queue_state
                })
            elif isinstance(frame, TreeAnimationFrame):
                frame_dict.update({
                    "visited_nodes": frame.visited_nodes,
                    "current_node": frame.current_node,
                    "path": frame.path,
                    "node_states": {str(k): v.value for k, v in frame.node_states.items()}
                })
            
            export_list.append(frame_dict)
        
        return export_list
