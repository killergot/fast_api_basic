from sqlalchemy.ext.asyncio import AsyncSession

class TemplateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db