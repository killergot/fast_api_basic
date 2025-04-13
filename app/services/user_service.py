from app.repositoryes.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.shemas.auth import UserOut


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_user_by_email(self, email: str):
        user = await self.repo.get_by_email(email)
        return UserOut.model_validate(user)

    async def get_user_by_id(self, id: int):
        user = await self.repo.get_by_id(id)
        return UserOut.model_validate(user)

