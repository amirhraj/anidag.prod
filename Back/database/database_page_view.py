from sqlalchemy import Column, Integer, String, DateTime,create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



Base = declarative_base()

class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    ip_hash = Column(String, nullable=True)
    anime_id = Column(String, nullable=True)
    title = Column(String, nullable=True)
    time_spent = Column(Integer, nullable=False)  # в секундах
    session_id = Column(String, nullable=True)  # уникальный ID сессии
    referer = Column(String, nullable=True)     # страница, с которой пришли
    device_info = Column(String, nullable=True) # строка user-agent или подробности
    created_at = Column(DateTime, default=datetime.utcnow)

# ✅ ВАЖНО: создаём таблицу, если её нет



