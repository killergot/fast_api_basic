import random

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, TIMESTAMP, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.psql import Base, engine
import uuid
from datetime import datetime

# Модель пользователей (users)
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    role = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,onupdate=datetime.utcnow)

    bank_accounts = relationship("BankAccount", back_populates="owner", cascade="all, delete, delete-orphan")
    transactions = relationship("BankTransaction", back_populates="user", cascade="all, delete, delete-orphan")


