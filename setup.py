import os
import subprocess
import sys

def setup_project():
    print("Setting up Student Feedback Portal...")
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Initialize database
    print("Initializing database...")
    from database import Database
    db = Database()
    print("Database initialized with default users.")
    
    print("Setup complete!")
    print("Run 'python app.py' to start the application")

if __name__ == "__main__":
    setup_project()