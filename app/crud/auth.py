from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models.auth import User
from app.services.jwt import get_jwt, verify_jwt
from app.shemas.auth import UserIn, UserOut, UserSessionOut
from hashlib import sha256



class UserCRUD:
    security = HTTPBearer()
    @staticmethod
    def get_user_if_user_exist(db: Session, email):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def encode_password(password):
        return sha256(password.encode()).hexdigest()

    @classmethod
    def create_user(cls,db: Session, user: UserIn):
        if cls.get_user_if_user_exist(db, user.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Email already registered')
        # Тут возможно стоит поменять на то, что не стоит выдавать инфу о существующих пользователях
        # Точнее вообще никакой инфы, всегда отвечать ok True, чтоб нельзя было перебрать базу пользователей

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            password=cls.encode_password(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return UserOut.model_validate(db_user)


    # В данном случае для ТЗ достаточно просто выдавать jwt
    # Нет необходимости сохранять сессии
    @classmethod
    def login_user(cls,db: Session, email: str, password: str):
        user =cls.get_user_if_user_exist(db, email)
        if not user or user.password != cls.encode_password(password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="email or password incorrect")
        token = get_jwt(user.id, email)
        return UserSessionOut.model_validate(token)

    @classmethod
    def get_current_user(cls,credentials: HTTPAuthorizationCredentials = Depends(security),
                         db: Session = Depends(get_db)):
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

        if cls.get_user_if_user_exist(db, claims['email']):
            return claims
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="email not registered"
        )


