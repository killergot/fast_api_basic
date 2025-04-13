from pydantic import BaseModel,ConfigDict, field_validator
from fastapi import HTTPException,status

class BankAccountIn(BaseModel):
    account_id: int

    @field_validator('account_id')
    @staticmethod
    def GT0(value):
        if value <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='account id must be greater than 0')
        return value

class BankAccountUserIn(BankAccountIn):
    user_id: int


class BankAccountOut(BankAccountUserIn):
    balance: int

    model_config = ConfigDict(from_attributes=True)


if __name__ == '__main__':
    a = BankAccountIn(account_id=1)
    b = BankAccountUserIn(user_id = 1,**a.model_dump())
    print(b.model_dump())