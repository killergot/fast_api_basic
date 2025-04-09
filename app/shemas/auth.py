from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID

MIN_LEN_PASS: int = 2

class PasswordValidatorMixin(BaseModel):
    password: str

    @field_validator('password')
    @classmethod
    def check_password(cls, value):
        if len(value) < MIN_LEN_PASS:
            raise ValueError(f'Password must be at least {MIN_LEN_PASS} characters')
        return value


class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserIn(UserBase,PasswordValidatorMixin):
    pass


class UserOut(UserBase):
    id: UUID

    model_config = {
        'from_attributes': True
    }


class UserLogin(PasswordValidatorMixin):
    email: EmailStr

class UserSessionOut(BaseModel):
    access_token: str
    expires_at: datetime