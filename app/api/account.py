from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.jwt import get_current_user

router = APIRouter(prefix="/account", tags=["account"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_user)])
async def create_account(db: Session = Depends(get_db),
                         user = Depends(get_current_user)):
    pass


@router.get("/all", status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user)])
async def get_all_accounts(db: Session = Depends(get_db),
                         user = Depends(get_current_user)):
    pass

@router.get("/{account_id}", status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user)])
async def get_account(account_id: int,
                         db: Session = Depends(get_db),
                         user = Depends(get_current_user)):
    pass

@router.delete("/{account_id}", status_code=status.HTTP_200_OK,
             dependencies=[Depends(get_current_user)])
async def try_delete_account(account_id: int,
                         db: Session = Depends(get_db),
                         user = Depends(get_current_user)):
    return {'msg': 'You can not delete your bank account:)'}



