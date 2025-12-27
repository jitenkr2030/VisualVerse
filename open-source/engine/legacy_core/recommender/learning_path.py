"""
Learning Path Recommendation Engine for VisualVerse
Provides personalized learning paths based on dependency graphs and student progress.
"""

import networkx as nx
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import math

from core.schema.base_models import ConceptNode, DifficultyLevel, DependencyGraph

class LearningMode(str, Enum):
    """Different learning path generation modes"""
    SEQUENTIAL = "sequential"  # Linear progression
    BRANCHING = "branching"    # Multiple paths available
    ADAPTIVE = "adaptive"      # Adapts based on performance
    REMEDIAL = "remedial"      # Focuses on weak areas

@dataclass
class StudentProfile:
    """Profile of a student's learning state"""
    user_id: str
    completed_concepts: Set[str]
    current_skill_level: DifficultyLevel
    learning_speed: float  # 0.5 = slow, 1.0 = normal, 2.0 = fast
    preferred_topics: List[str]
    struggling_concepts: Set[str]
    strong_concepts: Set[str]
    
@dataclass
class LearningPath:
    """A generated learning path with metadata"""
    path_id: str
    concepts: List[str]
    estimated_duration: int  # in minutes
    difficulty_progression: List[DifficultyLevel]
    prerequisite_gaps: List[str]
    recommendations: List[str]
    
