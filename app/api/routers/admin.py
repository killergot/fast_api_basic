from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.admin import AdminCRUD
from app.api.depencies.db import get_db

from app.shemas.auth import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", status_code=status.HTTP_200_OK,
            dependencies=[Depends(AdminCRUD.get_current)])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await AdminCRUD.get_users(db)

@router.get("/user_accounts/{user_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(AdminCRUD.get_current)])
async def read_user_accounts(user_id : int,db: AsyncSession = Depends(get_db)):
    return await AdminCRUD.get_user_accounts(db, user_id)

@router.put("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(user: UserOut, db: AsyncSession = Depends(get_db)):
    pass


