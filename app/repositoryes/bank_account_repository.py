from typing import Optional

from sqlalchemy import select

from app.db import BankAccount
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

class BankAccountRepository(TemplateRepository):

    async def get_all(self):
        data = select(BankAccount)
        accounts = await self.db.execute(data)
        return accounts.scalars().all()

    async def get_all_by_user(self, user_id: int):
        data = select(BankAccount).where(BankAccount.user_id == user_id)
        accounts = await self.db.execute(data)
        return accounts.scalars().all()

    async def get_one(self, account_id: int, user_id: int):
        return await self.db.get(BankAccount, (account_id, user_id))

    @except_handler
    async def create(self, account_id: int,
                     user_id: int) -> Optional[BankAccount]:
        new_account = BankAccount(account_id = account_id, user_id = user_id)
        self.db.add(new_account)
        await self.db.commit()
        await self.db.refresh(new_account)
        return new_account



    @except_handler
    async def delete(self,account_id: int, user_id: int) -> bool:
        await self.db.delete(await self.db.get(BankAccount, (account_id,user_id)))
        return True
