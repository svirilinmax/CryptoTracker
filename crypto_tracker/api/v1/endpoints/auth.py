from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import verify_password, make_token, get_current_user
from models.database import User
from models.schemas import UserResponse, UserCreateRequest, UserLoginRequest, Token
from crud.user import get_user_by_email, get_user_by_username, create_user


router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)):

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
        created_at=user.created_at
    )


@router.post("/login", response_model= Token)
async def login(credentials: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, credentials.email)

    if not user:
        raise HTTPException(401, "Invalid email or password")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    if not user.is_active:
        raise HTTPException(400, "Account Deactivated")

    token = make_token(user.id, user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_use