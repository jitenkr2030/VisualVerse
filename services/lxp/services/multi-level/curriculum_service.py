"""
Learner Experience Platform - Curriculum Service

This module provides curriculum hierarchy and learning path management
for the VisualVerse Learner Experience Platform.

Author: MiniMax Agent
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import json
import logging
import threading


logger = logging.getLogger(__name__)


class EducationLevel(str, Enum):
    """Education levels supported by the platform."""
    K12_PRIMARY = "K12_Primary"
    K12_MIDDLE = "K12_Middle"
    K12_SECONDARY = "K12_Secondary"
    K12_HIGHER_SECONDARY = "K12_HigherSecondary"
    COLLEGE_UNDERGRADUATE = "College_Undergraduate"
    COLLEGE_GRADUATE = "College_Graduate"
    PROFESSIONAL = "Professional"
    CORPORATE_TRAINING = "Corporate_Training"


class SubjectArea(str, Enum):
    """Subject areas for curriculum organization."""
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    ECONOMICS = "economics"
    FINANCE = "finance"
    GENERAL = "general"


class NodeType(str, Enum):
    """Types of curriculum nodes."""
    DOMAIN = "domain"
    SUBJECT = "subject"
    TOPIC = "topic"
    CONCEPT = "concept"
    LEARNING_OBJECT = "learning_object"
    ASSESSMENT = "assessment"


class DifficultyLevel(str, Enum):
    """Difficulty levels for learning content."""
    FOUNDATIONAL = "foundational"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class CurriculumNode:
    """
    A node in the curriculum hierarchy.
    
    Attributes:
        id: Unique node identifier
        type: Type of node
        name: Node name
        description: Node description
        code: Standard code (e.g., MATH-101)
        parent_id: Parent node ID
        children: List of child node IDs
        order: Display order
        metadata: Additional node data
        difficulty: Difficulty level
        estimated_hours: Estimated learning hours
        prerequisites: List of prerequisite node IDs
        learning_objectives: Learning objectives
        tags: Associated tags
        is_optional: Whether node is optional
        is_locked: Whether node is locked (prerequisites not met)
    """
    id: str
    type: str
    name: str
    description: str = ""
    code: str = ""
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    difficulty: str = DifficultyLevel.DEVELOPING.value
    estimated_hours: float = 1.0
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    is_optional: bool = False
    is_locked: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "code": self.code,
            "parentId": self.parent_id,
            "children": self.children,
            "order": self.order,
            "metadata": self.metadata,
            "difficulty": self.difficulty,
            "estimatedHours": self.estimated_hours,
            "prerequisites": self.prerequisites,
            "learningObjectives": self.learning_objectives,
            "tags": self.tags,
            "isOptional": self.is_optional,
            "isLocked": self.is_locked,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    @property
    def is_leaf(self) -> bool:
        """Check if node is a leaf (no children)."""
        return len(self.children) == 0
    
    @property
    def depth(self) -> int:
        """Get the depth of this node in the hierarchy."""
        return len(self.code.split('-')) if self.code else 0


@dataclass
class CurriculumTree:
    """
    Complete curriculum tree for an education level.
    
    Attributes:
        id: Unique tree identifier
        name: Tree name
        education_level: Associated education level
        root_nodes: List of root node IDs
        nodes: Dictionary of all nodes
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: str
    name: str
    education_level: str
    root_nodes: List[str] = field(default_factory=list)
    nodes: Dict[str, CurriculumNode] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "educationLevel": self.education_level,
            "rootNodes": self.root_nodes,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }
    
    def get_node(self, node_id: str) -> Optional[CurriculumNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_children(self, node_id: str) -> List[CurriculumNode]:
        """Get children of a node."""
        node = self.nodes.get(node_id)
        if not node:
            return []
        return [self.nodes[child_id] for child_id in node.children if child_id in self.nodes]
    
    def get_path(self, node_id: str) -> List[CurriculumNode]:
        """Get the path from root to a node."""
        path = []
        current = self.nodes.get(node_id)
        while current:
            path.insert(0, current)
            if current.parent_id:
                current = self.nodes.get(current.parent_id)
            else:
                current = None
        return path
    
    def get_leaves(self) -> List[CurriculumNode]:
        """Get all leaf nodes."""
        return [node for node in self.nodes.values() if node.is_leaf]
    
    def get_nodes_by_type(self, node_type: str) -> List[CurriculumNode]:
        """Get all nodes of a specific type."""
        return [node for node in self.nodes.values() if node.type == node_type]
    
    def validate_prerequisites(self, completed_ids: List[str]) -> Tuple[List[str], List[str]]:
        """
        Validate prerequisites against completed nodes.
        
        Args:
            completed_ids: List of completed node IDs
            
        Returns:
            Tuple of (missing_prerequisites, unlocked_nodes)
        """
        missing = []
        unlocked = []
        
        for node in self.nodes.values():
            if node.id in completed_ids:
                continue
            
            # Check if all prerequisites are met
            prereqs_met = all(prereq in completed_ids for prereq in node.prerequisites)
            
            if not prereqs_met and node.prerequisites:
                missing.append(node.id)
            elif prereqs_met or not node.prerequisites:
                unlocked.append(node.id)
        
        return missing, unlocked


@dataclass
class LearningModule:
    """
    A learning module containing multiple curriculum nodes.
    
    Attributes:
        id: Unique module identifier
        name: Module name
        description: Module description
        nodes: List of node IDs in this module
        estimated_duration: Estimated duration in hours
        order: Display order
        is_completed: Whether module is completed
        progress: Current progress percentage
    """
    id: str
    name: str
    description: str = ""
    nodes: List[str] = field(default_factory=list)
    estimated_duration: float = 2.0
    order: int = 0
    is_completed: bool = False
    progress: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "nodes": self.nodes,
            "estimatedDuration": self.estimated_duration,
            "order": self.order,
            "isCompleted": self.is_completed,
            "progress": self.progress
        }


