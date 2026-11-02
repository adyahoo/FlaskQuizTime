from app import db
from app.models import Question, Option

def get_options_by_question_id(question_id):
    return db.session.execute(
        db.select(Option).filter_by(question_id=question_id)
    ).scalars()

def check_answer(option_id):
    option = db.session.execute(
        db.select(Option).filter_by(id=option_id)
    ).scalar()

    return option.is_correct if option else False