"""
Learning Path Generation Service for VisualVerse Content Metadata Service

This module provides algorithms for generating optimal learning paths
based on prerequisite relationships and learning objectives. It implements
graph-based algorithms for topological sorting, path finding, and
learning sequence optimization. Integrates with the MasteryService for
personalized, mastery-aware path generation.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
from collections import deque

from ..models.learner_profile import (
    MasteryService,
    ConceptMastery,
    MasteryMetrics
)


logger = logging.getLogger(__name__)


# ============================================
# Data Classes for Learning Path Types
# ============================================

@dataclass
class LearningPathNode:
    """Represents a node in a learning path"""
    id: str
    name: str
    description: str
    duration_hours: float
    difficulty_level: str
    prerequisites: List[str]
    concepts: List[str]
    learning_outcomes: List[str]
    section_id: str
    section_order: int
    order_in_path: int
    
    # Mastery-aware fields
    estimated_mastery_score: float = 0.0  # Predicted after completion
    requires_review: bool = False  # If concept needs review first


@dataclass
class LearningPathMilestone:
    """Represents a milestone in a learning path"""
    name: str
    description: str
    unit_id: str
    concepts_mastered: List[str]
    after_unit: int


@dataclass
class LearningPath:
    """Represents a complete learning path"""
    id: str
    name: str
    description: str
    subject: str
    total_duration_hours: float
    total_units: int
    average_difficulty: str
    estimated_weeks: int
    nodes: List[LearningPathNode]
    milestones: List[LearningPathMilestone]
    created_at: datetime
    
    # Mastery-aware metrics
    current_mastery_average: float = 0.0
    projected_mastery_gain: float = 0.0
    concepts_to_review: List[str] = field(default_factory=list)


@dataclass
class PathGenerationConfig:
    """Configuration for path generation"""
    start_level: str
    target_level: str
    max_weekly_hours: int
    preferred_learning_style: Optional[str] = None
    include_prerequisites: bool = True
    group_by_section: bool = True
    
    # Mastery-aware configuration
    mastery_threshold: float = 0.7  # Minimum mastery to skip concept
    include_review_first: bool = True  # Include review items before new content
    adaptive_difficulty: bool = True  # Adjust based on current mastery


@dataclass
class PathValidationResult:
    """Result of path validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    total_prerequisite_hours: float
    achievable: bool
    
    # Mastery-aware validation results
    concepts_already_known: List[str] = field(default_factory=list)
    concepts_needing_review: List[str] = field(default_factory=list)
    estimated_start_mastery: float = 0.0


# ============================================
# Graph Node Class
# ============================================

class GraphNode:
    """Internal node class for the dependency graph"""
    
    def __init__(self, node_id: str, section_order: int = 0):
        self.id: str = node_id
        self.name: str = ""
        self.prerequisites: Set[str] = set()
        self.dependents: Set[str] = set()
        self.section_id: str = ""
        self.section_order: int = section_order
        self.duration_hours: float = 0.0
        self.difficulty_level: str = "intermediate"
        self.data: Any = None
        self.centrality: float = 0.0  # For identifying important concepts
    
    def add_prerequisite(self, prereq_id: str) -> None:
        """Add a prerequisite to this node"""
        self.prerequisites.add(prereq_id)
    
    def add_dependent(self, dep_id: str) -> None:
        """Add a dependent node to this node"""
        self.dependents.add(dep_id)
    
    def remove_prerequisite(self, prereq_id: str) -> bool:
        """Remove a prerequisite from this node"""
        return self.prerequisites.discard(prereq_id) is not None
    
    def has_prerequisites(self) -> bool:
        """Check if this node has any prerequisites"""
        return len(self.prerequisites) > 0
    
    def get_prerequisite_count(self) -> int:
        """Get the number of prerequisites"""
        return len(self.prerequisites)


# ============================================
# Graph Data Structure
# ============================================

