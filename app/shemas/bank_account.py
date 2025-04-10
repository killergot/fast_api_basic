from pydantic import BaseModel,ConfigDict

class BankAccountIn(BaseModel):
    id: int

class BankAccountOut(BankAccountIn):
    user_id: int
    balance: int

    model_config = ConfigDict(from_attributes=True)