from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import AsyncSessionLocal
from app.models.user import User
from fastapi import WebSocket


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.scalar(
        select(User).where(User.user_id == int(user_id))
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


async def require_profile_completed(
    user: User = Depends(get_current_user),
) -> User:
    if not user.profile_completed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Complete your profile first",
        )
    return user


async def get_current_user_ws(websocket: WebSocket) -> User:
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=1008)
        raise RuntimeError("Missing token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError()
    except JWTError:
        await websocket.close(code=1008)
        raise RuntimeError("Invalid token")

    async with AsyncSessionLocal() as db:
        user = await db.scalar(
            select(User).where(User.user_id == int(user_id))
        )

        if not user:
            await websocket.close(code=1008)
            raise RuntimeError("User not found")

        return user
