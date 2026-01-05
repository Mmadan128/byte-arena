from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    leaderboard_id: Mapped[int] = mapped_column(primary_key=True)

    contest_id: Mapped[int] = mapped_column(
        ForeignKey("contest.contest_id"), index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"), index=True
    )

    rank: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
