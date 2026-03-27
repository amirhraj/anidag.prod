from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey, ARRAY, Boolean,PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from typing import List, Dict
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


Base = declarative_base()

class AnimeAnons(Base):
    __tablename__ = 'anime_anons'

    id = Column(Integer, primary_key=True)
    mal_id = Column(Integer, nullable=False)  # MyAnimeList ID
    name = Column(String, nullable=False)  # Название аниме
    russian_name = Column(String, nullable=True)  # Русское название
    english_name = Column(String, nullable=True)  # Английское название
    japanese_name = Column(String, nullable=True)  # Японское название
    kind = Column(String, nullable=False)  # Тип аниме (например, tv, movie)
    rating = Column(String, nullable=False)  # Рейтинг (например, pg)
    score = Column(Integer, nullable=False)  # Оценка
    status = Column(String, nullable=False)  # Статус (анонс, вышло)
    episodes = Column(Integer, nullable=False)  # Количество серий
    episodes_aired = Column(Integer, nullable=False)  # Вышедшие серии
    duration = Column(Integer, nullable=False)  # Длительность
    aired_on = Column(PickleType, nullable=True)  # Дата выхода
    released_on = Column(JSON, nullable=True)  # Дата релиза
    url = Column(String, nullable=False)  # Ссылка на аниме
    season = Column(String, nullable=True)  # Сезон (например, весна, лето)
    poster = Column(JSON, nullable=False)  # Постер аниме
    created_at = Column(String, nullable=False)  # Дата создания записи
    updated_at = Column(String, nullable=False)  # Дата обновления записи
    next_episode_at = Column(DateTime, nullable=True)  # Дата выхода следующей серии
    is_censored = Column(Boolean, nullable=False)  # Наличие цензуры
    genres = Column(JSON, nullable=False)  # Жанры
    studios = Column(JSON, nullable=False)  # Студии
    videos = Column(JSON, nullable=True)  # Видео
    description = Column(String, nullable=True)  # Описание
    country = Column(String(2), nullable=True)

    class Config:
        orm_mode = True 


