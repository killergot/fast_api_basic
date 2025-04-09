from typing import Optional, List, Type
from uuid import UUID

from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.database.models.bank_account import BankAccount
from app.shemas.bank_account import BankAccountOut


class AccountCRUD:
    @staticmethod
    def get_if_exist(db: Session, account_id: int, user_id: int) -> Optional[BankAccount]:
        account_db: BankAccount = db.query(BankAccount).filter(BankAccount.id == account_id).first()
        if account_db is None:
            return None
        # Это нужно делать как-то более умно
        # Равенство не срабатывало без str из-за разности типов
        if str(user_id) != str(account_db.user_id):
            return None
        return account_db


    @classmethod
    def create(cls, db: Session, user: int) -> BankAccountOut:
        try:
            db_account = BankAccount(user_id=user)
            db.add(db_account)
            db.commit()
            db.refresh(db_account)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        return BankAccountOut.model_validate(db_account)

    @classmethod
    def get_all(cls, db: Session, user: int) -> list[Type[BankAccount]]:
        return (db.query(BankAccount)
                .filter(BankAccount.user_id == user).all())

    @classmethod
    def get_one(cls, db: Session, account_id: int, user_id: int) -> Optional[BankAccountOut]:
        db_account = cls.get_if_exist(db, account_id,user_id)
        if not db_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Account not found")
        return BankAccountOut.model_validate(db_account)


