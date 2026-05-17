#!/usr/bin/env python3
"""
Test script to check for common Flask app issues
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test imports
    print("Testing imports...")
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from datetime import datetime
    print("✓ Flask imports successful")
    
    # Test questions import
    from questions import QUESTIONS
    print(f"✓ Questions loaded: {len(QUESTIONS)} categories")
    
    # Test app creation
    print("Testing app creation...")
    from app import app, db, Score
    print("✓ App created successfully")
    
    # Test database
    print("Testing database...")
    with app.app_context():
        db.create_all()
        print("✓ Database tables created")
    
    # Test routes
    print("Testing routes...")
    with app.test_client() as client:
        # Test home page
        response = client.get('/')
        if response.status_code == 200:
            print("✓ Home page loads")
        else:
            print(f"✗ Home page error: {response.status_code}")
        
        # Test leaderboard
        response = client.get('/leaderboard')
        if response.status_code == 200:
            print("✓ Leaderboard loads")
        else:
            print(f"✗ Leaderboard error: {response.status_code}")
    
    print("\n🎉 All tests passed! App should run without errors.")
    print("\nTo run the app:")
    print("python app.py")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Install required packages: pip install flask flask-sqlalchemy")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()