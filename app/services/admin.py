from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.db import get_db
from app.db.models.auth import User
from app.db.models.bank_account import BankAccount
from app.utils.jwt import get_jwt, verify_jwt
from app.services.auth import UserCRUD

class AdminCRUD:
    security = HTTPBearer()

    @classmethod
    async def get_users(cls, db: AsyncSession):
        data = select(User)
        result = await db.execute(data)
        return result.scalars().all()

    @classmethod
    async def get_user_accounts(cls, db: AsyncSession, user_id: int):
        data = select(BankAccount).where(BankAccount.user_id == user_id)
        result = await db.execute(data)
        return result.scalars().all()

    @staticmethod
    async def get_current(credentials: HTTPAuthorizationCredentials = Depends(security),
                          db: AsyncSession = Depends(get_db)):
        if not credentials or not credentials.scheme.lower() == "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization scheme"
            )

        token = credentials.credentials
        claims = verify_jwt(token)
        if not claims:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        user = await UserCRUD.get_if_exist(db, claims['email'])
        if user:
            if user.is_admin:
                return claims
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not admin"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="email not registered"
        )


