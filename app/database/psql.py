from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import load_config

config = load_config()

DATABASE_URL = (f'postgresql://{config.database.db_user}'
                f':{config.database.db_pass}@'
                f'{config.database.db_host}/'
                f'{config.database.db_name}')

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
