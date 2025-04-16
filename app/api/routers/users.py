from idlelib.window import add_windows_to_menu

from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_user_service
from app.services import user_service
from app.services.role_service import ADMIN_ROLE
from app.shemas.user import UserOut, UserUpdateIn

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

@router.get("/get_all", status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_role(ADMIN_ROLE))])
async def get_all_users(user_service = Depends(get_user_service)):
    return await user_service.get_all_users()

@router.patch("/update_user", response_model=UserOut, status_code=status.HTTP_200_OK,
              dependencies=[Depends(require_role(ADMIN_ROLE))])
async def update_user(user: UserUpdateIn, user_service = Depends(get_user_service)):
    return await user_service.update_user(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role(ADMIN_ROLE))])
async def delete_user(user_id: int, user_service = Depends(get_user_service)):
    await user_service.del_user_by_id(user_id)