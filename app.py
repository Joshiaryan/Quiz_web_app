from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "quizmaster_secret_key_2024"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Questions database
QUESTIONS = {
    "science": [
        {"q": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2", "H2"], "answer": 0},
        {"q": "How many chromosomes do humans have?", "options": ["23", "46", "48", "44"], "answer": 1},
        {"q": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi Body"], "answer": 2},
        {"q": "What gas do plants absorb from the atmosphere?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 2},
        {"q": "What is the hardest natural substance on Earth?", "options": ["Gold", "Iron", "Diamond", "Quartz"], "answer": 2},
        {"q": "How many bones are in the adult human body?", "options": ["196", "206", "216", "226"], "answer": 1},
        {"q": "What is the speed of light (approx)?", "options": ["3x10^8 m/s", "3x10^6 m/s", "3x10^4 m/s", "3x10^10 m/s"], "answer": 0},
        {"q": "Which planet is known as the Red Planet?", "options": ["Venus", "Jupiter", "Mars", "Saturn"], "answer": 2},
        {"q": "What is the most abundant gas in Earth's atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Argon"], "answer": 2},
        {"q": "DNA stands for?", "options": ["Deoxyribonucleic Acid", "Diribonucleic Acid", "Deoxyribose Acid", "None of these"], "answer": 0},
    ],
    "math": [
        {"q": "What is the value of pi to 2 decimal places?", "options": ["3.14", "3.41", "3.12", "3.16"], "answer": 0},
        {"q": "What is the square root of 144?", "options": ["11", "12", "13", "14"], "answer": 1},
        {"q": "What is 15% of 200?", "options": ["25", "30", "35", "40"], "answer": 1},
        {"q": "Solve: 2x + 5 = 15. What is x?", "options": ["4", "5", "6", "7"], "answer": 1},
        {"q": "What is the sum of interior angles in a triangle?", "options": ["90 degrees", "180 degrees", "270 degrees", "360 degrees"], "answer": 1},
        {"q": "What is 7 factorial (7!)?", "options": ["2520", "5040", "720", "40320"], "answer": 1},
        {"q": "What is the derivative of x squared?", "options": ["x", "2x", "x squared", "2"], "answer": 1},
        {"q": "What is log base 10 of 1000?", "options": ["2", "3", "4", "10"], "answer": 1},
        {"q": "What is the area of a circle with radius 7? (pi=3.14)", "options": ["153.86", "143.86", "163.86", "133.86"], "answer": 0},
        {"q": "What does the Pythagorean theorem state?", "options": ["a+b=c", "a^2+b^2=c^2", "a^2-b^2=c", "ab=c^2"], "answer": 1},
    ],
    "physics": [
        {"q": "What is Newton's second law of motion?", "options": ["F=mv", "F=ma", "F=m/a", "F=a/m"], "answer": 1},
        {"q": "What is the SI unit of electric current?", "options": ["Volt", "Watt", "Ampere", "Ohm"], "answer": 2},
        {"q": "What is the SI unit of force?", "options": ["Joule", "Pascal", "Newton", "Watt"], "answer": 2},
        {"q": "What is the formula for kinetic energy?", "options": ["mgh", "0.5mv^2", "mv", "Fd"], "answer": 1},
        {"q": "What is Ohm's Law?", "options": ["V=IR", "V=I/R", "V=I+R", "V=I^2R"], "answer": 0},
        {"q": "What is the acceleration due to gravity on Earth?", "options": ["8.9 m/s^2", "9.8 m/s^2", "10.8 m/s^2", "11 m/s^2"], "answer": 1},
        {"q": "What type of wave is sound?", "options": ["Transverse", "Electromagnetic", "Longitudinal", "Surface"], "answer": 2},
        {"q": "What is the SI unit of energy?", "options": ["Watt", "Newton", "Joule", "Pascal"], "answer": 2},
        {"q": "What is the frequency of AC supply in most countries?", "options": ["50 Hz only", "60 Hz only", "50 Hz or 60 Hz", "100 Hz"], "answer": 2},
        {"q": "What does E=mc^2 represent?", "options": ["Kinetic energy", "Mass-energy equivalence", "Potential energy", "Wave energy"], "answer": 1},
    ],
}

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