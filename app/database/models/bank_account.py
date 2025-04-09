from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
from sqlalchemy.dialects.postgresql import UUID

class BankAccount(Base):
    __tablename__ = 'bank_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    balance = Column(Integer, nullable=False, default=0)

    owner = relationship('User', back_populates='bank_accounts')
    transactions = relationship('BankTransaction', back_populates='bank_accounts')