class LearningPathGenerator:
    """
    Generates personalized learning paths using graph algorithms
    and educational psychology principles.
    """
    
    def __init__(self):
        self.concept_graph = nx.DiGraph()
        self.concept_metadata: Dict[str, ConceptNode] = {}
        
    def load_concept_map(self, concept_map: Dict[str, ConceptNode]):
        """
        Load a concept map and build the dependency graph.
        
        Args:
            concept_map: Dictionary of concept_id -> ConceptNode
        """
        self.concept_metadata = concept_map
        self.concept_graph.clear()
        
        # Add nodes
        for concept_id, concept in concept_map.items():
            self.concept_graph.add_node(
                concept_id,
                difficulty=concept.difficulty,
                estimated_duration=concept.estimated_duration,
                prerequisites=concept.prerequisites
            )
            
        # Add edges for dependencies
        for concept_id, concept in concept_map.items():
            for prereq_id in concept.prerequisites:
                if prereq_id in concept_map:
                    self.concept_graph.add_edge(prereq_id, concept_id)
                    
        print(f"📊 Loaded concept map with {len(concept_map)} concepts")
        
    def generate_path(self, 
                     student_progress: Dict[str, bool], 
                     concept_map: Dict[str, ConceptNode],
                     mode: LearningMode = LearningMode.SEQUENTIAL,
                     max_concepts: int = 10) -> List[str]:
        """
        Generate a personalized learning path for a student.
        
        Args:
            student_progress: {concept_id: completion_status}
            concept_map: Complete concept map for the subject
            mode: Learning mode to use
            max_concepts: Maximum number of concepts in path
            
        Returns:
            List of concept IDs in recommended order
        """
        # Load concept map if not already loaded
        if concept_map != self.concept_metadata:
            self.load_concept_map(concept_map)
            
        # Create student profile
        student_profile = self._create_student_profile(student_progress)
        
        # Generate path based on mode
        if mode == LearningMode.SEQUENTIAL:
            return self._generate_sequential_path(student_profile, max_concepts)
        elif mode == LearningMode.BRANCHING:
            return self._generate_branching_path(student_profile, max_concepts)
        elif mode == LearningMode.ADAPTIVE:
            return self._generate_adaptive_path(student_profile, max_concepts)
        elif mode == LearningMode.REMEDIAL:
            return self._generate_remedial_path(student_profile, max_concepts)
        else:
            return self._generate_sequential_path(student_profile, max_concepts)
            
    def _create_student_profile(self, progress: Dict[str, bool]) -> StudentProfile:
        """Create a student profile from progress data"""
        completed = {cid for cid, completed in progress.items() if completed}
        
        # Calculate skill level based on completed concepts
        if not completed:
            skill_level = DifficultyLevel.BEGINNER
        else:
            completed_difficulties = [
                self.concept_metadata[cid].difficulty 
                for cid in completed if cid in self.concept_metadata
            ]
            
            if completed_difficulties:
                avg_difficulty = sum(
                    {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}[d.value]
                    for d in completed_difficulties
                ) / len(completed_difficulties)
                
                if avg_difficulty <= 1.5:
                    skill_level = DifficultyLevel.BEGINNER
                elif avg_difficulty <= 2.5:
                    skill_level = DifficultyLevel.INTERMEDIATE
                elif avg_difficulty <= 3.5:
                    skill_level = DifficultyLevel.ADVANCED
                else:
                    skill_level = DifficultyLevel.EXPERT
            else:
                skill_level = DifficultyLevel.BEGINNER
                
        return StudentProfile(
            user_id="student_001",  # Would come from auth system
            completed_concepts=completed,
            current_skill_level=skill_level,
            learning_speed=1.0,  # Default, would be learned over time
            preferred_topics=[],  # Would be learned from user behavior
            struggling_concepts=set(),  # Would come from assessment data
            strong_concepts=completed
        )
        
    def _generate_sequential_path(self, student: StudentProfile, max_concepts: int) -> List[str]:
        """Generate a sequential learning path"""
        path = []
        completed = student.completed_concepts
        available_concepts = self._get_available_concepts(completed)
        
        # Sort by difficulty progression and prerequisites
        sorted_concepts = self._sort_by_difficulty_progression(available_concepts, student)
        
        for concept_id in sorted_concepts:
            if len(path) >= max_concepts:
                break
                
            # Check if concept is still available (prerequisites might have been completed)
            if self._is_concept_unlocked(concept_id, completed):
                path.append(concept_id)
                completed.add(concept_id)  # Simulate completion for next iteration
                
        return path
        
    def _generate_branching_path(self, student: StudentProfile, max_concepts: int) -> List[str]:
        """Generate a branching learning path with multiple options"""
        path = []
        completed = student.completed_concepts.copy()
        available_concepts = self._get_available_concepts(completed)
        
        # Group concepts by topic/area
        topic_groups = self._group_concepts_by_topic(available_concepts)
        
        # Select concepts from different topics to provide variety
        concepts_per_topic = max(1, max_concepts // len(topic_groups))
        
        for topic, concepts in topic_groups.items():
            if len(path) >= max_concepts:
                break
                
            # Sort within topic by difficulty
            sorted_concepts = self._sort_by_difficulty_progression(concepts, student)
            
            for concept_id in sorted_concepts[:concepts_per_topic]:
                if len(path) >= max_concepts:
                    break
                    
                if self._is_concept_unlocked(concept_id, completed):
                    path.append(concept_id)
                    completed.add(concept_id)
                    
        return path
        
    def _generate_adaptive_path(self, student: StudentProfile, max_concepts: int) -> List[str]:
        """Generate an adaptive path based on student performance"""
        path = []
        completed = student.completed_concepts.copy()
        
        # Focus on concepts that match current skill level
        target_difficulty = self._get_next_difficulty_level(student.current_skill_level)
        
        for _ in range(max_concepts):
            available = self._get_available_concepts(concepts_to_ignore=completed)
            
            # Filter by target difficulty
            suitable_concepts = [
                cid for cid in available 
                if (cid in self.concept_metadata and 
                    self.concept_metadata[cid].difficulty == target_difficulty)
            ]
            
            if not suitable_concepts:
                # If no exact match, try adjacent difficulty
                suitable_concepts = available
                
            if not suitable_concepts:
                break
                
            # Select concept with best balance of challenge and prerequisite match
            best_concept = self._select_best_concept(suitable_concepts, completed, student)
            
            if best_concept:
                path.append(best_concept)
                completed.add(best_concept)
                
        return path
        
    def _generate_remedial_path(self, student: StudentProfile, max_concepts: int) -> List[str]:
        """Generate a remedial path focusing on weak areas"""
        path = []
        completed = student.completed_concepts.copy()
        
        # Get concepts that build on completed ones but weren't mastered
        weak_areas = self._identify_weak_areas(student)
        
        for weak_concept_id in weak_areas:
            if len(path) >= max_concepts:
                break
                
            # Find prerequisite concepts that might need reinforcement
            prereqs = self.concept_graph.predecessors(weak_concept_id)
            
            for prereq in prereqs:
                if (prereq not in completed and 
                    prereq in self.concept_metadata and
                    len(path) < max_concepts):
                    
                    path.append(prereq)
                    
            # Add the weak concept itself if there's space
            if len(path) < max_concepts and weak_concept_id in self.concept_metadata:
                path.append(weak_concept_id)
                
        return path
        
    def _get_available_concepts(self, completed: Set[str], concepts_to_ignore: Set[str] = None) -> Set[str]:
        """Get concepts that are available for learning (unlocked and not completed)"""
        if concepts_to_ignore is None:
            concepts_to_ignore = set()
            
        available = set()
        
        for concept_id in self.concept_graph.nodes:
            if (concept_id not in completed and 
                concept_id not in concepts_to_ignore and
                self._is_concept_unlocked(concept_id, completed)):
                available.add(concept_id)
                
        return available
        
    def _is_concept_unlocked(self, concept_id: str, completed: Set[str]) -> bool:
        """Check if a concept is unlocked based on completed prerequisites"""
        if concept_id not in self.concept_graph:
            return True  # Concept without dependencies is always unlocked
            
        prerequisites = list(self.concept_graph.predecessors(concept_id))
        return all(prereq in completed for prereq in prerequisites)
        
    def _sort_by_difficulty_progression(self, concepts: Set[str], student: StudentProfile) -> List[str]:
        """Sort concepts by optimal difficulty progression"""
        concept_list = list(concepts)
        
        def difficulty_score(concept_id):
            if concept_id not in self.concept_metadata:
                return 0
                
            concept = self.concept_metadata[concept_id]
            difficulty_value = {
                DifficultyLevel.BEGINNER: 1,
                DifficultyLevel.INTERMEDIATE: 2,
                DifficultyLevel.ADVANCED: 3,
                DifficultyLevel.EXPERT: 4
            }[concept.difficulty]
            
            # Target difficulty is one level above current
            target_difficulty = {
                DifficultyLevel.BEGINNER: 2,
                DifficultyLevel.INTERMEDIATE: 2,
                DifficultyLevel.ADVANCED: 3,
                DifficultyLevel.EXPERT: 4
            }[student.current_skill_level]
            
            # Prefer concepts at target difficulty
            difficulty_proximity = 1 / (1 + abs(difficulty_value - target_difficulty))
            
            # Consider learning speed
            speed_factor = 1 / student.learning_speed
            
            return difficulty_proximity * speed_factor
            
        return sorted(concept_list, key=difficulty_score, reverse=True)
        
    def _group_concepts_by_topic(self, concepts: Set[str]) -> Dict[str, Set[str]]:
        """Group concepts by topic/tag"""
        topics = {}
        
        for concept_id in concepts:
            if concept_id in self.concept_metadata:
                concept = self.concept_metadata[concept_id]
                
                # Use tags to group, or fall back to metadata
                if concept.tags:
                    for tag in concept.tags:
                        if tag not in topics:
                            topics[tag] = set()
                        topics[tag].add(concept_id)
                else:
                    # Use subject area from metadata
                    subject_area = concept.metadata.get("subject_area", "general")
                    if subject_area not in topics:
                        topics[subject_area] = set()
                    topics[subject_area].add(concept_id)
                    
        return topics
        
    def _get_next_difficulty_level(self, current: DifficultyLevel) -> DifficultyLevel:
        """Get the next appropriate difficulty level"""
        level_progression = {
            DifficultyLevel.BEGINNER: DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.INTERMEDIATE: DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.ADVANCED: DifficultyLevel.ADVANCED,
            DifficultyLevel.EXPERT: DifficultyLevel.EXPERT
        }
        return level_progression.get(current, DifficultyLevel.INTERMEDIATE)
        
    def _select_best_concept(self, concepts: List[str], completed: Set[str], student: StudentProfile) -> Optional[str]:
        """Select the best concept from available options"""
        best_concept = None
        best_score = -1
        
        for concept_id in concepts:
            if concept_id not in self.concept_metadata:
                continue
                
            concept = self.concept_metadata[concept_id]
            
            # Calculate relevance score
            score = 1.0
            
            # Prefer concepts matching preferred topics
            if concept.tags and student.preferred_topics:
                overlap = len(set(concept.tags) & set(student.preferred_topics))
                score *= (1 + overlap * 0.2)
                
            # Consider estimated duration vs student learning speed
            duration_factor = min(1.0, 30 / max(concept.estimated_duration, 1))
            score *= duration_factor
            
            if score > best_score:
                best_score = score
                best_concept = concept_id
                
        return best_concept
        
    def _identify_weak_areas(self, student: StudentProfile) -> List[str]:
        """Identify concepts that the student struggled with"""
        # This would typically come from assessment data
        # For now, we'll identify concepts with many prerequisites that aren't completed
        
        weak_areas = []
        for concept_id, concept in self.concept_metadata.items():
            if concept_id not in student.completed_concepts:
                # Check if this concept depends on many uncompleted concepts
                uncompleted_deps = [
                    dep for dep in concept.prerequisites 
                    if dep not in student.completed_concepts
                ]
                
                if len(uncompleted_deps) > 2:  # Threshold for being a "weak area"
                    weak_areas.append(concept_id)
                    
        return weak_areas
        
    def get_learning_analytics(self, path: List[str]) -> Dict[str, Any]:
        """Get analytics for a generated learning path"""
        if not path:
            return {}
            
        total_duration = sum(
            self.concept_metadata.get(cid, ConceptNode(estimated_duration=30)).estimated_duration
            for cid in path
        )
        
        difficulties = [
            self.concept_metadata.get(cid, ConceptNode(difficulty=DifficultyLevel.BEGINNER)).difficulty
            for cid in path
        ]
        
        return {
            "total_concepts": len(path),
            "estimated_duration_minutes": total_duration,
            "difficulty_progression": [d.value for d in difficulties],
            "difficulty_distribution": {
                d.value: difficulties.count(d) for d in set(difficulties)
            },
            "prerequisite_gaps": self._find_prerequisite_gaps(path),
            "learning_velocity": len(path) / max(total_duration / 30, 1)  # concepts per 30 minutes
        }
        
    def _find_prerequisite_gaps(self, path: List[str]) -> List[str]:
        """Find prerequisite concepts that aren't in the path"""
        gaps = []
        for concept_id in path:
            if concept_id in self.concept_metadata:
                prereqs = self.concept_metadata[concept_id].prerequisites
                for prereq in prereqs:
                    if prereq not in path:
                        gaps.append(prereq)
        return gaps