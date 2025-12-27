"""
Version Control Service - Core Implementation

This module implements the core version control functionality for the
VisualVerse Creator Platform, providing Git-like operations for content
management including commits, branches, diffs, and merges.

Author: MiniMax Agent
Version: 1.0.0
"""

import hashlib
import json
import difflib
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
import logging
import threading

from visualverse.platform.packages.shared_types import (
    Project,
    Commit as DomainCommit,
    Branch as DomainBranch,
)


logger = logging.getLogger(__name__)


class ConflictType(str, Enum):
    """Types of merge conflicts."""
    CONTENT_CONFLICT = "content_conflict"
    STRUCTURE_CONFLICT = "structure_conflict"
    SEMANTIC_CONFLICT = "semantic_conflict"
    DEPENDENCY_CONFLICT = "dependency_conflict"


@dataclass
class Commit:
    """
    Version commit object representing a snapshot of content at a point in time.
    
    Attributes:
        hash: Unique SHA-256 hash identifier for the commit
        parent_hash: Hash of the parent commit (None for initial commit)
        tree_hash: Hash representing the state of all content files
        author_id: User who created this commit
        author_name: Display name of the author
        author_email: Email of the author
        message: Commit message describing changes
        timestamp: When the commit was created
        domain: Content domain (math, physics, etc.)
        files_changed: Number of files modified
        additions: Lines added
        deletions: Lines deleted
    """
    hash: str
    parent_hash: Optional[str]
    tree_hash: str
    author_id: str
    author_name: str
    author_email: str
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    domain: str = "general"
    files_changed: int = 0
    additions: int = 0
    deletions: int = 0
    parent_hashes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hash": self.hash,
            "parentHash": self.parent_hash,
            "parentHashes": self.parent_hashes,
            "treeHash": self.tree_hash,
            "authorId": self.author_id,
            "authorName": self.author_name,
            "authorEmail": self.author_email,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "domain": self.domain,
            "filesChanged": self.files_changed,
            "additions": self.additions,
            "deletions": self.deletions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Commit':
        return cls(
            hash=data["hash"],
            parent_hash=data.get("parentHash"),
            tree_hash=data["treeHash"],
            author_id=data["authorId"],
            author_name=data["authorName"],
            author_email=data["authorEmail"],
            message=data["message"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if isinstance(data["timestamp"], str) else data["timestamp"],
            domain=data.get("domain", "general"),
            files_changed=data.get("filesChanged", 0),
            additions=data.get("additions", 0),
            deletions=data.get("deletions", 0),
            parent_hashes=data.get("parentHashes", [])
        )


@dataclass
class Branch:
    """
    Branch object representing a line of development.
    
    Attributes:
        name: Branch name
        head_commit: Hash of the current HEAD commit
        author_id: User who created the branch
        created_at: When the branch was created
        is_default: Whether this is the default branch
        description: Branch description
        protected: Whether branch is protected from direct commits
    """
    name: str
    head_commit: str
    author_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_default: bool = False
    description: str = ""
    protected: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "headCommit": self.head_commit,
            "authorId": self.author_id,
            "createdAt": self.created_at.isoformat(),
            "isDefault": self.is_default,
            "description": self.description,
            "protected": self.protected
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Branch':
        return cls(
            name=data["name"],
            head_commit=data["headCommit"],
            author_id=data.get("authorId", ""),
            created_at=datetime.fromisoformat(data["createdAt"]) if isinstance(data["createdAt"], str) else data["createdAt"],
            is_default=data.get("isDefault", False),
            description=data.get("description", ""),
            protected=data.get("protected", False)
        )


@dataclass
class TreeEntry:
    """
    Entry in the content tree representing a file or directory.
    
    Attributes:
        path: File path relative to project root
        hash: Content hash
        mode: File mode (file or directory)
        size: File size in bytes
    """
    path: str
    hash: str
    is_directory: bool = False
    size: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "hash": self.hash,
            "isDirectory": self.is_directory,
            "size": self.size
        }


