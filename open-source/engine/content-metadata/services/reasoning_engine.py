"""
Semantic Reasoning Engine for VisualVerse Content Metadata Layer

This module provides semantic reasoning capabilities including rule-based
inference, knowledge gap detection, concept similarity analysis, and
automatic concept categorization.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import time
import re
from collections import defaultdict, deque
from copy import deepcopy

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logging.warning("NetworkX not required for reasoning engine - using custom graph implementation")


from ..models.reasoning import (
    InferenceRule,
    InferenceRuleType,
    RelationshipDirection,
    ReasoningScope,
    InferenceConfidence,
    GapSeverity,
    InferredRelationship,
    KnowledgeGap,
    ConceptSimilarity,
    ConceptCluster,
    get_default_inference_rules
)


logger = logging.getLogger(__name__)


class ReasoningStats:
    """Statistics for reasoning engine operations"""
    
    def __init__(self):
        self.total_inferences: int = 0
        self.rules_executed: Dict[str, int] = defaultdict(int)
        self.inference_time_ms: float = 0.0
        self.last_run: Optional[datetime] = None
        self.gaps_detected: int = 0
        self.similarities_calculated: int = 0
        self.clusters_discovered: int = 0
        
        # Cycle tracking
        self.cycles_detected: int = 0
        self.cycles_resolved: int = 0
        
        # Error tracking
        self.errors: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'total_inferences': self.total_inferences,
            'rules_executed': dict(self.rules_executed),
            'inference_time_ms': self.inference_time_ms,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'gaps_detected': self.gaps_detected,
            'similarities_calculated': self.similarities_calculated,
            'clusters_discovered': self.clusters_discovered,
            'cycles_detected': self.cycles_detected,
            'cycles_resolved': self.cycles_resolved,
            'error_count': len(self.errors),
            'recent_errors': self.errors[-10:] if self.errors else []
        }


class ReasoningEngine:
    """
    Semantic reasoning engine for knowledge graph inference.
    
    This engine applies inference rules to derive implicit relationships,
    detect knowledge gaps, and perform similarity analysis on the
    knowledge graph.
    """
    
    def __init__(self):
        """Initialize the reasoning engine"""
        self._rules: Dict[str, InferenceRule] = {}
        self._inferred_relationships: Dict[str, InferredRelationship] = {}
        self._knowledge_gaps: Dict[str, KnowledgeGap] = {}
        self._similarities: Dict[str, ConceptSimilarity] = {}
        self._clusters: Dict[str, ConceptCluster] = {}
        
        # Statistics
        self._stats = ReasoningStats()
        
        # Register default rules
        self._register_default_rules()
    
    # =========================================================================
    # Rule Management
    # =========================================================================
    
    def register_rule(self, rule: InferenceRule) -> None:
        """Register an inference rule"""
        self._rules[rule.id] = rule
        logger.info(f"Registered inference rule: {rule.name} ({rule.rule_type.value})")
    
    def _register_default_rules(self) -> None:
        """Register default inference rules"""
        for rule in get_default_inference_rules():
            self._rules[rule.id] = rule
        logger.info(f"Registered {len(get_default_inference_rules())} default inference rules")
    
    def get_rule(self, rule_id: str) -> Optional[InferenceRule]:
        """Get a rule by ID"""
        return self._rules.get(rule_id)
    
    def list_rules(self, active_only: bool = True) -> List[InferenceRule]:
        """List all registered rules"""
        rules = list(self._rules.values())
        if active_only:
            rules = [r for r in rules if r.is_active]
        return rules
    
    def deactivate_rule(self, rule_id: str) -> bool:
        """Deactivate a rule"""
        if rule_id in self._rules:
            self._rules[rule_id].is_active = False
            return True
        return False
    
    # =========================================================================
    # Graph Building
    # =========================================================================
    
    def build_concept_graph(
        self,
        concepts: Dict[str, Dict[str, Any]],
        relationships: List[Dict[str, Any]]
    ) -> 'SimpleGraph':
        """
        Build a graph structure from concepts and relationships.
        
        Args:
            concepts: Dictionary of concept_id -> concept_data
            relationships: List of relationship dictionaries
            
        Returns:
            SimpleGraph instance
        """
        graph = SimpleGraph()
        
        # Add nodes
        for concept_id, data in concepts.items():
            node_data = {
                'id': concept_id,
                'name': data.get('name', data.get('display_name', concept_id)),
                'subject_id': data.get('subject_id', ''),
                'difficulty_level': data.get('difficulty_level', 'intermediate'),
                'type': data.get('type', 'theoretical'),
                'tags': data.get('tags', []),
                'keywords': data.get('keywords', []),
                'learning_objectives': data.get('learning_objectives', []),
                'description': data.get('description', ''),
                **data
            }
            graph.add_node(concept_id, node_data)
        
        # Add edges
        for rel in relationships:
            source = rel.get('source', rel.get('source_concept_id'))
            target = rel.get('target', rel.get('target_concept_id'))
            rel_type = rel.get('type', rel.get('relationship_type', 'prerequisite'))
            weight = rel.get('strength', rel.get('weight', 1.0))
            
            if source and target:
                graph.add_edge(source, target, {
                    'type': rel_type,
                    'weight': weight,
                    'is_explicit': True
                })
        
        return graph
    
    # =========================================================================
    # Inference Engine
    # =========================================================================
    
    def run_inference(
        self,
        graph: 'SimpleGraph',
        rule_ids: Optional[List[str]] = None,
        scope: ReasoningScope = ReasoningScope.GRAPH_WIDE
    ) -> Tuple[List[InferredRelationship], Dict[str, Any]]:
        """
        Run inference rules on the graph.
        
        Args:
            graph: Graph to run inference on
            rule_ids: Optional specific rules to apply (None = all active)
            scope: Scope of inference
            
        Returns:
            Tuple of (inferred_relationships, stats)
        """
        start_time = time.time()
        inferred = []
        
        # Get rules to apply
        if rule_ids:
            rules = [self._rules[r] for r in rule_ids if r in self._rules]
        else:
            rules = [r for r in self._rules.values() if r.is_active]
        
        logger.info(f"Running inference with {len(rules)} rules")
        
        # Apply each rule
        for rule in rules:
            try:
                new_inferences = self._apply_rule(graph, rule)
                inferred.extend(new_inferences)
                self._stats.rules_executed[rule.id] += len(new_inferences)
                
            except Exception as e:
                logger.error(f"Error applying rule {rule.id}: {e}")
                self._stats.errors.append(f"Rule {rule.id}: {str(e)}")
        
        # Store inferred relationships
        for inf in inferred:
            self._inferred_relationships[inf.id] = inf
        
        # Update statistics
        elapsed = (time.time() - start_time) * 1000
        self._stats.total_inferences += len(inferred)
        self._stats.inference_time_ms = elapsed
        self._stats.last_run = datetime.now()
        
        return inferred, {
            'total_inferred': len(inferred),
            'inference_time_ms': elapsed,
            'rules_applied': list(self._stats.rules_executed.keys()),
            'warnings': self._stats.errors[-5:] if self._stats.errors else []
        }
    
    def _apply_rule(
        self,
        graph: 'SimpleGraph',
        rule: InferenceRule
    ) -> List[InferredRelationship]:
        """Apply a single inference rule"""
        inferred = []
        
        if rule.rule_type == InferenceRuleType.TRANSITIVE:
            inferred = self._apply_transitive_rule(graph, rule)
        elif rule.rule_type == InferenceRuleType.SYMMETRIC:
            inferred = self._apply_symmetric_rule(graph, rule)
        elif rule.rule_type == InferenceRuleType.INVERSE:
            inferred = self._apply_inverse_rule(graph, rule)
        elif rule.rule_type == InferenceRuleType.SIMILARITY:
            inferred = self._apply_similarity_rule(graph, rule)
        elif rule.rule_type == InferenceRuleType.CLUSTER:
            inferred = self._apply_cluster_rule(graph, rule)
        
        return inferred
    
    def _apply_transitive_rule(
        self,
        graph: 'SimpleGraph',
        rule: InferenceRule
    ) -> List[InferredRelationship]:
        """Apply transitive inference rule"""
        inferred = []
        source_pred = rule.source_predicate
        target_pred = rule.target_predicate or f"derived_{source_pred}"
        
        # Find all paths up to max_hops
        for node in graph.nodes():
            paths = graph.find_all_paths(
                node,
                max_length=rule.max_hops,
                edge_filter=lambda d: d.get('type') == source_pred
            )
            
            for path in paths:
                if len(path) > 1:
                    source = path[0]
                    target = path[-1]
                    
                    # Check if direct edge already exists
                    if not graph.has_edge(source, target):
                        # Check if we already inferred this
                        existing = self._find_existing_inference(
                            source, target, target_pred
                        )
                        if not existing:
                            inf = self._create_inferred_relationship(
                                source, target, target_pred, rule, path
                            )
                            inferred.append(inf)
                            
                            # Add virtual edge to graph
                            graph.add_edge(source, target, {
                                'type': target_pred,
                                'is_inferred': True,
                                'rule_id': rule.id,
                                'confidence': rule.confidence_weight * self._calculate_path_confidence(path)
                            })
        
        return inferred
    
    def _apply_symmetric_rule(
        self,
        graph: 'SimpleGraph',
        rule: InferenceRule
    ) -> List[InferredRelationship]:
        """Apply symmetric inference rule"""
        inferred = []
        pred = rule.source_predicate
        
        for source, target, edge_data in graph.edges(data=True):
            if edge_data.get('type') == pred:
                # Check if inverse edge exists
                if not graph.has_edge(target, source):
                    existing = self._find_existing_inference(
                        target, source, pred, rule.id
                    )
                    if not existing:
                        inf = InferredRelationship(
                            source_concept_id=target,
                            target_concept_id=source,
                            relationship_type=pred,
                            rule_id=rule.id,
                            inference_confidence=InferenceConfidence.MEDIUM,
                            confidence_score=rule.confidence_weight * 0.8,
                            derivation_path=[{'from': source, 'to': target}],
                            hop_count=1
                        )
                        inferred.append(inf)
                        
                        # Add virtual edge
                        graph.add_edge(target, source, {
                            'type': pred,
                            'is_inferred': True,
                            'rule_id': rule.id,
                            'confidence': rule.confidence_weight * 0.8
                        })
        
        return inferred
    
    def _apply_inverse_rule(
        self,
        graph: 'SimpleGraph',
        rule: InferenceRule
    ) -> List[InferredRelationship]:
        """Apply inverse inference rule"""
        inferred = []
        source_pred = rule.source_predicate
        target_pred = rule.target_predicate or f"inverse_{source_pred}"
        
        inverse_map = {
            'prerequisite': 'enables',
            'leads_to': 'requires',
            'component_of': 'has_component'
        }
        inferred_pred = inverse_map.get(source_pred, target_pred)
        
        for source, target, edge_data in graph.edges(data=True):
            if edge_data.get('type') == source_pred:
                existing = self._find_existing_inference(
                    target, source, inferred_pred, rule.id
                )
                if not existing:
                    inf = InferredRelationship(
                        source_concept_id=target,
                        target_concept_id=source,
                        relationship_type=inferred_pred,
                        inverse_relationship=source_pred,
                        rule_id=rule.id,
                        inference_confidence=InferenceConfidence.HIGH,
                        confidence_score=rule.confidence_weight * 0.9,
                        derivation_path=[{'from': source, 'to': target}],
                        hop_count=1
                    )
                    inferred.append(inf)
        
        return inferred
    
    def _apply_similarity_rule(
        self,
        graph: 'SimpleGraph',
        rule: InferenceRule
    ) -> List[InferredRelationship]:
        """Apply similarity inference rule"""
        # Similarity is calculated separately and stored as ConceptSimilarity
        # This is a placeholder for similarity-based inference
        return []
    
    def _apply_cluster_rule(
        self,
        graph: 'SimpleGraph',
        rule: InferenceRule
    ) -> List[InferredRelationship]:
        """Apply clustering inference rule"""
        # Clustering is performed separately
        return []
    
    def _create_inferred_relationship(
        self,
        source: str,
        target: str,
        rel_type: str,
        rule: InferenceRule,
        path: List[str]
    ) -> InferredRelationship:
        """Create an inferred relationship from a path"""
        hop_count = len(path) - 1
        
        # Calculate confidence based on path length
        path_confidence = self._calculate_path_confidence(path)
        
        # Determine confidence level
        if path_confidence > 0.8:
            confidence = InferenceConfidence.HIGH
        elif path_confidence > 0.5:
            confidence = InferenceConfidence.MEDIUM
        else:
            confidence = InferenceConfidence.LOW
        
        # Build derivation path
        derivation = []
        for i in range(len(path) - 1):
            derivation.append({
                'from': path[i],
                'to': path[i + 1]
            })
        
        return InferredRelationship(
            source_concept_id=source,
            target_concept_id=target,
            relationship_type=rel_type,
            rule_id=rule.id,
            inference_confidence=confidence,
            confidence_score=rule.confidence_weight * path_confidence,
            derivation_path=derivation,
            hop_count=hop_count
        )
    
    def _calculate_path_confidence(self, path: List[str]) -> float:
        """Calculate confidence score for a path"""
        # Shorter paths have higher confidence
        max_hops = 5
        hop_count = len(path) - 1
        return max(0.3, 1.0 - (hop_count / max_hops) * 0.5)
    
    def _find_existing_inference(
        self,
        source: str,
        target: str,
        rel_type: str,
        rule_id: Optional[str] = None
    ) -> Optional[InferredRelationship]:
        """Check if an inference already exists"""
        for inf in self._inferred_relationships.values():
            if (inf.source_concept_id == source and
                inf.target_concept_id == target and
                inf.relationship_type == rel_type and
                (rule_id is None or inf.rule_id == rule_id)):
                return inf
        return None
    
    # =========================================================================
    # Knowledge Gap Detection
    # =========================================================================
    
    def detect_knowledge_gaps(
        self,
        graph: 'SimpleGraph',
        completed_concepts: Set[str],
        target_concepts: Optional[Set[str]] = None,
        include_minor_gaps: bool = False
    ) -> List[KnowledgeGap]:
        """
        Detect knowledge gaps based on completed concepts.
        
        Args:
            graph: Concept graph
            completed_concepts: Set of completed concept IDs
            target_concepts: Target concepts to check (None = all)
            include_minor_gaps: Include minor gaps
            
        Returns:
            List of detected knowledge gaps
        """
        gaps = []
        
        # If no target specified, check all concepts
        if target_concepts is None:
            target_concepts = set(graph.nodes())
        
        # Remove completed concepts
        targets_to_check = target_concepts - completed_concepts
        
        for target_id in targets_to_check:
            target_data = graph.get_node_data(target_id)
            if not target_data:
                continue
            
            # Find prerequisites
            prereqs = graph.get_prerequisites(target_id, recursive=False)
            
            # Check for missing prerequisites
            missing = []
            blocking = []
            
            for prereq in prereqs:
                if prereq not in completed_concepts:
                    prereq_data = graph.get_node_data(prereq)
                    missing.append({
                        'id': prereq,
                        'name': prereq_data.get('name', prereq) if prereq_data else prereq,
                        'difficulty': prereq_data.get('difficulty_level', 'unknown') if prereq_data else 'unknown'
                    })
                    
                    # Check if this blocks other concepts
                    dependents = graph.get_postrequisites(prereq)
                    for dep in dependents:
                        if dep not in completed_concepts and dep in target_concepts:
                            blocking.append(dep)
            
            if missing:
                # Determine severity
                severity = self._determine_gap_severity(
                    missing, blocking, include_minor_gaps
                )
                
                if severity:
                    gap = KnowledgeGap(
                        target_concept_id=target_id,
                        target_concept_name=target_data.get('name', target_id),
                        gap_type='missing_prerequisite',
                        severity=severity,
                        missing_concepts=missing,
                        blocking_concepts=list(set(blocking)),
                        suggested_prerequisites=[m['id'] for m in missing],
                        estimated_effort_hours=self._estimate_gap_effort(missing),
                        subject_id=target_data.get('subject_id', '')
                    )
                    
                    gaps.append(gap)
                    self._knowledge_gaps[gap.id] = gap
        
        # Find disconnected concepts
        disconnected = self._find_disconnected_concepts(
            graph, completed_concepts, target_concepts
        )
        
        for concept_id in disconnected:
            concept_data = graph.get_node_data(concept_id)
            if concept_data:
                gap = KnowledgeGap(
                    target_concept_id=concept_id,
                    target_concept_name=concept_data.get('name', concept_id),
                    gap_type='disconnected',
                    severity=GapSeverity.MINOR if include_minor_gaps else GapSeverity.MAJOR,
                    missing_relationships=[{
                        'type': 'prerequisite',
                        'suggestion': 'Add prerequisite relationships to connect this concept'
                    }],
                    subject_id=concept_data.get('subject_id', ''),
                    suggested_prerequisites=self._suggest_connectors(graph, concept_id)
                )
                gaps.append(gap)
        
        self._stats.gaps_detected = len(gaps)
        return gaps
    
    def _determine_gap_severity(
        self,
        missing: List[Dict[str, str]],
        blocking: List[str],
        include_minor: bool
    ) -> Optional[GapSeverity]:
        """Determine severity of a knowledge gap"""
        missing_count = len(missing)
        
        # Critical: Many missing prerequisites
        if missing_count >= 3:
            return GapSeverity.CRITICAL
        elif missing_count == 2:
            return GapSeverity.MAJOR
        elif missing_count == 1:
            if len(blocking) >= 3:
                return GapSeverity.MAJOR
            elif include_minor:
                return GapSeverity.MINOR
        
        return None
    
    def _find_disconnected_concepts(
        self,
        graph: 'SimpleGraph',
        completed: Set[str],
        targets: Set[str]
    ) -> Set[str]:
        """Find concepts that are disconnected from the learning path"""
        disconnected = set()
        
        # Build subgraph of incomplete targets
        incomplete = targets - completed
        
        for concept_id in incomplete:
            # Check if concept has any prerequisite path from completed concepts
            has_path = False
            
            for completed_id in completed:
                if graph.has_path(completed_id, concept_id):
                    has_path = True
                    break
            
            if not has_path:
                # Check if it has any prerequisites at all
                prereqs = graph.get_prerequisites(concept_id, recursive=False)
                if not prereqs or all(p in completed for p in prereqs):
                    # Concept is isolated
                    disconnected.add(concept_id)
        
        return disconnected
    
    def _suggest_connectors(
        self,
        graph: 'SimpleGraph',
        concept_id: str
    ) -> List[str]:
        """Suggest concepts that could connect to this concept"""
        suggestions = []
        
        # Find concepts in same subject with matching tags
        concept_data = graph.get_node_data(concept_id)
        if not concept_data:
            return suggestions
        
        subject = concept_data.get('subject_id')
        tags = set(concept_data.get('tags', []))
        
        for node_id in graph.nodes():
            if node_id == concept_id:
                continue
            
            node_data = graph.get_node_data(node_id)
            if not node_data:
                continue
            
            # Check subject
            if node_data.get('subject_id') == subject:
                node_tags = set(node_data.get('tags', []))
                
                # Check tag overlap
                if tags & node_tags:
                    suggestions.append(node_id)
        
        return suggestions[:5]
    
    def _estimate_gap_effort(self, missing: List[Dict[str, str]]) -> float:
        """Estimate effort to fill a knowledge gap"""
        total_hours = 0.0
        
        difficulty_hours = {
            'beginner': 0.5,
            'elementary': 1.0,
            'intermediate': 2.0,
            'advanced': 4.0,
            'expert': 8.0
        }
        
        for item in missing:
            diff = item.get('difficulty', 'intermediate')
            total_hours += difficulty_hours.get(diff, 2.0)
        
        return total_hours
    
    # =========================================================================
    # Concept Similarity
    # =========================================================================
    
    def calculate_similarity(
        self,
        graph: 'SimpleGraph',
        concept_a_id: str,
        concept_b_id: str,
        include_details: bool = True
    ) -> ConceptSimilarity:
        """Calculate similarity between two concepts"""
        node_a = graph.get_node_data(concept_a_id)
        node_b = graph.get_node_data(concept_b_id)
        
        if not node_a or not node_b:
            raise ValueError("One or both concepts not found")
        
        # Calculate different similarity components
        tag_sim = self._jaccard_similarity(
            set(node_a.get('tags', [])),
            set(node_b.get('tags', []))
        )
        
        keyword_sim = self._jaccard_similarity(
            set(node_a.get('keywords', [])),
            set(node_b.get('keywords', []))
        )
        
        objective_sim = self._jaccard_similarity(
            set(node_a.get('learning_objectives', [])),
            set(node_b.get('learning_objectives', []))
        )
        
        structural_sim = self._calculate_structural_similarity(
            graph, concept_a_id, concept_b_id
        )
        
        # Weighted overall score
        weights = {'tag': 0.3, 'keyword': 0.3, 'objective': 0.25, 'structural': 0.15}
        overall = (
            tag_sim * weights['tag'] +
            keyword_sim * weights['keyword'] +
            objective_sim * weights['objective'] +
            structural_sim * weights['structural']
        )
        
        # Find shared items
        shared_tags = list(set(node_a.get('tags', [])) & set(node_b.get('tags', [])))
        shared_keywords = list(set(node_a.get('keywords', [])) & set(node_b.get('keywords', [])))
        shared_objectives = list(set(node_a.get('learning_objectives', [])) & 
                                  set(node_b.get('learning_objectives', [])))
        
        similarity = ConceptSimilarity(
            concept_a_id=concept_a_id,
            concept_b_id=concept_b_id,
            overall_score=overall,
            tag_similarity=tag_sim,
            keyword_similarity=keyword_sim,
            objective_similarity=objective_sim,
            structural_similarity=structural_sim,
            shared_tags=shared_tags,
            shared_keywords=shared_keywords,
            shared_objectives=shared_objectives,
            recommended_as_prerequisite=overall > 0.7 and tag_sim < 0.3,
            recommended_for_review=overall > 0.6,
            calculation_method="weighted_average"
        )
        
        self._similarities[f"{concept_a_id}:{concept_b_id}"] = similarity
        self._stats.similarities_calculated += 1
        
        return similarity
    
    def _jaccard_similarity(
        self,
        set_a: Set[str],
        set_b: Set[str]
    ) -> float:
        """Calculate Jaccard similarity between two sets"""
        if not set_a and not set_b:
            return 0.0
        
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_structural_similarity(
        self,
        graph: 'SimpleGraph',
        concept_a: str,
        concept_b: str
    ) -> float:
        """Calculate structural similarity based on graph position"""
        # Get neighbors
        neighbors_a = set(graph.get_neighbors(concept_a))
        neighbors_b = set(graph.get_neighbors(concept_b))
        
        if not neighbors_a and not neighbors_b:
            return 0.0
        
        # Jaccard similarity of neighbors
        return self._jaccard_similarity(neighbors_a, neighbors_b)
    
    # =========================================================================
    # Concept Clustering
    # =========================================================================
    
    def discover_clusters(
        self,
        graph: 'SimpleGraph',
        concept_ids: Optional[List[str]] = None,
        min_similarity: float = 0.6,
        max_cluster_size: int = 20,
        min_cluster_size: int = 3
    ) -> List[ConceptCluster]:
        """Discover concept clusters using similarity"""
        # Get concepts to cluster
        if concept_ids is None:
            concept_ids = list(graph.nodes())
        
        # Calculate pairwise similarities
        similarities: Dict[Tuple[str, str], float] = {}
        
        for i, cid_a in enumerate(concept_ids):
            for cid_b in concept_ids[i + 1:]:
                try:
                    sim = self.calculate_similarity(graph, cid_a, cid_b, include_details=False)
                    similarities[(cid_a, cid_b)] = sim.overall_score
                except ValueError:
                    pass
        
        # Perform clustering using threshold-based approach
        clusters: List[Set[str]] = []
        assigned = set()
        
        for (a, b), sim in sorted(similarities.items(), key=lambda x: x[1], reverse=True):
            if sim < min_similarity:
                continue
            
            # Find which cluster a and b belong to
            cluster_a = self._find_cluster(clusters, a)
            cluster_b = self._find_cluster(clusters, b)
            
            if cluster_a is None and cluster_b is None:
                # Create new cluster
                if len(concept_ids) >= min_cluster_size:
                    clusters.append({a, b})
                    assigned.add(a)
                    assigned.add(b)
            elif cluster_a is not None and cluster_b is None:
                # Add b to a's cluster
                if len(cluster_a) < max_cluster_size and a not in assigned:
                    cluster_a.add(b)
                    assigned.add(b)
            elif cluster_a is None and cluster_b is not None:
                # Add a to b's cluster
                if len(cluster_b) < max_cluster_size and b not in assigned:
                    cluster_b.add(a)
                    assigned.add(a)
            elif cluster_a is not None and cluster_b is not None and cluster_a != cluster_b:
                # Merge clusters
                if len(cluster_a) + len(cluster_b) <= max_cluster_size:
                    cluster_a.update(cluster_b)
                    clusters = [c for c in clusters if c != cluster_b]
        
        # Convert to ConceptCluster objects
        result_clusters = []
        
        for i, concept_set in enumerate(clusters):
            if len(concept_set) < min_cluster_size:
                continue
            
            concept_list = list(concept_set)
            
            # Calculate cluster metrics
            cohesion = self._calculate_cluster_cohesion(concept_list, similarities)
            
            # Find centroid (concept with highest average similarity)
            centroid = self._find_centroid(concept_list, similarities)
            
            # Get cluster properties
            subject_counts: Dict[str, int] = defaultdict(int)
            difficulties: List[str] = []
            
            for cid in concept_list:
                data = graph.get_node_data(cid)
                if data:
                    subject_counts[data.get('subject_id', 'unknown')] += 1
                    difficulties.append(data.get('difficulty_level', 'intermediate'))
            
            # Calculate average difficulty
            diff_order = {'beginner': 0, 'elementary': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
            avg_diff = sum(diff_order.get(d, 2) for d in difficulties) / len(difficulties)
            diff_names = list(diff_order.keys())
            avg_diff_name = diff_names[min(int(avg_diff), len(diff_names) - 1)]
            
            cluster = ConceptCluster(
                id=f"cluster-{i + 1}",
                name=f"Concept Cluster {i + 1}",
                description=f"Cluster of {len(concept_list)} related concepts",
                concept_ids=concept_list,
                centroid_concept_id=centroid,
                cohesion_score=cohesion,
                average_difficulty=avg_diff_name,
                primary_subject=max(subject_counts.items(), key=lambda x: x[1])[0] if subject_counts else '',
                secondary_subjects=[k for k, v in subject_counts.items() if k != max(subject_counts.items(), key=lambda x: x[1])],
                suggested_order=self._suggest_learning_order(concept_list, graph),
                discovery_method="similarity_clustering"
            )
            
            result_clusters.append(cluster)
            self._clusters[cluster.id] = cluster
        
        self._stats.clusters_discovered = len(result_clusters)
        
        return result_clusters
    
    def _find_cluster(
        self,
        clusters: List[Set[str]],
        concept_id: str
    ) -> Optional[Set[str]]:
        """Find which cluster a concept belongs to"""
        for cluster in clusters:
            if concept_id in cluster:
                return cluster
        return None
    
    def _calculate_cluster_cohesion(
        self,
        concepts: List[str],
        similarities: Dict[Tuple[str, str], float]
    ) -> float:
        """Calculate cohesion of a cluster"""
        if len(concepts) < 2:
            return 1.0
        
        total_sim = 0.0
        count = 0
        
        for i, c_a in enumerate(concepts):
            for c_b in concepts[i + 1:]:
                key = (c_a, c_b) if (c_a, c_b) in similarities else (c_b, c_a)
                if key in similarities:
                    total_sim += similarities[key]
                    count += 1
        
        return total_sim / count if count > 0 else 0.0
    
    def _find_centroid(
        self,
        concepts: List[str],
        similarities: Dict[Tuple[str, str], float]
    ) -> Optional[str]:
        """Find the centroid concept of a cluster"""
        if not concepts:
            return None
        
        best_concept = concepts[0]
        best_score = -1.0
        
        for concept in concepts:
            total_sim = 0.0
            count = 0
            
            for other in concepts:
                if concept == other:
                    continue
                
                key = (concept, other) if (concept, other) in similarities else (other, concept)
                if key in similarities:
                    total_sim += similarities[key]
                    count += 1
            
            avg_sim = total_sim / count if count > 0 else 0
            if avg_sim > best_score:
                best_score = avg_sim
                best_concept = concept
        
        return best_concept
    
    def _suggest_learning_order(
        self,
        concepts: List[str],
        graph: 'SimpleGraph'
    ) -> List[str]:
        """Suggest a learning order for concepts in a cluster"""
        # Sort by depth in dependency graph
        depth_map = {}
        
        for concept in concepts:
            prereqs = graph.get_prerequisites(concept, recursive=True)
            depth_map[concept] = len(prereqs)
        
        return sorted(concepts, key=lambda c: depth_map.get(c, 0))
    
    # =========================================================================
    # Statistics and Utilities
    # =========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get reasoning engine statistics"""
        return self._stats.to_dict()
    
    def get_inferred_relationships(
        self,
        concept_id: Optional[str] = None,
        relationship_type: Optional[str] = None
    ) -> List[InferredRelationship]:
        """Get inferred relationships"""
        results = list(self._inferred_relationships.values())
        
        if concept_id:
            results = [
                r for r in results
                if r.source_concept_id == concept_id or r.target_concept_id == concept_id
            ]
        
        if relationship_type:
            results = [
                r for r in results
                if r.relationship_type == relationship_type
            ]
        
        return results
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._inferred_relationships.clear()
        self._knowledge_gaps.clear()
        self._similarities.clear()
        self._clusters.clear()
        self._stats = ReasoningStats()
        logger.info("Cleared all reasoning engine caches")


