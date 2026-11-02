from app import db
from app.models import QuizAttempt

def get_all_attempts():
    return db.session.execute(db.select(QuizAttempt).order_by(QuizAttempt.id)).scalars()

def get_high_score(user_id):
    user_scores = db.session.execute(
        db.select(QuizAttempt).filter_by(user_id=user_id).order_by(QuizAttempt.score.desc())
    ).scalar()

    all_scores = db.session.execute(
        db.select(QuizAttempt).order_by(QuizAttempt.score.desc())
    ).scalar()

    user_high_score = 0 if user_scores is None else user_scores[0].score
    all_time_high_score = 0 if all_scores is None else all_scores[0].score

    return {
        'user_high_score': user_high_score,
        'all_time_high_score': all_time_high_score
    }