class DependencyGraph:
    """
    A generic dependency graph for tracking prerequisite relationships.
    
    This class implements a directed acyclic graph (DAG) with methods for
    topological sorting, cycle detection, and path analysis.
    """
    
    def __init__(self):
        self._nodes: Dict[str, GraphNode] = {}
        self._node_data: Dict[str, Any] = {}
    
    def add_node(self, data: Any, section_id: str, section_order: int) -> None:
        """
        Add a node to the graph
        
        Args:
            data: Node data containing id, name, duration_hours, etc.
            section_id: The section this node belongs to
            section_order: The order of this node within its section
        """
        node_id = data.id
        
        if node_id in self._nodes:
            raise ValueError(f"Node with id '{node_id}' already exists")
        
        node = GraphNode(node_id, section_order)
        node.name = getattr(data, 'name', node_id)
        node.duration_hours = getattr(data, 'duration_hours', 0.0)
        node.section_id = section_id
        node.data = data
        
        # Extract difficulty level if available
        difficulty_level = getattr(data, 'difficulty_level', None)
        if difficulty_level:
            node.difficulty_level = difficulty_level
        
        self._nodes[node_id] = node
        self._node_data[node_id] = data
    
    def add_prerequisite(self, node_id: str, prereq_id: str) -> None:
        """
        Add a prerequisite relationship between two nodes
        
        Args:
            node_id: The dependent node
            prereq_id: The prerequisite node
        """
        if node_id not in self._nodes:
            raise ValueError(f"Node '{node_id}' not found")
        
        if prereq_id not in self._nodes:
            raise ValueError(f"Prerequisite '{prereq_id}' not found")
        
        self._nodes[node_id].add_prerequisite(prereq_id)
        self._nodes[prereq_id].add_dependent(node_id)
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by its ID"""
        return self._nodes.get(node_id)
    
    def get_all_nodes(self) -> List[GraphNode]:
        """Get all nodes in the graph"""
        return list(self._nodes.values())
    
    def get_node_data(self, node_id: str) -> Optional[Any]:
        """Get the original data for a node"""
        return self._node_data.get(node_id)
    
    def get_all_concept_ids(self) -> List[str]:
        """Get all concept IDs in the graph"""
        return list(self._nodes.keys())
    
    def topological_sort(self) -> List[str]:
        """
        Perform topological sort using Kahn's algorithm.
        
        Returns:
            List of node IDs in topological order
            
        Raises:
            ValueError: If the graph contains cycles
        """
        in_degree: Dict[str, int] = {}
        result: List[str] = []
        queue: deque = deque()
        
        # Initialize in-degrees
        for node_id, node in self._nodes.items():
            in_degree[node_id] = len(node.prerequisites)
            if len(node.prerequisites) == 0:
                queue.append(node_id)
        
        # Process nodes
        while queue:
            current_id = queue.popleft()
            result.append(current_id)
            
            current_node = self._nodes[current_id]
            for dependent_id in current_node.dependents:
                current_in_degree = in_degree[dependent_id]
                in_degree[dependent_id] = current_in_degree - 1
                
                if current_in_degree - 1 == 0:
                    queue.append(dependent_id)
        
        # Check for cycles
        if len(result) != len(self._nodes):
            raise ValueError("Graph contains cycles - cannot perform topological sort")
        
        return result
    
    def detect_cycles(self) -> bool:
        """
        Detect cycles in the graph using DFS.
        
        Returns:
            True if cycles are detected, False otherwise
        """
        visited: Set[str] = set()
        recursion_stack: Set[str] = set()
        
        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            recursion_stack.add(node_id)
            
            node = self._nodes.get(node_id)
            if not node:
                return False
            
            for prereq_id in node.prerequisites:
                if prereq_id not in visited:
                    if dfs(prereq_id):
                        return True
                elif prereq_id in recursion_stack:
                    return True  # Cycle detected
            
            recursion_stack.discard(node_id)
            return False
        
        for node_id in self._nodes.keys():
            if node_id not in visited:
                if dfs(node_id):
                    return True
        
        return False
    
    def get_all_prerequisites(self, node_id: str) -> List[str]:
        """
        Get all prerequisites for a node (transitive closure).
        
        Args:
            node_id: The node to get prerequisites for
            
        Returns:
            List of all prerequisite node IDs
        """
        result: List[str] = []
        visited: Set[str] = set()
        
        def collect(current_id: str) -> None:
            if current_id in visited:
                return
            visited.add(current_id)
            
            node = self._nodes.get(current_id)
            if not node:
                return
            
            for prereq_id in node.prerequisites:
                result.append(prereq_id)
                collect(prereq_id)
        
        collect(node_id)
        return list(set(result))
    
    def get_all_dependents(self, node_id: str) -> List[str]:
        """
        Get all dependents for a node (transitive closure).
        
        Args:
            node_id: The node to get dependents for
            
        Returns:
            List of all dependent node IDs
        """
        result: List[str] = []
        visited: Set[str] = set()
        
        def collect(current_id: str) -> None:
            if current_id in visited:
                return
            visited.add(current_id)
            
            node = self._nodes.get(current_id)
            if not node:
                return
            
            for dep_id in node.dependents:
                result.append(dep_id)
                collect(dep_id)
        
        collect(node_id)
        return list(set(result))
    
    def calculate_critical_path(self) -> Tuple[List[str], float]:
        """
        Calculate the longest path (critical path) for time estimation.
        
        Returns:
            Tuple of (path node IDs, total duration)
        """
        topo_order = self.topological_sort()
        distances: Dict[str, float] = {}
        predecessors: Dict[str, Optional[str]] = {}
        
        # Initialize
        for node_id in topo_order:
            distances[node_id] = 0.0
            predecessors[node_id] = None
        
        # Process in topological order
        for node_id in topo_order:
            node = self._nodes[node_id]
            node_distance = distances[node_id]
            
            for dependent_id in node.dependents:
                dep_node = self._nodes[dependent_id]
                new_distance = node_distance + node.duration_hours
                current_distance = distances[dependent_id]
                
                if new_distance > current_distance:
                    distances[dependent_id] = new_distance
                    predecessors[dependent_id] = node_id
        
        # Find the end node with maximum distance
        max_node = ""
        max_distance = 0.0
        for node_id, distance in distances.items():
            if distance > max_distance:
                max_distance = distance
                max_node = node_id
        
        # Reconstruct the path
        path: List[str] = []
        current: Optional[str] = max_node
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]
        
        return path, max_distance
    
    def get_nodes_by_section(self) -> Dict[str, List[GraphNode]]:
        """
        Group nodes by their section ID.
        
        Returns:
            Dictionary mapping section IDs to lists of nodes
        """
        result: Dict[str, List[GraphNode]] = {}
        
        for node in self._nodes.values():
            if node.section_id not in result:
                result[node.section_id] = []
            result[node.section_id].append(node)
        
        return result
    
    def calculate_levels(self) -> Dict[str, int]:
        """
        Calculate the level (distance from root) for each node.
        
        Returns:
            Dictionary mapping node IDs to their levels
        """
        levels: Dict[str, int] = {}
        visited: Set[str] = set()
        
        def set_level(node_id: str, level: int) -> None:
            if node_id in levels and levels[node_id] >= level:
                return
            levels[node_id] = level
            
            node = self._nodes.get(node_id)
            if not node:
                return
            
            for prereq_id in node.prerequisites:
                set_level(prereq_id, level - 1)
        
        # Start from nodes with no prerequisites
        for node_id, node in self._nodes.items():
            if len(node.prerequisites) == 0 and node_id not in visited:
                set_level(node_id, 0)
        
        # Handle remaining nodes
        for node_id in self._nodes.keys():
            if node_id not in levels:
                levels[node_id] = len(self.get_all_prerequisites(node_id))
        
        return levels
    
    def calculate_centrality(self) -> Dict[str, float]:
        """
        Calculate betweenness centrality for each node.
        
        Important concepts (high centrality) connect many other concepts
        and are often foundational to multiple topics.
        
        Returns:
            Dictionary mapping node IDs to centrality scores
        """
        # Simple approximation of betweenness centrality
        centrality: Dict[str, float] = {node_id: 0.0 for node_id in self._nodes}
        
        # Count how often each node appears in shortest paths
        topo_order = self.topological_sort()
        
        for start_node in self._nodes:
            for end_node in self._nodes:
                if start_node == end_node:
                    continue
                
                # Find path from start to end
                path = self._find_shortest_path(start_node, end_node)
                if path:
                    for node_id in path[1:-1]:  # Exclude endpoints
                        centrality[node_id] += 1
        
        # Normalize
        max_centrality = max(centrality.values()) if centrality else 1
        if max_centrality > 0:
            centrality = {k: v / max_centrality for k, v in centrality.items()}
        
        return centrality
    
    def _find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """Find shortest path using BFS"""
        if start == end:
            return [start]
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            current, path = queue.popleft()
            
            node = self._nodes.get(current)
            if not node:
                continue
            
            for prereq_id in node.prerequisites:
                if prereq_id == end:
                    return path + [prereq_id]
                
                if prereq_id not in visited:
                    visited.add(prereq_id)
                    queue.append((prereq_id, path + [prereq_id]))
        
        return None
    
    @property
    def node_count(self) -> int:
        """Get the number of nodes in the graph"""
        return len(self._nodes)


# ============================================
# Learning Path Generator
# ============================================

class LearningPathGenerator:
    """
    Generator for learning paths based on curriculum units and prerequisites.
    
    This class provides functionality to build learning paths from structured
    curriculum data, ensuring proper prerequisite ordering and optimal
    learning progression. Integrates with MasteryService for personalized,
    mastery-aware path generation.
    """
    
    # Difficulty level ordering
    DIFFICULTY_ORDER = {
        'beginner': 0,
        'elementary': 1,
        'intermediate': 2,
        'advanced': 3,
        'expert': 4
    }
    
    def __init__(
        self,
        subject: str,
        mastery_service: Optional[MasteryService] = None
    ):
        """
        Initialize the learning path generator.
        
        Args:
            subject: The subject this generator is for
            mastery_service: Optional mastery service for personalization
        """
        self.graph = DependencyGraph()
        self.subject = subject
        self._units: Dict[str, Any] = {}
        self._sections: Dict[str, Dict[str, Any]] = {}
        self._mastery_service = mastery_service
    
    def add_section(self, section_id: str, order: int, name: str) -> None:
        """
        Add a section to the curriculum.
        
        Args:
            section_id: Unique section identifier
            order: Section order within the curriculum
            name: Section name
        """
        self._sections[section_id] = {'order': order, 'name': name}
    
    def add_unit(self, section_id: str, unit: Any) -> None:
        """
        Add a learning unit to the curriculum.
        
        Args:
            section_id: The section this unit belongs to
            unit: Unit data with id, name, description, prerequisites, etc.
        """
        self._units[unit.id] = unit
        
        section_info = self._sections.get(section_id, {})
        section_order = section_info.get('order', 0)
        
        self.graph.add_node(unit, section_id, section_order)
        
        # Add prerequisites
        for prereq_id in getattr(unit, 'prerequisites', []):
            self.graph.add_prerequisite(unit.id, prereq_id)
    
    def set_mastery_service(self, mastery_service: MasteryService) -> None:
        """Set the mastery service for personalized path generation"""
        self._mastery_service = mastery_service
    
    def generate_path(
        self,
        start_unit_id: str,
        target_unit_id: str,
        config: PathGenerationConfig,
        learner_id: Optional[str] = None
    ) -> LearningPath:
        """
        Generate a learning path between two units.
        
        Args:
            start_unit_id: Starting unit ID
            target_unit_id: Target unit ID
            config: Path generation configuration
            learner_id: Optional learner ID for mastery-aware generation
            
        Returns:
            Generated learning path
            
        Raises:
            ValueError: If configuration is invalid
        """
        # Validate configuration
        validation = self._validate_configuration(start_unit_id, target_unit_id, config)
        if not validation.valid:
            raise ValueError(f"Invalid configuration: {', '.join(validation.errors)}")
        
        # Get mastery data if available
        mastery_map: Dict[str, ConceptMastery] = {}
        current_mastery_sum = 0.0
        known_concepts: List[str] = []
        review_concepts: List[str] = []
        
        if learner_id and self._mastery_service:
            mastery_records = self._mastery_service.get_all_mastery(learner_id)
            mastery_map = {m.concept_id: m for m in mastery_records}
            
            # Calculate current mastery stats
            for record in mastery_records:
                current_mastery_sum += record.mastery_score
                if record.is_considered_known(config.mastery_threshold):
                    known_concepts.append(record.concept_id)
                if record.is_overdue_for_review(datetime.now()):
                    review_concepts.append(record.concept_id)
        
        # Get all required units (including prerequisites if configured)
        required_units: Set[str] = set()
        
        if config.include_prerequisites:
            all_prereqs = self.graph.get_all_prerequisites(target_unit_id)
            for prereq_id in all_prereqs:
                if prereq_id >= start_unit_id and self._is_in_target_level_range(prereq_id, config):
                    required_units.add(prereq_id)
        
        required_units.add(target_unit_id)
        
        # Get topological order
        topo_order = self.graph.topological_sort()
        
        # Filter to only include units in range
        path_order = [
            node_id for node_id in topo_order
            if node_id in self._units
            and node_id >= start_unit_id
            and node_id <= target_unit_id
            and self._get_difficulty_order(self._units[node_id].difficulty_level) >= self._get_difficulty_order(config.start_level)
            and self._get_difficulty_order(self._units[node_id].difficulty_level) <= self._get_difficulty_order(config.target_level)
        ]
        
        # Build path nodes with mastery information
        path_nodes: List[LearningPathNode] = []
        order_in_path = 1
        total_duration = 0.0
        projected_gain = 0.0
        
        for unit_id in path_order:
            unit = self._units[unit_id]
            section_info = self._sections.get(getattr(unit, 'section_id', ''), {})
            
            # Check mastery status
            requires_review = False
            estimated_score = 0.0
            
            if unit_id in mastery_map:
                mastery = mastery_map[unit_id]
                estimated_score = min(1.0, mastery.mastery_score + 0.15)  # Projected gain
                if mastery.is_overdue_for_review(datetime.now()):
                    requires_review = True
            
            node = LearningPathNode(
                id=unit.id,
                name=unit.name,
                description=getattr(unit, 'description', ''),
                duration_hours=getattr(unit, 'duration_hours', 0.0),
                difficulty_level=getattr(unit, 'difficulty_level', 'intermediate'),
                prerequisites=getattr(unit, 'prerequisites', []),
                concepts=getattr(unit, 'concepts', []),
                learning_outcomes=getattr(unit, 'learning_outcomes', []),
                section_id=getattr(unit, 'section_id', ''),
                section_order=section_info.get('order', 0),
                order_in_path=order_in_path,
                estimated_mastery_score=estimated_score,
                requires_review=requires_review
            )
            
            path_nodes.append(node)
            total_duration += node.duration_hours
            
            if estimated_score > 0:
                projected_gain += (estimated_score - mastery_map.get(unit_id, ConceptMastery("", "", "")).mastery_score)
            
            order_in_path += 1
        
        # Generate milestones
        milestones = self._generate_milestones(path_nodes, target_unit_id)
        
        # Calculate estimated weeks
        estimated_weeks = int(total_duration / (config.max_weekly_hours * 4)) + 1
        
        # Calculate average difficulty
        if path_nodes:
            avg_diff_order = sum(
                self._get_difficulty_order(node.difficulty_level)
                for node in path_nodes
            ) / len(path_nodes)
            
            difficulties = ['beginner', 'elementary', 'intermediate', 'advanced', 'expert']
            avg_idx = min(int(avg_diff_order), len(difficulties) - 1)
            avg_difficulty = difficulties[avg_idx]
        else:
            avg_difficulty = 'intermediate'
        
        # Calculate current mastery average
        current_avg = current_mastery_sum / len(mastery_map) if mastery_map else 0.0
        
        return LearningPath(
            id=f"{self.subject}-{start_unit_id}-{target_unit_id}-{int(datetime.now().timestamp())}",
            name=f"{self.subject.capitalize()}: {start_unit_id} to {target_unit_id}",
            description=f"Learning path from {start_unit_id} to {target_unit_id} in {self.subject}",
            subject=self.subject,
            total_duration_hours=total_duration,
            total_units=len(path_nodes),
            average_difficulty=avg_difficulty,
            estimated_weeks=estimated_weeks,
            nodes=path_nodes,
            milestones=milestones,
            created_at=datetime.now(),
            current_mastery_average=current_avg,
            projected_mastery_gain=projected_gain,
            concepts_to_review=review_concepts
        )
    
    def generate_mastery_aware_path(
        self,
        target_unit_id: str,
        config: PathGenerationConfig,
        learner_id: str
    ) -> LearningPath:
        """
        Generate a mastery-aware learning path for a specific learner.
        
        This method considers the learner's current mastery levels and
        adjusts the path to include review items and skip already-known content.
        
        Args:
            target_unit_id: The target unit to learn
            config: Path generation configuration
            learner_id: The learner's ID
            
        Returns:
            Generated learning path with mastery considerations
        """
        if not self._mastery_service:
            raise ValueError("Mastery service not configured")
        
        # Get all prerequisites
        all_prereqs = self.graph.get_all_prerequisites(target_unit_id)
        
        # Get mastery data for prerequisites
        mastery_map = self._mastery_service.get_mastery_for_concepts(learner_id, all_prereqs)
        
        # Identify which concepts need work
        needs_work = []
        known = []
        for prereq_id in all_prereqs:
            mastery = mastery_map.get(prereq_id)
            if mastery and mastery.is_considered_known(config.mastery_threshold):
                known.append(prereq_id)
            else:
                needs_work.append(prereq_id)
        
        # Find optimal starting point
        start_unit = self._find_optimal_starting_point_for_learner(
            needs_work, mastery_map, config
        )
        
        # Generate path from start to target
        return self.generate_path(start_unit, target_unit_id, config, learner_id)
    
    def _find_optimal_starting_point_for_learner(
        self,
        prereq_ids: List[str],
        mastery_map: Dict[str, ConceptMastery],
        config: PathGenerationConfig
    ) -> str:
        """Find the best starting point based on learner's current mastery"""
        if not prereq_ids:
            return ""
        
        # Sort by mastery level (lowest first means we start with what needs most work)
        sorted_prereqs = sorted(
            prereq_ids,
            key=lambda pid: mastery_map.get(pid, ConceptMastery("", "", "")).mastery_score
        )
        
        return sorted_prereqs[0] if sorted_prereqs else ""
    
    def _validate_configuration(
        self,
        start_unit_id: str,
        target_unit_id: str,
        config: PathGenerationConfig
    ) -> PathValidationResult:
        """
        Validate the path generation configuration.
        
        Args:
            start_unit_id: Starting unit ID
            target_unit_id: Target unit ID
            config: Path generation configuration
            
        Returns:
            Validation result with errors, warnings, and status
        """
        errors: List[str] = []
        warnings: List[str] = []
        
        # Check if start and target units exist
        start_unit = self._units.get(start_unit_id)
        target_unit = self._units.get(target_unit_id)
        
        if not start_unit:
            errors.append(f"Start unit '{start_unit_id}' not found")
        
        if not target_unit:
            errors.append(f"Target unit '{target_unit_id}' not found")
        
        if start_unit and target_unit:
            # Check level progression
            start_diff = self._get_difficulty_order(start_unit.difficulty_level)
            target_diff = self._get_difficulty_order(target_unit.difficulty_level)
            config_start = self._get_difficulty_order(config.start_level)
            config_target = self._get_difficulty_order(config.target_level)
            
            if start_diff > target_diff:
                errors.append("Start unit difficulty must be less than or equal to target unit")
            
            if config_start > config_target:
                errors.append("Start level must be less than or equal to target level")
            
            # Check for cycles
            if self.graph.detect_cycles():
                errors.append("Graph contains cycles")
            
            # Calculate prerequisite hours
            prereqs = self.graph.get_all_prerequisites(target_unit_id)
            prereq_hours = sum(
                getattr(self._units.get(prereq_id, None), 'duration_hours', 0.0)
                for prereq_id in prereqs
            )
            
            # Check if path is achievable
            weekly_hours = config.max_weekly_hours
            total_hours = prereq_hours + getattr(target_unit, 'duration_hours', 0.0)
            weeks_needed = total_hours / (weekly_hours * 4)
            
            if weeks_needed > 52:  # More than a year
                warnings.append("This learning path may take longer than one year to complete")
        
        return PathValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            total_prerequisite_hours=sum(
                getattr(self._units.get(prereq_id, None), 'duration_hours', 0.0)
                for prereq_id in self.graph.get_all_prerequisites(target_unit_id)
            ),
            achievable=len(warnings) == 0
        )
    
    def _is_in_target_level_range(self, unit_id: str, config: PathGenerationConfig) -> bool:
        """Check if a unit is within the target level range"""
        unit = self._units.get(unit_id)
        if not unit:
            return False
        
        unit_diff = self._get_difficulty_order(unit.difficulty_level)
        start_diff = self._get_difficulty_order(config.start_level)
        target_diff = self._get_difficulty_order(config.target_level)
        
        return start_diff <= unit_diff <= target_diff
    
    def _get_difficulty_order(self, level: str) -> int:
        """Get the numeric order for a difficulty level"""
        return self.DIFFICULTY_ORDER.get(level.lower(), 2)
    
    def _generate_milestones(
        self,
        path_nodes: List[LearningPathNode],
        target_unit_id: str
    ) -> List[LearningPathMilestone]:
        """
        Generate milestones for the learning path.
        
        Args:
            path_nodes: List of path nodes
            target_unit_id: The final target unit ID
            
        Returns:
            List of milestones
        """
        milestones: List[LearningPathMilestone] = []
        concept_set: Set[str] = set()
        
        # Create milestones at section boundaries
        sections: Dict[int, List[LearningPathNode]] = {}
        for node in path_nodes:
            if node.section_order not in sections:
                sections[node.section_order] = []
            sections[node.section_order].append(node)
        
        milestone_index = 0
        for order, nodes in sections.items():
            last_node = nodes[-1]
            
            for node in nodes:
                concept_set.update(node.concepts)
            
            if last_node.id == target_unit_id or len(nodes) > 3:
                section_info = self._sections.get(last_node.section_id, {})
                milestones.append(LearningPathMilestone(
                    name=f"Milestone {++milestone_index}: {section_info.get('name', 'Section ' + str(order))}",
                    description=f"Completed {len(nodes)} units covering {len(concept_set)} concepts",
                    unit_id=last_node.id,
                    concepts_mastered=list(concept_set),
                    after_unit=last_node.order_in_path
                ))
                concept_set = set()
        
        return milestones
    
    def get_graph(self) -> DependencyGraph:
        """Get the internal dependency graph"""
        return self.graph
    
    def get_units(self) -> Dict[str, Any]:
        """Get all units in the curriculum"""
        return self._units


