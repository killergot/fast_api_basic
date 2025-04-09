from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.database.models.bank_account import BankAccount


class AccountCRUD:
    @staticmethod
    def is_exist_account(db: Session, account_id: int):
        return db.query(BankAccount).filter(BankAccount.id == account_id).one()

    @classmethod
    def create_account(cls, db: Session, user: id):
        db_account = BankAccount()

