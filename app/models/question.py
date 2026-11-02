from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class Question(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(unique=False, nullable=False)
    point: Mapped[int] = mapped_column(unique=False, nullable=False)
    created_at: Mapped[str] = mapped_column(unique=False, nullable=False)

    # one-to-many relationship with Option
    options: Mapped[list["Option"]] = relationship("Option", back_populates="question", cascade="all, delete-orphan")