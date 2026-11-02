from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer
from app import db

class Option(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    option: Mapped[str] = mapped_column(unique=False, nullable=False)
    is_correct: Mapped[bool] = mapped_column(unique=False, nullable=False)

    # Define the Foreign Key column pointing to the parent table
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"), nullable=False)

    # Relationship back to the parent model
    question: Mapped["Question"] = relationship("Question", back_populates="options")