"""
Admin Console - Flask Application
Enterprise-grade platform administration interface.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
import requests
import os

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static'
)

app.secret_key = os.getenv("VISUALVERSE_ADMIN_SECRET", "admin-secret-key-change-in-production")

# API Configuration
API_BASE_URL = os.getenv("VISUALVERSE_API_URL", "http://localhost:8001")
GOV_API_URL = os.getenv("VISUALVERSE_GOV_API_URL", "http://localhost:8003")
LXP_API_URL = os.getenv("VISUALVERSE_LXP_API_URL", "http://localhost:8002")


# ============== Authentication Decorator ==============

def login_required(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        if session.get('user', {}).get('role') not in ['admin', 'moderator']:
            flash('Admin access required', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ============== Authentication Routes ==============

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/auth/login",
                data={"username": email, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                session['user'] = data['user']
                session['access_token'] = data['access_token']
                session['refresh_token'] = data['refresh_token']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials', 'error')
        except Exception as e:
            flash(f'Connection error: {str(e)}', 'error')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout and clear session."""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# ============== Dashboard Routes ==============

@app.route('/')
@login_required
def dashboard():
    """Admin dashboard with system overview."""
    return render_template('dashboard.html', user=session.get('user'))


@app.route('/users')
@admin_required
def users():
    """User management page."""
    return render_template('users.html', user=session.get('user'))


@app.route('/content')
@login_required
def content():
    """Content management page."""
    return render_template('content.html', user=session.get('user'))


@app.route('/moderation')
@admin_required
def moderation():
    """Content moderation queue."""
    return render_template('moderation.html', user=session.get('user'))


@app.route('/analytics')
@admin_required
def analytics():
    """Analytics and reporting."""
    return render_template('analytics.html', user=session.get('user'))


@app.route('/settings')
@admin_required
def settings():
    """Platform settings."""
    return render_template('settings.html', user=session.get('user'))


# ============== API Proxy Routes ==============

@app.route('/api/users')
@admin_required
def api_users():
    """Proxy to governance API for users list."""
    try:
        response = requests.get(
            f"{GOV_API_URL}/api/v1/users",
            headers={'Authorization': f"Bearer {session.get('access_token')}"}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/moderation/queue')
@admin_required
def api_moderation_queue():
    """Proxy to governance API for moderation queue."""
    try:
        response = requests.get(
            f"{GOV_API_URL}/api/v1/moderation/queue",
            headers={'Authorization': f"Bearer {session.get('access_token')}"}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/moderation/<int:mod_id>/review', methods=['POST'])
@admin_required
def api_moderation_review(mod_id):
    """Proxy to governance API for moderation review."""
    try:
        response = requests.post(
            f"{GOV_API_URL}/api/v1/moderation/{mod_id}/review",
            json=request.json,
            headers={'Authorization': f"Bearer {session.get('access_token')}"}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics')
@admin_required
def api_analytics():
    """Proxy to governance API for analytics."""
    try:
        params = request.args
        response = requests.get(
            f"{GOV_API_URL}/api/v1/analytics/overview",
            params={
                'start_date': params.get('start_date'),
                'end_date': params.get('end_date')
            },
            headers={'Authorization': f"Bearer {session.get('access_token')}"}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/progress/stats')
@login_required
def api_progress_stats():
    """Proxy to LXP API for progress stats."""
    try:
        response = requests.get(
            f"{LXP_API_URL}/api/v1/progress/stats",
            headers={'Authorization': f"Bearer {session.get('access_token')}"}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============== Error Handlers ==============

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error='Internal server error'), 500


if __name__ == '__main__':
    port = int(os.getenv("ADMIN_CONSOLE_PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
