from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

MIN_LEN_PASS: int = 2

class PasswordValidatorMixin(BaseModel):
    password: str = Field(min_length=MIN_LEN_PASS)


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: int = 0

class UserIn(UserBase,PasswordValidatorMixin):
    pass


class UserUpdateIn(PasswordValidatorMixin):
    id: int
    full_name: Optional[str] = None
    password: Optional[str] = Field(min_length=MIN_LEN_PASS,default=None)

    @model_validator(mode='after')
    def at_least_one_field(self):
        if not self.full_name and not self.password:
            raise ValueError("Хотя бы одно поле (password или full_name) должно быть заполнено.")
        return self


class UserOut(UserBase):
    id: int

    model_config = {
        'from_attributes': True
    }


class UserLogin(PasswordValidatorMixin):
    email: EmailStr

class UserSessionOut(BaseModel):
    access_token: str
    expires_at: datetime

