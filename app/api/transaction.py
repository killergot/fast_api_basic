from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.crud.transaction import TransactionCRUD
from app.database import get_db, create_db
from app.crud.auth import UserCRUD
from app.shemas.transaction import TransactionIn, TransactionOtherIn, TransactionOut

router = APIRouter(prefix="/transaction", tags=["transaction"])

@router.post("/me", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(UserCRUD.get_current)])
async def do_transaction(db: Session = Depends(get_db),
                         user = Depends(UserCRUD.get_current)):
    pass

@router.post("/other", status_code=status.HTTP_201_CREATED,
             response_model=TransactionOut)
async def do_transaction(transaction: TransactionOtherIn,
                         db: Session = Depends(get_db)):
    return TransactionCRUD.create(db,
                                  transaction.user_id,
                                  transaction.account_id,
                                  transaction.amount,
                                  transaction.transaction_id,
                                  transaction.signature)

@router.get("/all", status_code=status.HTTP_200_OK,
            dependencies=[Depends(UserCRUD.get_current)])
async def get_all_transactions(db: Session = Depends(get_db),
                               user = Depends(UserCRUD.get_current)):
    pass

@router.get("/{account_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(UserCRUD.get_current)])
async def get_transaction(account_id: int,
                          db: Session = Depends(get_db),
                          user = Depends(UserCRUD.get_current)):
    pass

@router.delete("/{account_id}", status_code=status.HTTP_200_OK,
               dependencies=[Depends(UserCRUD.get_current)])
async def try_delete_transaction(account_id: int,
                                 db: Session = Depends(get_db),
                                 user = Depends(UserCRUD.get_current)):
    return {'msg': 'You can not delete your bank transaction:)'}




