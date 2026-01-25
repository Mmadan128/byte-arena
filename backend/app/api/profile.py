from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.services.codeforces import fetch_cf_user
from app.schemas.profile import ProfileSetupRequest

import secrets

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("/setup")
async def setup_profile(
    payload: ProfileSetupRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user.profile_completed:
        raise HTTPException(
            status_code=400,
            detail="Profile already completed",
        )

    cf_handle = payload.cf_handle

    cf_user = await fetch_cf_user(cf_handle)
    if not cf_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid Codeforces handle",
        )

    existing = await db.scalar(
        select(User).where(User.cf_handle == cf_handle)
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Codeforces handle already in use",
        )

    user.cf_handle = cf_handle
    user.cf_rating = cf_user.get("rating")
    user.profile_completed = True

    await db.commit()

    return {
        "message": "Profile completed",
        "cf_handle": cf_handle,
        "cf_rating": user.cf_rating,
    }

def generate_verification_token() -> str:
    return f"bytearena-{secrets.token_hex(6)}"

from app.schemas.profile import ProfileSetupRequest

@router.post("/verify/start")
async def start_cf_verification(
    payload: ProfileSetupRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cf_handle = payload.cf_handle

    cf_user = await fetch_cf_user(cf_handle)
    if not cf_user:
        raise HTTPException(400, "Invalid Codeforces handle")

    user.cf_handle = cf_handle
    user.cf_rating = cf_user.get("rating")

    token = generate_verification_token()
    user.cf_verify_token = token

    await db.commit()

    return {
        "message": "Add this token to your Codeforces organization field",
        "token": token,
        "cf_handle": cf_handle,
    }

from app.services.codeforces import verify_cf_ownership

@router.post("/verify/confirm")
async def confirm_cf_verification(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not user.cf_verify_token or not user.cf_handle:
        raise HTTPException(400, "Verification not started")

    cf_user = await fetch_cf_user(user.cf_handle)
    if not cf_user:
        raise HTTPException(400, "CF user not found")

    if not verify_cf_ownership(cf_user, user.cf_verify_token):
        raise HTTPException(400, "Token not found in CF organization")

    user.cf_verified = True
    user.cf_verify_token = None
    user.cf_rating = cf_user.get("rating")
    user.profile_completed = True

    await db.commit()

    return {
        "status": "verified",
        "cf_handle": user.cf_handle,
        "rating": user.cf_rating
    }