from fastapi import Depends, status, HTTPException
from fastapi.routing import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.guard import require_role
from app.api.depencies.services import get_auth_service
from app.api.depencies.db import get_db
from app.services.role_service import ADMIN_ROLE

from app.shemas.user import UserOut, UserIn, UserLogin, UserSessionOut
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserOut,
             status_code=status.HTTP_201_CREATED
             ,dependencies=[Depends(require_role(ADMIN_ROLE))],
             summary='Register a new user',
             description='Create a new user in database. Requre email and password.\n'
                         '- Only administrators can create new users.')
async def create_user(user: UserIn, service: AuthService = Depends(get_auth_service)):
    return await service.register(user)

@router.post("/login", response_model=UserSessionOut, status_code=status.HTTP_201_CREATED,
             summary='Login a user',
             description='Check credentials for a user and get token if successful')
async def login(user: UserLogin, service: AuthService = Depends(get_auth_service)):
    return await service.login(user)



