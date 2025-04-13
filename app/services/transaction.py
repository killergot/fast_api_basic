import uuid
from functools import singledispatchmethod, reduce
from operator import concat
from typing import Optional

from fastapi import HTTPException,status
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.config import load_config
from app.db.models.transaction import BankTransaction
from app.services.bank_account import AccountCRUD
from app.utils.hash import encode_data
from app.shemas.transaction import TransactionOut

SECRET_KEY = load_config().secret_keys.secret_key_signature

class TransactionCRUD:
    @staticmethod
    async def get_if_exist( db: AsyncSession, transaction_id: UUID, user_id: int):
        return await db.get(BankTransaction, transaction_id)


    @staticmethod
    def get_signature(*args):
        data = reduce(concat, [*map(str,args),SECRET_KEY])
        return encode_data(data)

    @classmethod
    async def create_from(cls,db: AsyncSession,
                  user_id: int,
                  account_id: int,
                  amount: int,
                  transaction_id,
                  signature):

        sign_try = cls.get_signature(
            account_id,
            amount,
            transaction_id,
            user_id
        )

        if signature is None or sign_try != signature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Signature does not valide')
        return await cls.create(db, user_id, account_id, amount,transaction_id, sign_try)

    @classmethod
    async def create(cls,db: AsyncSession,
                  user_id: int,
                  account_id: int,
                  amount: int,
                  transaction_id: Optional[UUID] = None,
                  signature: Optional[str] = None):
        transaction_id = transaction_id or uuid.uuid4()
        account_db = await AccountCRUD.get_if_exist(db, account_id,user_id)
        if account_db is None:
            # Создаем кошель, если его нема
            await AccountCRUD.create(
                db, account_id, user_id
            )
        if transaction_id is not None and await cls.get_if_exist(db,transaction_id, user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Transaction already exists')

        transaction_db = BankTransaction(
            transaction_id=transaction_id,
            user_id=user_id,
            account_id=account_id,
            amount=amount,
            signature=signature if signature is not None else cls.get_signature(account_id,
                                                                                amount,
                                                                                transaction_id,
                                                                                user_id),
        )
        db.add(transaction_db)
        await db.commit()
        await db.refresh(transaction_db)
        return TransactionOut.model_validate(transaction_db)

    @staticmethod
    async def get_all(db: AsyncSession, user_id: int):
        data = (select(BankTransaction)
                .where(BankTransaction.user_id == user_id))

        res = await db.execute(data)
        res = res.scalars().all()
        result = [{"id": t.transaction_id, "amount": t.amount, "account": t.account_id} for t in res]
        return result


