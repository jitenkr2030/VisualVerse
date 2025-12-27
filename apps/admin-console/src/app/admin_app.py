#!/usr/bin/env python3
"""
VisualVerse Admin Console
Comprehensive web-based administration interface for VisualVerse platform.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objs as go
import plotly.utils

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = 'visualverse_admin_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_console.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Database Models
class AdminUser(db.Model):
    """Admin user model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='admin')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemStats(db.Model):
    """System statistics model"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)
    total_users = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer, default=0)
    total_views = db.Column(db.Integer, default=0)
    total_renders = db.Column(db.Integer, default=0)
    avg_session_duration = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserActivity(db.Model):
    """User activity tracking"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    action = db.Column(db.String(100))
    lesson_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.Text)  # JSON data

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

# Routes
@app.route('/')
def admin_home():
    """Admin dashboard home"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = AdminUser.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password) and user.is_active:
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})
    
    return render_template('admin_login.html')

@app.route('/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/dashboard')
@login_required
def admin_dashboard():
    """Main admin dashboard"""
    return render_template('admin_dashboard.html')

@app.route('/api/dashboard/stats')
@login_required
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get current date stats
        today = datetime.now().date()
        today_stats = SystemStats.query.filter_by(date=today).first()
        
        if not today_stats:
            # Generate mock stats if none exist
            today_stats = SystemStats(
                date=today,
                total_users=1250,
                total_lessons=340,
                total_views=15670,
                total_renders=890,
                avg_session_duration=24.5
            )
            db.session.add(today_stats)
            db.session.commit()
        
        # Get weekly data for charts
        week_ago = today - timedelta(days=7)
        weekly_stats = SystemStats.query.filter(
            SystemStats.date >= week_ago
        ).order_by(SystemStats.date).all()
        
        # Prepare chart data
        dates = [stat.date.strftime('%Y-%m-%d') for stat in weekly_stats]
        users = [stat.total_users for stat in weekly_stats]
        lessons = [stat.total_lessons for stat in weekly_stats]
        views = [stat.total_views for stat in weekly_stats]
        
        stats = {
            'today': {
                'total_users': today_stats.total_users,
                'total_lessons': today_stats.total_lessons,
                'total_views': today_stats.total_views,
                'total_renders': today_stats.total_renders,
                'avg_session_duration': round(today_stats.avg_session_duration, 1)
            },
            'charts': {
                'dates': dates,
                'users': users,
                'lessons': lessons,
                'views': views
            },
            'recent_activity': get_recent_activity()
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users')
@login_required
def admin_users():
    """User management page"""
    return render_template('admin_users.html')

@app.route('/api/users')
@login_required
def get_users():
    """Get users list"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        users = AdminUser.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        user_list = []
        for user in users.items:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'created_at': user.created_at.isoformat()
            })
        
        return jsonify({
            'users': user_list,
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/lessons')
@login_required
def admin_lessons():
    """Lesson management page"""
    return render_template('admin_lessons.html')

@app.route('/api/lessons')
@login_required
def get_lessons():
    """Get lessons list"""
    try:
        # Mock lessons data for demonstration
        lessons = [
            {
                'id': 'lesson_1',
                'title': 'Introduction to Calculus',
                'subject': 'Mathematics',
                'creator': 'Dr. Sarah Johnson',
                'status': 'completed',
                'views': 1250,
                'rating': 4.7,
                'created_at': '2024-01-15T10:00:00Z',
                'duration': 1800
            },
            {
                'id': 'lesson_2',
                'title': 'Physics Fundamentals',
                'subject': 'Physics',
                'creator': 'Prof. Michael Chen',
                'status': 'processing',
                'views': 890,
                'rating': 4.5,
                'created_at': '2024-01-16T14:30:00Z',
                'duration': 2100
            },
            {
                'id': 'lesson_3',
                'title': 'Algorithm Design',
                'subject': 'Computer Science',
                'creator': 'Dr. Emily Rodriguez',
                'status': 'completed',
                'views': 2100,
                'rating': 4.9,
                'created_at': '2024-01-17T09:15:00Z',
                'duration': 2400
            }
        ]
        
        return jsonify({'lessons': lessons})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
@login_required
def admin_analytics():
    """Analytics page"""
    return render_template('admin_analytics.html')

@app.route('/api/analytics/engagement')
@login_required
def get_engagement_analytics():
    """Get engagement analytics"""
    try:
        # Mock analytics data
        engagement_data = {
            'daily_active_users': [120, 145, 132, 167, 189, 156, 178],
            'lesson_completions': [45, 52, 48, 61, 67, 54, 59],
            'average_session_time': [22.5, 24.1, 23.8, 25.2, 26.7, 24.9, 25.4],
            'top_subjects': [
                {'subject': 'Mathematics', 'completion_rate': 78.5},
                {'subject': 'Physics', 'completion_rate': 72.3},
                {'subject': 'Computer Science', 'completion_rate': 85.2},
                {'subject': 'Chemistry', 'completion_rate': 68.9},
                {'subject': 'Biology', 'completion_rate': 74.1}
            ]
        }
        
        return jsonify(engagement_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/system')
@login_required
def admin_system():
    """System monitoring page"""
    return render_template('admin_system.html')

@app.route('/api/system/health')
@login_required
def get_system_health():
    """Get system health status"""
    try:
        # Mock system health data
        health_status = {
            'services': {
                'visualverse_engine': {'status': 'healthy', 'uptime': '99.9%'},
                'rendering_service': {'status': 'healthy', 'uptime': '99.7%'},
                'content_database': {'status': 'healthy', 'uptime': '100%'},
                'user_database': {'status': 'healthy', 'uptime': '99.8%'},
                'file_storage': {'status': 'warning', 'uptime': '98.5%'},
                'cdn': {'status': 'healthy', 'uptime': '99.9%'}
            },
            'resources': {
                'cpu_usage': 45.2,
                'memory_usage': 62.8,
                'disk_usage': 34.1,
                'network_io': 125.6
            },
            'alerts': [
                {
                    'id': 1,
                    'severity': 'warning',
                    'message': 'File storage usage above 30%',
                    'timestamp': '2024-01-20T10:30:00Z'
                }
            ]
        }
        
        return jsonify(health_status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/settings')
@login_required
def admin_settings():
    """System settings page"""
    return render_template('admin_settings.html')

@app.route('/api/settings', methods=['GET', 'POST'])
@login_required
def manage_settings():
    """Manage system settings"""
    if request.method == 'GET':
        # Return current settings
        settings = {
            'system': {
                'maintenance_mode': False,
                'max_concurrent_renders': 10,
                'default_video_quality': 'hd',
                'session_timeout': 3600
            },
            'content': {
                'auto_approve_lessons': False,
                'max_lesson_duration': 3600,
                'require_creator_verification': True,
                'content_moderation_enabled': True
            },
            'users': {
                'registration_enabled': True,
                'email_verification_required': True,
                'max_account_age': 365,
                'suspicious_activity_threshold': 100
            }
        }
        return jsonify(settings)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            # In a real implementation, this would save to database
            return jsonify({'success': True, 'message': 'Settings updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

# Helper functions
def get_recent_activity():
    """Get recent system activity"""
    activities = [
        {
            'timestamp': '2024-01-20T15:30:00Z',
            'action': 'User Registration',
            'details': 'New user john.doe@example.com registered',
            'type': 'user'
        },
        {
            'timestamp': '2024-01-20T15:25:00Z',
            'action': 'Lesson Rendered',
            'details': 'Calculus lesson completed by Dr. Sarah Johnson',
            'type': 'content'
        },
        {
            'timestamp': '2024-01-20T15:20:00Z',
            'action': 'System Alert',
            'details': 'High CPU usage detected (85%)',
            'type': 'system'
        }
    ]
    return activities

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('admin_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('admin_500.html'), 500

# Initialize database
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if none exists
        if not AdminUser.query.first():
            admin_user = AdminUser(
                username='admin',
                email='admin@visualverse.com',
                password_hash=generate_password_hash('admin123'),
                role='super_admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Created default admin user: admin / admin123")

if __name__ == '__main__':
    init_db()
    print("🎓 Starting VisualVerse Admin Console...")
    print("📊 Access the admin console at: http://localhost:5001")
    print("🔐 Default credentials: admin / admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
