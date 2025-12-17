from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from db.base import Base


class User(Base):
    """User model - stores Telegram user information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    nickname = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_premium_tg_user = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship to offers
    offers = relationship("Offer", back_populates="user", cascade="all, delete-orphan")
    pay_clicks = relationship("PayClick", back_populates="user", cascade="all, delete-orphan")


class Offer(Base):
    """Offer model - stores special offer information and expiration dates"""
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    offer_expiration_date = Column(DateTime(timezone=True), nullable=False, index=True)
    last_reminder_sent = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    reminder_type = Column(String(50), nullable=True)  # 'last_call' or None for regular reminders
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Lead magnet tracking
    lesson_clicked_at = Column(DateTime(timezone=True), nullable=True, index=True)  # When user clicked "забрать урок"
    first_reminder_sent = Column(DateTime(timezone=True), nullable=True)  # First reminder sent (1 hour after click)
    second_reminder_sent = Column(DateTime(timezone=True), nullable=True)  # Second reminder sent (12 hours after click)

    # Relationship to user
    user = relationship("User", back_populates="offers")


class PayClick(Base):
    """Analytics: store pay button click events"""
    __tablename__ = "pay_clicks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="pay_clicks")

