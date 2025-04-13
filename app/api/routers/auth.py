from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.services import get_auth_service
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



