import uuid
from inspect import signature

from typing import Optional

from fastapi import HTTPException,status
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.bank_account import BankAccount
from app.db.models.transaction import BankTransaction
from app.repositoryes.bank_account_repository import BankAccountRepository

from app.repositoryes.transaction_repository import TransactionRepository
from app.shemas.transaction import TransactionOut, TransactionWebhookIn, TransactionIn, TransactionCreateIn
from app.utils.signature import get_signature


class TransactionService:
    def __init__(self, db: AsyncSession):
        self.repo = TransactionRepository(db)

    async def _get(self, transaction_id: UUID) -> BankTransaction:
        transaction = await self.repo.get_by_id(transaction_id)
        if transaction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Transaction not found')
        return transaction

    async def get(self, transaction_id: UUID):
        return TransactionOut.model_validate(await self._get(transaction_id))

    async def get_from_user(self, transaction_id: UUID, user_id: int):
        transaction: BankTransaction = await self._get(transaction_id)
        if transaction.user_id != user_id:
            # Подумал, что лучше просто не сообщать о таких транзакциях,если они есть
            # В таком случае при переборе не получится узнать id приватных транзакций
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Transaction not found')
        return TransactionOut.model_validate(transaction)


    async def check_webhook(self, transaction: TransactionWebhookIn):
        sign_try = get_signature(
            transaction.account_id,
            transaction.amount,
            transaction.transaction_id,
            transaction.user_id
        )
        if transaction.signature is None or sign_try != transaction.signature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Signature does not valide')
        return await self.create(TransactionCreateIn(**transaction.model_dump()))

    async def create(self, transaction: TransactionCreateIn):
        if await self.repo.get_by_id(transaction.transaction_id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Transaction already exists')

        # я не придумал ничего лучше, ибо я только в этом методе его вызываю
        # Если будет больше вызовов, то добавить BankAccountRepository в __init__
        account_repo = BankAccountRepository(self.repo.db)
        account = await account_repo.get_one(transaction.account_id, transaction.user_id)
        if account is None:
            _ = await account_repo.create(transaction.account_id, transaction.user_id)

        return await self.repo.create(**transaction.model_dump())

    async def create_from_user(self,transaction: TransactionIn, user_id: int):
        sign = get_signature(
            transaction.account_id,
            transaction.amount,
            transaction.transaction_id,
            user_id
        )
        return await self.create(TransactionCreateIn(signature = sign,user_id=user_id,**(transaction.model_dump())))


    async def get_all_by_user(self, user_id: int):
        data = await self.repo.get_all_by_user(user_id)
        return data

    async def delete(self, transaction_id: UUID):
        return await self.repo.delete(transaction_id)


