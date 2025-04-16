from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import load_config

config = load_config()

DATABASE_URL = (f'postgresql+asyncpg://{config.database.db_user}'
                f':{config.database.db_pass}@'
                f'{config.database.db_host}/'
                f'{config.database.db_name}')

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
