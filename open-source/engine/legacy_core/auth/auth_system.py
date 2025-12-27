"""
User Authentication and Progress Tracking System for VisualVerse
Provides user management, authentication, and learning progress analytics.
"""

import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

from core.schema.base_models import UserProgress, DifficultyLevel

@dataclass
class User:
    """User account information"""
    user_id: str
    username: str
    email: str
    password_hash: str
    salt: str
    created_at: str
    last_login: Optional[str] = None
    is_active: bool = True
    profile: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.profile is None:
            self.profile = {
                "display_name": self.username,
                "learning_preferences": {},
                "subject_interests": [],
                "skill_levels": {},
                "goals": []
            }

@dataclass
class LearningSession:
    """Learning session tracking"""
    session_id: str
    user_id: str
    subject: str
    concept_id: str
    start_time: str
    end_time: Optional[str] = None
    duration_minutes: int = 0
    completion_status: str = "in_progress"  # in_progress, completed, abandoned
    score: Optional[float] = None
    notes: str = ""
    
class UserManager:
    """Manages user accounts and authentication"""
    
    def __init__(self, data_dir: str = "/workspace/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.sessions_file = self.data_dir / "sessions.json"
        self.progress_file = self.data_dir / "progress.json"
        
        # Initialize data files
        self._init_data_files()
        
    def _init_data_files(self):
        """Initialize data files if they don't exist"""
        for file_path in [self.users_file, self.sessions_file, self.progress_file]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump({}, f)
    
    def _load_data(self, file_path: Path) -> Dict:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_data(self, file_path: Path, data: Dict):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _hash_password(self, password: str, salt: str = None) -> tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        return password_hash.hex(), salt
    
    def create_user(self, username: str, email: str, password: str) -> str:
        """Create a new user account"""
        users_data = self._load_data(self.users_file)
        
        # Check if username or email already exists
        for user_data in users_data.values():
            if user_data['username'] == username or user_data['email'] == email:
                raise ValueError("Username or email already exists")
        
        # Create new user
        user_id = str(uuid.uuid4())
        password_hash, salt = self._hash_password(password)
        
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            salt=salt,
            created_at=datetime.now().isoformat()
        )
        
        users_data[user_id] = asdict(user)
        self._save_data(self.users_file, users_data)
        
        return user_id
    
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return user_id"""
        users_data = self._load_data(self.users_file)
        
        for user_id, user_data in users_data.items():
            if user_data['username'] == username:
                password_hash, _ = self._hash_password(password, user_data['salt'])
                if password_hash == user_data['password_hash']:
                    # Update last login
                    user_data['last_login'] = datetime.now().isoformat()
                    self._save_data(self.users_file, users_data)
                    return user_id
        
        return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        users_data = self._load_data(self.users_file)
        user_data = users_data.get(user_id)
        
        if user_data:
            return User(**user_data)
        return None
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile"""
        users_data = self._load_data(self.users_file)
        
        if user_id in users_data:
            users_data[user_id]['profile'].update(profile_data)
            self._save_data(self.users_file, users_data)
            return True
        return False
    
    def start_learning_session(self, user_id: str, subject: str, concept_id: str) -> str:
        """Start a new learning session"""
        session_id = str(uuid.uuid4())
        
        session = LearningSession(
            session_id=session_id,
            user_id=user_id,
            subject=subject,
            concept_id=concept_id,
            start_time=datetime.now().isoformat()
        )
        
        sessions_data = self._load_data(self.sessions_file)
        sessions_data[session_id] = asdict(session)
        self._save_data(self.sessions_file, sessions_data)
        
        return session_id
    
    def end_learning_session(self, session_id: str, completion_status: str = "completed", 
                           score: Optional[float] = None, notes: str = "") -> bool:
        """End a learning session"""
        sessions_data = self._load_data(self.sessions_file)
        
        if session_id in sessions_data:
            session_data = sessions_data[session_id]
            session_data['end_time'] = datetime.now().isoformat()
            session_data['completion_status'] = completion_status
            session_data['score'] = score
            session_data['notes'] = notes
            
            # Calculate duration
            start_time = datetime.fromisoformat(session_data['start_time'])
            end_time = datetime.fromisoformat(session_data['end_time'])
            duration = int((end_time - start_time).total_seconds() / 60)
            session_data['duration_minutes'] = duration
            
            self._save_data(self.sessions_file, sessions_data)
            
            # Update progress if completed
            if completion_status == "completed":
                self._update_progress(session_data['user_id'], session_data['subject'], 
                                    session_data['concept_id'], score or 100.0, duration)
            
            return True
        return False
    
    def _update_progress(self, user_id: str, subject: str, concept_id: str, score: float, duration: int):
        """Update user progress for a concept"""
        progress_data = self._load_data(self.progress_file)
        
        if user_id not in progress_data:
            progress_data[user_id] = {}
        if subject not in progress_data[user_id]:
            progress_data[user_id][subject] = {}
        
        # Update or create progress entry
        if concept_id not in progress_data[user_id][subject]:
            progress_data[user_id][subject][concept_id] = {
                "status": "completed",
                "score": score,
                "time_spent": duration,
                "last_accessed": datetime.now().isoformat(),
                "completion_count": 1
            }
        else:
            progress_data[user_id][subject][concept_id]["score"] = max(
                progress_data[user_id][subject][concept_id]["score"], score
            )
            progress_data[user_id][subject][concept_id]["time_spent"] += duration
            progress_data[user_id][subject][concept_id]["last_accessed"] = datetime.now().isoformat()
            progress_data[user_id][subject][concept_id]["completion_count"] += 1
        
        self._save_data(self.progress_file, progress_data)
    
    def get_user_progress(self, user_id: str, subject: str = None) -> Dict[str, Any]:
        """Get user progress for a subject or all subjects"""
        progress_data = self._load_data(self.progress_file)
        
        if user_id not in progress_data:
            return {}
        
        if subject:
            return progress_data[user_id].get(subject, {})
        return progress_data[user_id]
    
    def get_learning_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive learning analytics for a user"""
        sessions_data = self._load_data(self.sessions_file)
        progress_data = self._load_data(self.progress_file)
        
        user_sessions = [s for s in sessions_data.values() if s['user_id'] == user_id]
        user_progress = progress_data.get(user_id, {})
        
        # Calculate analytics
        total_sessions = len(user_sessions)
        completed_sessions = len([s for s in user_sessions if s['completion_status'] == 'completed'])
        total_time = sum(s['duration_minutes'] for s in user_sessions if s['duration_minutes'] > 0)
        
        # Subject-wise analytics
        subject_stats = {}
        for subject, concepts in user_progress.items():
            completed_concepts = len([c for c in concepts.values() if c['status'] == 'completed'])
            total_concepts = len(concepts)
            avg_score = sum(c['score'] for c in concepts.values()) / len(concepts) if concepts else 0
            total_subject_time = sum(c['time_spent'] for c in concepts.values())
            
            subject_stats[subject] = {
                "completed_concepts": completed_concepts,
                "total_concepts": total_concepts,
                "completion_rate": (completed_concepts / total_concepts * 100) if total_concepts > 0 else 0,
                "average_score": round(avg_score, 1),
                "total_time_minutes": total_subject_time,
                "concepts_in_progress": total_concepts - completed_concepts
            }
        
        return {
            "overview": {
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
                "total_learning_time_minutes": total_time,
                "active_subjects": len(user_progress)
            },
            "subjects": subject_stats,
            "recent_activity": user_sessions[-10:] if user_sessions else [],
            "recommendations": self._generate_recommendations(user_id, user_progress)
        }
    
    def _generate_recommendations(self, user_id: str, user_progress: Dict) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        for subject, concepts in user_progress.items():
            # Find concepts with low scores that need review
            low_score_concepts = [
                concept_id for concept_id, data in concepts.items()
                if data['score'] < 70 and data['status'] == 'completed'
            ]
            
            if low_score_concepts:
                recommendations.append(f"Review concepts in {subject}: {', '.join(low_score_concepts[:3])}")
            
            # Find subjects with high completion rates for advancement
            completed_count = len([c for c in concepts.values() if c['status'] == 'completed'])
            if completed_count > 5:
                recommendations.append(f"Consider advancing to more complex topics in {subject}")
        
        # Add general recommendations
        if not recommendations:
            recommendations.append("Start with beginner concepts in your areas of interest")
            recommendations.append("Set consistent daily learning goals")
        
        return recommendations[:5]  # Return top 5 recommendations

class AuthService:
    """Authentication service wrapper"""
    
    def __init__(self):
        self.user_manager = UserManager()
        
    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            user_id = self.user_manager.create_user(username, email, password)
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_id
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user login"""
        user_id = self.user_manager.authenticate_user(username, password)
        
        if user_id:
            user = self.user_manager.get_user(user_id)
            return {
                "success": True,
                "message": "Login successful",
                "user_id": user_id,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "profile": user.profile
                }
            }
        else:
            return {
                "success": False,
                "message": "Invalid username or password"
            }
    
    def get_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        user = self.user_manager.get_user(user_id)
        if user:
            return {
                "success": True,
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email,
                    "profile": user.profile,
                    "created_at": user.created_at,
                    "last_login": user.last_login
                }
            }
        return {"success": False, "message": "User not found"}
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        success = self.user_manager.update_user_profile(user_id, profile_data)
        if success:
            return {"success": True, "message": "Profile updated successfully"}
        return {"success": False, "message": "Failed to update profile"}
    
    def start_session(self, user_id: str, subject: str, concept_id: str) -> Dict[str, Any]:
        """Start learning session"""
        session_id = self.user_manager.start_learning_session(user_id, subject, concept_id)
        return {
            "success": True,
            "session_id": session_id,
            "message": "Learning session started"
        }
    
    def end_session(self, session_id: str, completion_status: str = "completed", 
                   score: Optional[float] = None, notes: str = "") -> Dict[str, Any]:
        """End learning session"""
        success = self.user_manager.end_learning_session(session_id, completion_status, score, notes)
        if success:
            return {"success": True, "message": "Learning session ended"}
        return {"success": False, "message": "Failed to end session"}
    
    def get_progress(self, user_id: str, subject: str = None) -> Dict[str, Any]:
        """Get user progress"""
        progress = self.user_manager.get_user_progress(user_id, subject)
        return {
            "success": True,
            "progress": progress
        }
    
    def get_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get learning analytics"""
        analytics = self.user_manager.get_learning_analytics(user_id)
        return {
            "success": True,
            "analytics": analytics
        }

# Global auth service instance
auth_service = AuthService()