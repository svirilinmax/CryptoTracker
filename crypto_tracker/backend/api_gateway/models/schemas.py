from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# -------------Users---------------
class UserBase(BaseModel):
    """Базовая схема пользователя"""

    email: EmailStr
    username: str


class User(UserBase):
    """Схема для возврата данных пользователя (без пароля!)"""

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"password_hash"}


class UserCreateRequest(UserBase):
    """Схема для создания пользователя (регистрация)"""

    password: str


class UserLoginRequest(BaseModel):
    """Схема для входа в систему"""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Схема для ответа с данными пользователя"""

    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        exclude = {"password_hash"}


# -------------Asset---------------
# TODO: Добавьте валидацию полей с Field()
# Нет проверок на пустые строки, отрицательные цены, min > max
# См. REVIEW.md секция "Критические проблемы" пункт 3
class AssetBase(BaseModel):
    """Базовая схема валюты"""

    symbol: str  # TODO: Field(min_length=2, max_length=10, pattern="^[A-Z]+$")
    min_price: float  # TODO: Field(gt=0)
    max_price: float  # TODO: Field(gt=0) + validator для max_price > min_price


class AssetCreateRequest(AssetBase):
    """Схема для создания валюты"""

    pass


class AssetUpdateRequest(BaseModel):
    """Схема для обновления валюты"""

    symbol: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    is_active: Optional[bool] = None


class AssetResponse(BaseModel):
    """Схема для ответа с данными валюты"""

    id: int
    user_id: int
    symbol: str
    min_price: float
    max_price: float
    current_price: Optional[float] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# -------------PriceHistory---------------
class PriceHistoryBase(BaseModel):
    """Базовая схема истории цен"""

    price: float


class PriceHistoryCreate(PriceHistoryBase):
    """Схема для создания записи истории цен"""

    asset_id: int


class PriceHistory(PriceHistoryBase):
    """Полная схема истории цен"""

    id: int
    asset_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# -------------Token---------------
class Token(BaseModel):
    """Схема для JWT токена"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Данные внутри JWT токена"""

    username: Optional[str] = None
    user_id: Optional[int] = None
