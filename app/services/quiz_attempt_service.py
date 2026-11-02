from app import db
from app.models import QuizAttempt
from datetime import datetime, timezone

def get_all_attempts():
    return db.session.execute(db.select(QuizAttempt).order_by(QuizAttempt.id)).scalars()

def get_high_score(user_id):
    user_scores = db.session.execute(
        db.select(QuizAttempt).filter_by(user_id=user_id).order_by(QuizAttempt.score.desc())
    ).scalar()

    all_scores = db.session.execute(
        db.select(QuizAttempt).order_by(QuizAttempt.score.desc())
    ).scalar()

    user_high_score = 0 if user_scores is None else user_scores.score
    all_time_high_score = 0 if all_scores is None else all_scores.score

    return {
        'user_high_score': user_high_score,
        'all_time_high_score': all_time_high_score
    }

def add_quiz_attempt(user_id, score):
    new_attempt = QuizAttempt(
        user_id=user_id,
        score=score,
        attempted_at=datetime.now(timezone.utc)
    )
    db.session.add(new_attempt)
    db.session.commit()

    return new_attempt

def get_latest_attempt(user_id):
    return db.session.execute(
        db.select(QuizAttempt).filter_by(user_id=user_id).order_by(QuizAttempt.attempted_at.desc())
    ).scalar()