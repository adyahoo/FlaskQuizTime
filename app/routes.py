from flask import render_template, request, redirect, url_for, flash
from app import app,db
from app.services import user_service

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
    username = request.args.get('username')

    return render_template('quiz.html')

@app.route('/result')
def result():
    return render_template('result.html')