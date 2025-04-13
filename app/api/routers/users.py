from idlelib.window import add_windows_to_menu

from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_user_service
from app.services.role_service import ADMIN_ROLE
from app.shemas.auth import UserOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/get_me", response_model=UserOut, status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def get_me(user = Depends(get_current_user)):
    return user

@router.get("/get_user", response_model=UserOut, status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_role(ADMIN_ROLE))])
async def get_user_by_id(user_id: int,
                         user_service = Depends(get_user_service)):
    return await user_service.get_user_by_id(user_id)