from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
import os
from datetime import datetime
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Boolean
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Асинхронный движок для PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('BD_PROD_ADMIN')}:{os.getenv('BD_PROD_PASS')}@{os.getenv('BD_HOST')}/anime_db"
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class AnimeAllohaFilm(Base):
    __tablename__ = 'al_film'


    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String(255), nullable=True)  
    original_name = Column(String(255), nullable=True)  
    countries = Column(String(255), nullable=True)  
    alternative_name = Column(Text, nullable=True)  
    year = Column(Integer, nullable=True)  
    id_kp = Column(Integer, nullable=True)  
    link = Column(Text, nullable=True)
    poster_url =  Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    title_orig = Column(Text, nullable=True)
    alternative_id_kp = Column(Integer, nullable=True)  
    id_imdb = Column(String(20), nullable=True)  
    id_tmdb = Column(Integer, nullable=True)  
    token_movie = Column(String(255), nullable=True)  
    date = Column(DateTime, default=datetime.utcnow)  
    category = Column(String(100), nullable=True)  
    genre = Column(Text, nullable=True)  
    actors = Column(Text, nullable=True)  
    directors = Column(Text, nullable=True)  
    producers = Column(Text, nullable=True)  
    premiere_ru = Column(String(20), nullable=True)  
    premiere = Column(String(20), nullable=True)  
    age_restrictions = Column(Integer, nullable=True)  
    rating_kp = Column(Float, nullable=True)  
    rating_imdb = Column(Float, nullable=True)  
    time = Column(String(20), nullable=True)  
    poster = Column(String(500), nullable=True)  
    description = Column(Text, nullable=True)  
    iframe = Column(String(500), nullable=True)  
    quality = Column(String(50), nullable=True)  
    translation = Column(String(100), nullable=True)  
    translation_iframe = Column(JSON, nullable=True)  
    lgbt = Column(Boolean, default=False)  
    uhd = Column(Boolean, default=False)  
