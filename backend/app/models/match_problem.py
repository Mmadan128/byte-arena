from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class MatchProblem(Base):
    __tablename__ = "match_problem"

    match_problem_id: Mapped[int] = mapped_column(primary_key=True)

    match_id: Mapped[int] = mapped_column(
        ForeignKey("match.match_id"), index=True
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problem.problem_id"), index=True
    )
