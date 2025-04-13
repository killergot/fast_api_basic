from app.db.psql import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session