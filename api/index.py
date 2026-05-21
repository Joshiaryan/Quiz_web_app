from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os
from functools import wraps
# Set up folder paths
basedir = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(basedir, '..', 'templates')
static_folder = os.path.join(basedir, '..', 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- Models ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# ---------- Helper ----------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- Database Init ----------
def init_database():
    try:
        instance_dir = os.path.join(basedir, '..', 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(f"Database initialization note: {e}")

try:
    init_database()
except Exception:
    pass

# ---------- Routes ----------
@app.route('/')
def home():
    top_scores = []
    try:
        scores_data = db.session.query(Score).order_by(Score.score.desc()).limit(3).all()
        total_per_category = {"science": 10, "math": 10, "physics": 10}
        for s in scores_data:
            total = total_per_category.get(s.category, 10)
            top_scores.append({
                "username": s.name,
                "category": s.category,
                "score": s.score,
                "total": total,
                "percentage": int((s.score / total) * 100) if total else 0
            })
    except Exception as e:
        print(f"Home query error: {e}")
    return render_template('home.html', top_scores=top_scores)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Both fields are required.', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials.', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# ---------- Quiz Flow (protected) ----------
@app.route('/start', methods=['POST'])
@login_required
def start():
    username = session.get('username')
    category = request.form.get('category', '').strip()
    if not category:
        flash('Please select a category.', 'error')
        return redirect(url_for('home'))
    if category not in QUESTIONS:
        flash('Invalid category.', 'error')
        return redirect(url_for('home'))
    session['category'] = category
    session['questions'] = random.sample(QUESTIONS[category], len(QUESTIONS[category]))
    session['current'] = 0
    session['score'] = 0
    session['answers'] = []
    return redirect(url_for('quiz'))

@app.route('/quiz')
@login_required
def quiz():
    if 'questions' not in session:
        flash('Please start a quiz first.', 'error')
        return redirect(url_for('home'))
    current = session.get('current', 0)
    questions = session.get('questions', [])
    if current >= len(questions):
        return redirect(url_for('results'))
    question = questions[current]
    return render_template('quiz.html', username=session['username'], category=session['category'],
                           question=question, current=current + 1, total=len(questions))

@app.route('/answer', methods=['POST'])
@login_required
def answer():
    answer_idx = request.form.get('answer')
    if answer_idx is None:
        return redirect(url_for('quiz'))
    answer_idx = int(answer_idx)
    current = session.get('current', 0)
    questions = session.get('questions', [])
    question = questions[current]
    if answer_idx == question['answer']:
        session['score'] = session.get('score', 0) + 1
    session['answers'].append({
        'question': question['q'],
        'options': question['options'],
        'selected': answer_idx,
        'correct': question['answer']
    })
    session['current'] = current + 1
    if session['current'] >= len(questions):
        return redirect(url_for('results'))
    return redirect(url_for('quiz'))

@app.route('/results')
@login_required
def results():
    username = session.get('username')
    score = session.get('score', 0)
    total = len(session.get('questions', []))
    category = session.get('category', '')
    answers = session.get('answers', [])
    percentage = int((score / total * 100) if total else 0)
    rank = 1
    try:
        new_score = Score(name=username, score=score, category=category)
        db.session.add(new_score)
        db.session.commit()
        rank = db.session.query(Score).filter_by(category=category).filter(Score.score > score).count() + 1
    except Exception as e:
        print(f"Database save error: {e}")
    session.clear()
    return render_template('results.html', username=username, category=category, score=score,
                           total=total, percentage=percentage, rank=rank, review=answers)

@app.route('/leaderboard')
def leaderboard():
    category = request.args.get('category', 'all').lower()
    categories = ['science', 'math', 'physics']
    scores = []
    try:
        if category == 'all':
            scores_data = Score.query.order_by(Score.score.desc()).all()
        elif category in categories:
            scores_data = Score.query.filter_by(category=category).order_by(Score.score.desc()).all()
        else:
            scores_data = []
        total_per_category = {'science': 10, 'math': 10, 'physics': 10}
        for s in scores_data:
            total = total_per_category.get(s.category, 10)
            scores.append({
                'username': s.name,
                'category': s.category,
                'score': s.score,
                'total': total,
                'percentage': int((s.score / total) * 100) if total else 0,
                'date': s.timestamp
            })
    except Exception as e:
        print(f"Leaderboard query error: {e}")
    return render_template('leaderboard.html', scores=scores, category=category, categories=categories)

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Load quiz questions
from questions import QUESTIONS

if __name__ == '__main__':
    app.run(debug=True)
