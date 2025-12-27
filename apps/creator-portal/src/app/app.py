#!/usr/bin/env python3
"""
VisualVerse Creator Portal
Web-based interface for creating visual lessons using VisualVerse engine.

PROPRIETARY MODULE - See /PROPRIETARY_LICENSE.md for licensing terms

This module is part of VisualVerse's institutional/enterprise offering.
Copyright 2024 VisualVerse Contributors - All Rights Reserved
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import json
import asyncio
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from visualverse import initialize_visualverse

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'visualverse_creator_portal_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize VisualVerse engine
engine = None
try:
    engine = initialize_visualverse()
    print("✅ VisualVerse Engine initialized in Creator Portal")
except Exception as e:
    print(f"⚠️ VisualVerse Engine initialization failed: {e}")

# Global lesson storage (in production, this would be a database)
LESSONS_STORAGE = {}
USER_SESSIONS = {}

class LessonProgress:
    """Track lesson creation progress"""
    def __init__(self, lesson_id):
        self.lesson_id = lesson_id
        self.status = "pending"  # pending, processing, completed, error
        self.progress = 0
        self.messages = []
        self.start_time = datetime.now()
        self.output_file = None
    
    def update_progress(self, progress, message=""):
        self.progress = progress
        if message:
            self.messages.append({
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "progress": progress
            })
    
    def to_dict(self):
        return {
            "lesson_id": self.lesson_id,
            "status": self.status,
            "progress": self.progress,
            "messages": self.messages,
            "duration": (datetime.now() - self.start_time).total_seconds(),
            "output_file": self.output_file
        }

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Creator dashboard"""
    return render_template('dashboard.html')

@app.route('/lesson-creator')
def lesson_creator():
    """Lesson creation interface"""
    return render_template('lesson_creator.html')

@app.route('/lesson-manager')
def lesson_manager():
    """Lesson management interface"""
    return render_template('lesson_manager.html')

@app.route('/api/subjects')
def get_subjects():
    """Get available subjects"""
    if engine:
        subjects = engine.get_available_subjects()
        subject_info = []
        for subject in subjects:
            try:
                plugin = engine.plugins[subject]
                subject_info.append({
                    "id": subject,
                    "name": plugin.display_name,
                    "version": plugin.version
                })
            except:
                subject_info.append({
                    "id": subject,
                    "name": subject.title(),
                    "version": "1.0.0"
                })
        return jsonify({"subjects": subject_info})
    return jsonify({"subjects": []})

@app.route('/api/subjects/<subject_id>/concepts')
def get_concepts(subject_id):
    """Get concepts for a subject"""
    if engine and subject_id in engine.plugins:
        try:
            plugin = engine.plugins[subject_id]
            concept_map = plugin.get_concept_map()
            concepts = []
            for concept_id, concept in concept_map.items():
                concepts.append({
                    "id": concept.id,
                    "title": concept.title,
                    "description": concept.description,
                    "difficulty": concept.difficulty,
                    "prerequisites": concept.prerequisites,
                    "estimated_duration": concept.estimated_duration
                })
            return jsonify({"concepts": concepts})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"concepts": []})

@app.route('/api/lessons', methods=['GET'])
def get_lessons():
    """Get all lessons for current user"""
    # In production, this would check authentication
    lessons = []
    for lesson_id, lesson_data in LESSONS_STORAGE.items():
        lessons.append({
            "id": lesson_id,
            "title": lesson_data.get("title", "Untitled Lesson"),
            "subject": lesson_data.get("subject", "unknown"),
            "status": lesson_data.get("status", "draft"),
            "created_at": lesson_data.get("created_at", ""),
            "duration": lesson_data.get("duration", 0)
        })
    return jsonify({"lessons": lessons})

@app.route('/api/lessons', methods=['POST'])
def create_lesson():
    """Create a new lesson"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Extract lesson data
    title = data.get('title', 'Untitled Lesson')
    subject = data.get('subject', '')
    content = data.get('content', '')
    lesson_id = data.get('lesson_id', f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    # Validate required fields
    if not subject or not content:
        return jsonify({"error": "Subject and content are required"}), 400
    
    # Store lesson data
    lesson_data = {
        "id": lesson_id,
        "title": title,
        "subject": subject,
        "content": content,
        "status": "draft",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    LESSONS_STORAGE[lesson_id] = lesson_data
    
    return jsonify({
        "success": True,
        "lesson_id": lesson_id,
        "message": "Lesson created successfully"
    })

@app.route('/api/lessons/<lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get specific lesson"""
    if lesson_id in LESSONS_STORAGE:
        return jsonify({"lesson": LESSONS_STORAGE[lesson_id]})
    return jsonify({"error": "Lesson not found"}), 404

