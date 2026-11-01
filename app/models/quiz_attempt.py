from sqlalchemy.orm import Mapped, mapped_column
from app import db

class QuizAttempt(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=False, nullable=False)
    score: Mapped[int] = mapped_column(unique=False, nullable=False)
    attempted_at: Mapped[str] = mapped_column(unique=False, nullable=False)