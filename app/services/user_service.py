from app.repositoryes.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_email(self, email):
        return await self.repo.get_by_email(email)