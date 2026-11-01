import csv
from app import app, db
from app.models import User, QuizAttempt, Question

def user_mapper(row):
    existing = db.session.execute(
        db.select(User).filter_by(username=row['username'])
    ).scalar()

    if not existing:
        new_record = User(username=row['username'])
        db.session.add(new_record)

def question_mapper(row):
    existing = db.session.execute(
        db.select(Question).filter_by(id=row['id'])
    ).scalar()

    if not existing:
        new_record = Question(
            id=row['id'],
            question=row['question'],
            option_a=row['option_a'],
            option_b=row['option_b'],
            option_c=row['option_c'],
            option_d=row['option_d'],
            correct_option=row['correct_option'],
            created_at=row['created_at']
        )
        db.session.add(new_record)

def quiz_attempt_mapper(row):
    existing = db.session.execute(
        db.select(QuizAttempt).filter_by(id=row['id'])
    ).scalar()

    if not existing:
        new_record = QuizAttempt(
            id=row['id'],
            user_id=row['user_id'],
            score=row['score'],
            attempted_at=row['attempted_at']
        )
        db.session.add(new_record)

def import_csv_to_sqlite(filename, mapper):
    with app.app_context():
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                mapper(row)

            db.session.commit()
            print(f"Data from {filename} successfully imported into SQLite.")