from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.psql import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class BankAccount(Base):
    __tablename__ = 'bank_account'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    balance = Column(Integer, nullable=False)

    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='bankAccount')