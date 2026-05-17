#!/usr/bin/env python3
"""
QuizMaster System Test
Comprehensive test to verify all components work
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "info": "🔍",
        "success": "✅", 
        "error": "❌",
        "warning": "⚠️"
    }
    print(f"{colors.get(status, '•')} {message}")

def test_python():
    """Test Python installation"""
    print_status("Testing Python installation...")
    
    if sys.version_info < (3, 6):
        print_status(f"Python {sys.version.split()[0]} - Need 3.6+", "error")
        return False
    
    print_status(f"Python {sys.version.split()[0]} - OK", "success")
    return True

def test_packages():
    """Test required packages"""
    print_status("Testing required packages...")
    
    try:
        import flask
        print_status(f"Flask {flask.__version__} - OK", "success")
    except ImportError:
        print_status("Flask not found - Run: pip install flask", "error")
        return False
    
    try:
        import flask_sqlalchemy
        print_status("Flask-SQLAlchemy - OK", "success")
    except ImportError:
        print_status("Flask-SQLAlchemy not found - Run: pip install flask-sqlalchemy", "error")
        return False
    
    return True

def test_files():
    """Test required files exist"""
    print_status("Testing file structure...")
    
    required_files = [
        "app.py",
        "static/style.css",
        "templates/base.html",
        "templates/home.html", 
        "templates/quiz.html",
        "templates/results.html",
        "templates/leaderboard.html"
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print_status(f"{file} - Found", "success")
        else:
            print_status(f"{file} - Missing", "error")
            missing.append(file)
    
    return len(missing) == 0

def test_app_import():
    """Test app can be imported"""
    print_status("Testing app import...")
    
    try:
        from app import app, db, QUESTIONS
        print_status("App import - OK", "success")
        
        # Test questions data
        total_questions = sum(len(q) for q in QUESTIONS.values())
        print_status(f"Questions loaded: {total_questions} total", "success")
        
        return True
    except Exception as e:
        print_status(f"App import failed: {e}", "error")
        return False

def test_database():
    """Test database creation"""
    print_status("Testing database...")
    
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print_status("Database creation - OK", "success")
        return True
    except Exception as e:
        print_status(f"Database test failed: {e}", "error")
        return False

def test_routes():
    """Test app routes"""
    print_status("Testing routes...")
    
    try:
        from app import app
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print_status("Home route - OK", "success")
            else:
                print_status(f"Home route failed: {response.status_code}", "error")
                return False
            
            # Test leaderboard
            response = client.get('/leaderboard')
            if response.status_code == 200:
                print_status("Leaderboard route - OK", "success")
            else:
                print_status(f"Leaderboard route failed: {response.status_code}", "error")
                return False
            
            # Test API status
            response = client.get('/api/status')
            if response.status_code == 200:
                print_status("API status - OK", "success")
            else:
                print_status(f"API status failed: {response.status_code}", "error")
                return False
        
        return True
    except Exception as e:
        print_status(f"Route testing failed: {e}", "error")
        return False

def run_full_test():
    """Run complete system test"""
    print("🧠 QuizMaster System Test")
    print("=" * 40)
    
    tests = [
        ("Python Installation", test_python),
        ("Required Packages", test_packages), 
        ("File Structure", test_files),
        ("App Import", test_app_import),
        ("Database", test_database),
        ("Routes", test_routes)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
            else:
                print_status(f"{test_name} - FAILED", "error")
        except Exception as e:
            print_status(f"{test_name} - ERROR: {e}", "error")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print_status("ALL TESTS PASSED! 🎉", "success")
        print("\n🚀 Ready to run QuizMaster:")
        print("   python app.py")
        print("   Then open: http://127.0.0.1:5000")
        return True
    else:
        print_status(f"{total - passed} tests failed", "error")
        print("\n🔧 Check TROUBLESHOOTING.md for solutions")
        return False

def quick_test():
    """Quick test for basic functionality"""
    print("🔍 QuizMaster Quick Test")
    print("-" * 25)
    
    # Basic checks
    if not test_python():
        return False
    
    if not test_packages():
        print("💡 Try: pip install flask flask-sqlalchemy")
        return False
    
    if not os.path.exists("app.py"):
        print_status("app.py not found", "error")
        return False
    
    print_status("Quick test passed!", "success")
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        return quick_test()
    else:
        return run_full_test()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)