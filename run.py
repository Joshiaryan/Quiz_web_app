#!/usr/bin/env python3
"""
Enhanced run script with error handling
"""
import os
import sys

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_sqlalchemy
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install flask flask-sqlalchemy")
        return False

def run_app():
    """Run the Flask app with proper error handling"""
    if not check_requirements():
        return
    
    try:
        try:
            from app import app
        except ModuleNotFoundError:
            from api.index import app

        print("🚀 Starting QuizMaster...")
        print("📱 Open your browser to: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 QuizMaster stopped")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_app()