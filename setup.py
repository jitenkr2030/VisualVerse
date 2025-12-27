#!/usr/bin/env python3
"""
VisualVerse Setup and Installation Script
Sets up the complete VisualVerse system with all dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd=cwd,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")

def setup_manim():
    """Setup Manim Community dependencies"""
    print("🔧 Setting up Manim Community...")
    
    # Navigate to manim directory and install
    manim_dir = Path(__file__).parent / "manim-community"
    if manim_dir.exists():
        run_command(
            "pip install -e .",
            "Installing Manim Community",
            cwd=str(manim_dir)
        )
    else:
        print("❌ Manim directory not found")

def install_dependencies():
    """Install VisualVerse dependencies"""
    print("📦 Installing VisualVerse dependencies...")
    
    # Install from requirements.txt
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        run_command(
            f"pip install -r {requirements_file}",
            "Installing Python dependencies"
        )
    else:
        print("❌ requirements.txt not found")
        
    # Install additional system dependencies for Manim
    system_packages = [
        "ffmpeg",
        "texlive-latex-base",
        "texlive-latex-extra", 
        "texlive-fonts-recommended",
        "texlive-fonts-extra",
        "cairo",
        "pango",
        "gdk-pixbuf",
        "libxml2-dev",
        "libjpeg-dev",
        "libfreetype6-dev",
        "zlib1g-dev"
    ]
    
    print("🔧 Installing system dependencies...")
    for package in system_packages:
        run_command(
            f"apt-get update && apt-get install -y {package}",
            f"Installing {package}"
        )

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "renders",
        "templates",
        "static",
        "static/css",
        "static/js",
        "static/images",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        dir_path = Path(__file__).parent / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_flask_app():
    """Setup Flask application structure"""
    print("🌐 Setting up Flask application...")
    
    # Create __init__.py files for Python packages
    python_packages = [
        "core",
        "core/manim_wrapper",
        "core/render_queue", 
        "core/schema",
        "core/recommender",
        "platforms/math_verse",
        "platforms/physics_verse",
        "platforms/algo_verse",
        "platforms/fin_verse",
        "platforms/chem_verse",
        "apps/creator_portal"
    ]
    
    for package in python_packages:
        init_file = Path(__file__).parent / package / "__init__.py"
        init_file.touch()
        print(f"✅ Created __init__.py for {package}")

def create_config_files():
    """Create configuration files"""
    print("⚙️ Creating configuration files...")
    
    # Create Flask config
    flask_config = """
# VisualVerse Flask Configuration
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'visualverse-secret-key'
    DEBUG = True
    
    # Rendering settings
    RENDER_QUALITY = 'm'
    MAX_CONCURRENT_RENDERS = 2
    RENDER_TIMEOUT = 300
    
    # File paths
    RENDERS_DIR = os.path.join(os.getcwd(), 'renders')
    TEMP_DIR = os.path.join(os.getcwd(), 'temp')
    
    # Subject settings
    AVAILABLE_SUBJECTS = ['math', 'physics', 'algorithms', 'finance', 'chemistry']
"""
    
    config_file = Path(__file__).parent / "config.py"
    with open(config_file, 'w') as f:
        f.write(flask_config)
    print("✅ Created config.py")

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        sys.path.insert(0, str(Path(__file__).parent))
        
        from visualverse import initialize_visualverse
        engine = initialize_visualverse()
        
        subjects = engine.get_available_subjects()
        print(f"✅ Successfully initialized VisualVerse with {len(subjects)} subjects: {subjects}")
        
        # Test render engine
        engine.render_engine.start()
        queue_status = engine.render_engine.get_queue_status()
        print(f"✅ Render engine started: {queue_status}")
        
        engine.render_engine.stop()
        print("✅ All tests passed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def create_startup_script():
    """Create startup script"""
    print("🚀 Creating startup script...")
    
    startup_script = """#!/bin/bash
# VisualVerse Startup Script

echo "🎬 Starting VisualVerse Creator Portal..."

# Set environment variables
export FLASK_APP=apps/creator_portal/app.py
export FLASK_ENV=development
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Change to project directory
cd "$(dirname "$0")"

# Start the application
python apps/creator_portal/app.py
"""
    
    script_file = Path(__file__).parent / "start_visualverse.sh"
    with open(script_file, 'w') as f:
        f.write(startup_script)
    
    # Make executable
    os.chmod(script_file, 0o755)
    print("✅ Created start_visualverse.sh")

def main():
    """Main setup function"""
    print("🚀 VisualVerse Setup Starting...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Setup components
    create_directories()
    setup_flask_app()
    create_config_files()
    
    # Install dependencies
    install_dependencies()
    setup_manim()
    
    # Create startup script
    create_startup_script()
    
    # Test installation
    if test_installation():
        print("\n" + "=" * 50)
        print("🎉 VisualVerse Setup Complete!")
        print("\n📚 Available Commands:")
        print("  • python apps/creator_portal/app.py    - Start Creator Portal")
        print("  • ./start_visualverse.sh               - Start with startup script")
        print("  • python -m pytest                     - Run tests")
        print("\n🌐 Access the Creator Portal at: http://localhost:5000")
        print("\n📖 Documentation: See README.md for detailed usage")
    else:
        print("\n❌ Setup completed with errors. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()