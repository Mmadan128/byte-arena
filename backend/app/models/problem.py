from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Problem(Base):
    __tablename__ = "problem"

    problem_id: Mapped[int] = mapped_column(primary_key=True)

    # Example: "1760E" or "CF-1760-E"
    cf_problem_id: Mapped[str] = mapped_column(String, unique=True, index=True)

    title: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)   
    tags: Mapped[str] = mapped_column(String)          
