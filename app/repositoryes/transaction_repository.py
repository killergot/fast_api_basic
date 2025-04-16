from typing import Optional
from uuid import UUID

from sqlalchemy import select

from app.repositoryes.template import TemplateRepository
from app.db import BankTransaction
from app.core.except_handler import except_handler


class TransactionRepository(TemplateRepository):

    async def get_all(self):
        data = select(BankTransaction)
        transactions = await self.db.execute(data)
        return transactions.scalars().all()

    async def get_all_by_user(self, user_id):
        data = select(BankTransaction).where(BankTransaction.user_id == user_id)
        transactions = await self.db.execute(data)
        return transactions.scalars().all()

    async def get_by_id(self, transaction_id: UUID):
        return await self.db.get(BankTransaction, transaction_id)

    async def create(self,transaction_id: UUID,
                     user_id: int,
                     account_id: int,
                     amount: int,
                     signature: str) -> BankTransaction:
        new_transaction = BankTransaction(transaction_id=transaction_id,
                                   user_id=user_id,
                                   account_id=account_id,
                                   amount=amount,
                                   signature=signature)
        print(BankTransaction.__table__.columns.keys())

        self.db.add(new_transaction)
        await self.db.commit()
        await self.db.refresh(new_transaction)

        return new_transaction

    @except_handler
    async def delete(self, transaction_id: UUID) -> bool:
        await self.db.delete(await self.db.get(BankTransaction, transaction_id))
        return True
