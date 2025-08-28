from flask import Flask, redirect, render_template, request
from cs50 import SQL

app = Flask(__name__)
db = SQL("sqlite:///flashcards.db")

db.execute("""
CREATE TABLE IF NOT EXISTS flashcards (id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL,answer TEXT NOT NULL
)
""")

@app.route('/')
def index():
    flashcards = db.execute("SELECT * FROM flashcards")
    return render_template("index.html", flashcards=flashcards)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        if question and answer:
            db.execute("INSERT INTO flashcards (question, answer) VALUES (?,?)", question, answer)
        return redirect("/")
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    db.execute("DELETE FROM flashcards WHERE id=?", id)
    return redirect("/")

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method =='POST':
        flashcards = db.execute("SELECT * FROM flashcards")
        correct = 0
        total = len(flashcards)

        for flashcard in flashcards:
            user_answer = request.form.get(str(flashcard["id"]))
            if user_answer and user_answer.strip().lower() == flashcard["answer"].strip().lower():
                correct += 1

        return render_template('results.html', correct=correct, total=total)
    flashcards = db.execute("SELECT * FROM flashcards")
    return render_template('quiz.html', flashcards=flashcards)

def results():
    return render_template("results.html")
