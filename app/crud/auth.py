from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.database.models.auth import User
from app.services.jwt import  get_jwt
from app.shemas.auth import UserIn, UserOut, UserSessionOut
from hashlib import sha256



class UserService:
    @classmethod
    def get_user_if_user_exist(cls,db: Session, email):
        return db.query(User).filter(User.email == email).first()

    @classmethod
    def encode_password(cls,password):
        return sha256(password.encode()).hexdigest()

    @classmethod
    def create_user(cls,db: Session, user: UserIn):
        if cls.get_user_if_user_exist(db, user.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
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
        token = get_jwt(email)
        return UserSessionOut.model_validate(token)