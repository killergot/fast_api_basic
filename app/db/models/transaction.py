from sqlalchemy import Column, Integer, ForeignKey,ForeignKeyConstraint, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.psql import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class BankTransaction(Base):
    __tablename__ = 'bank_transaction'
    __table_args__ = (
        ForeignKeyConstraint(
            ['account_id', 'user_id'],
            ['bank_account.account_id', 'bank_account.user_id']
        ),
    )

    transaction_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    account_id: Mapped[Integer] = mapped_column(Integer, nullable=False)
    amount: Mapped[Integer] = mapped_column(Integer, nullable=False)
    signature: Mapped[str] = mapped_column(Text, nullable=False)

    bank_accounts = relationship('BankAccount',
                                back_populates='transactions',
                                foreign_keys=[account_id, user_id])
    user = relationship('User', back_populates='transactions')
