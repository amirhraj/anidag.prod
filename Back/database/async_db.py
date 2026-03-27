import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv(find_dotenv())

ASYNC_DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('BD_PROD_ADMIN')}:{os.getenv('BD_PROD_PASS')}"
    f"@{os.getenv('BD_HOST')}/anime_db"
)

class Base(DeclarativeBase):
    pass

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