class CurriculumService:
    """
    Service for managing curriculum hierarchies and learning paths.
    
    This service provides:
    - Curriculum tree management
    - Node CRUD operations
    - Prerequisite validation
    - Learning path generation
    - Progress tracking against curriculum
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the curriculum service.
        
        Args:
            storage_dir: Directory for persisting data
        """
        self.storage_dir = storage_dir or "/tmp/visualverse-lxp/curriculum"
        
        self.trees: Dict[str, CurriculumTree] = {}
        self.modules: Dict[str, LearningModule] = {}
        
        self.lock = threading.RLock()
        
        # Load existing data
        self._load_state()
        
        # Initialize default curricula if none exist
        if not self.trees:
            self._initialize_default_curricula()
        
        logger.info("CurriculumService initialized")
    
    def _load_state(self):
        """Load persisted state."""
        import os
        os.makedirs(self.storage_dir, exist_ok=True)
        
        trees_file = f"{self.storage_dir}/curriculum_trees.json"
        modules_file = f"{self.storage_dir}/learning_modules.json"
        
        if os.path.exists(trees_file):
            try:
                with open(trees_file, 'r') as f:
                    data = json.load(f)
                    self.trees = {
                        tid: CurriculumTree(**tree) 
                        for tid, tree in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load curriculum trees: {e}")
        
        if os.path.exists(modules_file):
            try:
                with open(modules_file, 'r') as f:
                    data = json.load(f)
                    self.modules = {
                        mid: LearningModule(**module) 
                        for mid, module in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load learning modules: {e}")
    
    def _save_state(self):
        """Persist state to storage."""
        import os
        from pathlib import Path
        
        Path(self.storage_dir).mkdir(parents=True, exist_ok=True)
        
        trees_file = f"{self.storage_dir}/curriculum_trees.json"
        modules_file = f"{self.storage_dir}/learning_modules.json"
        
        with open(trees_file, 'w') as f:
            json.dump(
                {tid: tree.to_dict() for tid, tree in self.trees.items()},
                f, indent=2
            )
        
        with open(modules_file, 'w') as f:
            json.dump(
                {mid: module.to_dict() for mid, module in self.modules.items()},
                f, indent=2
            )
    
    def _initialize_default_curricula(self):
        """Initialize default curriculum trees for each education level."""
        # K12 Secondary Curriculum (Grades 9-10)
        secondary_tree = CurriculumTree(
            id="curriculum-k12-secondary",
            name="K-12 Secondary Curriculum",
            education_level=EducationLevel.K12_SECONDARY.value
        )
        
        # Mathematics Domain
        math_domain = CurriculumNode(
            id="math-domain",
            type=NodeType.DOMAIN.value,
            name="Mathematics",
            code="MATH",
            order=0
        )
        secondary_tree.nodes[math_domain.id] = math_domain
        secondary_tree.root_nodes.append(math_domain.id)
        
        # Math Topics
        algebra = CurriculumNode(
            id="math-algebra",
            type=NodeType.TOPIC.value,
            name="Algebra",
            code="MATH-ALG",
            parent_id=math_domain.id,
            order=0
        )
        secondary_tree.nodes[algebra.id] = algebra
        
        linear_equations = CurriculumNode(
            id="math-linear-equations",
            type=NodeType.CONCEPT.value,
            name="Linear Equations",
            code="MATH-ALG-001",
            parent_id=algebra.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=2.0,
            learning_objectives=[
                "Solve linear equations in one variable",
                "Solve linear equations in two variables",
                "Graph linear equations"
            ]
        )
        secondary_tree.nodes[linear_equations.id] = linear_equations
        algebra.children.append(linear_equations.id)
        
        quadratic = CurriculumNode(
            id="math-quadratic",
            type=NodeType.CONCEPT.value,
            name="Quadratic Equations",
            code="MATH-ALG-002",
            parent_id=algebra.id,
            difficulty=DifficultyLevel.PROFICIENT.value,
            estimated_hours=3.0,
            prerequisites=[linear_equations.id],
            learning_objectives=[
                "Solve quadratic equations by factoring",
                "Solve quadratic equations using formula",
                "Understand discriminant"
            ]
        )
        secondary_tree.nodes[quadratic.id] = quadratic
        algebra.children.append(quadratic.id)
        
        geometry = CurriculumNode(
            id="math-geometry",
            type=NodeType.TOPIC.value,
            name="Geometry",
            code="MATH-GEOM",
            parent_id=math_domain.id,
            order=1
        )
        secondary_tree.nodes[geometry.id] = geometry
        
        triangles = CurriculumNode(
            id="math-triangles",
            type=NodeType.CONCEPT.value,
            name="Triangles and Properties",
            code="MATH-GEOM-001",
            parent_id=geometry.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=2.5
        )
        secondary_tree.nodes[triangles.id] = triangles
        geometry.children.append(triangles.id)
        
        # Physics Domain
        physics_domain = CurriculumNode(
            id="physics-domain",
            type=NodeType.DOMAIN.value,
            name="Physics",
            code="PHY",
            order=1
        )
        secondary_tree.nodes[physics_domain.id] = physics_domain
        secondary_tree.root_nodes.append(physics_domain.id)
        
        kinematics = CurriculumNode(
            id="physics-kinematics",
            type=NodeType.TOPIC.value,
            name="Kinematics",
            code="PHY-KIN",
            parent_id=physics_domain.id,
            order=0
        )
        secondary_tree.nodes[kinematics.id] = kinematics
        
        motion_1d = CurriculumNode(
            id="physics-motion-1d",
            type=NodeType.CONCEPT.value,
            name="Motion in One Dimension",
            code="PHY-KIN-001",
            parent_id=kinematics.id,
            difficulty=DifficultyLevel.FOUNDATIONAL.value,
            estimated_hours=2.0,
            learning_objectives=[
                "Understand distance and displacement",
                "Calculate velocity and acceleration",
                "Interpret motion graphs"
            ]
        )
        secondary_tree.nodes[motion_1d.id] = motion_1d
        kinematics.children.append(motion_1d.id)
        
        projectile = CurriculumNode(
            id="physics-projectile",
            type=NodeType.CONCEPT.value,
            name="Projectile Motion",
            code="PHY-KIN-002",
            parent_id=kinematics.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=2.5,
            prerequisites=[motion_1d.id],
            learning_objectives=[
                "Analyze projectile motion",
                "Calculate range and maximum height",
                "Understand independence of motions"
            ]
        )
        secondary_tree.nodes[projectile.id] = projectile
        kinematics.children.append(projectile.id)
        
        dynamics = CurriculumNode(
            id="physics-dynamics",
            type=NodeType.TOPIC.value,
            name="Dynamics",
            code="PHY-DYN",
            parent_id=physics_domain.id,
            order=1
        )
        secondary_tree.nodes[dynamics.id] = dynamics
        
        newton = CurriculumNode(
            id="physics-newton",
            type=NodeType.CONCEPT.value,
            name="Newton's Laws of Motion",
            code="PHY-DYN-001",
            parent_id=dynamics.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=3.0,
            learning_objectives=[
                "Understand Newton's three laws",
                "Apply laws to solve problems",
                "Understand action-reaction pairs"
            ]
        )
        secondary_tree.nodes[newton.id] = newton
        dynamics.children.append(newton.id)
        
        self.trees[secondary_tree.id] = secondary_tree
        
        # Higher Secondary Curriculum (Grades 11-12)
        higher_secondary = CurriculumTree(
            id="curriculum-k12-higher-secondary",
            name="K-12 Higher Secondary Curriculum",
            education_level=EducationLevel.K12_HIGHER_SECONDARY.value
        )
        
        # Add advanced topics
        calculus = CurriculumNode(
            id="hs-calculus",
            type=NodeType.TOPIC.value,
            name="Calculus",
            code="MATH-CALC",
            order=0
        )
        higher_secondary.nodes[calculus.id] = calculus
        higher_secondary.root_nodes.append(calculus.id)
        
        limits = CurriculumNode(
            id="hs-limits",
            type=NodeType.CONCEPT.value,
            name="Limits and Continuity",
            code="MATH-CALC-001",
            parent_id=calculus.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=3.0
        )
        higher_secondary.nodes[limits.id] = limits
        calculus.children.append(limits.id)
        
        differentiation = CurriculumNode(
            id="hs-differentiation",
            type=NodeType.CONCEPT.value,
            name="Differentiation",
            code="MATH-CALC-002",
            parent_id=calculus.id,
            difficulty=DifficultyLevel.PROFICIENT.value,
            prerequisites=[limits.id],
            estimated_hours=4.0
        )
        higher_secondary.nodes[differentiation.id] = differentiation
        calculus.children.append(differentiation.id)
        
        self.trees[higher_secondary.id] = higher_secondary
        
        # College Undergraduate Curriculum
        undergraduate = CurriculumTree(
            id="curriculum-college-undergraduate",
            name="College Undergraduate Curriculum",
            education_level=EducationLevel.COLLEGE_UNDERGRADUATE.value
        )
        
        cs_domain = CurriculumNode(
            id="cs-domain",
            type=NodeType.DOMAIN.value,
            name="Computer Science",
            code="CS",
            order=0
        )
        undergraduate.nodes[cs_domain.id] = cs_domain
        undergraduate.root_nodes.append(cs_domain.id)
        
        algorithms = CurriculumNode(
            id="cs-algorithms",
            type=NodeType.TOPIC.value,
            name="Algorithms",
            code="CS-ALG",
            parent_id=cs_domain.id,
            order=0
        )
        undergraduate.nodes[algorithms.id] = algorithms
        
        sorting = CurriculumNode(
            id="cs-sorting",
            type=NodeType.CONCEPT.value,
            name="Sorting Algorithms",
            code="CS-ALG-001",
            parent_id=algorithms.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=4.0
        )
        undergraduate.nodes[sorting.id] = sorting
        algorithms.children.append(sorting.id)
        
        searching = CurriculumNode(
            id="cs-searching",
            type=NodeType.CONCEPT.value,
            name="Searching Algorithms",
            code="CS-ALG-002",
            parent_id=algorithms.id,
            difficulty=DifficultyLevel.DEVELOPING.value,
            estimated_hours=3.0
        )
        undergraduate.nodes[searching.id] = searching
        algorithms.children.append(searching.id)
        
        self.trees[undergraduate.id] = undergraduate
        
        self._save_state()
        
        logger.info("Default curricula initialized")
    
    # Curriculum Tree Management
    def get_tree(self, tree_id: str) -> Optional[CurriculumTree]:
        """
        Get a curriculum tree by ID.
        
        Args:
            tree_id: Tree identifier
            
        Returns:
            CurriculumTree or None if not found
        """
        return self.trees.get(tree_id)
    
    def get_tree_by_level(self, education_level: str) -> Optional[CurriculumTree]:
        """
        Get curriculum tree for an education level.
        
        Args:
            education_level: Education level
            
        Returns:
            CurriculumTree or None if not found
        """
        for tree in self.trees.values():
            if tree.education_level == education_level:
                return tree
        return None
    
    def list_trees(self) -> List[CurriculumTree]:
        """List all curriculum trees."""
        return list(self.trees.values())
    
    # Node Management
    def add_node(self, tree_id: str, node: CurriculumNode) -> CurriculumNode:
        """
        Add a node to a curriculum tree.
        
        Args:
            tree_id: Tree identifier
            node: Node to add
            
        Returns:
            Added node
        """
        with self.lock:
            if tree_id not in self.trees:
                raise ValueError(f"Tree not found: {tree_id}")
            
            tree = self.trees[tree_id]
            tree.nodes[node.id] = node
            tree.updated_at = datetime.utcnow()
            
            # Add to parent's children list
            if node.parent_id and node.parent_id in tree.nodes:
                tree.nodes[node.parent_id].children.append(node.id)
            
            self._save_state()
            
            logger.info(f"Node added: {node.id} to tree {tree_id}")
            return node
    
    def update_node(self, tree_id: str, node_id: str, 
                   **updates) -> Optional[CurriculumNode]:
        """
        Update a node in a curriculum tree.
        
        Args:
            tree_id: Tree identifier
            node_id: Node to update
            **updates: Fields to update
            
        Returns:
            Updated node or None if not found
        """
        with self.lock:
            if tree_id not in self.trees:
                return None
            
            tree = self.trees[tree_id]
            if node_id not in tree.nodes:
                return None
            
            node = tree.nodes[node_id]
            
            for field, value in updates.items():
                if hasattr(node, field) and field not in ["id"]:
                    setattr(node, field, value)
            
            node.updated_at = datetime.utcnow()
            self._save_state()
            
            return node
    
    def get_node(self, tree_id: str, node_id: str) -> Optional[CurriculumNode]:
        """
        Get a specific node from a tree.
        
        Args:
            tree_id: Tree identifier
            node_id: Node identifier
            
        Returns:
            CurriculumNode or None if not found
        """
        tree = self.trees.get(tree_id)
        if tree:
            return tree.get_node(node_id)
        return None
    
    def get_node_path(self, tree_id: str, node_id: str) -> List[CurriculumNode]:
        """
        Get the path from root to a node.
        
        Args:
            tree_id: Tree identifier
            node_id: Node identifier
            
        Returns:
            List of nodes from root to the specified node
        """
        tree = self.trees.get(tree_id)
        if tree:
            return tree.get_path(node_id)
        return []
    
    # Learning Path Generation
    def generate_learning_path(self, tree_id: str, 
                              completed_ids: List[str],
                              target_node_id: str = None) -> List[CurriculumNode]:
        """
        Generate a learning path based on completed nodes.
        
        Args:
            tree_id: Curriculum tree identifier
            completed_ids: List of completed node IDs
            target_node_id: Optional target node to reach
            
        Returns:
            List of nodes in learning order
        """
        tree = self.trees.get(tree_id)
        if not tree:
            return []
        
        path = []
        
        # Get all incomplete nodes
        incomplete_nodes = [
            node for node in tree.nodes.values()
            if node.id not in completed_ids
        ]
        
        # Sort by prerequisites and order
        def sort_key(node):
            # Count uncompleted prerequisites
            prereq_count = sum(
                1 for prereq in node.prerequisites
                if prereq not in completed_ids
            )
            return (prereq_count, node.order)
        
        incomplete_nodes.sort(key=sort_key)
        
        # Build path respecting dependencies
        for node in incomplete_nodes:
            # Check if prerequisites are met
            prereqs_met = all(
                prereq in completed_ids or prereq in path
                for prereq in node.prerequisites
            )
            
            if prereqs_met:
                path.append(node)
        
        return path
    
    def get_recommended_sequence(self, tree_id: str, 
                                 completed_ids: List[str],
                                 limit: int = 5) -> List[CurriculumNode]:
        """
        Get recommended next content sequence.
        
        Args:
            tree_id: Curriculum tree identifier
            completed_ids: Already completed node IDs
            limit: Maximum items to return
            
        Returns:
            List of recommended nodes
        """
        path = self.generate_learning_path(tree_id, completed_ids)
        return path[:limit]
    
    def check_prerequisites(self, tree_id: str, node_id: str,
                           completed_ids: List[str]) -> Tuple[bool, List[str]]:
        """
        Check if prerequisites are met for a node.
        
        Args:
            tree_id: Curriculum tree identifier
            node_id: Node to check
            completed_ids: List of completed node IDs
            
        Returns:
            Tuple of (all_met, missing_prerequisites)
        """
        tree = self.trees.get(tree_id)
        if not tree:
            return False, [node_id]
        
        node = tree.nodes.get(node_id)
        if not node:
            return False, [node_id]
        
        missing = [p for p in node.prerequisites if p not in completed_ids]
        return len(missing) == 0, missing
    
    # Progress Tracking
    def calculate_progress(self, tree_id: str, 
                          completed_ids: List[str]) -> Dict[str, Any]:
        """
        Calculate progress against a curriculum tree.
        
        Args:
            tree_id: Curriculum tree identifier
            completed_ids: List of completed node IDs
            
        Returns:
            Progress statistics
        """
        tree = self.trees.get(tree_id)
        if not tree:
            return {"error": "Tree not found"}
        
        total_nodes = len(tree.nodes)
        completed = len([n for n in tree.nodes.values() if n.id in completed_ids])
        
        # Calculate by domain
        by_domain = {}
        for node in tree.nodes.values():
            domain = node.code.split('-')[0] if node.code else node.type
            if domain not in by_domain:
                by_domain[domain] = {"total": 0, "completed": 0}
            by_domain[domain]["total"] += 1
            if node.id in completed_ids:
                by_domain[domain]["completed"] += 1
        
        return {
            "totalNodes": total_nodes,
            "completedNodes": completed,
            "progressPercentage": (completed / total_nodes * 100) if total_nodes > 0 else 0,
            "byDomain": by_domain
        }
    
    def get_next_steps(self, tree_id: str, completed_ids: List[str],
                      limit: int = 3) -> List[CurriculumNode]:
        """
        Get recommended next steps for learning.
        
        Args:
            tree_id: Curriculum tree identifier
            completed_ids: Completed node IDs
            limit: Maximum items to return
            
        Returns:
            List of recommended next nodes
        """
        path = self.generate_learning_path(tree_id, completed_ids)
        return path[:limit]
    
    # Module Management
    def create_module(self, name: str, description: str = "",
                     node_ids: List[str] = None,
                     estimated_duration: float = 2.0) -> LearningModule:
        """
        Create a learning module.
        
        Args:
            name: Module name
            description: Module description
            node_ids: List of node IDs in this module
            estimated_duration: Estimated duration in hours
            
        Returns:
            Created LearningModule
        """
        import uuid
        
        module = LearningModule(
            id=f"module-{uuid.uuid4().hex[:12]}",
            name=name,
            description=description,
            nodes=node_ids or [],
            estimated_duration=estimated_duration
        )
        
        self.modules[module.id] = module
        self._save_state()
        
        return module
    
    def get_module(self, module_id: str) -> Optional[LearningModule]:
        """Get a learning module by ID."""
        return self.modules.get(module_id)
    
    def get_modules_for_tree(self, tree_id: str) -> List[LearningModule]:
        """Get all modules for a curriculum tree."""
        tree = self.trees.get(tree_id)
        if not tree:
            return []
        
        # Find modules that contain nodes from this tree
        tree_node_ids = set(tree.nodes.keys())
        return [
            m for m in self.modules.values()
            if any(nid in tree_node_ids for nid in m.nodes)
        ]


# Thread lock for thread-safe operations
CurriculumService.lock = __import__('threading').RLock()


def create_curriculum_service(storage_dir: str = None) -> CurriculumService:
    """
    Create and return the global curriculum service.
    
    Args:
        storage_dir: Optional storage directory
        
    Returns:
        CurriculumService instance
    """
    return CurriculumService(storage_dir)


__all__ = [
    "EducationLevel",
    "SubjectArea",
    "NodeType",
    "DifficultyLevel",
    "CurriculumNode",
    "CurriculumTree",
    "LearningModule",
    "CurriculumService",
    "create_curriculum_service"
]
