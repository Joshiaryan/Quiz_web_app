#!/usr/bin/env python3
"""
Simple startup script for QuizMaster
"""
import sys
import os

def main():
    print("🧠 QuizMaster - Starting Up...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required")
        return False
    
    # Check required modules
    try:
        import flask
        import flask_sqlalchemy
        print("✅ Required packages found")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("💡 Install with: pip install flask flask-sqlalchemy")
        return False
    
    # Check files exist
    required_files = [
        'static/style.css',
        'templates/base.html',
        'templates/home.html',
        'templates/quiz.html',
        'templates/results.html',
        'templates/leaderboard.html'
    ]

    if not (os.path.exists('app.py') or os.path.exists('api/index.py')):
        print("❌ Missing app entrypoint: app.py or api/index.py")
        return False
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Missing file: {file}")
            return False
    
    print("✅ All files found")
    
    # Start the app
    try:
        print("\n🚀 Starting QuizMaster...")
        print("🌐 Open your browser to: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop\n")
        
        try:
            from app import app
        except ModuleNotFoundError:
            from api.index import app

        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 QuizMaster stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()