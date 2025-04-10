import uuid
from functools import singledispatchmethod, reduce
from operator import concat
from typing import Optional

from fastapi import HTTPException,status
from uuid import UUID

from sqlalchemy.orm import Session

from app.config.config import load_config
from app.database.models.transaction import BankTransaction
from app.crud.bank_account import AccountCRUD
from app.services.hash import encode_data
from app.shemas.transaction import TransactionOut

SECRET_KEY = load_config().secret_keys.secret_key_signature

class TransactionCRUD:
    @staticmethod
    def get_if_exist( db: Session, transaction_id: UUID, user_id: int):
        temp =  (db.query(BankTransaction).
                filter(BankTransaction.transaction_id == transaction_id)
                .first())
        if temp and temp.user_id == user_id:
            return temp
        else:
            return None

    @staticmethod
    def get_signature(*args):
        data = reduce(concat, [*args,SECRET_KEY])
        return(encode_data(data))

    @classmethod
    def create(cls,db: Session,
                  user_id: int,
                  account_id: int,
                  amount: int,
                  transaction_id: Optional[UUID] = None,
                  signature: Optional[str] = None,):
        account_db = AccountCRUD.get_if_exist(db, account_id,user_id)
        if account_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Account not found')
        if transaction_id is not None and cls.get_if_exist(db,transaction_id, user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Transaction already exists')

        sign = cls.get_signature(
                str(account_id),
                str(amount),
                str(transaction_id),
                str(user_id)
            )
        if signature is not None and sign != signature:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Signature does not valide')

        transaction_db = BankTransaction(
            transaction_id=transaction_id if transaction_id is not None else uuid.uuid4(),
            user_id=user_id,
            account_id=account_id,
            amount=amount,
            signature=sign
        )
        db.add(transaction_db)
        db.commit()
        db.refresh(transaction_db)
        return TransactionOut.model_validate(transaction_db)

    @staticmethod
    def get_all(db: Session, user_id: int):
        res = db.query(BankTransaction).filter(BankTransaction.user_id==user_id).all()
        result = [{"id": t.transaction_id, "amount": t.amount, "account": t.account_id} for t in res]
        return result


