from uuid import UUID
from pydantic import BaseModel, field_validator, ConfigDict


class TransactionIn(BaseModel):
    account_id: int
    amount: int

    @field_validator('amount')
    @staticmethod
    def GT0(value):
        if value <= 0:
           raise Exception('amount must be greater than 0')
        return value

    @field_validator('account_id')
    @staticmethod
    def GT0(value):
        if value <= 0:
            raise Exception('account_id must be greater than 0')
        return value



class TransactionOtherIn(TransactionIn):
    transaction_id: UUID
    signature: str
    user_id: int

class TransactionOut(TransactionIn):
    transaction_id: UUID
    user_id: int

    model_config = ConfigDict(from_attributes=True)