"""
Render Queue System for VisualVerse
Handles asynchronous video rendering jobs using Celery and Redis.
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import threading
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.manim_wrapper.scene_manager import SceneManager, RenderJob

class JobStatus(str, Enum):
    """Status of a render job"""
    PENDING = "pending"
    QUEUED = "queued" 
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class RenderTask:
    """Represents a rendering task in the queue"""
    job_id: str
    scene_config: Dict[str, Any]
    priority: int
    created_at: datetime
    estimated_duration: int = 30  # seconds
    status: JobStatus = JobStatus.PENDING
    result_path: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for serialization"""
        return {
            "job_id": self.job_id,
            "scene_config": self.scene_config,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "estimated_duration": self.estimated_duration,
            "status": self.status.value,
            "result_path": self.result_path,
            "error_message": self.error_message
        }

class RenderEngine:
    """
    Manages rendering jobs and queue.
    Provides both synchronous and asynchronous rendering capabilities.
    """
    
    def __init__(self, max_concurrent_jobs: int = 2):
        self.max_concurrent_jobs = max_concurrent_jobs
        self.job_queue: List[RenderTask] = []
        self.active_jobs: Dict[str, RenderTask] = {}
        self.completed_jobs: Dict[str, RenderTask] = {}
        self.scene_manager = SceneManager()
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_jobs)
        self.is_running = False
        self._lock = threading.Lock()
        
    def start(self):
        """Start the render engine background workers"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()
            print("🎬 Render Engine started")
            
    def stop(self):
        """Stop the render engine"""
        self.is_running = False
        if hasattr(self, 'worker_thread'):
            self.worker_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        print("🛑 Render Engine stopped")
        
    def submit_job(self, scene_config: Dict[str, Any], priority: int = 0) -> str:
        """
        Submit a rendering job to the queue.
        
        Args:
            scene_config: Configuration for the scene to render
            priority: Job priority (higher number = higher priority)
            
        Returns:
            Job ID for tracking
        """
        job_id = str(uuid.uuid4())
        task = RenderTask(
            job_id=job_id,
            scene_config=scene_config,
            priority=priority,
            created_at=datetime.now()
        )
        
        with self._lock:
            self.job_queue.append(task)
            # Sort by priority (higher priority first)
            self.job_queue.sort(key=lambda x: (-x.priority, x.created_at))
            
        print(f"📝 Job {job_id} submitted to queue")
        return job_id
        
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific job"""
        # Check active jobs
        if job_id in self.active_jobs:
            task = self.active_jobs[job_id]
            return task.to_dict()
            
        # Check queue
        for task in self.job_queue:
            if task.job_id == job_id:
                return task.to_dict()
                
        # Check completed jobs
        if job_id in self.completed_jobs:
            task = self.completed_jobs[job_id]
            return task.to_dict()
            
        return None
        
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending or active job"""
        with self._lock:
            # Remove from queue
            self.job_queue = [task for task in self.job_queue if task.job_id != job_id]
            
            # Cancel active job
            if job_id in self.active_jobs:
                task = self.active_jobs[job_id]
                task.status = JobStatus.CANCELLED
                del self.active_jobs[job_id]
                self.completed_jobs[job_id] = task
                print(f"❌ Job {job_id} cancelled")
                return True
                
        return False
        
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue status"""
        with self._lock:
            return {
                "queued_jobs": len(self.job_queue),
                "active_jobs": len(self.active_jobs),
                "completed_jobs": len(self.completed_jobs),
                "max_concurrent": self.max_concurrent_jobs
            }
            
    def wait_for_job(self, job_id: str, timeout: int = 300) -> Optional[str]:
        """
        Wait for a job to complete and return the result path.
        
        Args:
            job_id: ID of the job to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            Path to rendered video file, or None if failed/timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            if not status:
                return None
                
            if status["status"] == JobStatus.COMPLETED.value:
                return status["result_path"]
            elif status["status"] == JobStatus.FAILED.value:
                print(f"Job {job_id} failed: {status.get('error_message', 'Unknown error')}")
                return None
            elif status["status"] == JobStatus.CANCELLED.value:
                print(f"Job {job_id} was cancelled")
                return None
                
            time.sleep(1)
            
        print(f"Job {job_id} timed out after {timeout} seconds")
        return None
        
    def _worker_loop(self):
        """Background worker that processes the queue"""
        while self.is_running:
            try:
                with self._lock:
                    # Check if we can start more jobs
                    if (len(self.active_jobs) < self.max_concurrent_jobs and 
                        self.job_queue):
                        
                        # Get next job
                        task = self.job_queue.pop(0)
                        self.active_jobs[task.job_id] = task
                        
                # Start job execution
                if task.job_id in self.active_jobs:
                    self._execute_job(task)
                    
            except Exception as e:
                print(f"Worker loop error: {e}")
                
            time.sleep(0.1)  # Small delay to prevent busy waiting
            
    def _execute_job(self, task: RenderTask):
        """Execute a single rendering job"""
        try:
            task.status = JobStatus.RENDERING
            print(f"🎬 Starting job {task.job_id}")
            
            # Create scene and render
            result_path = self.scene_manager.create_scene(task.scene_config)
            
            task.result_path = result_path
            task.status = JobStatus.COMPLETED
            
            # Move to completed jobs
            with self._lock:
                if task.job_id in self.active_jobs:
                    del self.active_jobs[task.job_id]
                self.completed_jobs[task.job_id] = task
                
            print(f"✅ Job {task.job_id} completed: {result_path}")
            
        except Exception as e:
            task.status = JobStatus.FAILED
            task.error_message = str(e)
            
            # Move to completed jobs
            with self._lock:
                if task.job_id in self.active_jobs:
                    del self.active_jobs[task.job_id]
                self.completed_jobs[task.job_id] = task
                
            print(f"❌ Job {task.job_id} failed: {e}")
            
    def render_sync(self, scene_config: Dict[str, Any]) -> str:
        """
        Render a scene synchronously (blocking call).
        
        Args:
            scene_config: Scene configuration
            
        Returns:
            Path to rendered video file
        """
        return self.scene_manager.create_scene(scene_config)
        
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed jobs to free memory"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        with self._lock:
            old_jobs = [
                job_id for job_id, task in self.completed_jobs.items()
                if task.created_at < cutoff_time
            ]
            
            for job_id in old_jobs:
                del self.completed_jobs[job_id]
                
        print(f"🧹 Cleaned up {len(old_jobs)} old jobs")

# Example usage and testing
if __name__ == "__main__":
    # Initialize render engine
    engine = RenderEngine(max_concurrent_jobs=2)
    engine.start()
    
    # Submit test jobs
    scene_config = {
        "title": "Test Scene",
        "text": ["Hello VisualVerse!", "This is a test animation."],
        "equations": ["E = mc^2", "a^2 + b^2 = c^2"]
    }
    
    job_id = engine.submit_job(scene_config, priority=1)
    print(f"Submitted job: {job_id}")
    
    # Wait for completion
    result_path = engine.wait_for_job(job_id)
    if result_path:
        print(f"Rendered video: {result_path}")
    else:
        print("Rendering failed")
        
    engine.stop()