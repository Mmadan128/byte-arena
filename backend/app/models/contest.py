from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from datetime import datetime

class Contest(Base):
    __tablename__ = "contest"

    contest_id: Mapped[int] = mapped_column(primary_key=True)
    contest_name: Mapped[str] = mapped_column(String)
    contest_type: Mapped[str] = mapped_column(String)  
    status: Mapped[str] = mapped_column(String)

    max_players: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
