from fastapi import FastAPI, HTTPException, Depends, Request, Response,  Response,File, UploadFile, Form, Query,  Body 
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from jwt import PyJWTError, ExpiredSignatureError   
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session,aliased
from sqlalchemy import func, select,text, desc , extract , case , cast, Date, distinct
from models.ongoing_model import AnimeSchema,AnimeList
from crud import add_anime, add_anime_film_al, add_anime_main, add_anime_ova, add_anime_film, add_anime_anons, add_anime_top, add_anime_search,add_alloha_ongoing
from models.ongoing_model import AnimeSchema,AnimeList , UserCreate, LoginRequest
from typing import List , Optional
from database.db_al_film import AnimeAllohaFilm, async_session
from  database.database_setup_ongoing  import  AnimeSchemaBase, Like, View
from  database.database_main_titles  import  MainTitle
from  database.database_setup_OVA  import  AnimeOvaBase
from  database.database_anons  import  AnimeAnons
from  database.database_Top100anime import  AnimeTopBase
from  database.database_films import AnimeFilmBase
from database.database_search import AnimeSearchTitle
from database.match_bd import AL_ONGOING_ANIME_SCHEMA
from database.db_al_ongoing import AL_ONGOING
from database.database_page_view import PageView
from  database.database_user import User, Token,  UserAPIKey, WatchLater, WatchHistory, ProfileBackground
from database.sync_db import SessionLocal
from sqlalchemy import func, String, cast
from datetime import datetime, timezone, timedelta
from auth.auth_jwt import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token, decode_access
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
import logging
from pathlib import Path
from hashPassFunction.util import get_password_hash , verify_password
from hashlib import sha256
from jose import JWTError
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
import uuid
import shutil
import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from reaction.reaction import router as reactions_router
from comments.comments import router as comments_router
from authentication.authentication import router as authentication
from typing import Any


logger = logging.getLogger("uvicorn")



app = FastAPI()

current_date = datetime.now().date()

app.add_middleware( TrustedHostMiddleware, allowed_hosts=[ 
        "anidag.ru",
        "www.anidag.ru",
        "5.35.87.245",
        "localhost",
        "127.0.0.1",
        "localhost:3000",
        "localhost:5174",
        "backend"
     ] )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://5.35.87.245", 
    "http://localhost:5174" , 
    "localhost:5174" , 
    "https://localhost:3000",
    'http://anidag.ru', 
    'https://anidag.ru' , 
    'http://www.anidag.ru', 
    'https://www.anidag.ru'
    ],  # Разрешить все источники. Лучше указать конкретные домены в продакшене.
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(comments_router)
app.include_router(reactions_router)
app.include_router(authentication)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from collections.abc import AsyncGenerator

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_ip_hash(ip: str) -> str:
    return sha256(ip.encode()).hexdigest()


from pathlib import Path
import os

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/uploads"))
BACKGROUND_DIR = Path(os.getenv("BACKGROUND_DIR", "/app/back_fon"))
AVATARS_DIR = UPLOAD_DIR / "avatars"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
BACKGROUND_DIR.mkdir(parents=True, exist_ok=True)
AVATARS_DIR.mkdir(parents=True, exist_ok=True)

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(BACKGROUND_DIR, exist_ok=True)

app.mount("/api/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/api/back_fon", StaticFiles(directory=str(BACKGROUND_DIR)), name="backgrounds")

# app.mount("/api/defaultimg", StaticFiles(directory="/var/www/html/Back/default_img"), name="defaultimg")

# UPLOAD_DIR = Path('/var/www/html/Back/uploads/avatars') 


# Определение страны у пользователя
async def get_country_from_ip(ip: str) -> str:
    """
    Определяем страну по IP через сервис ip-api.com
    """
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://ip-api.com/json/{ip}?fields=countryCode")
            data = resp.json()
            print(data, "DATA")
            return data.get("countryCode", "UNKNOWN")
    except Exception:
        return "UNKNOWN"


@app.get("/api/geo-info")
async def geo_info(request: Request):
    """
    Возвращает IP и страну пользователя
    """
    # IP пользователя (если за прокси/Nginx — может быть не реальный)
    ip = request.client.host  
    print(ip, "АЙПИ АДРЕС")

    # Узнаем страну
    country = await get_country_from_ip(ip)
    logger.info(f"Country: {country}")
    return {"ip": ip, "country": country}


    

@app.get("/api/health")
def health():
    return {"status": "ok"}






##############################################ALLOHA




