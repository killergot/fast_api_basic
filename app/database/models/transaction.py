from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class BankTransaction(Base):
    __tablename__ = 'bank_transaction'

    transaction_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    account_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('bank_account.id'), nullable=False)
    amount: Mapped[Integer] = mapped_column(Integer, nullable=False)
    signature: Mapped[str] = mapped_column(Text, nullable=False)

    bank_accounts = relationship('BankAccount',
                                back_populates='transactions')
    user = relationship('User', back_populates='transactions')
