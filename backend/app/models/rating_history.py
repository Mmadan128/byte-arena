from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class RatingHistory(Base):
    __tablename__ = "rating_history"

    rating_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"), index=True
    )

    contest_id: Mapped[int] = mapped_column(
        ForeignKey("contest.contest_id"), index=True
    )

    old_rating: Mapped[int] = mapped_column(Integer)
    new_rating: Mapped[int] = mapped_column(Integer)
    change: Mapped[int] = mapped_column(Integer)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
