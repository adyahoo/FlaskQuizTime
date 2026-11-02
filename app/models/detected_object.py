from sqlalchemy.orm import Mapped, mapped_column
from app import db

class DetectedObject(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(unique=False, nullable=False)
    label: Mapped[str] = mapped_column(unique=False, nullable=False)
    score: Mapped[float] = mapped_column(unique=False, nullable=False)