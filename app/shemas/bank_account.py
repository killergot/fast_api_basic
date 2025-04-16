from pydantic import BaseModel,ConfigDict, Field
from fastapi import HTTPException,status

class BankAccountIn(BaseModel):
    account_id: int = Field(gt=0)

class BankAccountUserIn(BankAccountIn):
    user_id: int = Field(gt=0)


class BankAccountOut(BankAccountUserIn):
    balance: int

    model_config = ConfigDict(from_attributes=True)


if __name__ == '__main__':
    a = BankAccountIn(account_id=1)
    b = BankAccountUserIn(user_id = 1,**a.model_dump())
    print(b.model_dump())