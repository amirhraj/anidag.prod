from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey, TIMESTAMP, func, Text, UniqueConstraint,  Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from sqlalchemy import Column, DateTime


load_dotenv(find_dotenv())



Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=True)  # character varying
    created_at = Column(TIMESTAMP, server_default=func.now())  # timestamp without time zone
    is_banned = Column(Boolean, default=False)  
    tokens = relationship("Token", back_populates="user")
    is_verified = Column(Boolean, default=False) # новая колонка 27.02
    verification_token = Column(String, nullable=True) # новая колонка 27.02
    comments = relationship("Comment", back_populates="user")
    avatars = Column(String, nullable=True)

    api_keys = relationship("UserAPIKey", back_populates="user")
    watch_later_items = relationship("WatchLater", back_populates="user", cascade="all, delete")

    background_id = Column(Integer, ForeignKey("profile_backgrounds.id"), nullable=True)
    background = relationship(
    "ProfileBackground",
    foreign_keys=[background_id]
    )

    gl_background_id = Column(Integer, ForeignKey("profile_backgrounds.id"), nullable=True)
    gl_background = relationship("ProfileBackground", foreign_keys=[gl_background_id])


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    refresh_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tokens")
    login_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)  # integer
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # integer
    content = Column(Text, nullable=False)  # text
    created_at = Column(TIMESTAMP, server_default=func.now())  # timestamp without time zone
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # timestamp without time zone
    anime_id = Column(String, nullable=False)  # character varying
    parent_comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)  # integer
    user = relationship("User", back_populates="comments")

# Таблица создана в будущем для того чтобы привязывать хеши к одному юзер айди
class UserAPIKey(Base):
    __tablename__ = "user_api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_hash = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expired_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="api_keys")

class WatchLater(Base):
    __tablename__ = "watch_later"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    anime_id = Column(String, nullable=False)  # например: "serial-12345"
    type = Column(String, nullable=False)      # например: "tv", "movie", "ova"
    api = Column(String, nullable=False)       # например: "/api/titles/tv/"
    is_active = Column(Boolean, default=True) 

    __table_args__ = (
        UniqueConstraint('user_id', 'anime_id', name='_user_title_uc'),
    )

    user = relationship("User", back_populates="watch_later_items")



class WatchHistory(Base):
    __tablename__ = "watch_history"
    __table_args__ = (
        UniqueConstraint("user_id", "anime_id", "episode", name="user_anime_episode_unique"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ip_hash = Column(Text, nullable=False)
    anime_id = Column(String, nullable=False)
    episode = Column(Integer, nullable=False)
    title = Column(String)
    current_time = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    progress = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=False), nullable=False, default=func.now())
    created_at = Column(DateTime(timezone=False), nullable=False, default=func.now())
    type = Column(String(100), nullable=True)
    api = Column(String(150), nullable=True)



class ProfileBackground(Base):
    __tablename__ = "profile_backgrounds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    image_url = Column(Text, nullable=False)

