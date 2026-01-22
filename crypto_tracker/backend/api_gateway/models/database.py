from datetime import datetime

from core.database import Base
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """
    Модель пользователя системы
    Хранит учетные данные и основную информацию о пользователе
    """

    __tablename__ = "users"

    # Основные поля пользователя
    id = Column(Integer, primary_key=True, index=True)  # Уникальный id
    username = Column(String, unique=True, index=True)  # Логин пользователя
    email = Column(String, unique=True, index=True)  # Email, тоже уникальный для входа
    password_hash = Column(String)  # Хеш пароля
    is_active = Column(Boolean, default=True)  # Флаг активности аккаунта
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата регистрации

    assets = relationship("Asset", back_populates="user")


class Asset(Base):
    """
    Модель актива (валюты) для отслеживания
    Каждая валюта привязан к конкретному пользователю
    """

    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный id
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )  # Ссылка на владельца
    symbol = Column(
        String, index=True
    )  # Название валюты (например: "bitcoin", "ethereum")
    min_price = Column(Float)  # Нижний порог цены для уведомления
    max_price = Column(Float)  # Верхний порог цены для уведомления
    current_price = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # Дата добавления актива
    is_active = Column(Boolean, default=True)  # Флаг активности отслеживания

    user = relationship("User", back_populates="assets")
    price_history = relationship("PriceHistory", back_populates="asset")


class PriceHistory(Base):
    """
    История цен активов
    Хранит все изменения цен для построения графиков и аналитики
    """

    __tablename__ = "price_history"

    # Поля для записи истории
    id = Column(
        Integer, primary_key=True, index=True
    )  # Уникальный идентификатор записи
    asset_id = Column(
        Integer, ForeignKey("assets.id", ondelete="CASCADE")
    )  # Ссылка на актив (внешний ключ)
    price = Column(Float)  # Цена актива в момент записи
    recorded_at = Column(DateTime, default=datetime.utcnow)  # Временная записи

    asset = relationship(
        "Asset", back_populates="price_history"
    )  # Позволяет получить доступ к данным актива из записи цены
