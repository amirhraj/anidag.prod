from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey, ARRAY, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from typing import List, Dict
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


Base = declarative_base()


class AnimeSearchTitle(Base):
    __tablename__ = 'anime_search_titles'
    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    link = Column(String, nullable=False)
    title = Column(String, nullable=False)
    title_orig = Column(String, nullable=False)
    # other_title = Column(ARRAY(String), nullable=True)
    # translation_id = Column(Integer, ForeignKey("translations.id"), nullable=False)
    # translation = relationship("TranslationBase")
    personupdate = Column(DateTime, nullable=True)
    year = Column(Integer, nullable=False)
    last_season = Column(Integer, nullable=True)
    last_episode = Column(Integer, nullable=True)
    episodes_count = Column(Integer, nullable=True)
    kinopoisk_id = Column(String, nullable=True)
    imdb_id = Column(String, nullable=True)
    worldart_link = Column(String, nullable=True)
    shikimori_id = Column(String, nullable=False)
    quality = Column(String, nullable=True)
    camrip = Column(Boolean, nullable=True)
    lgbt = Column(Boolean, nullable=True)
    blocked_countries = Column(ARRAY(String), nullable=True)
    blocked_seasons = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    seasons = Column(JSON, nullable=True)
    material_data = Column(JSON, nullable=False)
    screenshots=Column(ARRAY(String), nullable=True)
    premiere_world = Column(DateTime, nullable=True)  
    aired_at = Column(DateTime, nullable=True)        
    released_at = Column(DateTime, nullable=True)     
    countries = Column(ARRAY(String), nullable=True) 
    description = Column(String, nullable=True)
    anime_description = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)
    anime_poster_url = Column(String, nullable=True)
    anime_studios = Column(ARRAY(String), nullable=True)
    next_episode_at = Column(DateTime, nullable=True) 
    anime_genres = Column(ARRAY(String), nullable=True)
    anime_kind = Column(String, nullable=True)
    all_status = Column(String, nullable=True)
    anime_status = Column(String, nullable=True) 
    # likes = relationship('Like', back_populates='anime') # Новая колонка
    # like_count = Column(Integer, default=0) # Общее количество лайков # Новая колонка
    # dislike_count = Column(Integer, default=0) # Общее количество дизлайков  # Новая колонка
    # view_count = Column(Integer, default=0) # Новая колонка
    episodes_total = Column(Integer, nullable=True) # Новая колонка
    kinopoisk_rating = Column(Float, nullable=True) # Новая колонка
    shikimori_rating = Column(Float, nullable=True) # Новая колонка
    country = Column(String(2), nullable=True)

