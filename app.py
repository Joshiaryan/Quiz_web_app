from api.index import app, db, Score, QUESTIONS

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
