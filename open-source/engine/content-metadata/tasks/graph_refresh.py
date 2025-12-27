#!/usr/bin/env python3
"""
Graph Refresh Task for VisualVerse Content Metadata Layer

This script rebuilds the dependency graph from database records and
materializes it to persistent storage. It is designed to be run as a
periodic task (cron job) or background worker.

Usage:
    python tasks/graph_refresh.py                    # Full refresh
    python tasks/graph_refresh.py --incremental     # Incremental update
    python tasks/graph_refresh.py --status          # Show current status

Licensed under the Apache License, Version 2.0
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
import json
import pickle

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.graph.engine import DependencyGraphEngine, GraphStats, RelationshipType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GraphRefreshTask:
    """
    Task for refreshing the dependency graph from database records.
    
    This task can perform full rebuilds or incremental updates depending
    on the configuration and data changes.
    """
    
    def __init__(
        self,
        storage_path: str = "/tmp/visualverse/graph_snapshots",
        version: Optional[str] = None
    ):
        """
        Initialize the graph refresh task.
        
        Args:
            storage_path: Path to store graph snapshots
            version: Optional version string for this refresh
        """
        self.storage_path = storage_path
        self.version = version or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.graph = DependencyGraphEngine()
        
        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Track refresh metrics
        self._refresh_start: Optional[datetime] = None
        self._refresh_end: Optional[datetime] = None
        self._records_processed: int = 0
        self._changes_detected: int = 0
    
    def run_full_refresh(
        self,
        concepts_data: List[Dict[str, Any]],
        relationships_data: List[Dict[str, Any]]
    ) -> GraphStats:
        """
        Perform a full graph rebuild.
        
        Args:
            concepts_data: List of concept dictionaries
            relationships_data: List of relationship dictionaries
            
        Returns:
            GraphStats with build statistics
        """
        self._refresh_start = datetime.now()
        logger.info(f"Starting full graph refresh (version: {self.version})")
        logger.info(f"Loading {len(concepts_data)} concepts and {len(relationships_data)} relationships")
        
        # Build the graph
        stats = self.graph.build_graph(concepts_data, relationships_data)
        
        # Set version
        self.graph.set_materialization_version(self.version)
        
        # Save snapshot
        self._save_snapshot()
        
        self._refresh_end = datetime.now()
        self._records_processed = len(concepts_data) + len(relationships_data)
        
        duration = (self._refresh_end - self._refresh_start).total_seconds()
        logger.info(
            f"Graph refresh complete in {duration:.2f}s. "
            f"Nodes: {stats.node_count}, Edges: {stats.edge_count}, "
            f"Cycles: {stats.cycle_count}"
        )
        
        return stats
    
    def run_incremental_refresh(
        self,
        new_concepts: List[Dict[str, Any]] = None,
        updated_concepts: List[Dict[str, Any]] = None,
        deleted_concept_ids: List[str] = None,
        new_relationships: List[Dict[str, Any]] = None,
        deleted_relationship_ids: List[tuple] = None
    ) -> Dict[str, Any]:
        """
        Perform an incremental graph update.
        
        Args:
            new_concepts: New concepts to add
            updated_concepts: Updated concepts to refresh
            deleted_concept_ids: Concept IDs to remove
            new_relationships: New relationships to add
            deleted_relationship_ids: Relationship IDs to remove
            
        Returns:
            Update summary dictionary
        """
        self._refresh_start = datetime.now()
        logger.info(f"Starting incremental graph refresh (version: {self.version})")
        
        summary = {
            'new_concepts': 0,
            'updated_concepts': 0,
            'deleted_concepts': 0,
            'new_relationships': 0,
            'deleted_relationships': 0,
            'cycles_detected': 0
        }
        
        # Load existing graph if available
        self._load_latest_snapshot()
        
        # Add new concepts
        if new_concepts:
            from services.graph.engine import GraphNode
            for concept_data in new_concepts:
                node = self._create_node_from_data(concept_data)
                self.graph.add_node(node)
                summary['new_concepts'] += 1
        
        # Update existing concepts
        if updated_concepts:
            for concept_data in updated_concepts:
                node_id = concept_data.get('id')
                if node_id and self.graph.get_node(node_id):
                    self.graph.remove_node(node_id)
                    node = self._create_node_from_data(concept_data)
                    self.graph.add_node(node)
                    summary['updated_concepts'] += 1
        
        # Delete concepts
        if deleted_concept_ids:
            for node_id in deleted_concept_ids:
                if self.graph.remove_node(node_id):
                    summary['deleted_concepts'] += 1
        
        # Add new relationships
        if new_relationships:
            for rel_data in new_relationships:
                if self.graph.add_edge(
                    rel_data.get('source'),
                    rel_data.get('target'),
                    RelationshipType(rel_data.get('type', 'prerequisite')),
                    rel_data.get('strength', 1.0)
                ):
                    summary['new_relationships'] += 1
        
        # Delete relationships
        if deleted_relationship_ids:
            for source, target in deleted_relationship_ids:
                if self.graph.remove_edge(source, target):
                    summary['deleted_relationships'] += 1
        
        # Check for cycles after updates
        cycles = self.graph.detect_cycles()
        summary['cycles_detected'] = len(cycles)
        
        if cycles:
            logger.warning(f"Cycles detected after incremental update: {cycles}")
        
        # Save updated graph
        self.graph.set_materialization_version(self.version)
        self._save_snapshot()
        
        self._refresh_end = datetime.now()
        self._changes_detected = sum(
            summary[k] for k in summary if k != 'cycles_detected'
        )
        
        duration = (self._refresh_end - self._refresh_start).total_seconds()
        logger.info(
            f"Incremental refresh complete in {duration:.2fs}. "
            f"Changes: {self._changes_detected}"
        )
        
        return summary
    
    def _create_node_from_data(self, data: Dict[str, Any]):
        """Create a GraphNode from dictionary data"""
        from services.graph.engine import GraphNode
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
                'keywords': data.get('keywords', [])
            }
        )
    
    def _save_snapshot(self) -> str:
        """Save the current graph to storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save binary snapshot
        binary_path = os.path.join(
            self.storage_path,
            f"graph_{self.version}_{timestamp}.pkl"
        )
        with open(binary_path, 'wb') as f:
            f.write(self.graph.serialize_binary())
        
        # Save JSON metadata
        metadata = {
            'version': self.version,
            'timestamp': timestamp,
            'node_count': self.graph.node_count,
            'edge_count': self.graph.edge_count,
            'binary_file': os.path.basename(binary_path)
        }
        metadata_path = os.path.join(
            self.storage_path,
            f"graph_{self.version}_{timestamp}.json"
        )
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update latest symlink
        latest_path = os.path.join(self.storage_path, "latest.json")
        with open(latest_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Saved graph snapshot to {binary_path}")
        
        return binary_path
    
    def _load_latest_snapshot(self) -> bool:
        """Load the latest graph snapshot"""
        latest_path = os.path.join(self.storage_path, "latest.json")
        
        if not os.path.exists(latest_path):
            logger.info("No existing graph snapshot found")
            return False
        
        try:
            with open(latest_path, 'r') as f:
                metadata = json.load(f)
            
            binary_path = os.path.join(self.storage_path, metadata.get('binary_file', ''))
            
            if os.path.exists(binary_path):
                with open(binary_path, 'rb') as f:
                    self.graph.deserialize_binary(f.read())
                
                logger.info(
                    f"Loaded existing graph: {self.graph.node_count} nodes, "
                    f"{self.graph.edge_count} edges"
                )
                return True
            
        except Exception as e:
            logger.warning(f"Error loading graph snapshot: {e}")
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current graph status"""
        self._load_latest_snapshot()
        
        stats = self.graph.get_stats()
        
        return {
            'version': self.version,
            'status': 'loaded' if not self.graph.is_empty else 'empty',
            'node_count': stats.node_count,
            'edge_count': stats.edge_count,
            'subject_counts': stats.subject_counts,
            'difficulty_distribution': stats.difficulty_distribution,
            'cycles_detected': stats.cycle_count,
            'isolated_nodes_count': len(stats.isolated_nodes),
            'last_refreshed': stats.last_refreshed.isoformat() if stats.last_refreshed else None,
            'snapshot_count': self._count_snapshots()
        }
    
    def _count_snapshots(self) -> int:
        """Count available snapshots"""
        if not os.path.exists(self.storage_path):
            return 0
        
        return len([
            f for f in os.listdir(self.storage_path)
            if f.endswith('.pkl')
        ])
    
    def cleanup_old_snapshots(self, keep_count: int = 5) -> int:
        """
        Remove old snapshots, keeping the most recent ones.
        
        Args:
            keep_count: Number of snapshots to keep
            
        Returns:
            Number of snapshots removed
        """
        if not os.path.exists(self.storage_path):
            return 0
        
        # Get all snapshot files
        snapshots = [
            f for f in os.listdir(self.storage_path)
            if f.endswith('.pkl')
        ]
        
        if len(snapshots) <= keep_count:
            return 0
        
        # Sort by modification time
        snapshots.sort(key=lambda f: os.path.getmtime(
            os.path.join(self.storage_path, f)
        ), reverse=True)
        
        # Remove old ones
        removed = 0
        for snapshot in snapshots[keep_count:]:
            base_name = snapshot.replace('.pkl', '')
            
            # Remove associated JSON files
            for ext in ['.pkl', '.json']:
                path = os.path.join(self.storage_path, base_name + ext)
                if os.path.exists(path):
                    os.remove(path)
                    removed += 1
        
        logger.info(f"Cleaned up {removed // 2} old snapshots")
        
        return removed // 2


def get_sample_data() -> tuple:
    """
    Get sample data for demonstration purposes.
    
    In production, this would be replaced with actual database queries.
    
    Returns:
        Tuple of (concepts, relationships)
    """
    concepts = [
        {
            'id': 'basic-arithmetic',
            'name': 'Basic Arithmetic',
            'display_name': 'Basic Arithmetic',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'beginner',
            'estimated_duration': 60,
            'description': 'Fundamental operations with numbers',
            'tags': ['arithmetic', 'numbers', 'operations'],
            'learning_objectives': ['Understand addition', 'Understand subtraction']
        },
        {
            'id': 'fractions',
            'name': 'Fractions',
            'display_name': 'Fractions',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'elementary',
            'estimated_duration': 90,
            'description': 'Understanding and operating with fractions',
            'tags': ['fractions', 'numbers', 'rational'],
            'learning_objectives': ['Understand fraction notation', 'Add fractions']
        },
        {
            'id': 'decimals',
            'name': 'Decimals',
            'display_name': 'Decimals',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'elementary',
            'estimated_duration': 90,
            'description': 'Working with decimal numbers',
            'tags': ['decimals', 'numbers', 'place-value'],
            'learning_objectives': ['Understand decimal notation', 'Convert fractions to decimals']
        },
        {
            'id': 'percentages',
            'name': 'Percentages',
            'display_name': 'Percentages',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'elementary',
            'estimated_duration': 60,
            'description': 'Understanding and calculating percentages',
            'tags': ['percentages', 'ratios', 'proportions'],
            'learning_objectives': ['Convert between percentages and fractions', 'Calculate percentages']
        },
        {
            'id': 'algebra-basics',
            'name': 'Algebra Basics',
            'display_name': 'Algebra Basics',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'intermediate',
            'estimated_duration': 120,
            'description': 'Introduction to algebraic expressions and equations',
            'tags': ['algebra', 'expressions', 'equations'],
            'learning_objectives': ['Write algebraic expressions', 'Solve simple equations']
        },
        {
            'id': 'linear-equations',
            'name': 'Linear Equations',
            'display_name': 'Linear Equations',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'intermediate',
            'estimated_duration': 150,
            'description': 'Solving and graphing linear equations',
            'tags': ['linear', 'equations', 'graphing'],
            'learning_objectives': ['Solve linear equations', 'Graph linear equations']
        },
        {
            'id': 'functions',
            'name': 'Functions',
            'display_name': 'Functions',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'intermediate',
            'estimated_duration': 180,
            'description': 'Understanding and using mathematical functions',
            'tags': ['functions', 'mappings', 'relations'],
            'learning_objectives': ['Understand function notation', 'Evaluate functions']
        },
        {
            'id': 'quadratic-equations',
            'name': 'Quadratic Equations',
            'display_name': 'Quadratic Equations',
            'subject_id': 'mathematics',
            'type': 'theoretical',
            'difficulty_level': 'advanced',
            'estimated_duration': 180,
            'description': 'Solving quadratic equations using various methods',
            'tags': ['quadratic', 'equations', 'polynomials'],
            'learning_objectives': ['Solve by factoring', 'Use quadratic formula']
        },
        {
            'id': 'velocity-physics',
            'name': 'Velocity',
            'display_name': 'Velocity and Speed',
            'subject_id': 'physics',
            'type': 'theoretical',
            'difficulty_level': 'intermediate',
            'estimated_duration': 90,
            'description': 'Understanding velocity and speed in physics',
            'tags': ['velocity', 'motion', 'kinematics'],
            'learning_objectives': ['Distinguish velocity from speed', 'Calculate velocity']
        },
        {
            'id': 'acceleration',
            'name': 'Acceleration',
            'display_name': 'Acceleration',
            'subject_id': 'physics',
            'type': 'theoretical',
            'difficulty_level': 'intermediate',
            'estimated_duration': 120,
            'description': 'Understanding acceleration and motion',
            'tags': ['acceleration', 'motion', 'forces'],
            'learning_objectives': ['Understand acceleration', 'Apply kinematic equations']
        }
    ]
    
    relationships = [
        {'source': 'fractions', 'target': 'decimals', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'decimals', 'target': 'percentages', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'basic-arithmetic', 'target': 'fractions', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'basic-arithmetic', 'target': 'decimals', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'fractions', 'target': 'algebra-basics', 'type': 'prerequisite', 'strength': 0.9},
        {'source': 'algebra-basics', 'target': 'linear-equations', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'algebra-basics', 'target': 'functions', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'linear-equations', 'target': 'quadratic-equations', 'type': 'prerequisite', 'strength': 0.8},
        {'source': 'functions', 'target': 'quadratic-equations', 'type': 'prerequisite', 'strength': 0.7},
        {'source': 'velocity-physics', 'target': 'acceleration', 'type': 'prerequisite', 'strength': 1.0},
        {'source': 'functions', 'target': 'velocity-physics', 'type': 'application_of', 'strength': 0.8},
        {'source': 'linear-equations', 'target': 'velocity-physics', 'type': 'application_of', 'strength': 0.7}
    ]
    
    return concepts, relationships


def main():
    """Main entry point for the graph refresh task"""
    parser = argparse.ArgumentParser(
        description="VisualVerse Graph Refresh Task"
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Perform a full graph refresh'
    )
    parser.add_argument(
        '--incremental',
        action='store_true',
        help='Perform an incremental update'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current graph status'
    )
    parser.add_argument(
        '--cleanup',
        type=int,
        default=0,
        help='Clean up old snapshots, keeping specified count'
    )
    parser.add_argument(
        '--storage',
        type=str,
        default='/tmp/visualverse/graph_snapshots',
        help='Storage path for graph snapshots'
    )
    
    args = parser.parse_args()
    
    task = GraphRefreshTask(storage_path=args.storage)
    
    if args.status:
        status = task.get_status()
        print("\n=== Graph Status ===")
        print(f"Status: {status['status']}")
        print(f"Nodes: {status['node_count']}")
        print(f"Edges: {status['edge_count']}")
        print(f"Cycles: {status['cycles_detected']}")
        print(f"Last Refreshed: {status['last_refreshed']}")
        print(f"\nSubject Distribution:")
        for subj, count in status.get('subject_counts', {}).items():
            print(f"  {subj}: {count}")
        print()
    
    elif args.full:
        # Load sample data (in production, load from database)
        concepts, relationships = get_sample_data()
        
        stats = task.run_full_refresh(concepts, relationships)
        
        print("\n=== Graph Refresh Complete ===")
        print(f"Nodes: {stats.node_count}")
        print(f"Edges: {stats.edge_count}")
        print(f"Cycles: {stats.cycle_count}")
        print(f"Isolated Concepts: {len(stats.isolated_nodes)}")
        print(f"Top Central Concepts:")
        for concept in stats.central_concepts[:5]:
            print(f"  - {concept['name']} (score: {concept.get('centrality_score', 0):.3f})")
        print()
    
    elif args.incremental:
        # Example incremental update
        result = task.run_incremental_refresh(
            new_concepts=[
                {
                    'id': 'new-concept',
                    'name': 'New Concept',
                    'display_name': 'New Concept',
                    'subject_id': 'mathematics',
                    'type': 'theoretical',
                    'difficulty_level': 'beginner',
                    'estimated_duration': 30
                }
            ],
            new_relationships=[
                {'source': 'new-concept', 'target': 'basic-arithmetic', 'type': 'prerequisite'}
            ]
        )
        
        print("\n=== Incremental Update Complete ===")
        for key, value in result.items():
            print(f"{key}: {value}")
        print()
    
    elif args.cleanup > 0:
        removed = task.cleanup_old_snapshots(args.cleanup)
        print(f"Cleaned up {removed} old snapshot sets")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
