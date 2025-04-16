from typing import Optional
import logging

from sqlalchemy import select

from app.db.models.user import User
from app.repositoryes.template import TemplateRepository
from app.core.except_handler import except_handler

log = logging.getLogger(__name__)

class UserRepository(TemplateRepository):
    async def get_all(self):
        data = select(User)
        users = await self.db.execute(data)
        return users.scalars().all()

    async def get_by_email(self, email: str):
        data = select(User).where(User.email == email)
        user = await self.db.execute(data)
        return user.scalars().first()

    async def get_by_id(self, user_id: int):
        return await self.db.get(User, user_id)

    async def create(self, full_name: str,
                     email: str,
                     password: str,
                     role: Optional[int] = None) -> User:
        new_user = User(full_name=full_name,
                        email=email,
                        password=password,
                        role=role)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def update(self, user_id: int, full_name: str,password: str):
        user = await self.db.get(User, user_id)
        user.full_name = full_name
        user.password = password
        await self.db.commit()
        await self.db.refresh(user)
        return user

    @except_handler
    async def delete(self, user_id: int) -> bool:
        await self.db.delete(await self.db.get(User, user_id))
        await self.db.commit()
        return True