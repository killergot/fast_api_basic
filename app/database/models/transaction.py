from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class BankTransaction(Base):
    __tablename__ = 'bank_transaction'

    transaction_id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('bank_account.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    signature = Column(Text, nullable=False)

    bank_accounts = relationship('BankAccount',
                                back_populates='transactions')
    user = relationship('User', back_populates='transactions')
