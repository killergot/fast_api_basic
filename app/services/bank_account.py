from typing import Optional


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status


from app.db.models.bank_account import BankAccount
from app.shemas.bank_account import BankAccountOut


class AccountCRUD:
    @staticmethod
    async def get_if_exist(db: AsyncSession, account_id: int, user_id: int) -> Optional[BankAccount]:
        account_db: BankAccount = await db.get(BankAccount, (account_id, user_id))
        if account_db is None:
            return None
        return account_db

    @classmethod
    async def create(cls, db: AsyncSession,account_id : int, user: int) -> BankAccountOut:
        try:
            db_account = BankAccount(id = account_id, user_id=user)
            db.add(db_account)
            await db.commit()
            await db.refresh(db_account)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        return BankAccountOut.model_validate(db_account)

    @classmethod
    async def get_all(cls, db: AsyncSession, user: int) -> tuple[BankAccount]:
        data = select(BankAccount).where(BankAccount.user_id == user)
        result = await db.execute(data)
        return result.scalars().all()

    @classmethod
    async def get_one(cls, db: AsyncSession, account_id: int, user_id: int) -> BankAccountOut:
        try:
            db_account = await cls.get_if_exist(db, account_id,user_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Wrong in account_id, check this (mb < 0 ?)")
        if not db_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Account not found")
        return BankAccountOut.model_validate(db_account)


