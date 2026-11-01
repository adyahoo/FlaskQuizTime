from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')
@app.route('/result')
def result():
    return render_template('result.html')