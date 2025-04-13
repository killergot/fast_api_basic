from typing import Optional

from sqlalchemy import select

from app.db import BankAccount
from app.repositoryes.template import TemplateRepository


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

    async def create(self, account_id: int,
                     user_id: int) -> Optional[BankAccount]:
        try:
            new_account = BankAccount(account_id = account_id, user_id = user_id)
            self.db.add(new_account)
            await self.db.commit()
            await self.db.refresh(new_account)
            return new_account
        except:
            return None

    async def delete(self,account_id: int, user_id: int) -> bool:
        try:
            await self.db.delete(await self.db.get(BankAccount, (account_id,user_id)))
            return True
        except Exception as e:
            print(e)
            return False