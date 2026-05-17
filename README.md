# 🧠 QuizMaster - Professional Quiz Web App

A modern, dark-themed quiz application built with Flask featuring Science, Math, and Physics categories with ranking system and leaderboards.

![QuizMaster](https://img.shields.io/badge/QuizMaster-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![Flask](https://img.shields.io/badge/Flask-3.0+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🔬 3 Categories**: Science, Math, Physics (10 questions each)
- **🏆 Ranking System**: Track your rank among all players
- **📊 High Score Tracking**: Only saves your best score per category
- **🎯 Leaderboard**: View top players with category filters
- **📝 Answer Review**: See correct vs wrong answers after each quiz
- **🎨 Professional Dark Theme**: Animated background, glassmorphism cards
- **📱 Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/quizmaster.git
cd quizmaster
```

2. **Install dependencies**
```bash
pip install flask flask-sqlalchemy
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
Navigate to: `http://127.0.0.1:5000`

## 📁 Project Structure

```
QuizMaster/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/
│   └── style.css         # Professional dark theme CSS
├── templates/
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Landing page with category selection
│   ├── quiz.html         # Quiz interface with progress bar
│   ├── results.html      # Results page with score circle
│   └── leaderboard.html  # Leaderboard with category filters
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🎮 How to Play

1. **Enter Your Name**: Type your username on the home page
2. **Choose Category**: Select Science, Math, or Physics
3. **Answer Questions**: 10 multiple-choice questions per category
4. **View Results**: See your score, rank, and answer review
5. **Check Leaderboard**: Compare with other players

## 🛠 Technical Details

- **Backend**: Flask + SQLAlchemy (SQLite database)
- **Frontend**: HTML5, CSS3 with animations, Vanilla JavaScript
- **Database**: Automatic SQLite database creation
- **Responsive**: Mobile-first design

## 🎨 Design Features

- **Animated Background**: Floating orbs and gradient overlays
- **Glassmorphism**: Blur effects and transparent cards
- **Smooth Animations**: CSS transitions and keyframe animations
- **Progress Indicators**: Animated progress bars
- **Score Visualization**: Circular progress indicator
- **Medal System**: 🥇🥈🥉 for top 3 players

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**: Install Flask and Flask-SQLAlchemy
   ```bash
   pip install flask flask-sqlalchemy
   ```

2. **Port Already in Use**: Change port in `app.py`
   ```python
   app.run(debug=True, port=5001)
   ```

3. **Database Issues**: Delete `quiz.db` file to reset database

### Browser Compatibility:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📊 Question Categories

Each category contains 10 carefully crafted questions:

- **Science**: Biology, Chemistry, General Science
- **Math**: Algebra, Geometry, Calculus basics
- **Physics**: Mechanics, Electricity, Waves

## 🏆 Scoring System

- **Score**: Number of correct answers (0-10)
- **Percentage**: Score converted to percentage
- **Rank**: Your position among all players in that category
- **Best Score**: Only your highest percentage is saved per category

## 🔄 Adding More Questions

Edit the `QUESTIONS` dictionary in `app.py` to add more questions:

```python
QUESTIONS = {
    "science": [
        {"q": "Your question?", "options": ["A", "B", "C", "D"], "answer": 0},
        # answer is the index (0=A, 1=B, 2=C, 3=D)
    ]
}
```

## 📱 Mobile Support

The app is fully responsive and works great on:
- Smartphones (iOS/Android)
- Tablets
- Desktop computers
- Different screen orientations

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Enhancements

- [ ] Timer for each question
- [ ] Difficulty levels
- [ ] User accounts and login
- [ ] More categories
- [ ] Question explanations
- [ ] Social sharing
- [ ] Dark/Light theme toggle

## 📞 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/quizmaster/issues) on GitHub.

---

**Enjoy testing your knowledge with QuizMaster! 🧠✨**

Made with ❤️ by [Your Name]