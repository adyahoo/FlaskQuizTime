from sqlalchemy.orm import Mapped, mapped_column
from app import db

class Question(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(unique=False, nullable=False)
    option_a: Mapped[str] = mapped_column(unique=False, nullable=False)
    option_b: Mapped[str] = mapped_column(unique=False, nullable=False)
    option_c: Mapped[str] = mapped_column(unique=False, nullable=False)
    option_d: Mapped[str] = mapped_column(unique=False, nullable=False)
    correct_option: Mapped[int] = mapped_column(unique=False, nullable=False)
    created_at: Mapped[str] = mapped_column(unique=False, nullable=False)