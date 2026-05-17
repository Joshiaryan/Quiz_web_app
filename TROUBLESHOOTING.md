# 🔧 QuizMaster Troubleshooting Guide

## 🚀 Quick Start (Most Common Solution)

```bash
# 1. Navigate to project folder
cd "j:\python learn\Quiz App"

# 2. Install requirements
pip install flask flask-sqlalchemy

# 3. Run the app
python app.py
```

Then open: **http://127.0.0.1:5000**

---

## 🐛 Common Issues & Solutions

### 1. **"Python was not found" Error**

**Problem:** Python not in PATH or wrong version

**Solutions:**
```bash
# Try these commands in order:
python app.py
py app.py
python3 app.py
C:\Users\[username]\AppData\Local\Microsoft\WindowsApps\python.exe app.py
```

### 2. **"No module named 'flask'" Error**

**Problem:** Flask not installed

**Solution:**
```bash
pip install flask flask-sqlalchemy
# OR
pip3 install flask flask-sqlalchemy
# OR
py -m pip install flask flask-sqlalchemy
```

### 3. **"Address already in use" Error**

**Problem:** Port 5000 is busy

**Solution:** Change port in `app.py`:
```python
app.run(debug=True, host="127.0.0.1", port=5001)  # Use 5001 instead
```

### 4. **CSS/Styles Not Loading**

**Problem:** Static files not found

**Check:**
- File exists: `static/style.css`
- Correct folder structure
- No browser cache issues (Ctrl+F5 to refresh)

### 5. **Database Errors**

**Problem:** SQLite database issues

**Solutions:**
```bash
# Delete database file and restart
del quiz.db
python app.py
```

### 6. **Quiz Not Working in Browser**

**Problem:** JavaScript or form issues

**Check:**
- Browser console for errors (F12)
- Try different browser (Chrome, Firefox, Edge)
- Disable browser extensions
- Clear browser cache

---

## 🔍 Debugging Steps

### Step 1: Test Basic Flask
```python
# Create test.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Flask is working!"

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 2: Check Database
```python
# In Python console
from app import app, db, Score
with app.app_context():
    print(Score.query.all())
```

### Step 3: Test API Endpoint
Visit: `http://127.0.0.1:5000/api/status`

Should return:
```json
{
  "status": "ok",
  "database": "connected",
  "total_scores": 0,
  "categories": ["science", "math", "physics"]
}
```

---

## 🌐 Browser Compatibility

### Supported Browsers:
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

### If Using Older Browser:
- Update browser to latest version
- Try Chrome or Firefox
- Disable JavaScript blockers

---

## 📁 File Structure Check

Ensure you have:
```
Quiz App/
├── app.py                 ✅ Main application
├── static/
│   └── style.css         ✅ Styles
├── templates/
│   ├── base.html         ✅ Base template
│   ├── home.html         ✅ Home page
│   ├── quiz.html         ✅ Quiz page
│   ├── results.html      ✅ Results page
│   └── leaderboard.html  ✅ Leaderboard
├── requirements.txt      ✅ Dependencies
└── README.md            ✅ Documentation
```

---

## 🔧 Advanced Debugging

### Enable Debug Mode
In `app.py`, ensure:
```python
app.run(debug=True)  # Shows detailed errors
```

### Check Logs
Look for error messages in terminal when running app.

### Test Individual Components

**Test Templates:**
```bash
# Check if templates render
curl http://127.0.0.1:5000/
```

**Test Database:**
```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database OK")
```

---

## 🆘 Still Not Working?

### 1. **Complete Reset**
```bash
# Delete everything and re-download
del quiz.db
del __pycache__ /s /q
python app.py
```

### 2. **Try Minimal Version**
Create `simple_test.py`:
```python
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>QuizMaster Test</h1>
    <p>If you see this, Flask is working!</p>
    <a href="/test">Test Link</a>
    '''

@app.route('/test')
def test():
    return '<h2>Test page works!</h2>'

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. **Check System Requirements**
- Windows 10/11
- Python 3.6+
- 100MB free space
- Internet connection (for Google Fonts)

---

## 📞 Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| 404 | Page not found | Check URL, restart app |
| 500 | Server error | Check terminal for error details |
| Connection refused | App not running | Start app with `python app.py` |
| Template not found | Missing HTML files | Check templates/ folder |

---

## ✅ Success Checklist

- [ ] Python installed and working
- [ ] Flask installed (`pip install flask flask-sqlalchemy`)
- [ ] All files in correct folders
- [ ] App starts without errors
- [ ] Browser opens http://127.0.0.1:5000
- [ ] Home page loads with form
- [ ] Can start quiz and answer questions
- [ ] Results page shows score
- [ ] Leaderboard displays scores

---

**If none of these solutions work, the issue might be system-specific. Try running on a different computer or using a Python virtual environment.**