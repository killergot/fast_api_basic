from pydantic import BaseModel,ConfigDict

class BankAccountOut(BaseModel):
    id: int
    user_id: int
    balance: int

    model_config = ConfigDict(from_attributes=True)