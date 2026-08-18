from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Any

from sqlalchemy import (
    BigInteger, Integer, String, Numeric, Boolean, Date, ForeignKey, Index, func
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger, unique=True, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    preferred_notification: Mapped[str] = mapped_column(
        String(50), default="telegram", server_default="telegram"
    )

    trackings: Mapped[list["Tracking"]] = relationship(
        "Tracking", back_populates="user", cascade="all, delete-orphan" # связывание с отслеживаниями, созданными пользователем
    )


class Tracking(Base):
    __tablename__ = "trackings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    origin_code: Mapped[str] = mapped_column(String(50), nullable=False)
    destination_code: Mapped[str] = mapped_column(String(50), nullable=False)
    origin_name: Mapped[str] = mapped_column(String(255), nullable=False)
    destination_name: Mapped[str] = mapped_column(String(255), nullable=False)
    departure_date: Mapped[date] = mapped_column(Date, nullable=False)
    target_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    car_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    transport_type: Mapped[str] = mapped_column(String(50), nullable=False)
    route: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="trackings") # связывание с пользователем, который создал отслеживание
    price_history: Mapped[list["PriceHistory"]] = relationship(
        "PriceHistory", back_populates="tracking", cascade="all, delete-orphan" # связывание с историей цен для данного отслеживания
    )

    __table_args__ = (
        Index(
            "idx_unique_tracking",
            "user_id",
            "origin_code",
            "destination_code",
            "departure_date",
            "transport_type",
            unique=True,
            postgresql_where=(is_active == True),
        ),
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), primary_key=True)
    tracking_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trackings.id", ondelete="CASCADE"), primary_key=True
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    carrier: Mapped[str] = mapped_column(String(255), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    details: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    tracking: Mapped["Tracking"] = relationship("Tracking", back_populates="price_history") # связывание с отслеживанием, к которому относится данная запись истории цен

    __table_args__ = (
        Index("idx_price_history_tracking_id", "tracking_id", time.desc()),
    )