@app.post("/api/addallohaongoing")
async def sync_anime(movies: list[dict[str, Any]]):
    try:
        saved_count = await add_alloha_ongoing(movies)

        return {
            "status": "success",
            "fetched": len(movies),
            "saved": saved_count,
            "message": "Данные сохранены в PostgreSQL"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from database.sync_db import SessionLocal
import uuid
from rapidfuzz import fuzz


SIMILARITY_THRESHOLD = 80


def title_similarity(a: str, b: str) -> int:
    if not a or not b:
        return 0

    return max(
        fuzz.ratio(a, b),
        fuzz.partial_ratio(a, b),
        fuzz.token_sort_ratio(a, b),
        fuzz.token_set_ratio(a, b),
    )


def match_alloha_anime():
    db = SessionLocal()

    try:
        anime_rows = db.execute(text("""
            SELECT id, title_orig
            FROM public.anime_schema
            WHERE title_orig IS NOT NULL
              AND trim(title_orig) <> ''
        """)).mappings().all()

        alloha_rows = db.execute(text("""
            SELECT id, original_name
            FROM public.al_ongoing
            WHERE original_name IS NOT NULL
              AND trim(original_name) <> ''
        """)).mappings().all()

        anime_list = [
            {
                "id": row["id"],
                "title_orig": row["title_orig"],
            }
            for row in anime_rows
        ]

        alloha_list = [
            {
                "id": row["id"],
                "original_name": row["original_name"],
            }
            for row in alloha_rows
        ]

        inserted = 0
        skipped_conflict = 0
        no_match = 0

        for alloha in alloha_list:
            best_match = None
            best_score = 0

            for anime in anime_list:
                score = title_similarity(
                    alloha["original_name"],
                    anime["title_orig"]
                )

                if score > best_score:
                    best_score = score
                    best_match = anime

            if best_match and best_score >= SIMILARITY_THRESHOLD:
                result = db.execute(text("""
                    INSERT INTO public.al_ongoing_anime_schema (
                        al_ongoing_id,
                        anime_schema_id,
                        common_uid
                    )
                    VALUES (:a_id, :b_id, :uid)
                    ON CONFLICT (al_ongoing_id, anime_schema_id) DO NOTHING
                    RETURNING id
                """), {
                    "a_id": alloha["id"],
                    "b_id": best_match["id"],
                    "uid": str(uuid.uuid4())
                }).first()

                if result:
                    inserted += 1
                    print(
                        f"[LINK] "
                        f"{alloha['original_name']} -> {best_match['title_orig']} "
                        f"(score={best_score})"
                    )
                else:
                    skipped_conflict += 1
                    print(
                        f"[SKIP-CONFLICT] "
                        f"{alloha['original_name']} -> {best_match['title_orig']} "
                        f"(score={best_score})"
                    )
            else:
                no_match += 1
                print(
                    f"[NO MATCH] "
                    f"{alloha['original_name']} "
                    f"(best_score={best_score})"
                )

        db.commit()

        return {
            "status": "success",
            "inserted": inserted,
            "skipped_conflict": skipped_conflict,
            "no_match": no_match,
            "threshold": SIMILARITY_THRESHOLD
        }

    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
        raise

    finally:
        db.close()


@app.post("/api/match-alloha-anime")
def match_alloha_anime_api():
    try:
        return match_alloha_anime()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#################################################


@app.post("/api/anime")
def create_anime(anime_data: dict, db: Session = Depends(get_db)):
    try:
        # print("Полученные данные:", anime_data)
        # anime_json = json.dumps(anime_data)
        anime = add_anime(anime_data, db)
        print("Аниме успешно добавлено:", anime)
    except IntegrityError as e:
        # Логируем ошибку и выводим информацию о поле, вызвавшем ошибку
        logging.error(f"Ошибка целостности данных: {e}")
        raise HTTPException(status_code=400, detail=f"Ошибка целостности данных: {e}")
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    return anime

@app.post("/api/animeMainTitles")
def create_anime_main_titles(anime_data: dict, db: Session = Depends(get_db)):
    try:
        # print("Полученные данные:", anime_data)
        anime = add_anime_main(anime_data, db)
        print("Аниме успешно добавлено:", anime)
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    return anime


@app.post("/api/animeOva")
def create_anime_main_titles(anime_data: dict, db: Session = Depends(get_db)):
    try:
        # print("Полученные данные:", anime_data)
        anime = add_anime_ova(anime_data, db)
        print("Аниме успешно добавлено:", anime)
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    return anime

@app.post("/api/animeFilm")
def create_anime_film(anime_data: dict, db: Session = Depends(get_db)):
    try:
        # print("Полученные данные:", anime_data)
        anime = add_anime_film(anime_data, db)
        print("Аниме успешно добавлено:", anime)
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    return anime

@app.post("/api/animeFilmal/")
async def create_anime_film(anime_data: Dict, db: AsyncSession = Depends(get_async_db)):
    try:
        print("📩 Полученные данные:", anime_data)
        anime = await add_anime_film_al(anime_data, db)  # <-- функция тоже async
        print("✅ Аниме успешно добавлено:", anime)
    except Exception as e:
        print("❌ Ошибка:", e)
        raise HTTPException(status_code=400, detail=str(e))
    return anime




@app.post("/api/animeTop")
def create_anime_Anons(anime_data: dict, db: Session = Depends(get_db)):
    try:
        print("Полученные данные:", anime_data)
        anime = add_anime_top(anime_data, db)
        print("Аниме успешно добавлено:", anime)
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    return anime


@app.post("/api/animeSearch/")
def create_anime_search(anime_data: dict=Body(...), db: Session = Depends(get_db)):
    try:
        print("Полученные данные:", anime_data)

        anime = add_anime_search(anime_data, db)
        print("Аниме успешно добавлено:", anime)
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    return anime



@app.get("/api/animes")
def read_animes(skip: int =0 , limit: int = 10, db: Session = Depends(get_db)):
    animes = (
    db.query(AnimeSchemaBase)
    # .distinct(AnimeSchemaBase.title)
    # .filter(func.date(AnimeSchemaBase.updated_at) == current_date)
    .order_by( AnimeSchemaBase.updated_at.desc())
    .offset(skip)
    .limit(limit)
    .all()
)

    unique_animes = {}
    
    for anime in animes:
        # Если title еще не в словаре, добавляем его
        if anime.title not in unique_animes:
           
            unique_animes[anime.title] = anime

    # Получаем список уникальных аниме
    # print( unique_animes)
    print( list(unique_animes.values()), "АНИМЕ ПРИШЛО +++=+")
    return list(unique_animes.values())


@app.get("/api/animesMainTitles")
def read_animes( skip: int =0 , limit: int = 50, db: Session = Depends(get_db)):
    animes = (
            db.query(MainTitle)
            .order_by(MainTitle.updated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    unique_animes = {}
    for anime in animes:
        if anime.title not in unique_animes:
            unique_animes[anime.title] = anime
    return list(unique_animes.values())



@app.get("/api/animesMainTitlesTV")
def read_animes(skip: int= 0, limit: int = 10, db: Session = Depends(get_db)):
    animes = db.query(MainTitle).distinct(MainTitle.title).offset(skip).limit(limit)
    unique_animes = {}
    
    for anime in animes:
        # Если title еще не в словаре, добавляем его
        if anime.title not in unique_animes:
            unique_animes[anime.title] = anime
    return list(unique_animes.values())



@app.get("/api/animeTop")
def read_animes_top(skip: int= 0, limit: int = 50, db: Session = Depends(get_db)):
    # animes = db.query(AnimeTopBase).distinct(AnimeTopBase.title).offset(skip).limit(limit)
    animes = (
            db.query(AnimeTopBase)
            # .distinct(AnimeTopBase.title)
            .order_by(desc(AnimeTopBase.shikimori_rating), desc(AnimeTopBase.created_at))  # Добавляем сортировку по убыванию по полю years
            .offset(skip)
            .limit(limit)
            .all()
        )
    unique_animes = {}
    
    for anime in animes:
        # Если title еще не в словаре, добавляем его
        if anime.title not in unique_animes:
            unique_animes[anime.title] = anime
    return list(unique_animes.values())


@app.get("/api/animeOvaAll")
def read_animes(skip: int=0, limit: int= 16, db: Session = Depends(get_db)):
    # animes = db.query(AnimeOvaBase).distinct(AnimeOvaBase.title).order_by(AnimeOvaBase.updated_at.desc()).all()
    # animes = db.query(AnimeOvaBase).distinct(AnimeOvaBase.title).order_by(AnimeOvaBase.title, AnimeOvaBase.updated_at.desc()).all()
    animes = db.query(AnimeOvaBase).order_by(AnimeOvaBase.aired_at.desc()).offset(skip).limit(limit)
    unique_animes = {} 
    for anime in animes:
        # Если title еще не в словаре, добавляем его
        if anime.title not in unique_animes:
            unique_animes[anime.title] = anime

    # Получаем список уникальных аниме
    return list(unique_animes.values())




@app.get("/api/animeSearch/")
def read_animes(skip: int=0, limit: int= 16, db: Session = Depends(get_db)):
    animes = db.query(AnimeSearchTitle).order_by(AnimeSearchTitle.personupdate.desc()).offset(skip).limit(limit)
  
    unique_animes = {} 
    for anime in animes:
        # Если title еще не в словаре, добавляем его
        if anime.title not in unique_animes:
            unique_animes[anime.title] = anime

    # Получаем список уникальных аниме
    return list(unique_animes.values())




@app.get("/api/animeSearch/{id}")
def read_animes(id: str , db: Session = Depends(get_db)):
    anime = db.query(AnimeSearchTitle).filter(AnimeSearchTitle.id == id).first()
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return {
        "card" : anime
    }


@app.get("/api/animeGenres/{id}")
def read_animes(id: str, db: Session = Depends(get_db)):
    # animes = db.query(AnimeOvaBase).distinct(AnimeOvaBase.title).order_by(AnimeOvaBase.updated_at.desc()).all()
    animes = (
        db.query(AnimeSchemaBase)
    )
    
    unique_animes = {} 
    for anime in animes:
        genres = anime.material_data.get('all_genres', [])
        if id in genres:
            if anime.title not in unique_animes:
                unique_animes[anime.title] = anime

    # Получаем список уникальных аниме
    return list(unique_animes.values())

    
@app.get("/api/animesAnons")
def get_anime_anons(
    year: Optional[int] = None,
    month: Optional[int] = None,
    skip: int = 0,
    limit: int = 40,
    db: Session = Depends(get_db)
):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    query = db.query(AnimeAnons)

    # Если явно указаны год и/или месяц — фильтруем по ним
    if year:
        query = query.filter(extract("year", cast(AnimeAnons.created_at, Date)) == year)
    if month:
        query = query.filter(extract("month", cast(AnimeAnons.created_at, Date)) == month)

    # Сортировка: сначала записи с датой, потом без, приоритет — текущий месяц и год
    query = query.order_by(
        case(
            (AnimeAnons.created_at == None, 2),
            (extract("year", cast(AnimeAnons.created_at, Date)) > current_year, 1),
            else_=0
        ),
        case(
            (extract("month", cast(AnimeAnons.created_at, Date)) == current_month, 0),
            else_=1
        ),
        cast(AnimeAnons.created_at, Date).desc()
    ).offset(skip).limit(limit)

    results = query.all()

    # Отбор уникальных тайтлов по имени
    unique_animes = {}
    for anime in results:
        if anime.name not in unique_animes:
            unique_animes[anime.name] = anime

    return list(unique_animes.values())
    

    # return animes

@app.get("/api/animeOvaAll/{id}")
def read_animes(id: str , db: Session = Depends(get_db)):
    anime = db.query(AnimeOvaBase).filter(AnimeOvaBase.id == id).first()
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return {
        "card": anime
    }
    # return animes

# @app.get("/api/animes/{id}")
# def get_anime(id: str, db: Session = Depends(get_db)):
#     anime = db.query(AnimeSchemaBase).filter(AnimeSchemaBase.id == id).first()
#     if anime is None:
#         raise HTTPException(status_code=404, detail="Anime not found")
#     return anime


@app.get("/api/animes/{anime_id}")
def read_anime(anime_id: str, db: Session = Depends(get_db)):
    anime = db.query(AnimeSchemaBase).filter(AnimeSchemaBase.id == anime_id).first()

    if not anime:
        raise HTTPException(status_code=404, detail="Аниме не найдено")

    # ищем связь
    al_relation = (
        db.query(AL_ONGOING_ANIME_SCHEMA)
        .filter(AL_ONGOING_ANIME_SCHEMA.anime_schema_id == anime_id)
        .first()
    )

    al_ongoing = None

    if al_relation:
        al_ongoing = (
            db.query(AL_ONGOING)
            .filter(AL_ONGOING.id == al_relation.al_ongoing_id)
            .first()
        )

    return {
        "card": anime,
        "al_ongoing": al_ongoing
    }

@app.get("/api/animesTitleMine/{id}")
def get_anime(id: str, db: Session = Depends(get_db)):
    anime = db.query(MainTitle).filter(MainTitle.id == id).first()
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return {
        "card": anime
    }

@app.get("/api/animeFilms")
def get_anime_film(skip: int=0, limit: int= 16, db: Session = Depends(get_db)):

    try:
        # animes = db.query(AnimeFilmBase).all()
        # animes = db.query(AnimeFilmBase).distinct(AnimeFilmBase.title).offset(skip).limit(limit)
        animes = db.query(AnimeFilmBase).order_by(AnimeFilmBase.aired_at.desc()).offset(skip).limit(limit)
        unique_animes = {}
        for anime in animes:
            if anime.title not in unique_animes:
                unique_animes[anime.title] = anime
        return list(unique_animes.values())
    except Exception as e:
        print("Ошибка при добавлении аниме:", str(e))
        raise HTTPException(status_code=400, detail=str(e))


# @app.get("/api/animeFilm/{id}")
# def get_anime(id: str, db: Session = Depends(get_db)):
#     anime = db.query(AnimeFilmBase).filter(AnimeFilmBase.id == id).first()
#     if anime is None:
#         raise HTTPException(status_code=404, detail="Anime not found")
#     return anime


@app.get("/api/animeFilm/{id}")
def get_anime(id: str, db: Session = Depends(get_db)):
    result = (
        db.query(AnimeFilmBase, AnimeAllohaFilm.iframe)
        .outerjoin(AnimeAllohaFilm, AnimeAllohaFilm.title_orig == AnimeFilmBase.title_orig)
        .filter(AnimeFilmBase.id == id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Anime not found")

    anime_obj, token_movie = result

    # Преобразуем объект SQLAlchemy в dict
    anime_dict = {k: v for k, v in anime_obj.__dict__.items() if k != "_sa_instance_state"}

    # Добавляем token_movie в словарь
    anime_dict["iframe"] = token_movie


    return {
        "card": jsonable_encoder(anime_dict)
    }

@app.get("/api/animeTop/{id}")
def read_animes_top(id: str, db: Session = Depends(get_db)):
    anime = db.query(AnimeTopBase).filter(AnimeTopBase.id == id).first()
    if anime is None:
        raise HTTPException(status_code=404, detail="Anime not found")
    return {
        "card":  anime
    }

@app.get("/api/animes/scheduler/")
def get_anime(db: Session = Depends(get_db)):
    # animes = db.query(AnimeSchemaBase).all()
    # animes = db.query(AnimeSchemaBase).distinct(AnimeSchemaBase.title).all()
    animes = (
        db.query(AnimeSchemaBase)
        .filter(AnimeSchemaBase.all_status == "ongoing")
        .filter(AnimeSchemaBase.anime_status == "ongoing")
        .distinct(AnimeSchemaBase.title)
        .all()
    )

    unique_animes = {} 
    for anime in animes:
        # Если title еще не в словаре, добавляем его
        if anime.title not in unique_animes:
            unique_animes[anime.title] = anime

    # Получаем список уникальных аниме
    return list(unique_animes.values())







MAX_SIZE_MB = 2  # Лимит размера аватара

# Функция для создания папок, если их нет
def create_avatar_folders(user_id: int):
    print(f"Создание папок для user_id: {user_id}")
    # Разбиваем ID на части для создания вложенных папок
    subfolders = [str(user_id // 1000), str(user_id % 1000)]
    folder_path = UPLOAD_DIR / Path(*subfolders)
    
    # Создаем папки, если они не существуют
    if not folder_path.exists():
        print(f"Папка {folder_path} не существует, создаем...")
        folder_path.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Папка {folder_path} уже существует.")
    
    return folder_path

# Функция для сжатия изображения
def compress_image(image_path: Path, output_path: Path):
    """Функция для сжатия изображения"""
    print(f"Сжатие изображения: {image_path} -> {output_path}")
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Конвертируем в RGB (если PNG)
        img.save(output_path, "JPEG", quality=75)  # Сжимаем до 75% качества
    print(f"Изображение сжато и сохранено в {output_path}")


def update_user_avatar(user_id: int, avatar_path: str, db: Session):
    print(user_id, avatar_path, "СОХРАНЕНИЯ В БД")
    # Находим пользователя по user_id
    
    user = db.query(User).filter(User.id == user_id).first()
    
    # Если пользователь найден, обновляем путь к аватару
    if user:
        user.avatars = avatar_path
        db.commit()
        print(f"Путь к аватару для пользователя {user_id} обновлён: {avatar_path}")
    else:
        print(f"Пользователь с id {user_id} не найден.")

# Функция для загрузки и обработки аватара
@app.post("/api/upload-avatar")
async def upload_avatar(user_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    print("\nНачало обработки запроса на загрузку аватара")
    print(f"Полученный user_id: {user_id}, тип: {type(user_id)}")
    print(f"Имя файла: {file.filename}")
    print(f"Тип файла: {file.content_type}")

    try:
        # Преобразуем user_id в int
        user_id = int(user_id)
        print(f"Преобразованный user_id: {user_id}, тип: {type(user_id)}")
    except ValueError as e:
        print(f"Ошибка преобразования user_id в int: {e}")
        raise HTTPException(status_code=400, detail=f"Некорректный user_id: {user_id}")

    # Проверяем расширение файла
    if file.content_type not in ["image/png", "image/jpeg"]:
        print(f"Неподдерживаемый тип файла: {file.content_type}")
        raise HTTPException(status_code=400, detail="Только PNG и JPEG!")

    # Создаем папки для пользователя
    user_folder = create_avatar_folders(user_id)
    print(f"Папка пользователя: {user_folder}")

    # Генерируем уникальное имя для файла
    file_extension = file.filename.split('.')[-1]
    avatar_filename = f"{uuid.uuid4()}.{file_extension}"
    print(f"Сгенерированное имя файла: {avatar_filename}")

    # Путь для сохранения оригинального файла
    file_path = user_folder / avatar_filename
    print(f"Полный путь для сохранения файла: {file_path}")

    # Сохраняем оригинальный файл
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"Файл успешно сохранен: {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")

    # Проверяем размер файла
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    print(f"Размер файла: {file_size_mb:.2f} MB")
    if file_size_mb > MAX_SIZE_MB:
        print(f"Файл слишком большой ({file_size_mb:.2f} MB), начинаем сжатие...")
        # Если файл слишком большой, сжимаем его
        compressed_path = file_path.with_name(f"compressed_{file.filename}")
        try:
            compress_image(file_path, compressed_path)
            file_path.unlink()  # Удаляем оригинал
            avatar_path = str(file_path)
            uploads_index = avatar_path.lower().find("uploads")
            path_slice = avatar_path[uploads_index:]
            update_user_avatar(user_id, path_slice, db)
            print(f"Оригинальный файл удален: {file_path}")
            return {"filename": compressed_path.name, "status": "Сжат"}
        except Exception as e:
            print(f"Ошибка при сжатии файла: {e}")
            raise HTTPException(status_code=500, detail="Ошибка при сжатии файла")
    else:
        
        avatar_path = str(file_path)
        
        uploads_index = avatar_path.lower().find("uploads")
        path_slice = avatar_path[uploads_index:]
        update_user_avatar(user_id, path_slice, db)
        print("Файл соответствует ограничению по размеру, сжатие не требуется.")
        return {"filename": file.filename, "status": "Загружен"}





    
# @app.get('/api/user/{user_id}')
# def getUsers(user_id: str,  db: Session = Depends(get_db)):
#     user_id_id = int(user_id)
    
#     user = db.query(User).filter(User.id == user_id_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Пользователь не найден")
    
#     return {
#         "id": user.id,
#         "name": user.username,
#         "avatar_url": user.avatars
#     }



@app.get('/api/user/{user_id}')
def get_user_with_stats(user_id: str, db: Session = Depends(get_db)):
    user_id_int = int(user_id)

    user = db.query(User).filter(User.id == user_id_int).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    stats = db.query(
            func.count().filter(Like.is_like == True, Like.user_id == user_id_int).label("likes"),
            func.count().filter(Like.is_like == False, Like.user_id == user_id_int).label("dislikes"),
        ).first()

    view_count = (
        db.query(func.count(View.id))
        .filter(View.user_id == user_id_int)
        .scalar()
    )

    background_url = None
    if user.background_id:
        background = db.query(ProfileBackground).filter(ProfileBackground.id == user.background_id).first()
        if background:
            background_url = background.image_url

    return {
        "id": user.id,
        "name": user.username,
        "avatar_url": user.avatars,
        "likes": stats.likes,
        "dislikes": stats.dislikes,
        "views": view_count,
        "bk_image": background_url
    }



@app.post("/api/track-time")
async def track_time(data: dict, request: Request, db: Session = Depends(get_db)):
    page = data.get("referer")
    time_spent = data.get("time_spent")
    anime_id = data.get('anime_id')
    device_info = data.get('device_info')
    user_id = data.get('user_id')
    

    if not page or not time_spent:
        return {"error": "Неверные данные"}

    # ip = request.client.host
    ip = request.headers.get("X-Forwarded-For") 
    ip_hash = get_ip_hash(ip)

    # Пытаемся достать user_id из токена
    auth_header = request.headers.get("Authorization")
    user_id = None

    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            decoded = decode_access(token)
            user_id = int(decoded.get("sub"))
        except Exception:
            pass

    view = PageView(
        referer=page,
        time_spent=time_spent,
        anime_id=anime_id,
        device_info=device_info,
        user_id=user_id,
        ip_hash=ip_hash
    )
    db.add(view)
    db.commit()

    return {"message": "Время просмотра сохранено"}




# ===================================================== Смотреть позже


@app.post("/api/watch-later/add/{anime_id}")
async def add_watch_later(anime_id: str, request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        token = auth_header.split(" ")[1]
        dec = decode_access(token)
        user_id = int(dec.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    exists = db.query(WatchLater).filter_by(user_id=user_id, anime_id=anime_id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Title already in watch later list")
    
    body = await  request.json()
    type_ = body.get("type")
    api = body.get("api")

    if not type_ or not api:
        raise HTTPException(status_code=400, detail="Missing 'type' or 'api' in request")

    entry = WatchLater(user_id=user_id, anime_id=anime_id , type=type_, api=api)
    db.add(entry)
    db.commit()
    return {"status": "added", "anime_id": anime_id}




@app.delete("/api/watch-later/remove/{anime_id}")
def remove_watch_later(anime_id: str, request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        token = auth_header.split(" ")[1]
        dec = decode_access(token)
        user_id = int(dec.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    entry = db.query(WatchLater).filter_by(user_id=user_id, anime_id=anime_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(entry)
    db.commit()
    return {"status": "removed", "anime_id": anime_id}




@app.get("/api/watch-later/")
def get_watch_later(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        token = auth_header.split(" ")[1]
        decoded = decode_access(token)
        user_id = int(decoded.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    watch_list = db.query(WatchLater).filter_by(user_id=user_id).all()

    results = []

    # movie: '/animeFilm',
    # card: '/animesTitleMine',
    # tv:'/animesTitleMine',
    # ova: '/animeOvaAll',
    # top: '/animeTop',
    # animeongoing: '/animes',
    # ongoing : '/animes',
    # anons: '/animeAnons',
    # search: '/animeSearch'

    for item in watch_list:
        anime = None
        if item.api == '/animesTitleMine':
            anime = db.query(MainTitle).filter_by(id=item.anime_id).first()
        if item.api == '/animes':
            anime = db.query(AnimeSchemaBase).filter_by(id=item.anime_id).first()
        elif item.api == '/animeOvaAll':
            anime = db.query(AnimeOvaBase).filter_by(id=item.anime_id).first()
        elif item.api == '/animeFilm':
            anime = db.query(AnimeFilmBase).filter_by(id=item.anime_id).first()
        elif item.api == '/animeSearch':
            anime = db.query(AnimeSearchTitle).filter_by(id=item.anime_id).first()
        elif item.api == '/animeTop':
            anime = db.query(AnimeTopBase).filter_by(id=item.anime_id).first()

        if anime:
            results.append({
                "id": item.id,
                "type": item.type,
                "api": item.api,
                "data": anime 
            })

    return results


@app.get("/api/watch-later/status/{anime_id}")
def get_watch_later_status(anime_id: str, request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        token = auth_header.split(" ")[1]
        dec = decode_access(token)
        user_id = int(dec.get("sub"))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    entry = db.query(WatchLater).filter_by(user_id=user_id, anime_id=anime_id).first()
    return {"is_added": bool(entry and entry.is_active)}





#==============================================Сохраняем историю просмотров

@app.post("/api/watch-history")
async def save_watch_history(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    ip = request.headers.get("X-Forwarded-For")  #Prod
    # ip = request.client.host
    ip_hash = get_ip_hash(ip)

    # Вытаскиваем поля вручную
    user_id = data.get("user_id")
    anime_id = data.get("anime_id")
    episode = data.get("episode")
    title = data.get("title")
    current_time = data.get("current_time")
    duration = data.get("duration")
    progress = data.get("progress")
    updated_at = data.get("updated_at")
    type = data.get("type")
    api=data.get("api")



    if not all([user_id, anime_id, episode, current_time, duration, progress, updated_at]):
        raise HTTPException(status_code=400, detail="Недостаточно данных")

    # Проверка: существует ли такая запись
    history = db.query(WatchHistory).filter_by(
        user_id=user_id,
        anime_id=anime_id,
        episode=episode
    ).first()

    if history:
        # обновляем
        history.current_time = current_time
        history.duration = duration
        history.progress = progress
        history.updated_at = updated_at
    else:
        # создаём
        history = WatchHistory(
            user_id=user_id,
            anime_id=anime_id,
            ip_hash=ip_hash,
            episode=episode,
            title=title,
            current_time=current_time,
            duration=duration,
            progress=progress,
            updated_at=updated_at,
            created_at=datetime.utcnow(),
            type=type,
            api=api
        )
        db.add(history)

    db.commit()
    return {"status": "saved"}





@app.get("/api/watch-history/{user_id}")
def get_watch_history(
    user_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(6, ge=1, le=50),  # сколько карточек возвращать (по умолчанию 10)
    offset: int = Query(0, ge=0)          # с какого элемента начинать
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    watch_list = (
        db.query(WatchHistory)
        .filter(WatchHistory.user_id == user_id)
        .order_by(WatchHistory.updated_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = (
        db.query(WatchHistory)
        .filter(WatchHistory.user_id == user_id)
        .count()
    )

    MODEL_MAP = {
        '/animesTitleMine': MainTitle,
        '/animes': AnimeSchemaBase,
        '/animeOvaAll': AnimeOvaBase,
        '/animeFilm': AnimeFilmBase,
        '/animeSearch': AnimeSearchTitle,
        '/animeTop': AnimeTopBase
    }

    result = []
    for item in watch_list:
        model = MODEL_MAP.get(item.api)
        anime = db.query(model).filter_by(id=item.anime_id).first() if model else None

        result.append({
            "anime_id": item.anime_id,
            "episode": item.episode,
            "current_time": item.current_time,
            "duration": item.duration,
            "progress": item.progress,
            "updated_at": item.updated_at.isoformat(),
            "title": anime.title if anime else item.title,
            "poster_url": getattr(anime, "poster_url", None),
            "type": item.type
        })

    return {
        "user": {
            "id": user.id,
            "username": user.username,
        },
        "history": result,
        "total": total
    }





###########################################Картинки для фона

@app.get("/api/backgrounds")
def get_profile_backgrounds(db: Session = Depends(get_db)):
    backgrounds = db.query(ProfileBackground).all()
    return [
        {
            "id": bg.id,
            "name": bg.name,
            "image_url": bg.image_url
        }
        for bg in backgrounds
    ]

@app.post("/api/backgrounds/set")
def set_background(request: Request, background_id: int, user_id: int = None, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]  # Извлекаем токен из заголовка Authorization
        # print(token)


        check_token_access = decode_access_token(token=token)
        
        user_id = int(check_token_access.get("sub"))
        # print( user_id, "==========================tooooooken")
        if check_token_access is None:
                raise HTTPException(status_code=401, detail="Invalid access token")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        background = db.query(ProfileBackground).filter(ProfileBackground.id == background_id).first()
        if not background:
            raise HTTPException(status_code=404, detail="Background not found")
        
        user.background_id = background.id
        db.commit()

        return {
                "status": "ok",
                "background": {
                    "id": background.id,
                    "name": background.name,
                    "image_url": background.image_url
                }
            }
    




@app.post("/api/global-backgrounds/set")
def set_background(request: Request, background_id: int, user_id: int = None, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]  # Извлекаем токен из заголовка Authorization
        # print(token)


        check_token_access = decode_access_token(token=token)
        
        user_id = int(check_token_access.get("sub"))
        # print( user_id, "==========================tooooooken")
        if check_token_access is None:
                raise HTTPException(status_code=401, detail="Invalid access token")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        background = db.query(ProfileBackground).filter(ProfileBackground.id == background_id).first()
        if not background:
            raise HTTPException(status_code=404, detail="Background not found")
        
        user.gl_background_id = background.id
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "status": "ok",
        "gl_background_id": user.gl_background_id,
        "background": {
            "id": background.id,
            "name": background.name,
            "image_url": background.image_url
        }
        }

   
#========================================АДМИН




@app.post("/api/adminlogin")
async def admin_login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")

    if user.role != "Admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён: недостаточно прав")

    # 🔐 Генерация токенов
    access_token = create_access_token(data={
        "sub": str(user.id),
        "email": user.email,
        "login": user.username,
        "role": user.role
    })

    refresh_token = create_refresh_token(data={
        "sub": str(user.id),
        "email": user.email,
        "login": user.username,
        "role": user.role
    })

    # 💾 Сохраняем refresh_token в базу
    db_token = Token(
        refresh_token=refresh_token,
        user_id=user.id
    )
    db.add(db_token)
    db.commit()

    # 🌐 Ответ клиенту
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "login": user.username,
        "avatar_url": user.avatars,
        "role": user.role
    })

    # 🍪 Установка куки с refresh_token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        path="/"
    )

    return response


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login") 

EXCLUDED_IPS = [
    'd75c08b022f6eec43cc7124549cc1759dbaa49d2558cd0a2a9af2ee720ad9f3f',
    '990a379d263082b25593fdae33eaa23ec210e63d04facf2b6bb87f9300837fd2'
]




def get_current_admin(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        # Можно использовать твою функцию decode_access_token
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=400, detail="Невалидный токен")

        role = payload.get("role")
        
        if role != "Admin":
            raise HTTPException(status_code=403, detail="Недостаточно прав")

        return payload  # возвращаем всю информацию из токена (user_id, role, email и т.д.)

    except JWTError as e:
        print(f"Ошибка при декодировании токена: {e}")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен",
            headers={"WWW-Authenticate": "Bearer"},
        )



@app.get("/api/admin/stats")
def get_admin_stats(
    period: str = Query("week"),
    db: Session = Depends(get_db),
    admin_data: dict = Depends(get_current_admin)
):
    now = datetime.utcnow()

    # Выбираем дату начала в зависимости от периода
    delta_map = {
        "week": timedelta(days=7),
        "month": timedelta(days=30),
        "halfyear": timedelta(days=180),
        "year": timedelta(days=365)
    }

    if period not in delta_map:
        raise HTTPException(status_code=400, detail="Некорректный период")

    since = now - delta_map[period]

    result = (
        db.query(
            func.date(View.viewed_at).label("day"),
            func.count(distinct(View.ip_hash)).label("views")
        )
        .filter(
            View.viewed_at >= since,
            View.ip_hash.notin_(EXCLUDED_IPS)
        )
        .group_by(func.date(View.viewed_at))
        .order_by(func.date(View.viewed_at))
        .all()
    )

    return [{"date": row.day.isoformat(), "views": row.views} for row in result]



MODEL_MAP = {
    '/animesTitleMine': MainTitle,
    '/animes': AnimeSchemaBase,
    '/animeOvaAll': AnimeOvaBase,
    '/animeFilm': AnimeFilmBase,
    '/animeSearch': AnimeSearchTitle,
    '/animeTop': AnimeTopBase
}

# @app.delete("/api/anime/{anime_id}")
# def delete_anime(anime_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
#     """
#     Удаляет тайтл из всех баз по ID. Только для Admin.
#     Записывает id и title удалённого аниме в файл deleted_anime.log
#     """
#     found = False
#     deleted_items = []

#     for model in MODEL_MAP.values():
#         anime = db.query(model).filter(model.id == anime_id).first()
#         if anime:
#             deleted_items.append({"id": anime.id, "title": getattr(anime, "title", "Unknown")})
#             db.delete(anime)
#             db.commit()
#             found = True
#             # Если нужно удалять только из первой найденной таблицы, можно добавить break

#     if not found:
#         raise HTTPException(status_code=404, detail=f"Аниме с ID {anime_id} не найдено ни в одной таблице")

#     # Записываем удалённые элементы в файл
#     log_file = "/app/logs/deleted_anime.log"
#     with open(log_file, "a", encoding="utf-8") as f:
#         for item in deleted_items:
#             f.write(f"{datetime.now().isoformat()} | ID: {item['id']} | Title: {item['title']}\n")

#     return {"detail": f"Аниме с ID {anime_id} успешно удалено", "deleted": deleted_items}







@app.delete("/api/anime/{anime_id}")
def delete_anime(
    anime_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    found = False
    deleted_items = []

    try:
        # 1. Сначала удалить записи из связующей таблицы
        deleted_links_count = (
            db.query(AL_ONGOING_ANIME_SCHEMA)
            .filter(AL_ONGOING_ANIME_SCHEMA.anime_schema_id == anime_id)
            .delete(synchronize_session=False)
        )

        # 2. Потом удалить аниме из основных таблиц
        for model in MODEL_MAP.values():
            anime = db.query(model).filter(model.id == anime_id).first()
            if anime:
                deleted_items.append({
                    "id": anime.id,
                    "title": getattr(anime, "title", "Unknown"),
                    "table": model.__tablename__
                })
                db.delete(anime)
                found = True

        if not found:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=f"Аниме с ID {anime_id} не найдено ни в одной таблице"
            )

        # 3. Один commit в конце
        db.commit()

        # 4. Лог после успешного commit
        os.makedirs("/app/logs", exist_ok=True)
        log_file = "/app/logs/deleted_anime.log"

        with open(log_file, "a", encoding="utf-8") as f:
            for item in deleted_items:
                f.write(
                    f"{datetime.now().isoformat()} | "
                    f"ID: {item['id']} | "
                    f"Title: {item['title']}\n"
                )

        return {
            "detail": f"Аниме с ID {anime_id} успешно удалено",
            "deleted": deleted_items,
            "deleted_links_count": deleted_links_count
        }

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка целостности данных при удалении: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении аниме: {repr(e)}"
        )








@app.get("/api/top-viewed", response_model=List[dict])
async def get_top_viewed(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)  # только админ
):
    """
    Возвращает топ-10 самых просматриваемых тайтлов,
    исключая определённые ip_hash.
    """
    try:
        stmt = (
            select(
                View.anime_id,
                View.title,
                func.count().label("views_count")
            )
            .group_by(View.anime_id, View.title)
            .order_by(desc("views_count"))
            .limit(20)
        )

        result = db.execute(stmt).all()

        return [
            {
                "anime_id": row.anime_id,
                "title": row.title,
                "views_count": row.views_count
            }
            for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {e}")



#======================================================ПОИСК

from fastapi import APIRouter, Query
import httpx
import os



KODIK_TOKEN = os.getenv("TOKEN")

@app.get("/api/search/anime")
async def search_anime(query: str = Query(..., min_length=1)):
    url = "https://kodik-api.com/search"
    print()

    params = {
        "token": KODIK_TOKEN,
        "type": "anime,anime-serial",
        "with_material_data": "true",
        "title": query
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
       

    return response.json()
