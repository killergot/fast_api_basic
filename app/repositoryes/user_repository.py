from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.auth import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

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

    async def delete(self, user_id: int) -> bool:
        try:
            await self.db.delete(await self.db.get(User, user_id))
            return True
        except Exception as e:
            print(e)
            return False