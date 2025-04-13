from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, PrimaryKeyConstraint
from app.db.psql import Base

class BankAccount(Base):
    __tablename__ = 'bank_account'
    __table_args__ = (
        PrimaryKeyConstraint('account_id', 'user_id'),
    )

    account_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    owner: Mapped["User"] = relationship('User', back_populates='bank_accounts')
    transactions: Mapped[list["BankTransaction"]] = relationship('BankTransaction', back_populates='bank_accounts')
