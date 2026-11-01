from flask import render_template
from app import app,db
from app.models import User, Question, QuizAttempt

@app.route('/')
def index():
    users = db.session.execute(db.select(Question).order_by(Question.id)).scalars()
    return render_template('index.html', users=users)
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
@app.route('/result')
def result():
    return render_template('result.html')