@app.route('/api/lessons/<lesson_id>/render', methods=['POST'])
def render_lesson(lesson_id):
    """Render a lesson using VisualVerse engine"""
    if lesson_id not in LESSONS_STORAGE:
        return jsonify({"error": "Lesson not found"}), 404
    
    lesson_data = LESSONS_STORAGE[lesson_id]
    progress_tracker = LessonProgress(lesson_id)
    
    # Update status
    lesson_data["status"] = "processing"
    lesson_data["render_started_at"] = datetime.now().isoformat()
    
    # Start background rendering
    socketio.start_background_task(render_lesson_async, lesson_data, progress_tracker)
    
    return jsonify({
        "success": True,
        "lesson_id": lesson_id,
        "message": "Rendering started"
    })

def render_lesson_async(lesson_data, progress_tracker):
    """Async lesson rendering"""
    try:
        progress_tracker.update_progress(10, "Initializing rendering engine...")
        socketio.emit('render_progress', progress_tracker.to_dict())
        
        if engine:
            progress_tracker.update_progress(30, "Loading subject plugin...")
            subject = lesson_data["subject"]
            
            if subject in engine.plugins:
                progress_tracker.update_progress(50, "Generating animation...")
                socketio.emit('render_progress', progress_tracker.to_dict())
                
                # Create lesson using engine
                result = engine.create_lesson(
                    subject=subject,
                    lesson_id=lesson_data["id"],
                    content=lesson_data["content"]
                )
                
                progress_tracker.update_progress(80, "Finalizing output...")
                socketio.emit('render_progress', progress_tracker.to_dict())
                
                # Mark as completed
                lesson_data["status"] = "completed"
                lesson_data["render_completed_at"] = datetime.now().isoformat()
                lesson_data["output"] = result
                progress_tracker.status = "completed"
                progress_tracker.output_file = result
                
            else:
                raise ValueError(f"Subject {subject} not available")
        else:
            # Mock rendering for demo
            progress_tracker.update_progress(60, "Generating mock animation...")
            import time
            time.sleep(2)
            
            progress_tracker.update_progress(90, "Encoding video...")
            time.sleep(1)
            
            lesson_data["status"] = "completed"
            lesson_data["render_completed_at"] = datetime.now().isoformat()
            lesson_data["output"] = f"mock_animation_{lesson_data['id']}.mp4"
            progress_tracker.status = "completed"
            progress_tracker.output_file = f"mock_animation_{lesson_data['id']}.mp4"
        
        progress_tracker.update_progress(100, "Rendering completed!")
        
    except Exception as e:
        lesson_data["status"] = "error"
        lesson_data["error"] = str(e)
        progress_tracker.status = "error"
        progress_tracker.update_progress(0, f"Error: {str(e)}")
    
    socketio.emit('render_progress', progress_tracker.to_dict())

@app.route('/api/lessons/<lesson_id>/progress')
def get_lesson_progress(lesson_id):
    """Get rendering progress for a lesson"""
    # This would typically check against a progress database
    # For demo, return mock progress
    return jsonify({
        "lesson_id": lesson_id,
        "status": "completed",
        "progress": 100,
        "messages": [
            {"timestamp": "2025-12-25T12:00:00", "message": "Rendering completed!", "progress": 100}
        ]
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected to Creator Portal')
    emit('connected', {'data': 'Connected to VisualVerse Creator Portal'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected from Creator Portal')

@socketio.on('join_lesson')
def handle_join_lesson(data):
    """Join a lesson room for real-time updates"""
    lesson_id = data.get('lesson_id')
    if lesson_id:
        socketio.join_room(f"lesson_{lesson_id}")
        emit('joined_lesson', {'lesson_id': lesson_id})

if __name__ == '__main__':
    print("🎓 Starting VisualVerse Creator Portal...")
    print("📚 Access the portal at: http://localhost:5000")
    
    # Create necessary directories
    os.makedirs('static/outputs', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
