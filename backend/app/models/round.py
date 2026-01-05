from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import datetime

class Round(Base):
    __tablename__ = "round"

    round_id: Mapped[int] = mapped_column(primary_key=True)
    contest_id: Mapped[int] = mapped_column(ForeignKey("contest.contest_id"))

    round_number: Mapped[int] = mapped_column(Integer)
    round_type: Mapped[str] = mapped_column(String)

    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
