from typing import List

from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.bank_account import AccountCRUD
from app.database import get_db
from app.crud.auth import UserCRUD
from app.shemas.bank_account import BankAccountOut

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(UserCRUD.get_current)])
async def create_account(db: AsyncSession = Depends(get_db),
                         user = Depends(UserCRUD.get_current)):
    return await AccountCRUD.create(db, user['id'])


@router.get("/all", status_code=status.HTTP_200_OK,
            dependencies=[Depends(UserCRUD.get_current)],
            response_model=List[BankAccountOut])
async def get_all_accounts(db: AsyncSession = Depends(get_db),
                           user = Depends(UserCRUD.get_current)):
    return await AccountCRUD.get_all(db, user['id'])

@router.get("/{account_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(UserCRUD.get_current)],
            response_model=BankAccountOut)
async def get_account(account_id: int,
                      db: AsyncSession = Depends(get_db),
                      user = Depends(UserCRUD.get_current)):
    return await AccountCRUD.get_one(db, account_id, user['id'])

@router.delete("/{account_id}", status_code=status.HTTP_200_OK,
               dependencies=[Depends(UserCRUD.get_current)])
async def try_delete_account(account_id: int):
    return {'msg': 'You can not delete your bank account:)'}



