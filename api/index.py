from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from questions import QUESTIONS

app = Flask(__name__)
app.secret_key = "quizmaster_secret_key_2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    try:
        top_scores = Score.query.order_by(Score.percentage.desc(), Score.score.desc()).limit(5).all()
    except:
        top_scores = []
    return render_template("home.html", top_scores=top_scores)

@app.route("/start", methods=["POST"])
def start():
    username = request.form.get("username", "").strip()
    category = request.form.get("category", "")
    
    if not username:
        flash("Please enter your name")
        return redirect(url_for("home"))
    
    if category not in QUESTIONS:
        flash("Please select a valid category")
        return redirect(url_for("home"))
    
    session.clear()
    session["username"] = username
    session["category"] = category
    session["current"] = 0
    session["score"] = 0
    session["answers"] = []
    
    return redirect(url_for("quiz"))

@app.route("/quiz")
def quiz():
    category = session.get("category")
    current = session.get("current", 0)
    
    if not category:
        return redirect(url_for("home"))
    
    questions = QUESTIONS.get(category, [])
    
    if current >= len(questions):
        return redirect(url_for("results"))
    
    return render_template(
        "quiz.html",
        question=questions[current],
        current=current + 1,
        total=len(questions),
        category=category,
        username=session.get("username"),
    )

@app.route("/answer", methods=["POST"])
def answer():
    category = session.get("category")
    current = session.get("current", 0)
    
    if not category:
        return redirect(url_for("home"))
    
    questions = QUESTIONS.get(category, [])
    selected = request.form.get("answer")
    
    if selected is None or current >= len(questions):
        return redirect(url_for("quiz"))
    
    try:
        selected = int(selected)
        correct = questions[current]["answer"]
        
        answers = session.get("answers", [])
        answers.append({"selected": selected, "correct": correct})
        session["answers"] = answers
        
        if selected == correct:
            session["score"] = session.get("score", 0) + 1
        
        session["current"] = current + 1
        
    except (ValueError, IndexError):
        pass
    
    return redirect(url_for("quiz"))

@app.route("/results")
def results():
    username = session.get("username")
    category = session.get("category")
    
    if not username or not category:
        return redirect(url_for("home"))
    
    score = session.get("score", 0)
    answers = session.get("answers", [])
    questions = QUESTIONS.get(category, [])
    total = len(questions)
    percentage = round((score / total) * 100, 1) if total else 0
    
    try:
        existing = Score.query.filter_by(username=username, category=category).first()
        if existing:
            if percentage > existing.percentage:
                existing.score = score
                existing.total = total
                existing.percentage = percentage
                existing.date = datetime.utcnow()
        else:
            new_score = Score(
                username=username,
                category=category,
                score=score,
                total=total,
                percentage=percentage
            )
            db.session.add(new_score)
        
        db.session.commit()
        
        rank = Score.query.filter(
            Score.category == category,
            Score.percentage > percentage
        ).count() + 1
        
    except Exception as e:
        print(f"Database error: {e}")
        rank = 1
    
    review = []
    for i in range(min(len(answers), len(questions))):
        review.append({
            "question": questions[i]["q"],
            "options": questions[i]["options"],
            "selected": answers[i]["selected"],
            "correct": answers[i]["correct"],
        })
    
    return render_template(
        "results.html",
        username=username,
        category=category,
        score=score,
        total=total,
        percentage=percentage,
        review=review,
        rank=rank,
    )

@app.route("/leaderboard")
def leaderboard():
    category = request.args.get("category", "all")
    categories = list(QUESTIONS.keys())
    
    try:
        query = Score.query
        if category in categories:
            query = query.filter_by(category=category)
        scores = query.order_by(Score.percentage.desc(), Score.score.desc()).limit(20).all()
    except:
        scores = []
    
    return render_template(
        "leaderboard.html",
        scores=scores,
        category=category,
        categories=categories
    )

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("home"))

@app.errorhandler(500)
def server_error(error):
    return redirect(url_for("home"))

if __name__ == "__main__":
    print("QuizMaster - Starting...")
    print("Open your browser to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host="127.0.0.1", port=5000)