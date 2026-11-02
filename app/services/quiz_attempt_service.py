from app import db
from app.models import QuizAttempt

def get_all_attempts():
    return db.session.execute(db.select(QuizAttempt).order_by(QuizAttempt.id)).scalars()