from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class Submission(Base):
    __tablename__ = "submission"

    submission_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    contest_id: Mapped[int] = mapped_column(ForeignKey("contest.contest_id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("match.match_id"))
    problem_id: Mapped[int]

    cf_submission_id: Mapped[str]
    verdict: Mapped[str]
    language: Mapped[str]

    submission_time: Mapped[datetime]
    execution_time: Mapped[float | None]