# ============================================================================
# Simple Graph Implementation (No NetworkX dependency)
# ============================================================================

class SimpleGraph:
    """
    Simple graph implementation without NetworkX dependency.
    
    Provides core graph operations needed by the reasoning engine.
    """
    
    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._adjacency: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
        self._reverse_adjacency: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
    
    def add_node(self, node_id: str, data: Dict[str, Any]) -> None:
        """Add a node to the graph"""
        self._nodes[node_id] = data
    
    def has_node(self, node_id: str) -> bool:
        """Check if node exists"""
        return node_id in self._nodes
    
    def get_node_data(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get node data"""
        return self._nodes.get(node_id)
    
    def nodes(self):
        """Get all node IDs"""
        return list(self._nodes.keys())
    
    def add_edge(
        self,
        source: str,
        target: str,
        edge_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an edge to the graph"""
        self._adjacency[source][target] = edge_data or {}
        self._reverse_adjacency[target][source] = edge_data or {}
    
    def has_edge(self, source: str, target: str) -> bool:
        """Check if edge exists"""
        return target in self._adjacency.get(source, {})
    
    def get_edge_data(self, source: str, target: str) -> Optional[Dict[str, Any]]:
        """Get edge data"""
        return self._adjacency.get(source, {}).get(target)
    
    def edges(self, data: bool = False):
        """Get all edges"""
        for source in self._adjacency:
            for target in self._adjacency[source]:
                if data:
                    yield source, target, self._adjacency[source][target]
                else:
                    yield source, target
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """Get neighbors of a node"""
        return list(self._adjacency.get(node_id, {}).keys())
    
    def get_prerequisites(
        self,
        node_id: str,
        recursive: bool = False
    ) -> List[str]:
        """Get prerequisite nodes"""
        prereqs = list(self._reverse_adjacency.get(node_id, {}).keys())
        
        if recursive:
            all_prereqs = set(prereqs)
            to_process = list(prereqs)
            
            while to_process:
                current = to_process.pop()
                current_prereqs = self._reverse_adjacency.get(current, {}).keys()
                
                for prereq in current_prereqs:
                    if prereq not in all_prereqs:
                        all_prereqs.add(prereq)
                        to_process.append(prereq)
            
            prereqs = list(all_prereqs)
        
        return prereqs
    
    def get_postrequisites(
        self,
        node_id: str,
        recursive: bool = False
    ) -> List[str]:
        """Get postrequisite nodes"""
        postreqs = list(self._adjacency.get(node_id, {}).keys())
        
        if recursive:
            all_postreqs = set(postreqs)
            to_process = list(postreqs)
            
            while to_process:
                current = to_process.pop()
                current_postreqs = self._adjacency.get(current, {}).keys()
                
                for postreq in current_postreqs:
                    if postreq not in all_postreqs:
                        all_postreqs.add(postreq)
                        to_process.append(postreq)
            
            postreqs = list(all_postreqs)
        
        return postreqs
    
    def has_path(self, source: str, target: str) -> bool:
        """Check if path exists between nodes"""
        if source == target:
            return True
        
        visited = {source}
        queue = deque([source])
        
        while queue:
            current = queue.popleft()
            
            for neighbor in self._adjacency.get(current, {}):
                if neighbor == target:
                    return True
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
    
    def find_all_paths(
        self,
        source: str,
        max_length: int = 5,
        edge_filter: Optional[Callable] = None
    ) -> List[List[str]]:
        """Find all paths from source within max_length"""
        paths = []
        
        def dfs(current: str, path: List[str], depth: int):
            if depth >= max_length:
                return
            
            for neighbor in self._adjacency.get(current, {}):
                edge_data = self._adjacency[current][neighbor]
                
                if edge_filter and not edge_filter(edge_data):
                    continue
                
                new_path = path + [neighbor]
                paths.append(new_path)
                
                dfs(neighbor, new_path, depth + 1)
        
        dfs(source, [source], 0)
        
        return paths
    
    def clear(self) -> None:
        """Clear the graph"""
        self._nodes.clear()
        self._adjacency.clear()
        self._reverse_adjacency.clear()
    
    def __len__(self) -> int:
        """Get number of nodes"""
        return len(self._nodes)
