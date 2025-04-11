from pydantic import BaseModel,ConfigDict, field_validator

class BankAccountIn(BaseModel):
    id: int

    @field_validator('id')
    @staticmethod
    def GT0(value):
        if value <= 0:
            raise Exception('amount must be greater than 0')
        return value

class BankAccountOut(BankAccountIn):
    user_id: int
    balance: int

    model_config = ConfigDict(from_attributes=True)