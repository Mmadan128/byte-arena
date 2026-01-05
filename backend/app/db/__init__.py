from app.db.base import Base
from app.db.session import engine

from app.models import (
    User,
    Contest,
    Round,
    ContestParticipant,
    Match,
    Submission,
    Problem,
    MatchProblem,
    Leaderboard,
    RatingHistory,
)

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
