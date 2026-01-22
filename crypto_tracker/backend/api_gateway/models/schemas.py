from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# -------------Users---------------
class UserBase(BaseModel):
    """Базовая схема пользователя"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


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

    password: str = Field(..., min_length=12, max_length=128)

    @field_validator("password")
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        if not any(c in "!@#$%^&*" for c in v):
            raise ValueError("Password must contain special character")
        return v


class UserLoginRequest(BaseModel):
    """Схема для входа в систему"""

    email: EmailStr
    password: str = Field(..., min_length=1)


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
class CryptoSymbol(str, Enum):
    BTC = "BTC"
    ETH = "ETH"
    ADA = "ADA"
    DOT = "DOT"
    SOL = "SOL"


class AssetBase(BaseModel):
    """Базовая схема валюты"""

    symbol: CryptoSymbol
    min_price: float = Field(..., gt=0)
    max_price: float = Field(..., gt=0)

    @field_validator("max_price")
    @classmethod
    def validate_max_price(cls, v, info):
        if info.data and "min_price" in info.data and v <= info.data["min_price"]:
            raise ValueError("max_price должен быть больше min_price")
        return v


class AssetCreateRequest(AssetBase):
    """Схема для создания валюты"""

    pass


class AssetUpdateRequest(BaseModel):
    """Схема для обновления валюты"""

    symbol: Optional[str] = Field(None, min_length=2, max_length=10, pattern="^[A-Z]+$")
    min_price: Optional[float] = Field(None, gt=0)
    max_price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None

    @field_validator("max_price")
    @classmethod
    def validate_max_price(cls, v, info):
        if v is not None and info.data and "min_price" in info.data:
            min_price = info.data.get("min_price")
            if min_price is not None and v <= min_price:
                raise ValueError("max_price должен быть больше min_price")
        return v


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

    price: float = Field(..., gt=0)


class PriceHistoryCreate(PriceHistoryBase):
    """Схема для создания записи истории цен"""

    asset_id: int = Field(..., gt=0)


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
