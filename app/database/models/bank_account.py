from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class BankAccount(Base):
    __tablename__ = 'bank_account'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    balance = Column(Integer, nullable=False)

    owner = relationship('User', back_populates='bank_accounts')
    transactions = relationship('BankTransaction', back_populates='bank_accounts')