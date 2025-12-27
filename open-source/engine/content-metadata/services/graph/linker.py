"""
Cross-Subject Linker for VisualVerse Content Metadata Layer

This module provides algorithms for identifying transferable concepts,
shared prerequisites across subjects, and interdisciplinary learning path
generation. It enables the discovery of connections between different
subject areas.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import re
from collections import defaultdict

from .engine import DependencyGraphEngine, GraphNode, RelationshipType, PathResult


logger = logging.getLogger(__name__)


class TransferabilityScore(Enum):
    """Levels of concept transferability between subjects"""
    DIRECT = "direct"           # Same concept, different contexts
    ANALOGOUS = "analogous"     # Similar concept with different representation
    FOUNDATIONAL = "foundational"  # Underlying concept used in multiple subjects
    APPLICATION = "application" # Concept applied in different domain
    RELATED = "related"         # Weakly related concept


@dataclass
class CrossSubjectLink:
    """Represents a link between concepts from different subjects"""
    source_concept_id: str
    source_subject_id: str
    target_concept_id: str
    target_subject_id: str
    transferability: TransferabilityScore
    strength: float
    reasoning: str
    shared_principles: List[str] = field(default_factory=list)
    context_differences: List[str] = field(default_factory=list)
    suggested_learning_sequence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'source_concept_id': self.source_concept_id,
            'source_subject_id': self.source_subject_id,
            'target_concept_id': self.target_concept_id,
            'target_subject_id': self.target_subject_id,
            'transferability': self.transferability.value,
            'strength': self.strength,
            'reasoning': self.reasoning,
            'shared_principles': self.shared_principles,
            'context_differences': self.context_differences,
            'suggested_learning_sequence': self.suggested_learning_sequence,
            'metadata': self.metadata
        }


@dataclass
class InterdisciplinaryPath:
    """Represents a learning path that spans multiple subjects"""
    id: str
    name: str
    description: str
    concepts: List[Dict[str, Any]]
    subjects_involved: List[str]
    total_duration_minutes: int
    transition_points: List[Dict[str, Any]]
    learning_synergies: List[str]
    difficulty_progression: List[str]
    created_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'concepts': self.concepts,
            'subjects_involved': self.subjects_involved,
            'total_duration_minutes': self.total_duration_minutes,
            'transition_points': self.transition_points,
            'learning_synergies': self.learning_synergies,
            'difficulty_progression': self.difficulty_progression,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class SharedPrerequisite:
    """Represents a shared prerequisite between subjects"""
    concept_id: str
    concept_name: str
    subjects: List[str]
    usage_count: int
    bridging_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'concept_id': self.concept_id,
            'concept_name': self.concept_name,
            'subjects': self.subjects,
            'usage_count': self.usage_count,
            'bridging_score': self.bridging_score
        }


class InterdisciplinaryLinker:
    """
    Service for identifying and managing cross-subject relationships.
    
    This linker analyzes the knowledge graph to discover connections
    between different subjects, enabling interdisciplinary learning paths
    and concept transferability analysis.
    """
    
    # Known subject bridging relationships
    SUBJECT_BRIDGES = {
        ('mathematics', 'physics'): {
            'shared_concepts': ['calculus', 'functions', 'vectors', 'graphs', 'derivatives', 'integrals'],
            'transfer_patterns': {
                'functions': 'Used to model physical relationships',
                'calculus': 'Applied to understand rates of change in physics',
                'vectors': 'Essential for representing physical quantities'
            }
        },
        ('mathematics', 'chemistry'): {
            'shared_concepts': ['stoichiometry', 'equilibrium', 'rate equations', 'logarithms'],
            'transfer_patterns': {
                'logarithms': 'Used in pH calculations and reaction rates',
                'rate equations': 'Mathematical modeling of reaction kinetics'
            }
        },
        ('physics', 'chemistry'): {
            'shared_concepts': ['energy', 'forces', 'molecular motion', 'thermodynamics'],
            'transfer_patterns': {
                'thermodynamics': 'Core concept in both physics and chemistry',
                'energy': 'Fundamental concept connecting both disciplines'
            }
        },
        ('mathematics', 'computer_science'): {
            'shared_concepts': ['algorithms', 'logic', 'discrete math', 'functions', 'recursion'],
            'transfer_patterns': {
                'algorithms': 'Mathematical procedures implemented in code',
                'logic': 'Foundation for programming and proofs'
            }
        },
        ('physics', 'computer_science'): {
            'shared_concepts': ['simulation', 'computational complexity', 'signals'],
            'transfer_patterns': {
                'simulation': 'Computer models of physical systems',
                'signals': 'Digital signal processing'
            }
        },
        ('economics', 'mathematics'): {
            'shared_concepts': ['optimization', 'functions', 'statistics', 'calculus'],
            'transfer_patterns': {
                'optimization': 'Used for finding maximum profit/minimum cost',
                'calculus': 'Marginal analysis in economics'
            }
        }
    }
    
    def __init__(self, graph_engine: DependencyGraphEngine):
        """
        Initialize the interdisciplinary linker.
        
        Args:
            graph_engine: The dependency graph engine to use for analysis
        """
        self.graph = graph_engine
        self._cached_links: Dict[str, CrossSubjectLink] = {}
        self._semantic_cache: Dict[str, Dict[str, Any]] = {}
    
    # =========================================================================
    # Concept Transferability Analysis
    # =========================================================================
    
    def find_transferable_concepts(
        self,
        concept_id: str,
        target_subject_id: Optional[str] = None,
        min_strength: float = 0.3
    ) -> List[CrossSubjectLink]:
        """
        Find concepts in other subjects that are transferable.
        
        Args:
            concept_id: The source concept ID
            target_subject_id: Optional specific target subject
            min_strength: Minimum transferability strength
            
        Returns:
            List of CrossSubjectLink objects
        """
        source_node = self.graph.get_node(concept_id)
        if not source_node:
            return []
        
        cache_key = f"{concept_id}:{target_subject_id or 'all'}"
        if cache_key in self._cached_links:
            return [self._cached_links[cache_key]]
        
        links = []
        
        # Get all subjects
        subjects = self.graph._subject_index.keys()
        
        for subject_id in subjects:
            if subject_id == source_node.subject_id:
                continue
            
            if target_subject_id and subject_id != target_subject_id:
                continue
            
            # Find potential matches in target subject
            target_concepts = self.graph.get_concepts_by_subject(subject_id)
            
            for target_concept in target_concepts:
                transferability = self._assess_transferability(
                    source_node,
                    target_concept,
                    source_node.subject_id,
                    subject_id
                )
                
                if transferability.strength >= min_strength:
                    links.append(transferability)
        
        # Sort by strength
        links.sort(key=lambda x: x.strength, reverse=True)
        
        return links
    
    def _assess_transferability(
        self,
        source: GraphNode,
        target: Dict[str, Any],
        source_subject: str,
        target_subject: str
    ) -> CrossSubjectLink:
        """
        Assess the transferability between two concepts.
        
        Args:
            source: Source concept node
            target: Target concept dictionary
            source_subject: Source subject ID
            target_subject: Target subject ID
            
        Returns:
            CrossSubjectLink with transferability assessment
        """
        # Check known bridges first
        subject_pair = tuple(sorted([source_subject, target_subject]))
        if subject_pair in self.SUBJECT_BRIDGES:
            bridge = self.SUBJECT_BRIDGES[subject_pair]
            
            # Check for shared concepts
            source_name_lower = source.name.lower()
            target_name_lower = target.get('name', '').lower()
            
            for shared_concept in bridge['shared_concepts']:
                if shared_concept in source_name_lower or shared_concept in target_name_lower:
                    transfer_type = self._determine_transfer_type(
                        source, target, bridge, shared_concept
                    )
                    
                    return CrossSubjectLink(
                        source_concept_id=source.id,
                        source_subject_id=source_subject,
                        target_concept_id=target.get('id', ''),
                        target_subject_id=target_subject,
                        transferability=transfer_type,
                        strength=0.9,
                        reasoning=bridge['transfer_patterns'].get(
                            shared_concept,
                            f"{shared_concept} is a shared concept between {source_subject} and {target_subject}"
                        ),
                        shared_principles=[shared_concept],
                        context_differences=self._identify_context_differences(
                            source_subject, target_subject, shared_concept
                        ),
                        metadata={'detection_method': 'known_bridge'}
                    )
        
        # Fall back to semantic analysis
        return self._semantic_transferability_analysis(source, target, source_subject, target_subject)
    
    def _determine_transfer_type(
        self,
        source: GraphNode,
        target: Dict[str, Any],
        bridge: Dict[str, Any],
        shared_concept: str
    ) -> TransferabilityScore:
        """Determine the type of transferability"""
        source_name = source.name.lower()
        target_name = target.get('name', '').lower()
        
        # Check if concepts are essentially the same
        if shared_concept in source_name and shared_concept in target_name:
            return TransferabilityScore.DIRECT
        
        # Check for application relationship
        if 'application' in source_name or 'applied' in target_name:
            return TransferabilityScore.APPLICATION
        
        # Check if foundational
        if any(word in source_name for word in ['basic', 'fundamental', 'introduction']):
            return TransferabilityScore.FOUNDATIONAL
        
        return TransferabilityScore.ANALOGOUS
    
    def _semantic_transferability_analysis(
        self,
        source: GraphNode,
        target: Dict[str, Any],
        source_subject: str,
        target_subject: str
    ) -> CrossSubjectLink:
        """Perform semantic analysis for transferability"""
        # Calculate semantic similarity
        similarity = self._calculate_semantic_similarity(source, target)
        
        if similarity >= 0.8:
            transfer_type = TransferabilityScore.DIRECT
            strength = min(0.95, similarity)
        elif similarity >= 0.6:
            transfer_type = TransferabilityScore.ANALOGOUS
            strength = min(0.85, similarity * 0.9)
        elif similarity >= 0.4:
            transfer_type = TransferabilityScore.APPLICATION
            strength = min(0.75, similarity * 0.8)
        elif similarity >= 0.2:
            transfer_type = TransferabilityScore.RELATED
            strength = min(0.6, similarity * 0.7)
        else:
            return CrossSubjectLink(
                source_concept_id=source.id,
                source_subject_id=source_subject,
                target_concept_id=target.get('id', ''),
                target_subject_id=target_subject,
                transferability=TransferabilityScore.RELATED,
                strength=0.0,
                reasoning="No significant transferability detected",
                shared_principles=[],
                context_differences=[],
                metadata={'detection_method': 'semantic', 'similarity': similarity}
            )
        
        reasoning = self._generate_transfer_reasoning(
            source, target, source_subject, target_subject, similarity
        )
        
        return CrossSubjectLink(
            source_concept_id=source.id,
            source_subject_id=source_subject,
            target_concept_id=target.get('id', ''),
            target_subject_id=target_subject,
            transferability=transfer_type,
            strength=strength,
            reasoning=reasoning,
            shared_principles=self._find_shared_principles(source, target),
            context_differences=self._identify_context_differences(
                source_subject, target_subject, source.name
            ),
            metadata={'detection_method': 'semantic', 'similarity': similarity}
        )
    
    def _calculate_semantic_similarity(
        self,
        source: GraphNode,
        target: Dict[str, Any]
    ) -> float:
        """Calculate semantic similarity between two concepts"""
        score = 0.0
        
        # Name similarity (simplified)
        source_name = source.name.lower()
        target_name = target.get('name', '').lower()
        
        # Check for exact or partial matches
        if source_name == target_name:
            score += 0.4
        elif source_name in target_name or target_name in source_name:
            score += 0.3
        else:
            # Word overlap
            source_words = set(re.findall(r'\w+', source_name))
            target_words = set(re.findall(r'\w+', target_name))
            if source_words and target_words:
                overlap = len(source_words & target_words)
                score += min(0.2, overlap * 0.1)
        
        # Tag overlap
        source_tags = set(source.tags)
        target_tags = set(target.get('tags', []))
        if source_tags and target_tags:
            tag_overlap = len(source_tags & target_tags)
            score += min(0.3, tag_overlap * 0.15)
        
        # Keyword overlap
        source_keywords = set(source.metadata.get('keywords', []))
        target_keywords = set(target.get('keywords', []))
        if source_keywords and target_keywords:
            keyword_overlap = len(source_keywords & target_keywords)
            score += min(0.3, keyword_overlap * 0.15)
        
        return min(1.0, score)
    
    def _generate_transfer_reasoning(
        self,
        source: GraphNode,
        target: Dict[str, Any],
        source_subject: str,
        target_subject: str,
        similarity: float
    ) -> str:
        """Generate human-readable reasoning for transferability"""
        if similarity >= 0.8:
            return f"This concept is directly applicable from {source_subject} to {target_subject}."
        elif similarity >= 0.6:
            return f"Similar concepts exist in both {source_subject} and {target_subject} with analogous applications."
        elif similarity >= 0.4:
            return f"Principles from {source_subject} can be applied in {target_subject} contexts."
        else:
            return f"Related concepts in {source_subject} and {target_subject} may provide complementary perspectives."
    
    def _find_shared_principles(
        self,
        source: GraphNode,
        target: Dict[str, Any]
    ) -> List[str]:
        """Find shared underlying principles between concepts"""
        principles = []
        
        # Extract principles from learning objectives
        source_objectives = source.metadata.get('learning_objectives', [])
        target_objectives = target.get('learning_objectives', [])
        
        # Simple keyword matching for principles
        principle_keywords = ['understand', 'analyze', 'apply', 'solve', 'model', 'calculate']
        
        for objective in source_objectives + target_objectives:
            for keyword in principle_keywords:
                if keyword in objective.lower():
                    if keyword not in principles:
                        principles.append(keyword)
        
        return principles[:5]
    
    def _identify_context_differences(
        self,
        source_subject: str,
        target_subject: str,
        concept: str
    ) -> List[str]:
        """Identify contextual differences for a concept across subjects"""
        differences = []
        
        # Subject-specific contexts
        subject_contexts = {
            'mathematics': 'abstract and theoretical',
            'physics': 'physical and measurable',
            'chemistry': 'molecular and reactive',
            'biology': 'organic and living',
            'computer_science': 'computational and algorithmic',
            'economics': 'resource allocation and market'
        }
        
        source_context = subject_contexts.get(source_subject, 'discipline-specific')
        target_context = subject_contexts.get(target_subject, 'discipline-specific')
        
        if source_context != target_context:
            differences.append(f"In {source_subject}: {source_context} context")
            differences.append(f"In {target_subject}: {target_context} context")
        
        return differences
    
    # =========================================================================
    # Shared Prerequisites Analysis
    # =========================================================================
    
    def find_shared_prerequisites(
        self,
        subject_ids: List[str],
        min_usage: int = 2
    ) -> List[SharedPrerequisite]:
        """
        Find concepts that serve as prerequisites for multiple subjects.
        
        Args:
            subject_ids: List of subject IDs to analyze
            min_usage: Minimum number of subjects using this prerequisite
            
        Returns:
            List of SharedPrerequisite objects
        """
        concept_subjects: Dict[str, Set[str]] = defaultdict(set)
        concept_names: Dict[str, str] = {}
        
        for subject_id in subject_ids:
            concepts = self.graph.get_concepts_by_subject(subject_id)
            
            for concept in concepts:
                concept_id = concept.get('id', '')
                if concept_id:
                    concept_subjects[concept_id].add(subject_id)
                    concept_names[concept_id] = concept.get('name', '')
        
        shared = []
        for concept_id, subjects in concept_subjects.items():
            if len(subjects) >= min_usage:
                # Calculate bridging score
                bridging_score = self._calculate_bridging_score(concept_id, subjects)
                
                shared.append(SharedPrerequisite(
                    concept_id=concept_id,
                    concept_name=concept_names.get(concept_id, concept_id),
                    subjects=list(subjects),
                    usage_count=len(subjects),
                    bridging_score=bridging_score
                ))
        
        # Sort by bridging score
        shared.sort(key=lambda x: x.bridging_score, reverse=True)
        
        return shared
    
    def _calculate_bridging_score(
        self,
        concept_id: str,
        subjects: Set[str]
    ) -> float:
        """Calculate how well a concept bridges subjects"""
        score = 0.0
        
        # Base score from number of subjects
        score += len(subjects) * 0.3
        
        # Check if concept is foundational
        node = self.graph.get_node(concept_id)
        if node:
            # Check if many concepts depend on this
            dependents = self.graph.get_postrequisites(concept_id)
            score += min(0.5, len(dependents) * 0.05)
            
            # Difficulty bonus (foundational concepts often at lower levels)
            difficulty_bonus = {'beginner': 0.2, 'elementary': 0.15, 'intermediate': 0.1}
            score += difficulty_bonus.get(node.difficulty_level, 0)
        
        return min(1.0, score)
    
    # =========================================================================
    # Interdisciplinary Path Generation
    # =========================================================================
    def generate_interdisciplinary_path(
        self,
        start_concept_id: str,
        end_concept_id: str,
        max_concepts: int = 20
    ) -> Optional[InterdisciplinaryPath]:
        """
        Generate a learning path that spans multiple subjects.
        
        Args:
            start_concept_id: Starting concept ID
            end_concept_id: Target concept ID
            max_concepts: Maximum number of concepts in the path
            
        Returns:
            InterdisciplinaryPath or None if not possible
        """
        # Find path in the full graph
        path_result = self.graph.find_learning_path(start_concept_id, end_concept_id)
        
        if not path_result:
            return None
        
        path = path_result.path[:max_concepts]
        if len(path_result.path) > max_concepts:
            logger.warning(f"Path too long, limiting to {max_concepts} concepts")
        
        # Analyze subjects and transitions
        concepts_data = []
        subjects_involved = set()
        transition_points = []
        learning_synergies = []
        
        prev_subject = None
        
        for i, concept_id in enumerate(path):
            node = self.graph.get_node(concept_id)
            if node:
                concepts_data.append(node.to_dict())
                subjects_involved.add(node.subject_id)
                
                # Detect subject transitions
                if prev_subject and prev_subject != node.subject_id:
                    transition_points.append({
                        'at_concept': concept_id,
                        'from_subject': prev_subject,
                        'to_subject': node.subject_id,
                        'transition_order': len(transition_points) + 1
                    })
                    
                    # Identify synergy at transition
                    synergy = self._identify_synergy(prev_subject, node.subject_id)
                    if synergy:
                        learning_synergies.append(synergy)
                
                prev_subject = node.subject_id
        
        # Generate path name
        start_node = self.graph.get_node(start_concept_id)
        end_node = self.graph.get_node(end_concept_id)
        
        if start_node and end_node:
            name = f"Interdisciplinary: {start_node.subject_id} to {end_node.subject_id}"
        else:
            name = f"Interdisciplinary Path: {start_concept_id} to {end_concept_id}"
        
        return InterdisciplinaryPath(
            id=f"idp-{start_concept_id}-{end_concept_id}",
            name=name,
            description=f"Learning path from {start_concept_id} to {end_concept_id} across {len(subjects_involved)} subjects",
            concepts=concepts_data,
            subjects_involved=list(subjects_involved),
            total_duration_minutes=path_result.total_duration,
            transition_points=transition_points,
            learning_synergies=learning_synergies,
            difficulty_progression=path_result.difficulty_progression,
            created_at=datetime.now()
        )
    
    def _identify_synergy(
        self,
        subject_a: str,
        subject_b: str
    ) -> Optional[str]:
        """Identify learning synergy between subjects"""
        subject_pair = tuple(sorted([subject_a, subject_b]))
        
        synergies = {
            ('mathematics', 'physics'): "Physics provides real-world applications for mathematical concepts",
            ('mathematics', 'chemistry'): "Chemistry demonstrates practical applications of mathematical modeling",
            ('physics', 'chemistry'): "Chemistry and physics together explain molecular behavior",
            ('mathematics', 'computer_science'): "Computer science implements mathematical algorithms",
            ('economics', 'mathematics'): "Mathematics provides tools for economic analysis"
        }
        
        return synergies.get(subject_pair)
    
    # =========================================================================
    # Cross-Subject Graph Operations
    # =========================================================================
    
    def find_common_descendants(
        self,
        concept_a_id: str,
        concept_b_id: str
    ) -> Dict[str, List[str]]:
        """
        Find concepts that both input concepts lead to.
        
        Args:
            concept_a_id: First concept ID
            concept_b_id: Second concept ID
            
        Returns:
            Dictionary with common descendants and unique descendants
        """
        descendants_a = set(self.graph.get_postrequisites(concept_a_id))
        descendants_b = set(self.graph.get_postrequisites(concept_b_id))
        
        common = descendants_a & descendants_b
        unique_a = descendants_a - descendants_b
        unique_b = descendants_b - descendants_a
        
        return {
            'common_concepts': sorted(list(common)),
            'unique_to_a': sorted(list(unique_a)),
            'unique_to_b': sorted(list(unique_b)),
            'convergence_point': list(common)[0] if common else None
        }
    
    def find_convergence_point(
        self,
        concept_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Find where multiple concepts converge in the learning path.
        
        Args:
            concept_ids: List of concept IDs to find convergence for
            
        Returns:
            Convergence information or None
        """
        if len(concept_ids) < 2:
            return None
        
        # Get all postrequisites
        all_postreqs: Set[str] = set()
        postreq_sets = []
        
        for concept_id in concept_ids:
            postreqs = set(self.graph.get_postrequisites(concept_id))
            postreq_sets.append(postreqs)
            all_postreqs.update(postreqs)
        
        if not all_postreqs:
            return None
        
        # Find intersection
        intersection = postreq_sets[0]
        for postreq_set in postreq_sets[1:]:
            intersection &= postreq_set
        
        if not intersection:
            return {
                'has_convergence': False,
                'message': 'Concepts do not converge in the learning graph'
            }
        
        # Find earliest convergence (closest to inputs)
        earliest = None
        min_depth = float('inf')
        
        for concept_id in intersection:
            depth = sum(
                len(self.graph.get_prerequisites(concept_id))
                for _ in concept_ids
            )
            if depth < min_depth:
                min_depth = depth
                earliest = concept_id
        
        return {
            'has_convergence': True,
            'convergence_concept_id': earliest,
            'convergence_node': self.graph.get_node(earliest).to_dict() if earliest else None,
            'convergence_depth': min_depth,
            'number_of_converging_paths': len(intersection)
        }
    
    def analyze_subject_bridges(self) -> List[Dict[str, Any]]:
        """
        Analyze all bridges between subjects.
        
        Returns:
            List of subject bridge analyses
        """
        bridges = []
        
        subject_ids = list(self.graph._subject_index.keys())
        
        for i, subject_a in enumerate(subject_ids):
            for subject_b in subject_ids[i + 1:]:
                bridge = self._analyze_subject_pair(subject_a, subject_b)
                if bridge:
                    bridges.append(bridge)
        
        return bridges
    
    def _analyze_subject_pair(
        self,
        subject_a: str,
        subject_b: str
    ) -> Optional[Dict[str, Any]]:
        """Analyze the bridge between two subjects"""
        concepts_a = self.graph.get_concepts_by_subject(subject_a)
        concepts_b = self.graph.get_concepts_by_subject(subject_b)
        
        # Find transferable concepts
        transfers = []
        for concept_a in concepts_a[:20]:  # Limit for performance
            links = self.find_transferable_concepts(
                concept_a.get('id', ''),
                target_subject_id=subject_b,
                min_strength=0.5
            )
            for link in links:
                transfers.append({
                    'from': concept_a.get('name', ''),
                    'to': link.target_concept_id,
                    'type': link.transferability.value,
                    'strength': link.strength
                })
        
        if not transfers:
            return None
        
        return {
            'subject_a': subject_a,
            'subject_b': subject_b,
            'total_bridges': len(transfers),
            'transfer_types': self._count_transfer_types(transfers),
            'strongest_bridges': sorted(
                transfers,
                key=lambda x: x['strength'],
                reverse=True
            )[:5],
            'average_bridge_strength': sum(t['strength'] for t in transfers) / len(transfers)
        }
    
    def _count_transfer_types(self, transfers: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count transfer types"""
        counts = {}
        for transfer in transfers:
            transfer_type = transfer['type']
            counts[transfer_type] = counts.get(transfer_type, 0) + 1
        return counts
    
    # =========================================================================
    # Cache Management
    # =========================================================================
    
    def clear_cache(self) -> None:
        """Clear the link cache"""
        self._cached_links.clear()
        self._semantic_cache.clear()
    
    def refresh_cache(self, concept_ids: Optional[List[str]] = None) -> int:
        """
        Refresh the cache for specific concepts or all.
        
        Args:
            concept_ids: Specific concepts to refresh, or None for all
            
        Returns:
            Number of cache entries refreshed
        """
        refreshed = 0
        
        if concept_ids is None:
            self.clear_cache()
            concept_ids = list(self.graph._nodes.keys())
        
        for concept_id in concept_ids:
            links = self.find_transferable_concepts(concept_id)
            for link in links:
                cache_key = f"{link.source_concept_id}:{link.target_subject_id}"
                self._cached_links[cache_key] = link
                refreshed += 1
        
        return refreshed
