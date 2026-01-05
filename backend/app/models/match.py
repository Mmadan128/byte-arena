from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class Match(Base):
    __tablename__ = "match"

    match_id: Mapped[int] = mapped_column(primary_key=True)

    round_id: Mapped[int] = mapped_column(ForeignKey("round.round_id"))
    player1_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("user.user_id"))

    problem_id: Mapped[int] = mapped_column(Integer)

    start_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    end_time: Mapped[datetime | None]
