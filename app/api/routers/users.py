from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.guard import get_current_user
from app.shemas.auth import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/get_me", response_model=UserOut, status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def get_info_about_me(user = Depends(get_current_user)):
    return user