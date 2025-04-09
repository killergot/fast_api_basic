from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.database.models.bank_account import BankAccount
from app.shemas.bank_account import BankAccountOut


class AccountCRUD:
    @staticmethod
    def is_exist_account(db: Session, account_id: int):
        return db.query(BankAccount).filter(BankAccount.id == account_id).one()

    @classmethod
    def create_account(cls, db: Session, user: id):
        db_account = BankAccount(user_id=user)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return BankAccountOut.model_to_dict(db_account)


