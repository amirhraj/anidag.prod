from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, ForeignKey,create_engine
from sqlalchemy.orm import relationship
from database import Base  # Предполагается, что у вас есть базовый класс Base
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



Base = declarative_base()


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)  # integer
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # integer
    content = Column(Text, nullable=False)  # text
    created_at = Column(TIMESTAMP, server_default=func.now())  # timestamp without time zone
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # timestamp without time zone
    anime_id = Column(String, nullable=False)  # character varying
    parent_comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)  # integer