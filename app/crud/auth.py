from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.database.models.auth import User
from app.services.hash import encode_data
from app.services.jwt import get_jwt, verify_jwt
from app.shemas.auth import UserIn, UserOut, UserSessionOut

class UserCRUD:
    security = HTTPBearer()
    @staticmethod
    async def get_if_exist(db: AsyncSession, email):
        stmt = select(User).filter(User.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def create(cls, db: AsyncSession, user: UserIn):
        if await cls.get_if_exist(db, user.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Email already registered')
        # Тут возможно стоит поменять на то, что не стоит выдавать инфу о существующих пользователях
        # Точнее вообще никакой инфы, всегда отвечать ok True, чтоб нельзя было перебрать базу пользователей

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            password=encode_data(user.password)
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return UserOut.model_validate(db_user)


    # В данном случае для ТЗ достаточно просто выдавать jwt
    # Нет необходимости сохранять сессии
    @classmethod
    async def login(cls, db: AsyncSession, email: str, password: str):
        user = await cls.get_if_exist(db, email)
        if not user or user.password != encode_data(password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="email or password incorrect")
        token = get_jwt(user.id, email)
        return UserSessionOut.model_validate(token)

    @classmethod
    def get_current(cls, credentials: HTTPAuthorizationCredentials = Depends(security),
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

        if cls.get_if_exist(db, claims['email']):
            return claims
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="email not registered"
        )


