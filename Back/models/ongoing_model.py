from pydantic import BaseModel, EmailStr, FieldValidationInfo, field_validator
from typing import List, Optional,Dict ,Any
from datetime import datetime
import re

# Pydantic-схема для валидации входящих данных
# class Screenshot(BaseModel):
#     link: str

# class Episode(BaseModel):
#     link: str
#     screenshots: List[str]

# class Season(BaseModel):
#     link: str
#     episodes: Dict[str, Episode]
    
class Translation(BaseModel):
    id: int
    title: str
    type: str



class AnimeSchema(BaseModel):
    id: str
    type : Optional[str] = None
    link : Optional[str] = None
    title: str
    title_orig: str
    other_title: Optional[str] = None
    translation:Translation
    year: int
    last_season:int
    last_episode:int
    episodes_count: int
    kinopoisk_id:Optional[str] = None
    imdb_id:str
    worldart_link: str
    shikimori_id: str
    quality:str
    camrip:bool
    lgbt:bool
    blocked_countries:List[str] = []
    blocked_seasons: Dict[str,str] = {}
    created_at: datetime
    updated_at:datetime
    seasons: Any
    material_data: Any
    screenshots:list[str]
    class Config:
        extra = "ignore"
    
    # screenshots: List[str]


class AnimeList(BaseModel):
    results: List[AnimeSchema]



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    @field_validator("password")
    def validate_password(cls, value: str, info: FieldValidationInfo):
        # Проверка длины пароля
        if len(value) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов.")
        
        # Проверка наличия цифр
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать минимум одну цифру.")
        
        # Проверка наличия букв верхнего регистра
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать минимум одну заглавную букву.")
        
        # Проверка наличия специальных символов
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Пароль должен содержать минимум один специальный символ.")
        
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str