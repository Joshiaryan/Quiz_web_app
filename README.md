# QuizMaster - Quiz Web Application

A modern, interactive web-based quiz application built with Flask. Challenge your knowledge in Science, Math, and Physics categories!

## 🎯 Features

- **Multiple Categories**: Test your knowledge in Science, Math, and Physics
- **Interactive Quiz Interface**: User-friendly quiz experience with progress tracking
- **Score Tracking**: All scores are stored in a SQLite database
- **Leaderboard**: View top performers globally or by category
- **Answer Review**: Detailed review of answers after quiz completion
- **Session Management**: Secure session handling for user data
- **Responsive Design**: Modern, mobile-friendly interface

## 📋 Categories

1. **Science** - Biology, Chemistry, General Science
2. **Math** - Algebra, Geometry, Calculus
3. **Physics** - Mechanics, Waves, Energy

Each category contains 10 questions with 4 multiple-choice options.

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Joshiaryan/Quiz_web_app.git
   cd Quiz_web_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
Quiz_web_app/
├── api/
│   └── index.py          # Flask app, routes, and database models
├── instance/
│   └── quiz.db           # SQLite database (auto-created)
├── static/
│   └── style.css         # Styling and responsive design
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Home page with quiz selection
│   ├── quiz.html         # Quiz question display
│   ├── results.html      # Results and answer review
│   └── leaderboard.html  # Global and category leaderboards
├── questions.py          # Quiz questions database
├── app.py                # Entry point for Vercel deployment
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment config
└── README.md             # This file
```

## 🔧 API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display home page |
| `/start` | POST | Initialize a new quiz session |
| `/quiz` | GET | Display current question |
| `/answer` | POST | Process answer and move to next question |
| `/results` | GET | Display quiz results and save score |
| `/leaderboard` | GET | Display leaderboard (accepts `category` parameter) |

## 💾 Database Schema

### Score Model
```
- id: Integer (Primary Key)
- name: String(100) - Player name
- score: Integer - Number of correct answers
- category: String(50) - Quiz category
- timestamp: DateTime - When quiz was completed
```

## 🎮 How to Play

1. **Start**: Enter your name and select a category
2. **Answer**: Choose an answer for each of the 10 questions
3. **Review**: Check your score and see the correct answers
4. **Compete**: View the leaderboard to see how you rank

## 📊 Scoring System

- Correct Answer: +1 point
- Wrong Answer: 0 points
- Percentage: (Score / 10) × 100%

## 🌐 Deployment

This app is ready to deploy on **Vercel**:

1. Push code to GitHub
2. Connect repository to Vercel
3. Vercel automatically deploys using `vercel.json` config
4. Access via your Vercel URL

## 📦 Dependencies

- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM

See `requirements.txt` for versions.

## 🛠️ Development

### Running with auto-reload
```bash
python app.py
```

### Database Reset
Delete `instance/quiz.db` and restart the app to reset all scores.

## 📝 Questions

Questions are stored in `questions.py` with the following structure:
```python
{
    "category_name": [
        {
            "q": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": 0  # Index of correct answer
        }
    ]
}
```

## 🎨 Customization

### Add New Questions
Edit `questions.py` to add more quiz questions.

### Styling
Modify `static/style.css` to change the appearance.

### Add Categories
Add new category in `questions.py` and update templates accordingly.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Joshiaryan**
- GitHub: [@Joshiaryan](https://github.com/Joshiaryan)
- Repository: [Quiz_web_app](https://github.com/Joshiaryan/Quiz_web_app)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more questions
- Improve the UI/UX
- Fix bugs
- Add new features

## 📞 Support

For issues or suggestions, please create an issue on GitHub.

---

**Happy Quizzing! 🎓**
