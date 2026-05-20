from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from questions import QUESTIONS
import os

# Set up folder paths
basedir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(basedir, '..', 'templates')
static_folder = os.path.join(basedir, '..', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Initialize database with error handling
def init_database():
    try:
        # Ensure instance directory exists
        instance_dir = os.path.join(basedir, '..', 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        with app.app_context():
            db.create_all()
    except Exception as e:
        # Fail silently in serverless environments
        print(f"Database initialization note: {e}")

# Try to initialize database on startup
try:
    init_database()
except Exception:
    pass

from flask import render_template, request, session, redirect, url_for, flash
from datetime import datetime
import random

# Retry initialization on first request
_db_initialized = False

@app.before_request
def ensure_db_initialized():
    global _db_initialized
    if not _db_initialized:
        try:
            init_database()
            _db_initialized = True
        except Exception:
            pass

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/start", methods=["POST"])
def start():
    username = request.form.get("username", "").strip()
    category = request.form.get("category", "").strip()
    
    if not username or not category:
        flash("Please enter your name and select a category", "error")
        return redirect(url_for("home"))
    
    if category not in QUESTIONS:
        flash("Invalid category", "error")
        return redirect(url_for("home"))
    
    session["username"] = username
    session["category"] = category
    session["questions"] = random.sample(QUESTIONS[category], len(QUESTIONS[category]))
    session["current"] = 0
    session["score"] = 0
    session["answers"] = []
    
    return redirect(url_for("quiz"))

@app.route("/quiz")
def quiz():
    if "username" not in session or "questions" not in session:
        flash("Please start a quiz first", "error")
        return redirect(url_for("home"))
    
    current = session.get("current", 0)
    questions = session.get("questions", [])
    
    if current >= len(questions):
        return redirect(url_for("results"))
    
    question = questions[current]
    return render_template(
        "quiz.html",
        username=session["username"],
        category=session["category"],
        question=question,
        current=current + 1,
        total=len(questions)
    )

@app.route("/answer", methods=["POST"])
def answer():
    if "username" not in session or "questions" not in session:
        return redirect(url_for("home"))
    
    answer_idx = request.form.get("answer")
    if answer_idx is None:
        return redirect(url_for("quiz"))
    
    answer_idx = int(answer_idx)
    current = session.get("current", 0)
    questions = session.get("questions", [])
    question = questions[current]
    
    is_correct = answer_idx == question["answer"]
    if is_correct:
        session["score"] = session.get("score", 0) + 1
    
    session["answers"].append({
        "question": question["q"],
        "options": question["options"],
        "selected": answer_idx,
        "correct": question["answer"]
    })
    
    session["current"] = current + 1
    
    if session["current"] >= len(questions):
        return redirect(url_for("results"))
    
    return redirect(url_for("quiz"))

@app.route("/results")
def results():
    if "username" not in session or "score" not in session:
        return redirect(url_for("home"))
    
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    category = session.get("category", "")
    username = session.get("username", "")
    answers = session.get("answers", [])
    
    percentage = int((score / total * 100) if total > 0 else 0)
    
    # Save to database (with error handling for serverless environments)
    rank = 1
    try:
        new_score = Score(
            name=username,
            score=score,
            category=category
        )
        db.session.add(new_score)
        db.session.commit()
        
        # Get rank
        rank = db.session.query(Score).filter_by(category=category).filter(Score.score > score).count() + 1
    except Exception as e:
        print(f"Database save error: {e}")
        # Continue without saving in serverless environments
    
    # Clear session
    session.clear()
    
    return render_template(
        "results.html",
        username=username,
        category=category,
        score=score,
        total=total,
        percentage=percentage,
        rank=rank,
        review=answers
    )

@app.route("/leaderboard")
def leaderboard():
    category = request.args.get("category", "all").lower()
    categories = ["science", "math", "physics"]
    scores = []
    
    try:
        if category == "all":
            scores_data = db.session.query(Score).order_by(Score.score.desc()).all()
        elif category in categories:
            scores_data = db.session.query(Score).filter_by(category=category).order_by(Score.score.desc()).all()
        else:
            scores_data = []
        
        # Format scores for display
        total_per_category = {"science": 10, "math": 10, "physics": 10}
        
        for s in scores_data:
            scores.append({
                "username": s.name,
                "category": s.category,
                "score": s.score,
                "total": total_per_category.get(s.category, 10),
                "percentage": int((s.score / total_per_category.get(s.category, 10) * 100)),
                "date": s.timestamp
            })
    except Exception as e:
        print(f"Leaderboard query error: {e}")
        scores = []  # Return empty leaderboard on error
    
    return render_template(
        "leaderboard.html",
        scores=scores,
        category=category,
        categories=categories
    )

# Route to handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return '', 204

