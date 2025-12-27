"""
Dependency Graph Engine for VisualVerse Content Metadata Layer

This module provides NetworkX-based graph operations for managing concept
prerequisite relationships. It supports building, querying, and analyzing
the knowledge dependency graph with periodic materialization to persistent storage.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import logging
import json
import pickle

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logging.warning("NetworkX not installed. Graph operations will be limited.")


logger = logging.getLogger(__name__)


class RelationshipType(str, Enum):
    """Types of relationships in the knowledge graph"""
    PREREQUISITE = "prerequisite"
    ANALOGOUS_TO = "analogous_to"
    APPLICATION_OF = "application_of"
    COMPONENT_OF = "component_of"
    RELATED_TO = "related_to"
    EXTENDS = "extends"
    BUILDS_ON = "builds_on"
    LEADS_TO = "leads_to"


@dataclass
class GraphNode:
    """Represents a node in the dependency graph"""
    id: str
    name: str
    subject_id: str
    difficulty_level: str
    concept_type: str
    duration_minutes: int
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'subject_id': self.subject_id,
            'difficulty_level': self.difficulty_level,
            'concept_type': self.concept_type,
            'duration_minutes': self.duration_minutes,
            'tags': self.tags,
            'metadata': self.metadata
        }


@dataclass
class GraphEdge:
    """Represents an edge in the dependency graph"""
    source_id: str
    target_id: str
    relationship_type: RelationshipType
    strength: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'relationship_type': self.relationship_type.value,
            'strength': self.strength,
            'metadata': self.metadata
        }


@dataclass
class PathResult:
    """Result of a pathfinding operation"""
    path: List[str]
    total_duration: int
    difficulty_progression: List[str]
    concepts_by_subject: Dict[str, List[str]]
    is_feasible: bool
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'path': self.path,
            'total_duration': self.total_duration,
            'difficulty_progression': self.difficulty_progression,
            'concepts_by_subject': self.concepts_by_subject,
            'is_feasible': self.is_feasible,
            'warnings': self.warnings
        }


class GraphStats:
    """Statistics about the dependency graph"""
    
    def __init__(self):
        self.node_count: int = 0
        self.edge_count: int = 0
        self.subject_counts: Dict[str, int] = {}
        self.difficulty_distribution: Dict[str, int] = {}
        self.cycle_count: int = 0
        self.isolated_nodes: List[str] = []
        self.central_concepts: List[Dict[str, Any]] = []
        self.last_refreshed: Optional[datetime] = None
        self.materialization_version: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'node_count': self.node_count,
            'edge_count': self.edge_count,
            'subject_counts': self.subject_counts,
            'difficulty_distribution': self.difficulty_distribution,
            'cycle_count': self.cycle_count,
            'isolated_nodes': self.isolated_nodes,
            'central_concepts': self.central_concepts,
            'last_refreshed': self.last_refreshed.isoformat() if self.last_refreshed else None,
            'materialization_version': self.materialization_version
        }


class DependencyGraphEngine:
    """
    NetworkX-based engine for managing concept dependency relationships.
    
    This engine provides efficient graph operations for prerequisite tracking,
    learning path finding, and knowledge structure analysis. It supports
    periodic materialization to enable persistence without requiring a
    dedicated graph database.
    """
    
    def __init__(self):
        """Initialize the dependency graph engine"""
        if not NETWORKX_AVAILABLE:
            raise RuntimeError("NetworkX is required for graph operations. Install with: pip install networkx")
        
        self._graph: nx.DiGraph = nx.DiGraph()
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: List[GraphEdge] = []
        self._subject_index: Dict[str, Set[str]] = {}  # subject_id -> set of concept IDs
        self._difficulty_index: Dict[str, Set[str]] = {}  # difficulty -> set of concept IDs
        self._last_built: Optional[datetime] = None
        self._materialization_version: str = ""
    
    # =========================================================================
    # Graph Building and Maintenance
    # =========================================================================
    
    def build_graph(
        self,
        concepts: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> GraphStats:
        """
        Build the dependency graph from concept and relationship data.
        
        Args:
            concepts: List of concept dictionaries with id, name, subject_id, etc.
            relationships: List of relationship dictionaries with source, target, type
            
        Returns:
            GraphStats with graph statistics
        """
        self._graph.clear()
        self._nodes.clear()
        self._edges.clear()
        self._subject_index.clear()
        self._difficulty_index.clear()
        
        # Add nodes
        for concept_data in concepts:
            node = self._create_node(concept_data)
            self._add_node(node)
        
        # Add edges
        for rel_data in relationships:
            self._add_edge_from_data(rel_data)
        
        # Build indexes
        self._build_indexes()
        
        # Calculate statistics
        stats = self._calculate_stats()
        self._last_built = datetime.now()
        
        return stats
    
    def _create_node(self, data: Dict[str, Any]) -> GraphNode:
        """Create a GraphNode from dictionary data"""
        return GraphNode(
            id=data.get('id', ''),
            name=data.get('name', data.get('display_name', '')),
            subject_id=data.get('subject_id', ''),
            difficulty_level=data.get('difficulty_level', 'intermediate'),
            concept_type=data.get('type', 'theoretical'),
            duration_minutes=data.get('estimated_duration', 30),
            tags=data.get('tags', []),
            metadata={
                'description': data.get('description', ''),
                'learning_objectives': data.get('learning_objectives', []),
                'keywords': data.get('keywords', []),
                'curriculum_standards': data.get('curriculum_standards', [])
            }
        )
    
    def _add_node(self, node: GraphNode) -> None:
        """Add a node to the graph"""
        self._nodes[node.id] = node
        self._graph.add_node(
            node.id,
            name=node.name,
            subject_id=node.subject_id,
            difficulty_level=node.difficulty_level,
            concept_type=node.concept_type,
            duration_minutes=node.duration_minutes,
            tags=node.tags
        )
    
    def _add_edge_from_data(self, data: Dict[str, Any]) -> None:
        """Add an edge from relationship data"""
        source = data.get('source', data.get('source_concept_id', ''))
        target = data.get('target', data.get('target_concept_id', ''))
        rel_type = data.get('type', data.get('relationship_type', 'prerequisite'))
        strength = data.get('strength', 1.0)
        
        if not source or not target:
            return
        
        # Convert string to enum if needed
        if isinstance(rel_type, str):
            try:
                rel_type = RelationshipType(rel_type)
            except ValueError:
                rel_type = RelationshipType.PREREQUISITE
        
        edge = GraphEdge(
            source_id=source,
            target_id=target,
            relationship_type=rel_type,
            strength=strength,
            metadata=data.get('metadata', {})
        )
        self._edges.append(edge)
        
        self._graph.add_edge(
            source,
            target,
            relationship_type=rel_type.value,
            strength=strength
        )
    
    def _build_indexes(self) -> None:
        """Build lookup indexes for efficient querying"""
        for node_id, node in self._nodes.items():
            # Subject index
            if node.subject_id not in self._subject_index:
                self._subject_index[node.subject_id] = set()
            self._subject_index[node.subject_id].add(node_id)
            
            # Difficulty index
            if node.difficulty_level not in self._difficulty_index:
                self._difficulty_index[node.difficulty_level] = set()
            self._difficulty_index[node.difficulty_level].add(node_id)
    
    def add_node(self, node: GraphNode) -> None:
        """Add a single node to the graph"""
        self._add_node(node)
        
        # Update indexes
        if node.subject_id not in self._subject_index:
            self._subject_index[node.subject_id] = set()
        self._subject_index[node.subject_id].add(node.id)
        
        if node.difficulty_level not in self._difficulty_index:
            self._difficulty_index[node.difficulty_level] = set()
        self._difficulty_index[node.difficulty_level].add(node.id)
    
    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_type: RelationshipType = RelationshipType.PREREQUISITE,
        strength: float = 1.0
    ) -> bool:
        """
        Add an edge between two nodes.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship_type: Type of relationship
            strength: Relationship strength (0.0 to 1.0)
            
        Returns:
            True if edge was added successfully
        """
        if source_id not in self._nodes:
            logger.warning(f"Source node {source_id} not found")
            return False
        
        if target_id not in self._nodes:
            logger.warning(f"Target node {target_id} not found")
            return False
        
        edge = GraphEdge(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            strength=strength
        )
        self._edges.append(edge)
        
        self._graph.add_edge(
            source_id,
            target_id,
            relationship_type=relationship_type.value,
            strength=strength
        )
        
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node and its edges from the graph"""
        if node_id not in self._nodes:
            return False
        
        # Remove from indexes
        node = self._nodes[node_id]
        if node.subject_id in self._subject_index:
            self._subject_index[node.subject_id].discard(node_id)
        if node.difficulty_level in self._difficulty_index:
            self._difficulty_index[node.difficulty_level].discard(node_id)
        
        # Remove node
        del self._nodes[node_id]
        self._graph.remove_node(node_id)
        
        # Remove associated edges
        self._edges = [
            e for e in self._edges
            if e.source_id != node_id and e.target_id != node_id
        ]
        
        return True
    
    def remove_edge(
        self,
        source_id: str,
        target_id: str,
        relationship_type: Optional[RelationshipType] = None
    ) -> bool:
        """Remove an edge from the graph"""
        for i, edge in enumerate(self._edges):
            if (edge.source_id == source_id and
                edge.target_id == target_id and
                (relationship_type is None or edge.relationship_type == relationship_type)):
                self._edges.pop(i)
                
                # Remove from NetworkX graph
                try:
                    self._graph.remove_edge(source_id, target_id)
                except nx.NetworkXError:
                    pass
                
                return True
        
        return False
    
    # =========================================================================
    # Prerequisite and Dependency Queries
    # =========================================================================
    
    def get_prerequisites(
        self,
        concept_id: str,
        recursive: bool = True,
        relationship_types: Optional[List[RelationshipType]] = None
    ) -> List[str]:
        """
        Get all prerequisites for a concept.
        
        Args:
            concept_id: The concept ID to find prerequisites for
            recursive: Whether to include transitive prerequisites
            relationship_types: Filter by specific relationship types
            
        Returns:
            List of prerequisite concept IDs
        """
        if concept_id not in self._graph:
            return []
        
        if recursive:
            # Use NetworkX ancestors for transitive closure
            prereqs = list(nx.ancestors(self._graph, concept_id))
            return sorted(prereqs)
        else:
            # Direct prerequisites only
            prereqs = list(self._graph.predecessors(concept_id))
            
            if relationship_types:
                filtered = []
                for prereq_id in prereqs:
                    for edge in self._edges:
                        if (edge.source_id == prereq_id and
                            edge.target_id == concept_id and
                            edge.relationship_type in relationship_types):
                            filtered.append(prereq_id)
                            break
                return filtered
            
            return prereqs
    
    def get_postrequisites(
        self,
        concept_id: str,
        recursive: bool = True
    ) -> List[str]:
        """
        Get all concepts that depend on this concept.
        
        Args:
            concept_id: The concept ID to find postrequisites for
            recursive: Whether to include transitive dependents
            
        Returns:
            List of dependent concept IDs
        """
        if concept_id not in self._graph:
            return []
        
        if recursive:
            # Use NetworkX descendants for transitive closure
            postreqs = list(nx.descendants(self._graph, concept_id))
            return sorted(postreqs)
        else:
            return list(self._graph.successors(concept_id))
    
    def get_direct_prerequisites(self, concept_id: str) -> List[Dict[str, Any]]:
        """Get direct prerequisites with full metadata"""
        result = []
        
        for edge in self._edges:
            if edge.target_id == concept_id:
                source = self._nodes.get(edge.source_id)
                if source:
                    result.append({
                        'concept': source.to_dict(),
                        'relationship_type': edge.relationship_type.value,
                        'strength': edge.strength
                    })
        
        return result
    
    # =========================================================================
    # Path Finding
    # =========================================================================
    
    def find_learning_path(
        self,
        start_concept_id: str,
        target_concept_id: str,
        max_concepts: int = 50
    ) -> Optional[PathResult]:
        """
        Find an optimal learning path between two concepts.
        
        Uses shortest path algorithm weighted by concept duration and difficulty.
        
        Args:
            start_concept_id: Starting concept ID
            target_concept_id: Target concept ID
            max_concepts: Maximum path length
            
        Returns:
            PathResult with the path details, or None if no path exists
        """
        if start_concept_id not in self._graph or target_concept_id not in self._graph:
            return None
        
        try:
            # Find shortest path
            path = nx.shortest_path(
                self._graph,
                source=start_concept_id,
                target=target_concept_id
            )
            
            if len(path) > max_concepts:
                logger.warning(f"Path too long ({len(path)} concepts), limiting to {max_concepts}")
                return None
            
            # Calculate path metrics
            total_duration = 0
            difficulty_progression = []
            concepts_by_subject: Dict[str, List[str]] = {}
            
            for concept_id in path:
                node = self._nodes.get(concept_id)
                if node:
                    total_duration += node.duration_minutes
                    difficulty_progression.append(node.difficulty_level)
                    
                    if node.subject_id not in concepts_by_subject:
                        concepts_by_subject[node.subject_id] = []
                    concepts_by_subject[node.subject_id].append(concept_id)
            
            return PathResult(
                path=path,
                total_duration=total_duration,
                difficulty_progression=difficulty_progression,
                concepts_by_subject=concepts_by_subject,
                is_feasible=True
            )
            
        except nx.NetworkXNoPath:
            logger.info(f"No path found from {start_concept_id} to {target_concept_id}")
            return None
    
    def find_all_paths(
        self,
        start_concept_id: str,
        target_concept_id: str,
        max_paths: int = 10
    ) -> List[PathResult]:
        """
        Find multiple learning paths between two concepts.
        
        Args:
            start_concept_id: Starting concept ID
            target_concept_id: Target concept ID
            max_paths: Maximum number of paths to return
            
        Returns:
            List of PathResult objects
        """
        results = []
        
        if start_concept_id not in self._graph or target_concept_id not in self._graph:
            return results
        
        try:
            # Use simple_paths for all simple paths
            paths = list(nx.simple_paths.simple_paths(
                self._graph,
                start_concept_id,
                target_concept_id,
                cutoff=20
            ))[:max_paths]
            
            for path in paths:
                total_duration = sum(
                    self._nodes.get(cid, GraphNode(cid, "", "", "", "", 0)).duration_minutes
                    for cid in path
                )
                
                results.append(PathResult(
                    path=path,
                    total_duration=total_duration,
                    difficulty_progression=[],
                    concepts_by_subject={},
                    is_feasible=True
                ))
                
        except nx.NetworkXNoPath:
            pass
        
        return results
    
    def find_optimal_path_dijkstra(
        self,
        start_concept_id: str,
        target_concept_id: str,
        weight_by: str = "duration"
    ) -> Optional[PathResult]:
        """
        Find optimal path using Dijkstra's algorithm.
        
        Args:
            start_concept_id: Starting concept ID
            target_concept_id: Target concept ID
            weight_by: Weight metric ('duration', 'difficulty', 'custom')
            
        Returns:
            Optimal PathResult
        """
        if start_concept_id not in self._graph or target_concept_id not in self._graph:
            return None
        
        try:
            # Create weighted graph
            if weight_by == "duration":
                weight_func = lambda u, v, data: self._nodes.get(u, GraphNode("", "", "", "", "", 0)).duration_minutes
            elif weight_by == "difficulty":
                difficulty_values = {
                    'beginner': 1, 'elementary': 2, 'intermediate': 3,
                    'advanced': 4, 'expert': 5
                }
                weight_func = lambda u, v, data: difficulty_values.get(
                    self._nodes.get(u, GraphNode("", "", "", "", "", 0)).difficulty_level,
                    3
                )
            else:
                weight_func = lambda u, v, data: 1
            
            path = nx.dijkstra_path(
                self._graph,
                start_concept_id,
                target_concept_id,
                weight=weight_func
            )
            
            total_duration = sum(
                self._nodes.get(cid, GraphNode(cid, "", "", "", "", 0)).duration_minutes
                for cid in path
            )
            
            return PathResult(
                path=path,
                total_duration=total_duration,
                difficulty_progression=[],
                concepts_by_subject={},
                is_feasible=True
            )
            
        except (nx.NetworkXNoPath, nx.NetworkXError):
            return None
    
    # =========================================================================
    # Graph Analysis
    # =========================================================================
    
    def detect_cycles(self) -> List[List[str]]:
        """
        Detect cycles in the graph.
        
        Returns:
            List of cycles, where each cycle is a list of concept IDs
        """
        try:
            cycles = list(nx.simple_cycles(self._graph))
            return [list(c) for c in cycles]
        except nx.NetworkXError:
            return []
    
    def detect_cycles_with_details(self) -> List[Dict[str, Any]]:
        """
        Detect cycles with detailed information.
        
        Returns:
            List of cycle information dictionaries
        """
        cycles = self.detect_cycles()
        results = []
        
        for cycle in cycles:
            cycle_concepts = []
            total_duration = 0
            
            for concept_id in cycle:
                node = self._nodes.get(concept_id)
                if node:
                    cycle_concepts.append(node.to_dict())
                    total_duration += node.duration_minutes
            
            results.append({
                'cycle': cycle,
                'concepts': cycle_concepts,
                'length': len(cycle),
                'total_duration_minutes': total_duration,
                'severity': 'critical' if len(cycle) < 4 else 'warning'
            })
        
        return results
    
    def find_isolated_concepts(self) -> List[Dict[str, Any]]:
        """
        Find concepts with no connections.
        
        Returns:
            List of isolated concept information
        """
        isolated = []
        
        for node_id in self._graph.nodes():
            if self._graph.degree(node_id) == 0:
                node = self._nodes.get(node_id)
                if node:
                    isolated.append(node.to_dict())
        
        return isolated
    
    def find_central_concepts(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Find the most central concepts using betweenness centrality.
        
        Args:
            top_n: Number of top concepts to return
            
        Returns:
            List of central concept information
        """
        if len(self._graph) == 0:
            return []
        
        # Calculate betweenness centrality
        centrality = nx.betweenness_centrality(self._graph)
        
        # Sort by centrality
        sorted_concepts = sorted(
            centrality.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        results = []
        for concept_id, centrality_score in sorted_concepts:
            node = self._nodes.get(concept_id)
            if node:
                result = node.to_dict()
                result['centrality_score'] = centrality_score
                results.append(result)
        
        return results
    
    def find_foundational_concepts(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Find foundational concepts (prerequisites for many others).
        
        These are concepts with high out-degree that many other concepts depend on.
        
        Args:
            top_n: Number of concepts to return
            
        Returns:
            List of foundational concept information
        """
        if len(self._graph) == 0:
            return []
        
        # Calculate out-degree (number of concepts that depend on this one)
        out_degrees = dict(self._graph.out_degree())
        
        sorted_concepts = sorted(
            out_degrees.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        results = []
        for concept_id, out_degree in sorted_concepts:
            node = self._nodes.get(concept_id)
            if node:
                result = node.to_dict()
                result['dependent_count'] = out_degree
                results.append(result)
        
        return results
    
    def get_concept_depth(self, concept_id: str) -> int:
        """
        Calculate the depth of a concept in the dependency tree.
        
        Depth is the length of the longest path from any root node.
        
        Args:
            concept_id: The concept ID
            
        Returns:
            Depth value (0 for root concepts)
        """
        if concept_id not in self._graph:
            return -1
        
        # Find all predecessors
        predecessors = list(nx.ancestors(self._graph, concept_id))
        
        if not predecessors:
            return 0
        
        # Calculate longest path from any root
        max_depth = 0
        for prereq_id in predecessors:
            prereq_depth = self.get_concept_depth(prereq_id)
            if prereq_depth > max_depth:
                max_depth = prereq_depth
        
        return max_depth + 1
    
    # =========================================================================
    # Subject-Specific Queries
    # =========================================================================
    
    def get_concepts_by_subject(self, subject_id: str) -> List[Dict[str, Any]]:
        """Get all concepts for a subject"""
        if subject_id not in self._subject_index:
            return []
        
        return [
            self._nodes[cid].to_dict()
            for cid in sorted(self._subject_index[subject_id])
            if cid in self._nodes
        ]
    
    def get_concepts_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get all concepts at a specific difficulty level"""
        if difficulty not in self._difficulty_index:
            return []
        
        return [
            self._nodes[cid].to_dict()
            for cid in sorted(self._difficulty_index[difficulty])
            if cid in self._nodes
        ]
    
    def get_subject_prerequisite_graph(self, subject_id: str) -> nx.DiGraph:
        """
        Extract the subgraph for a specific subject.
        
        Args:
            subject_id: The subject ID
            
        Returns:
            NetworkX DiGraph for the subject
        """
        if subject_id not in self._subject_index:
            return nx.DiGraph()
        
        subject_nodes = self._subject_index[subject_id]
        return self._graph.subgraph(subject_nodes).copy()
    
    # =========================================================================
    # Serialization and Materialization
    # =========================================================================
    
    def serialize(self) -> Dict[str, Any]:
        """Serialize the graph to a dictionary"""
        return {
            'version': self._materialization_version,
            'created_at': datetime.now().isoformat(),
            'nodes': {
                node_id: node.to_dict()
                for node_id, node in self._nodes.items()
            },
            'edges': [edge.to_dict() for edge in self._edges],
            'subject_index': {
                subj: list(nodes)
                for subj, nodes in self._subject_index.items()
            },
            'difficulty_index': {
                diff: list(nodes)
                for diff, nodes in self._difficulty_index.items()
            }
        }
    
    def serialize_binary(self) -> bytes:
        """Serialize the graph to binary format (pickle)"""
        return pickle.dumps({
            'nodes': self._nodes,
            'edges': self._edges,
            'subject_index': self._subject_index,
            'difficulty_index': self._difficulty_index,
            'graph': self._graph,
            'version': self._materialization_version,
            'timestamp': datetime.now()
        })
    
    def deserialize(self, data: Dict[str, Any]) -> None:
        """Deserialize the graph from a dictionary"""
        self._materialization_version = data.get('version', '')
        
        # Clear existing
        self._nodes.clear()
        self._edges.clear()
        self._subject_index.clear()
        self._difficulty_index.clear()
        self._graph.clear()
        
        # Load nodes
        for node_id, node_data in data.get('nodes', {}).items():
            node = GraphNode(**node_data)
            self._nodes[node_id] = node
            self._graph.add_node(
                node_id,
                name=node.name,
                subject_id=node.subject_id,
                difficulty_level=node.difficulty_level
            )
        
        # Load edges
        for edge_data in data.get('edges', []):
            try:
                rel_type = RelationshipType(edge_data['relationship_type'])
                edge = GraphEdge(
                    source_id=edge_data['source_id'],
                    target_id=edge_data['target_id'],
                    relationship_type=rel_type,
                    strength=edge_data.get('strength', 1.0)
                )
                self._edges.append(edge)
                self._graph.add_edge(
                    edge_data['source_id'],
                    edge_data['target_id'],
                    relationship_type=rel_type.value,
                    strength=edge_data.get('strength', 1.0)
                )
            except (KeyError, ValueError) as e:
                logger.warning(f"Error loading edge: {e}")
        
        # Rebuild indexes
        self._build_indexes()
    
    def deserialize_binary(self, data: bytes) -> None:
        """Deserialize the graph from binary format"""
        loaded = pickle.loads(data)
        
        self._nodes = loaded['nodes']
        self._edges = loaded['edges']
        self._subject_index = loaded['subject_index']
        self._difficulty_index = loaded['difficulty_index']
        self._graph = loaded['graph']
        self._materialization_version = loaded.get('version', '')
    
    def set_materialization_version(self, version: str) -> None:
        """Set the materialization version"""
        self._materialization_version = version
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    def _calculate_stats(self) -> GraphStats:
        """Calculate graph statistics"""
        stats = GraphStats()
        
        stats.node_count = len(self._nodes)
        stats.edge_count = len(self._edges)
        stats.materialization_version = self._materialization_version
        stats.last_refreshed = self._last_built
        
        # Subject counts
        for subject_id, nodes in self._subject_index.items():
            stats.subject_counts[subject_id] = len(nodes)
        
        # Difficulty distribution
        for difficulty, nodes in self._difficulty_index.items():
            stats.difficulty_distribution[difficulty] = len(nodes)
        
        # Cycle detection
        stats.cycle_count = len(self.detect_cycles())
        
        # Isolated nodes
        stats.isolated_nodes = [
            node_id for node_id in self._graph.nodes()
            if self._graph.degree(node_id) == 0
        ]
        
        # Central concepts
        stats.central_concepts = self.find_central_concepts(10)
        
        return stats
    
    def get_stats(self) -> GraphStats:
        """Get current graph statistics"""
        return self._calculate_stats()
    
    def get_graph(self) -> nx.DiGraph:
        """Get the underlying NetworkX graph"""
        return self._graph.copy()
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID"""
        return self._nodes.get(node_id)
    
    def get_all_nodes(self) -> List[GraphNode]:
        """Get all nodes"""
        return list(self._nodes.values())
    
    @property
    def is_empty(self) -> bool:
        """Check if the graph is empty"""
        return len(self._nodes) == 0
    
    @property
    def node_count(self) -> int:
        """Get node count"""
        return len(self._nodes)
    
    @property
    def edge_count(self) -> int:
        """Get edge count"""
        return len(self._edges)
