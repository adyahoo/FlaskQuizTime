from app import db
from app.models import Question

def get_all_questions():
    return db.session.execute(db.select(Question).order_by(Question.id)).scalars()

def get_all_questions_with_options():
    # create query of one-to-many relationship to get all questions with their options in one query
    return db.session.execute(
        db.select(Question).options(db.joinedload(Question.options)).order_by(Question.id)
    ).unique().scalars().all()