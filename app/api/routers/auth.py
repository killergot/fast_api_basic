from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.auth import get_auth_service
from app.api.depencies.db import get_db

from app.shemas.auth import UserOut, UserIn, UserLogin, UserSessionOut
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, service: AuthService = Depends(get_auth_service)):
    return await service.register(user)

@router.post("/login", response_model=UserSessionOut, status_code=status.HTTP_201_CREATED)
async def login(user: UserLogin, service: AuthService = Depends(get_auth_service)):
    return await service.login(user)

# @router.get("/get_me", response_model=UserOut, status_code=status.HTTP_200_OK,
#             dependencies=[Depends(UserCRUD.get_current)])
# async def get_info_about_me(user = Depends(UserCRUD.get_current), db: AsyncSession = Depends(get_db)):
#     user = await UserCRUD.get_if_exist(db, user['email'])
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_UNAUTHORIZED)
#     return UserOut.model_validate(user)

