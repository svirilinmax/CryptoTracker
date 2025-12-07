from core.database import get_db
from core.security import get_current_user, make_token, verify_password
from fastapi import APIRouter, Depends, HTTPException, Request
from models.database import User
from models.schemas import Token, UserCreateRequest, UserLoginRequest, UserResponse
from repositories.user import create_user, get_user_by_email, get_user_by_username
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
@limiter.limit("3/hour")
async def register(
    request: Request, user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)
):
    if await get_user_by_email(db, user_data.email):
        raise HTTPException(400, "Email already taken")

    if await get_user_by_username(db, user_data.username):
        raise HTTPException(400, "Username already taken")

    user = await create_user(db, user_data)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        created_at=user.created_at,
    )


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request, credentials: UserLoginRequest, db: AsyncSession = Depends(get_db)
):
    user = await get_user_by_email(db, credentials.email)
    dummy_hash = (
        "$pbkdf2-sha256$29000$N2YMIWQsBWBMae09x1jrPQ$1t8iyB2A.WF/Z5JZv."
        "lfCIhXXN33N23OSgQYThBYRfw"
    )

    if user:
        is_valid = verify_password(credentials.password, user.password_hash)
    else:
        verify_password(credentials.password, dummy_hash)
        is_valid = False

    if not is_valid or not user:
        raise HTTPException(401, "Invalid email or password")

    if not user.is_active:
        raise HTTPException(400, "Account Deactivated")

    token = make_token(user.id, user.username)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
