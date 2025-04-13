from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status


from app.repositoryes.bank_account_repository import BankAccountRepository
from app.shemas.bank_account import BankAccountOut, BankAccountUserIn


class BankAccountService:
    def __init__(self, db: AsyncSession):
        self.repo = BankAccountRepository(db)

    async def get_account(self,account: BankAccountUserIn):
        account = await self.repo.get_one(account.account_id,account.user_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Account not found')
        return BankAccountOut.model_validate(account)

    async def create_account(self,account: BankAccountUserIn):
        if await self.repo.get_one(account.account_id,account.user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Account already exists')
        account = await self.repo.create(account.account_id,account.user_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Bad parameters')
        return BankAccountOut.model_validate(account)

    async def get_all_by_user(self,user_id: int):
        accounts = await self.repo.get_all_by_user(user_id)
        return accounts

    async def delete_account(self,account: BankAccountUserIn):
        if not await self.repo.delete(account.account_id,account.user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Bad parameters')
        return {'ok': True}