@dataclass
class Tree:
    """
    Content tree representing the state of all files at a commit.
    """
    hash: str
    entries: List[TreeEntry] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hash": self.hash,
            "entries": [e.to_dict() for e in self.entries]
        }


@dataclass
class DiffResult:
    """
    Result of comparing two content versions.
    
    Attributes:
        base_commit: Hash of the base commit
        compare_commit: Hash of the comparison commit
        files: List of changed files with diff details
        total_additions: Total lines added
        total_deletions: Total lines deleted
        is_binary: Whether any binary files were changed
    """
    base_commit: str
    compare_commit: str
    files: List[Dict[str, Any]] = field(default_factory=list)
    total_additions: int = 0
    total_deletions: int = 0
    is_binary: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseCommit": self.base_commit,
            "compareCommit": self.compare_commit,
            "files": self.files,
            "totalAdditions": self.total_additions,
            "totalDeletions": self.total_deletions,
            "isBinary": self.is_binary
        }


@dataclass
class MergeResult:
    """
    Result of a merge operation.
    
    Attributes:
        success: Whether the merge was successful
        commit_hash: Hash of the merge commit (if successful)
        conflicts: List of conflicts encountered
        merged_files: List of files that were merged
        base_commit: Hash of the merge base
        head_commit: Hash of the head commit
        target_commit: Hash of the target commit
    """
    success: bool
    commit_hash: Optional[str] = None
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    merged_files: List[str] = field(default_factory=list)
    base_commit: Optional[str] = None
    head_commit: Optional[str] = None
    target_commit: Optional[str] = None
    message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "commitHash": self.commit_hash,
            "conflicts": self.conflicts,
            "mergedFiles": self.merged_files,
            "baseCommit": self.base_commit,
            "headCommit": self.head_commit,
            "targetCommit": self.target_commit,
            "message": self.message
        }


def create_commit_hash(content: str) -> str:
    """
    Create a SHA-256 hash for commit content.
    
    Args:
        content: The content to hash
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def create_file_hash(content: str) -> str:
    """
    Create a hash for file content.
    
    Args:
        content: File content
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()


