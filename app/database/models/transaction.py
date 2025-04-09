from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class BankTransaction(Base):
    __tablename__ = 'bank_transaction'

    transaction_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey('bank_account.id'), nullable=False)
    amount = Column(Integer, nullable=False)

    bank_account = relationship('BankAccount',
                                back_populates='transactions')
    user = relationship('User', back_populates='transactions')
