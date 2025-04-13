from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, Field

MIN_LEN_PASS: int = 2

class PasswordValidatorMixin(BaseModel):
    password: str #Field(min_length=MIN_LEN_PASS)

    @field_validator('password')
    @staticmethod
    def check_password(value):
        if len(value) < MIN_LEN_PASS:
            raise ValueError(f'Password must be at least {MIN_LEN_PASS} characters')
        return value


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: int = 0

class UserIn(UserBase,PasswordValidatorMixin):
    pass


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