from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey, ARRAY, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from typing import List, Dict
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


Base = declarative_base()


class AnimeOvaBase(Base):
    __tablename__ = 'anime_ova'

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    title_orig = Column(String, nullable=False)
    # other_title = Column(ARRAY(String), nullable=True)
    # translation_id = Column(Integer, ForeignKey("translations.id"), nullable=False)
    # translation = relationship("TranslationBase")
    year = Column(Integer, nullable=False)
    # last_season = Column(Integer, nullable=False)
    # last_episode = Column(Integer, nullable=False)
    # episodes_count = Column(Integer, nullable=False)
    kinopoisk_id = Column(String, nullable=True)
    imdb_id = Column(String, nullable=True)
    worldart_link = Column(String, nullable=True)
    shikimori_id = Column(String, nullable=False)
    quality = Column(String, nullable=False)
    camrip = Column(Boolean, nullable=False)
    lgbt = Column(Boolean, nullable=False)
    blocked_countries = Column(ARRAY(String), nullable=True)
    # blocked_seasons = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    material_data = Column(JSON, nullable=False)
    screenshots=Column(ARRAY(String), nullable=True)
    premiere_world = Column(DateTime, nullable=True) 
    aired_at = Column(DateTime, nullable=True)        
    released_at = Column(DateTime, nullable=True)  
    countries = Column(ARRAY(String), nullable=True) # Новая колонка
    description = Column(String, nullable=True)
    anime_description = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)
    anime_poster_url = Column(String, nullable=True)
    anime_studios = Column(ARRAY(String), nullable=True)
    anime_genres = Column(ARRAY(String), nullable=True)
    all_status = Column(String, nullable=True) # Новая колонка
    anime_status = Column(String, nullable=True) # Новая колонка  
    country = Column(String(2), nullable=True)

   
    # screenshots = Column(ARRAY(String), nullable=False)
# Создание движка и базы данных


