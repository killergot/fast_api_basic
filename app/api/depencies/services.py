from fastapi import  Depends


from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depencies.db import get_db
from app.services.auth_service import AuthService
from app.services.bank_account_service import BankAccountService
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_bank_account_service(db: AsyncSession = Depends(get_db)):
    return BankAccountService(db)

async def get_bank_transaction_service(db: AsyncSession = Depends(get_db)):
    return TransactionService(db)