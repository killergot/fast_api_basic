from pydantic import BaseModel, field_validator

class BankAccountOut(BaseModel):
    id: int
    owner_id: int
    balance: int




