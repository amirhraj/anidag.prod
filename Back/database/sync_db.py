import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

SYNC_DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('BD_PROD_ADMIN')}:{os.getenv('BD_PROD_PASS')}"
    f"@{os.getenv('BD_HOST')}/anime_db"
)

sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
)



