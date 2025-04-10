from uuid import UUID

from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.transaction import TransactionCRUD
from app.database import get_db, create_db
from app.crud.auth import UserCRUD
from app.shemas.transaction import TransactionIn, TransactionOtherIn, TransactionOut

router = APIRouter(prefix="/transaction", tags=["transaction"])

@router.post("/me", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(UserCRUD.get_current)])
async def do_transaction(transaction: TransactionIn,
                         db: AsyncSession = Depends(get_db),
                         user = Depends(UserCRUD.get_current)):
    return await TransactionCRUD.create(db,
                                  user['id'],
                                  transaction.account_id,
                                  transaction.amount)

@router.post("/other", status_code=status.HTTP_201_CREATED,
             response_model=TransactionOut)
async def do_transaction(transaction: TransactionOtherIn,
                         db: AsyncSession = Depends(get_db)):
    '''В общем я не знаю как надо было сделать уникальные транзакции:
    Для каждого или для всех. Я сделал так, что для всех пользователей
    uuid транзакции повторяться не может'''
    return await TransactionCRUD.create_from(db,
                                  transaction.user_id,
                                  transaction.account_id,
                                  transaction.amount,
                                  transaction.transaction_id,
                                  transaction.signature)

@router.get("/all", status_code=status.HTTP_200_OK,
            dependencies=[Depends(UserCRUD.get_current)])
async def get_all_transactions(db: AsyncSession = Depends(get_db),
                               user = Depends(UserCRUD.get_current)):
    return await TransactionCRUD.get_all(db,user['id'])

@router.get("/{transaction_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(UserCRUD.get_current)])
async def get_transaction(transaction_id: UUID,
                          db: AsyncSession = Depends(get_db),
                          user = Depends(UserCRUD.get_current)):
    temp = await TransactionCRUD.get_if_exist(db, transaction_id, user['id'])
    if temp is None or temp.user_id != user['id']:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Transaction not found")
    else:
        return TransactionOut.model_validate(temp)

@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK,
               dependencies=[Depends(UserCRUD.get_current)])
async def try_delete_transaction(transaction_id: UUID):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deleting transactions is not allowed by system policy"
    )




