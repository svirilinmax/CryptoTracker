from backend.api_gateway.core.database import get_db
from backend.api_gateway.core.security import (
    get_current_user,
    make_token,
    verify_password,
)
from backend.api_gateway.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from backend.api_gateway.models.database import User
from backend.api_gateway.models.schemas import (
    Token,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

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
        created_at=user.created_at,
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, credentials.email)

    if not user:
        raise HTTPException(401, "Invalid email or password")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    if not user.is_active:
        raise HTTPException(400, "Account Deactivated")

    token = make_token(user.id, user.username)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
