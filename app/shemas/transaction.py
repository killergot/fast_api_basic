from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class TransactionBase(BaseModel):
    account_id: int = Field(gt=0)
    # Я посчитал, что 0 и отрицательные тразнакции у нас быть не могут)
    amount: int = Field(gt=0)

class TransactionIn(TransactionBase):
    transaction_id: UUID

class TransactionWebhookIn(TransactionIn):
    signature: str
    user_id: int

class TransactionCreateIn(TransactionWebhookIn):
    pass

class TransactionOut(TransactionIn):
    user_id: int

    model_config = ConfigDict(from_attributes=True)