# ============================================
# Utility Functions
# ============================================

def calculate_estimated_completion_time(
    path_nodes: List[LearningPathNode],
    hours_per_week: int
) -> Dict[str, int]:
    """
    Calculate estimated completion time for a learning path.
    
    Args:
        path_nodes: List of nodes in the learning path
        hours_per_week: Available study hours per week
        
    Returns:
        Dictionary with weeks, months, and years estimates
    """
    total_hours = sum(node.duration_hours for node in path_nodes)
    weeks = (total_hours + hours_per_week - 1) // hours_per_week
    months = (weeks + 3) // 4
    years = (months + 11) // 12
    
    return {
        'weeks': weeks,
        'months': months,
        'years': years
    }


def find_optimal_starting_point(
    units: Dict[str, Any],
    target_unit_id: str
) -> List[str]:
    """
    Find the optimal starting point for learning a target unit.
    
    This function performs a reverse traversal from the target unit
    to identify all prerequisite units in the correct order.
    
    Args:
        units: Dictionary of units by ID
        target_unit_id: The target unit to learn
        
    Returns:
        List of unit IDs in optimal learning order
    """
    visited: Set[str] = set()
    result: List[str] = []
    
    def traverse(unit_id: str) -> None:
        if unit_id in visited:
            return
        visited.add(unit_id)
        
        unit = units.get(unit_id)
        if not unit:
            return
        
        for prereq_id in getattr(unit, 'prerequisites', []):
            traverse(prereq_id)
        
        result.append(unit_id)
    
    traverse(target_unit_id)
    return result


def group_by_difficulty(units: Dict[str, Any]) -> Dict[str, List[Any]]:
    """
    Group units by their difficulty level.
    
    Args:
        units: Dictionary of units by ID
        
    Returns:
        Dictionary mapping difficulty levels to lists of units
    """
    grouped: Dict[str, List[Any]] = {}
    
    for unit_id, unit in units.items():
        level = getattr(unit, 'difficulty_level', 'intermediate')
        if level not in grouped:
            grouped[level] = []
        grouped[level].append(unit)
    
    return grouped
