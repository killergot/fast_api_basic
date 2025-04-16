from fastapi import  HTTPException, status

from app.repositoryes.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.shemas.auth import UserOut


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def _get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    async def get_user_by_email(self, email: str):
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return UserOut.model_validate(user)

    async def get_user_by_id(self, id: int):
        user = await self._get_user(id)
        return UserOut.model_validate(user)

    async def get_all_users(self):
        users = await self.repo.get_all()
        result = [{'id': user.id, 'email': user.email, 'role': user.role} for user in users]
        return result

    async def del_user_by_id(self, id: int):
        user = await self._get_user(id)
        if not await self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_500_NOT_FOUND,
                                detail="Error deleting user")
