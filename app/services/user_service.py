from app import db
from app.models import User

def get_all_users():
    return db.session.execute(db.select(User).order_by(User.id)).scalars()

def is_user_exist(username):
    existing = db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar()

    return existing is not None

def get_user_by_username(username):
    return db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar()

def create_user(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return new_user