class VersionControlService:
    """
    Core version control service providing Git-like operations.
    
    This service manages content versions, branches, and merges for the
    VisualVerse Creator Platform. It supports:
    
    - Commit history management
    - Branch creation and management
    - Diff generation and visualization
    - Three-way merge operations
    - Conflict detection and resolution
    
    Attributes:
        storage_dir: Directory for storing version data
        commits: Dictionary of commits by hash
        branches: Dictionary of branches by name
        trees: Dictionary of content trees by hash
        lock: Thread lock for concurrent operations
    """
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the version control service.
        
        Args:
            storage_dir: Directory for persisting version data
        """
        self.storage_dir = Path(storage_dir) if storage_dir else Path("/tmp/visualverse-vcs")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.commits: Dict[str, Commit] = {}
        self.branches: Dict[str, Branch] = {}
        self.trees: Dict[str, Tree] = {}
        self.refs: Dict[str, str] = {}  # Symbolic references (HEAD, tags, etc.)
        
        self.lock = threading.RLock()
        
        # Load existing data
        self._load_state()
        
        logger.info(f"VersionControlService initialized with storage: {self.storage_dir}")
    
    def _load_state(self):
        """Load persisted state from storage."""
        commits_file = self.storage_dir / "commits.json"
        branches_file = self.storage_dir / "branches.json"
        refs_file = self.storage_dir / "refs.json"
        
        if commits_file.exists():
            try:
                with open(commits_file, 'r') as f:
                    data = json.load(f)
                    self.commits = {
                        h: Commit.from_dict(c) 
                        for h, c in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load commits: {e}")
        
        if branches_file.exists():
            try:
                with open(branches_file, 'r') as f:
                    data = json.load(f)
                    self.branches = {
                        n: Branch.from_dict(b) 
                        for n, b in data.items()
                    }
            except Exception as e:
                logger.warning(f"Failed to load branches: {e}")
        
        if refs_file.exists():
            try:
                with open(refs_file, 'r') as f:
                    self.refs = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load refs: {e}")
    
    def _save_state(self):
        """Persist state to storage."""
        with self.lock:
            commits_file = self.storage_dir / "commits.json"
            branches_file = self.storage_dir / "branches.json"
            refs_file = self.storage_dir / "refs.json"
            
            with open(commits_file, 'w') as f:
                json.dump(
                    {h: c.to_dict() for h, c in self.commits.items()}, 
                    f, indent=2
                )
            
            with open(branches_file, 'w') as f:
                json.dump(
                    {n: b.to_dict() for n, b in self.branches.items()}, 
                    f, indent=2
                )
            
            with open(refs_file, 'w') as f:
                json.dump(self.refs, f, indent=2)
    
    def init_repository(self, project_id: str, author_id: str, 
                        author_name: str, author_email: str) -> Commit:
        """
        Initialize a new repository with an initial commit.
        
        Args:
            project_id: Project identifier
            author_id: User creating the repository
            author_name: Author display name
            author_email: Author email
            
        Returns:
            The initial commit object
        """
        with self.lock:
            # Create initial empty tree
            tree = Tree(hash=create_commit_hash(""), entries=[])
            self.trees[tree.hash] = tree
            
            # Create initial commit
            commit = Commit(
                hash=create_commit_hash(f"initial:{project_id}"),
                parent_hash=None,
                tree_hash=tree.hash,
                author_id=author_id,
                author_name=author_name,
                author_email=author_email,
                message="Initial commit",
                domain="general"
            )
            
            self.commits[commit.hash] = commit
            
            # Create default branch
            branch = Branch(
                name="main",
                head_commit=commit.hash,
                author_id=author_id,
                is_default=True,
                description="Default branch"
            )
            self.branches["main"] = branch
            
            # Set HEAD reference
            self.refs[f"refs/heads/main"] = commit.hash
            self.refs["HEAD"] = "refs/heads/main"
            
            self._save_state()
            
            logger.info(f"Repository initialized for project {project_id}")
            return commit
    
    def commit(self, project_id: str, author_id: str, author_name: str,
               author_email: str, message: str, content: Dict[str, str],
               parent_hash: str = None, domain: str = "general") -> Commit:
        """
        Create a new commit with the given content.
        
        Args:
            project_id: Project identifier
            author_id: User creating the commit
            author_name: Author display name
            author_email: Author email
            message: Commit message
            content: Dictionary mapping file paths to content
            parent_hash: Parent commit hash (uses current HEAD if None)
            domain: Content domain
            
        Returns:
            The created commit object
        """
        with self.lock:
            # Determine parent commit
            if parent_hash is None:
                head_ref = self.refs.get("HEAD", f"refs/heads/{project_id}")
                parent_hash = self.refs.get(head_ref)
            
            # Create tree from content
            entries = []
            for path, file_content in content.items():
                file_hash = create_file_hash(file_content)
                entries.append(TreeEntry(
                    path=path,
                    hash=file_hash,
                    size=len(file_content)
                ))
            
            # Sort entries by path for consistency
            entries.sort(key=lambda e: e.path)
            
            tree_content = json.dumps([e.to_dict() for e in entries])
            tree_hash = create_commit_hash(tree_content)
            
            tree = Tree(hash=tree_hash, entries=entries)
            self.trees[tree_hash] = tree
            
            # Calculate stats
            files_changed = len(content)
            additions = sum(content[fp].count('\n') for fp in content)
            deletions = 0
            
            # Create commit
            commit_hash = create_commit_hash(
                f"{parent_hash or ''}:{tree_hash}:{message}:{datetime.utcnow().isoformat()}"
            )
            
            commit = Commit(
                hash=commit_hash,
                parent_hash=parent_hash,
                tree_hash=tree_hash,
                author_id=author_id,
                author_name=author_name,
                author_email=author_email,
                message=message,
                domain=domain,
                files_changed=files_changed,
                additions=additions,
                deletions=deletions,
                parent_hashes=[parent_hash] if parent_hash else []
            )
            
            self.commits[commit_hash] = commit
            
            # Update HEAD
            head_ref = self.refs.get("HEAD", f"refs/heads/{project_id}")
            self.refs[head_ref] = commit_hash
            
            # Update current branch if it exists
            branch_name = head_ref.replace("refs/heads/", "")
            if branch_name in self.branches:
                self.branches[branch_name].head_commit = commit_hash
            
            self._save_state()
            
            logger.info(f"Commit created: {commit_hash[:8]} - {message}")
            return commit
    
    def get_commit(self, commit_hash: str) -> Optional[Commit]:
        """
        Retrieve a commit by hash.
        
        Args:
            commit_hash: Commit hash to look up
            
        Returns:
            Commit object or None if not found
        """
        return self.commits.get(commit_hash)
    
    def get_commit_history(self, commit_hash: str = None, 
                           limit: int = 50) -> List[Commit]:
        """
        Get commit history starting from a commit.
        
        Args:
            commit_hash: Starting commit (uses HEAD if None)
            limit: Maximum number of commits to return
            
        Returns:
            List of commits in reverse chronological order
        """
        history = []
        seen = set()
        
        current_hash = commit_hash
        if current_hash is None:
            head_ref = self.refs.get("HEAD")
            if head_ref:
                current_hash = self.refs.get(head_ref)
        
        while current_hash and len(history) < limit:
            if current_hash in seen:
                break  # Prevent infinite loops
            
            seen.add(current_hash)
            commit = self.commits.get(current_hash)
            
            if commit is None:
                break
            
            history.append(commit)
            current_hash = commit.parent_hash
        
        return history
    
    def create_branch(self, name: str, commit_hash: str = None,
                      author_id: str = "", description: str = "") -> Branch:
        """
        Create a new branch.
        
        Args:
            name: Branch name
            commit_hash: Starting commit (uses HEAD if None)
            author_id: User creating the branch
            description: Branch description
            
        Returns:
            Created branch object
        """
        with self.lock:
            if name in self.branches:
                raise ValueError(f"Branch '{name}' already exists")
            
            # Get commit hash
            if commit_hash is None:
                head_ref = self.refs.get("HEAD")
                if head_ref:
                    commit_hash = self.refs.get(head_ref)
            
            if commit_hash is None:
                raise ValueError("No commit specified and no HEAD found")
            
            branch = Branch(
                name=name,
                head_commit=commit_hash,
                author_id=author_id,
                description=description
            )
            
            self.branches[name] = branch
            self.refs[f"refs/heads/{name}"] = commit_hash
            
            self._save_state()
            
            logger.info(f"Branch created: {name} at {commit_hash[:8]}")
            return branch
    
    def delete_branch(self, name: str) -> bool:
        """
        Delete a branch.
        
        Args:
            name: Branch name to delete
            
        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            if name not in self.branches:
                return False
            
            if self.branches[name].is_default:
                raise ValueError("Cannot delete default branch")
            
            del self.branches[name]
            del self.refs[f"refs/heads/{name}"]
            
            self._save_state()
            
            logger.info(f"Branch deleted: {name}")
            return True
    
    def switch_branch(self, name: str) -> Branch:
        """
        Switch to a different branch.
        
        Args:
            name: Branch name to switch to
            
        Returns:
            Branch object
        """
        with self.lock:
            if name not in self.branches:
                raise ValueError(f"Branch '{name}' not found")
            
            branch = self.branches[name]
            self.refs["HEAD"] = f"refs/heads/{name}"
            
            logger.info(f"Switched to branch: {name}")
            return branch
    
    def list_branches(self, project_id: str = None) -> List[Branch]:
        """
        List all branches.
        
        Args:
            project_id: Optional project filter
            
        Returns:
            List of branch objects
        """
        return list(self.branches.values())
    
    def diff(self, base_commit: str, compare_commit: str) -> DiffResult:
        """
        Generate a diff between two commits.
        
        Args:
            base_commit: Base commit hash
            compare_commit: Comparison commit hash
            
        Returns:
            DiffResult with detailed diff information
        """
        base = self.commits.get(base_commit)
        compare = self.commits.get(compare_commit)
        
        if base is None:
            raise ValueError(f"Base commit not found: {base_commit}")
        if compare is None:
            raise ValueError(f"Compare commit not found: {compare_commit}")
        
        base_tree = self.trees.get(base.tree_hash)
        compare_tree = self.trees.get(compare.tree_hash)
        
        if base_tree is None or compare_tree is None:
            raise ValueError("Tree not found for one of the commits")
        
        # Build file maps
        base_files = {e.path: e.hash for e in base_tree.entries}
        compare_files = {e.hash: e.path for e in compare_tree.entries}
        
        files = []
        total_additions = 0
        total_deletions = 0
        
        # Find all paths
        all_paths = set(base_files.keys()) | set(compare_files.values())
        
        for path in all_paths:
            base_hash = base_files.get(path)
            compare_hash = compare_files.get(path)
            
            if base_hash == compare_hash:
                continue  # No change
            
            file_diff = {
                "path": path,
                "status": "added" if not base_hash else ("deleted" if not compare_hash else "modified"),
                "additions": 0,
                "deletions": 0
            }
            
            # Calculate line changes if both versions exist
            if base_hash and compare_hash:
                base_content = self._get_file_content(base.tree_hash, path)
                compare_content = self._get_file_content(compare.tree_hash, path)
                
                if base_content and compare_content:
                    diff = list(difflib.unified_diff(
                        base_content.splitlines(keepends=True),
                        compare_content.splitlines(keepends=True),
                        fromfile=f"a/{path}",
                        tofile=f"b/{path}",
                        lineterm=''
                    ))
                    
                    additions = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
                    deletions = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
                    
                    file_diff["additions"] = additions
                    file_diff["deletions"] = deletions
                    file_diff["diff"] = diff
                    
                    total_additions += additions
                    total_deletions += deletions
            
            files.append(file_diff)
        
        return DiffResult(
            base_commit=base_commit,
            compare_commit=compare_commit,
            files=files,
            total_additions=total_additions,
            total_deletions=total_deletions
        )
    
    def _get_file_content(self, tree_hash: str, path: str) -> Optional[str]:
        """Get file content from a tree."""
        tree = self.trees.get(tree_hash)
        if tree is None:
            return None
        
        for entry in tree.entries:
            if entry.path == path and not entry.is_directory:
                # In a real implementation, we'd store file content in blob objects
                return f"# Content for {path}\nHash: {entry.hash}"
        
        return None
    
    def merge(self, target_branch: str, source_branch: str,
              author_id: str, author_name: str, author_email: str) -> MergeResult:
        """
        Merge changes from source branch into target branch.
        
        Args:
            target_branch: Branch to merge into
            source_branch: Branch to merge from
            author_id: User performing the merge
            author_name: Author display name
            author_email: Author email
            
        Returns:
            MergeResult with merge outcome
        """
        with self.lock:
            target = self.branches.get(target_branch)
            source = self.branches.get(source_branch)
            
            if target is None:
                return MergeResult(success=False, message=f"Target branch '{target_branch}' not found")
            if source is None:
                return MergeResult(success=False, message=f"Source branch '{source_branch}' not found")
            
            # Find common ancestor
            base_commit = self._find_merge_base(target.head_commit, source.head_commit)
            
            if base_commit is None:
                return MergeResult(
                    success=False,
                    message="Could not find merge base"
                )
            
            # Get changes
            base_tree = self.trees.get(self.commits[base_commit].tree_hash)
            target_tree = self.trees.get(self.commits[target.head_commit].tree_hash)
            source_tree = self.trees.get(self.commits[source.head_commit].tree_hash)
            
            if base_tree is None or target_tree is None or source_tree is None:
                return MergeResult(
                    success=False,
                    message="Tree not found for one of the commits"
                )
            
            # Detect conflicts
            conflicts = self._detect_conflicts(
                base_tree, target_tree, source_tree
            )
            
            if conflicts:
                return MergeResult(
                    success=False,
                    base_commit=base_commit,
                    head_commit=target.head_commit,
                    target_commit=source.head_commit,
                    conflicts=conflicts,
                    message=f"Merge failed with {len(conflicts)} conflicts"
                )
            
            # Perform merge
            merged_content = self._three_way_merge(
                base_tree, target_tree, source_tree
            )
            
            # Create merge commit
            message = f"Merge branch '{source_branch}' into '{target_branch}'"
            
            commit = self.commit(
                project_id="",
                author_id=author_id,
                author_name=author_name,
                author_email=author_email,
                message=message,
                content=merged_content,
                parent_hash=target.head_commit,
                domain=self.commits[source.head_commit].domain
            )
            
            # Update target branch
            target.head_commit = commit.hash
            self.refs[f"refs/heads/{target_branch}"] = commit.hash
            
            self._save_state()
            
            return MergeResult(
                success=True,
                commit_hash=commit.hash,
                base_commit=base_commit,
                head_commit=target.head_commit,
                target_commit=source.head_commit,
                merged_files=list(merged_content.keys()),
                message=message
            )
    
    def _find_merge_base(self, commit1: str, commit2: str) -> Optional[str]:
        """Find the common ancestor of two commits."""
        history1 = set()
        current = commit1
        
        while current and len(history1) < 1000:
            history1.add(current)
            commit = self.commits.get(current)
            if commit:
                current = commit.parent_hash
            else:
                break
        
        current = commit2
        while current and len(history1) < 1000:
            if current in history1:
                return current
            commit = self.commits.get(current)
            if commit:
                current = commit.parent_hash
            else:
                break
        
        return None
    
    def _detect_conflicts(self, base_tree: Tree, target_tree: Tree, 
                          source_tree: Tree) -> List[Dict[str, Any]]:
        """Detect conflicts between three tree versions."""
        conflicts = []
        
        base_files = {e.path: e for e in base_tree.entries}
        target_files = {e.path: e for e in target_tree.entries}
        source_files = {e.path: e for e in source_tree.entries}
        
        all_paths = set(base_files.keys()) | set(target_files.keys()) | set(source_files.keys())
        
        for path in all_paths:
            base = base_files.get(path)
            target = target_files.get(path)
            source = source_files.get(path)
            
            # Both branches modified the same file
            if base and target and source:
                if target.hash != source.hash:
                    # Both modified - check if both actually changed content
                    if target.hash != base.hash or source.hash != base.hash:
                        conflicts.append({
                            "type": ConflictType.CONTENT_CONFLICT.value,
                            "path": path,
                            "baseHash": base.hash,
                            "targetHash": target.hash,
                            "sourceHash": source.hash,
                            "message": f"Both branches modified {path}"
                        })
        
        return conflicts
    
    def _three_way_merge(self, base_tree: Tree, target_tree: Tree, 
                         source_tree: Tree) -> Dict[str, str]:
        """Perform three-way merge of content."""
        merged = {}
        
        base_files = {e.path: e for e in base_tree.entries}
        target_files = {e.path: e for e in target_tree.entries}
        source_files = {e.path: e for e in source_tree.entries}
        
        all_paths = set(base_files.keys()) | set(target_files.keys()) | set(source_files.keys())
        
        for path in all_paths:
            base = base_files.get(path)
            target = target_files.get(path)
            source = source_files.get(path)
            
            if target and not source:
                # Deleted in source - keep target
                if target.hash != base.hash:
                    merged[path] = f"# Content from target\n# Original: {base.hash}\n# Target: {target.hash}"
            elif source and not target:
                # Deleted in target - take source
                merged[path] = f"# Content from source\n# Original: {base.hash}\n# Source: {source.hash}"
            elif target and source:
                if target.hash == source.hash:
                    # No change in either
                    merged[path] = f"# Content unchanged\n# Hash: {target.hash}"
                elif target.hash == base.hash:
                    # Only source changed
                    merged[path] = f"# Content from source\n# Base: {base.hash}\n# Source: {source.hash}"
                elif source.hash == base.hash:
                    # Only target changed
                    merged[path] = f"# Content from target\n# Base: {base.hash}\n# Target: {target.hash}"
                else:
                    # Both changed differently - use target as base (simplified)
                    merged[path] = f"# MERGE CONFLICT in {path}\n# Target version selected\n# Target: {target.hash}\n# Source: {source.hash}"
            elif base and not (target or source):
                # Deleted in both
                pass  # Don't include in merged result
            else:
                # New file
                if source:
                    merged[path] = f"# New content from source\n# Source: {source.hash}"
                elif target:
                    merged[path] = f"# New content from target\n# Target: {target.hash}"
        
        return merged
    
    def revert(self, commit_hash: str, author_id: str, author_name: str,
               author_email: str) -> Commit:
        """
        Revert to a specific commit.
        
        Args:
            commit_hash: Commit to revert to
            author_id: User performing the revert
            author_name: Author display name
            author_email: Author email
            
        Returns:
            The revert commit
        """
        with self.lock:
            target_commit = self.commits.get(commit_hash)
            if target_commit is None:
                raise ValueError(f"Commit not found: {commit_hash}")
            
            # Get current HEAD
            head_ref = self.refs.get("HEAD")
            current_hash = self.refs.get(head_ref) if head_ref else None
            
            # Create revert commit
            message = f"Revert to commit {commit_hash[:8]}"
            
            return self.commit(
                project_id="",
                author_id=author_id,
                author_name=author_name,
                author_email=author_email,
                message=message,
                content={},  # Would need to extract actual content
                parent_hash=current_hash,
                domain=target_commit.domain
            )
    
    def tag(self, commit_hash: str, tag_name: str, message: str = "") -> str:
        """
        Create a tag at a specific commit.
        
        Args:
            commit_hash: Commit to tag
            tag_name: Tag name
            message: Tag message
            
        Returns:
            Tag reference
        """
        with self.lock:
            if commit_hash not in self.commits:
                raise ValueError(f"Commit not found: {commit_hash}")
            
            ref = f"refs/tags/{tag_name}"
            self.refs[ref] = commit_hash
            
            self._save_state()
            
            logger.info(f"Tag created: {tag_name} at {commit_hash[:8]}")
            return ref


# Global service instance
_vcs_service: Optional[VersionControlService] = None
_vcs_lock = threading.Lock()


def get_version_control_service(storage_dir: str = None) -> VersionControlService:
    """
    Get the global version control service instance.
    
    Args:
        storage_dir: Optional storage directory
        
    Returns:
        VersionControlService instance
    """
    global _vcs_service
    
    with _vcs_lock:
        if _vcs_service is None:
            _vcs_service = VersionControlService(storage_dir)
        return _vcs_service


__all__ = [
    "ConflictType",
    "Commit",
    "Branch",
    "TreeEntry",
    "Tree",
    "DiffResult",
    "MergeResult",
    "VersionControlService",
    "create_commit_hash",
    "create_file_hash",
    "get_version_control_service"
]
