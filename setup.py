#!/usr/bin/env python
"""
Setup script for Password Detection Tool
This script helps with initial setup and database initialization
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def run_command(command, description):
    """Run a command and report status"""
    print(f"\n{description}...", end=" ")
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True)
        print("✓ Done")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {e}")
        return False

def setup_environment():
    """Setup Python environment"""
    print_header("Environment Setup")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ is required")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        if run_command("python -m venv venv", "Creating virtual environment"):
            print("✓ Virtual environment created")
        else:
            return False
    else:
        print("✓ Virtual environment already exists")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    # Determine pip command based on OS
    pip_cmd = "venv\\Scripts\\pip" if sys.platform == "win32" else "venv/bin/pip"
    
    if run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python packages"):
        return True
    else:
        print("✗ Failed to install dependencies")
        return False

def setup_database():
    """Setup database"""
    print_header("Database Setup")
    
    print("\nDatabase Configuration Required:")
    print("You need to manually set up MySQL database.")
    print("\nSteps:")
    print("1. Start MySQL server")
    print("2. Run: mysql -u root -p")
    print("3. Execute: CREATE DATABASE password_detector;")
    print("4. Update .env file with your MySQL credentials")
    
    input("\nPress Enter once you've completed the database setup...")
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_header("Configuration File")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    print("\nCreating .env file...")
    
    env_content = """FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-change-this-in-production
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@localhost:3306/password_detector
DEBUG=True
"""
    
    env_file.write_text(env_content)
    print("✓ .env file created")
    print("⚠ Important: Update the database credentials in .env file!")
    
    return True

def initialize_app():
    """Initialize the Flask application"""
    print_header("Application Initialization")
    
    python_cmd = "venv\\Scripts\\python" if sys.platform == "win32" else "venv/bin/python"
    
    print("\nInitializing database tables...")
    
    init_script = f"""
from app import app, db

with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully")
"""
    
    # Create and run initialization script
    init_file = Path("init_db.py")
    init_file.write_text(init_script)
    
    if run_command(f"{python_cmd} init_db.py", "Creating database tables"):
        init_file.unlink()  # Remove temporary file
        return True
    else:
        print("⚠ Database initialization may have failed")
        print("Try running manually: python init_db.py")
        if init_file.exists():
            init_file.unlink()
        return False

def main():
    """Main setup function"""
    print_header("Password Detection Tool - Setup Wizard")
    print("\nThis script will help you set up the application.")
    
    steps = [
        ("Environment Setup", setup_environment),
        ("Install Dependencies", install_dependencies),
        ("Configuration", create_env_file),
        ("Database Setup", setup_database),
        ("Application Initialization", initialize_app),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n✗ Setup failed at: {step_name}")
            print("\nPlease fix the issues and try again.")
            return False
    
    print_header("Setup Complete!")
    print("\n✓ Your Password Detection Tool is ready to use!")
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Run the application:")
    print("   python app.py")
    print("\n3. Open your browser to: http://localhost:5000")
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
