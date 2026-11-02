from flask import render_template, request, redirect, url_for, flash
from app import app,db
from app.services import quiz_attempt_service, user_service, question_service, option_service

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = user_service.get_user_by_username(username=request.form['username'])

    if not user:
        user = user_service.create_user(username=request.form['username'])

    return redirect(url_for('quiz', username=user.username))

@app.route('/quiz')
def quiz():
    questions = question_service.get_all_questions_with_options()

    return render_template('quiz.html', questions=questions)

@app.route('/result')
def result():
    return render_template('result.html')