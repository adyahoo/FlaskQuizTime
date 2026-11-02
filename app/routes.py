from flask import render_template, request, redirect, url_for
from app import app
from app.services import quiz_attempt_service, user_service, question_service, option_service

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = user_service.get_user_by_username(username=request.form['username'])

    if not user:
        user = user_service.create_user(username=request.form['username'])

    return redirect(url_for('quiz', user=user.id))

@app.route('/quiz')
def quiz():
    user_id = request.args.get('user')

    questions = question_service.get_all_questions_with_options()
    high_scores = quiz_attempt_service.get_high_score(user_id=user_id)

    return render_template('quiz.html', questions=questions, high_scores=high_scores, user_id=user_id)

@app.route('/submit_quiz/<int:user_id>', methods=['POST'])
def submit_quiz(user_id):
    score = 0
    form = request.form

    for name, value in form.items():
        question_id = int(name.split('_')[1])
        option_id = int(value)

        question = question_service.get_question_by_id(question_id=question_id)
        is_correct = option_service.check_answer(option_id=option_id)
        score += question.point if is_correct else 0

    quiz_attempt_service.add_quiz_attempt(user_id=user_id, score=score)

    return redirect(url_for('result', user_id=user_id))

@app.route('/result')
def result():
    user_id = request.args.get('user_id')

    high_scores = quiz_attempt_service.get_high_score(user_id=user_id)
    latest_score = quiz_attempt_service.get_latest_attempt(user_id=user_id).score

    return render_template('result.html', user_id=user_id, high_scores=high_scores, latest_score=latest_score)