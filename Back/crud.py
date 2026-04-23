from sqlalchemy.orm import Session
from sqlalchemy import select, desc
# from database.database_setup_ongoing import Season as SeasonModel, Episode as EpisodeModel
# from models.ongoing_model import AnimeSchema, Season, Episode , MaterialData
from sqlalchemy.exc import IntegrityError
from database.database_setup_ongoing import AnimeSchemaBase
from database.database_main_titles import MainTitle
from database.database_setup_OVA import AnimeOvaBase
from database.database_films import AnimeFilmBase 
from database.database_anons import AnimeAnons
from database.database_Top100anime import AnimeTopBase
from database.database_search import AnimeSearchTitle
from database.db_al_ongoing import AL_ONGOING
from database.async_db import async_engine , Base, AsyncSessionLocal
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime,timezone
from database.db_al_film import AnimeAllohaFilm
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
import json
import os


def decode_unicode(json_str):
    return json.loads(json_str, strict=False)

 # Импортируйте модель из правильного модуля







# SKIP_IDS = {'serial-59734', 'serial-59956','serial-68150' , 'serial-68260', 'serial-68198'}
SKIP_TITLE = {'Адский учитель Нубэ [ТВ-2, часть 1]'}

LOG_FILE = "/app/logs/deleted_anime.log"
def load_skip_from_log():
    """
    Читает лог и возвращает два множества:
    - skip_ids: ID удалённых аниме
    - skip_titles: title удалённых аниме
    """
    skip_ids = set()
    skip_titles = set()
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                # ожидаем формат: "2025-09-11T12:34:56 | ID: serial-69558 | Title: My Anime Title"
                parts = line.strip().split("|")
                if len(parts) >= 3:
                    id_part = parts[1].strip()
                    title_part = parts[2].strip()
                    
                    if id_part.startswith("ID: "):
                        skip_ids.add(id_part.replace("ID: ", ""))
                    if title_part.startswith("Title: "):
                        skip_titles.add(title_part.replace("Title: ", ""))
    return skip_ids, skip_titles

def add_anime(anime_data: dict, db: Session):
    results = []
    not_add = []
    skip_ids, skip_titles = load_skip_from_log()

    for anime in anime_data["results"]:
        # if anime["id"] in skip_ids:
        #     continue
        if anime["title"] in skip_titles:
            continue
        # if anime.get("year") and int(anime["year"]) > 2024:
        #     continue
        # Запрос к базе данных, чтобы найти запись тайтла
        existing_anime = db.query(AnimeSchemaBase) \
            .filter(AnimeSchemaBase.title == anime["title"]) \
            .order_by(AnimeSchemaBase.updated_at.desc()) \
            .first()

        current_date = datetime.now()

        if existing_anime:
            # Сравнение количества вышедших эпизодов
            if anime['episodes_count'] > existing_anime.episodes_count:
            # if anime["material_data"].get("next_episode_at") == current_date:
                # Обновление полей существующего аниме
                existing_anime.episodes_count = anime["episodes_count"]
                existing_anime.last_season = anime["last_season"]
                existing_anime.last_episode = anime["last_episode"]
                existing_anime.updated_at = anime["updated_at"]
                existing_anime.personupdate = datetime.now(timezone.utc)

                # Обновляем остальные поля
                existing_anime.type = anime.get("type")
                existing_anime.link = anime.get("link")
                existing_anime.title_orig = anime["title_orig"]
                existing_anime.year = anime["year"]
                existing_anime.kinopoisk_id = anime.get("kinopoisk_id")
                existing_anime.imdb_id = anime.get("imdb_id")
                existing_anime.worldart_link = anime.get("worldart_link")
                existing_anime.shikimori_id = anime.get("shikimori_id")
                existing_anime.quality = anime["quality"]
                existing_anime.camrip = anime["camrip"]
                existing_anime.lgbt = anime["lgbt"]
                existing_anime.blocked_countries = anime["blocked_countries"]
                existing_anime.blocked_seasons = anime["blocked_seasons"]
                existing_anime.created_at = anime["created_at"]
                existing_anime.material_data = anime["material_data"]
                existing_anime.screenshots = anime["screenshots"]
                existing_anime.premiere_world = anime["material_data"].get("premiere_world")
                existing_anime.aired_at = anime["material_data"].get("aired_at")
                existing_anime.released_at = anime["material_data"].get("released_at")
                existing_anime.countries = anime["material_data"].get("countries") if not existing_anime.countries else existing_anime.countries
                # existing_anime.description = anime["material_data"].get("description")
                # existing_anime.anime_description = anime["material_data"].get("anime_description")
                # existing_anime.poster_url = anime["material_data"].get("poster_url")
                # existing_anime.anime_poster_url = anime["material_data"].get("anime_poster_url")
                existing_anime.anime_studios = anime["material_data"].get("anime_studios")
                existing_anime.next_episode_at = anime["material_data"].get("next_episode_at")
                existing_anime.anime_genres = anime["material_data"].get("anime_genres")
                # existing_anime.anime_kind = anime["material_data"].get("anime_kind")
                existing_anime.all_status = anime["material_data"].get("all_status")
                existing_anime.anime_status = anime["material_data"].get("anime_status")
                existing_anime.episodes_total = anime["material_data"].get("episodes_total")
                existing_anime.kinopoisk_rating = anime["material_data"].get("kinopoisk_rating")
                existing_anime.shikimori_rating = anime["material_data"].get("shikimori_rating")                

                try: 
                    db.commit() 
                    db.refresh(existing_anime) 
                    results.append(existing_anime) 
                    print(f"Тайтл '{existing_anime.title}' обновлен в базе данных.") 
                except IntegrityError as e: 
                    db.rollback() 
                    print(f"Ошибка: не удалось обновить тайтл '{existing_anime.title}' из-за конфликта целостности. {str(e)}")
            else:
                not_add.append(existing_anime.title)
                print(f"Новых серий для '{existing_anime.title}' нет, обновление не требуется")
        else:
            # Если тайтл не найден, создаем новую запись
            new_anime = AnimeSchemaBase(
                id=anime["id"],
                type=anime.get("type"),
                link=anime.get("link"),
                title=anime["title"],
                title_orig=anime["title_orig"],
                year=anime["year"],
                last_season=anime["last_season"],
                last_episode=anime["last_episode"],
                episodes_count=anime["episodes_count"],
                kinopoisk_id=anime.get("kinopoisk_id"),
                imdb_id=anime.get("imdb_id"),
                worldart_link=anime.get("worldart_link"),
                shikimori_id=anime.get("shikimori_id"),
                quality=anime["quality"],
                camrip=anime["camrip"],
                lgbt=anime["lgbt"],
                blocked_countries=anime["blocked_countries"],
                blocked_seasons=anime["blocked_seasons"],
                created_at=anime["created_at"],
                updated_at=anime["updated_at"],
                seasons=anime["seasons"],
                material_data=anime["material_data"],
                screenshots=anime["screenshots"],
                personupdate = datetime.now(timezone.utc),
                premiere_world=anime["material_data"].get("premiere_world"),
                aired_at=anime["material_data"].get("aired_at"),
                released_at=anime["material_data"].get("released_at"),
                countries=anime["material_data"].get("countries"),
                description=anime["material_data"].get("description"),
                anime_description =anime["material_data"].get("anime_description"),
                poster_url = anime["material_data"].get("poster_url"),
                anime_poster_url = anime["material_data"].get("anime_poster_url"),
                anime_studios = anime["material_data"].get("anime_studios"),
                next_episode_at = anime["material_data"].get("next_episode_at"),
                anime_genres = anime["material_data"].get("anime_genres"),
                # anime_kind = anime["material_data"].get("anime_kind"),
                all_status =  anime["material_data"].get("all_status"),
                anime_status =  anime["material_data"].get("anime_status"),
                episodes_total = anime["material_data"].get("episodes_total"),
                kinopoisk_rating = anime["material_data"].get("kinopoisk_rating"),
                shikimori_rating = anime["material_data"].get("shikimori_rating")               

            )
            try:
                db.add(new_anime)
                db.commit()
                db.refresh(new_anime)
                results.append(new_anime)
                print(f"Тайтл '{new_anime.title}' добавлен в базу данных.")
            except IntegrityError:
                db.rollback()
                print(f"Ошибка: не удалось добавить тайтл '{new_anime.title}' из-за конфликта целостности.")
 
    return results





# def add_anime_main(anime_data: dict, db: Session):
#     results = []
#     skip_ids, skip_titles = load_skip_from_log()

#     for anime in anime_data["results"]:
#         if anime["title"] in skip_titles:
#                 continue
#         exists = db.query(MainTitle).filter_by(title_orig=anime["title_orig"]).first()
#         if exists:
#             continue
       
#         anime_db = MainTitle(
#             id=anime["id"],
#             type=anime.get("type"),
#             link=anime.get("link"),
#             title=anime["title"],
#             title_orig=anime["title_orig"],
#             # other_title=anime.get("other_title"),
#             # translation_id=None,
#             year=anime["year"],
#             last_season=anime["last_season"],
#             last_episode=anime["last_episode"],
#             episodes_count=anime["episodes_count"],
#             kinopoisk_id=anime.get("kinopoisk_id"),
#             imdb_id=anime.get("imdb_id"),
#             worldart_link=anime.get("worldart_link"),
#             shikimori_id=anime["shikimori_id"],
#             quality=anime["quality"],
#             camrip=anime["camrip"],
#             lgbt=anime["lgbt"],
#             blocked_countries=anime["blocked_countries"],
#             blocked_seasons=anime["blocked_seasons"],
#             created_at=anime["created_at"],
#             updated_at=anime["updated_at"],
#             seasons=anime["seasons"],
#             material_data=anime["material_data"],
#             screenshots=anime["screenshots"],
#             premiere_world=anime["material_data"].get("premiere_world"),
#             aired_at=anime["material_data"].get("aired_at"),
#             released_at=anime["material_data"].get("released_at"),
#             countries=anime["material_data"].get("countries"),
#             description=anime["material_data"].get("description"),
#             anime_description =anime["material_data"].get("anime_description"),
#             poster_url = anime["material_data"].get("poster_url"),
#             anime_poster_url = anime["material_data"].get("anime_poster_url"),
#             anime_studios = anime["material_data"].get("anime_studios"),
#             next_episode_at = anime["material_data"].get("next_episode_at"),
#             anime_genres = anime["material_data"].get("anime_genres"),
#             # anime_kind = anime["material_data"].get("anime_kind"),
#             all_status =  anime["material_data"].get("all_status"),
#             anime_status =  anime["material_data"].get("anime_status")            
#         )
#         try:
      
#             db.add(anime_db)
#             db.commit()
#             db.refresh(anime_db)
#             results.append(anime_db)
#         except IntegrityError:
#             db.rollback()
#     return results

from sqlalchemy.exc import IntegrityError


def add_anime_main(anime_data: dict, db: Session):
    results = []
    skip_ids, skip_titles = load_skip_from_log()


    for anime in anime_data["results"]:
        # print(anime["title"] in skip_titles,anime["title"],  "SKIIIIIIIIIP")
        if anime["title"] in skip_titles:
            continue

        exists = db.query(MainTitle.id).filter_by(title_orig=anime["title_orig"]).first()
        if exists:
            continue

        anime_db = MainTitle(
            id=anime["id"],
            type=anime.get("type"),
            link=anime.get("link"),
            title=anime["title"],
            title_orig=anime["title_orig"],
            year=anime["year"],
            last_season=anime["last_season"],
            last_episode=anime["last_episode"],
            episodes_count=anime["episodes_count"],
            kinopoisk_id=anime.get("kinopoisk_id"),
            imdb_id=anime.get("imdb_id"),
            worldart_link=anime.get("worldart_link"),
            shikimori_id=anime["shikimori_id"],
            quality=anime["quality"],
            camrip=anime["camrip"],
            lgbt=anime["lgbt"],
            blocked_countries=anime["blocked_countries"],
            blocked_seasons=anime["blocked_seasons"],
            created_at=anime["created_at"],
            updated_at=anime["updated_at"],
            seasons=anime["seasons"],
            material_data=anime["material_data"],
            screenshots=anime["screenshots"],
            premiere_world=anime["material_data"].get("premiere_world"),
            aired_at=anime["material_data"].get("aired_at"),
            released_at=anime["material_data"].get("released_at"),
            countries=anime["material_data"].get("countries"),
            description=anime["material_data"].get("description"),
            anime_description=anime["material_data"].get("anime_description"),
            poster_url=anime["material_data"].get("poster_url"),
            anime_poster_url=anime["material_data"].get("anime_poster_url"),
            anime_studios=anime["material_data"].get("anime_studios"),
            next_episode_at=anime["material_data"].get("next_episode_at"),
            anime_genres=anime["material_data"].get("anime_genres"),
            all_status=anime["material_data"].get("all_status"),
            anime_status=anime["material_data"].get("anime_status")
        )

        db.add(anime_db)
        results.append(anime_db)

    try:
        db.commit()
        for anime_db in results:
            db.refresh(anime_db)
    except IntegrityError:
        db.rollback()
        return []

    return results


def add_anime_ova(anime_data: dict, db: Session):
    results = []
    for anime in anime_data["results"]:
        exists = db.query(AnimeOvaBase.id).filter_by(title_orig=anime["title_orig"]).first()
        if exists:
            continue
        anime_db = AnimeOvaBase(
            id=anime["id"],
            type=anime.get("type"),
            link=anime.get("link"),
            title=anime["title"],
            title_orig=anime["title_orig"],
            # other_title=anime.get("other_title"),
            # translation_id=None,
            year=anime["year"],
            # last_season=anime["last_season"],
            # last_episode=anime["last_episode"],
            # episodes_count=anime["episodes_count"],
            kinopoisk_id=anime.get("kinopoisk_id"),
            imdb_id=anime.get("imdb_id"),
            worldart_link=anime.get("worldart_link"),
            shikimori_id=anime["shikimori_id"],
            quality=anime["quality"],
            camrip=anime["camrip"],
            lgbt=anime["lgbt"],
            blocked_countries=anime["blocked_countries"],
            # blocked_seasons=anime["blocked_seasons"],
            created_at=anime["created_at"],
            updated_at=anime["updated_at"],
            material_data=anime["material_data"],
            screenshots=anime["screenshots"],
            premiere_world=anime["material_data"].get("premiere_world"),
            aired_at=anime["material_data"].get("aired_at"),
            released_at=anime["material_data"].get("released_at"),
            countries=anime["material_data"].get("countries"),
            description=anime["material_data"].get("description"),
            anime_description =anime["material_data"].get("anime_description"),
            poster_url = anime["material_data"].get("poster_url"),
            anime_poster_url = anime["material_data"].get("anime_poster_url"),
            anime_studios = anime["material_data"].get("anime_studios"),
            anime_genres = anime["material_data"].get("anime_genres"),
            all_status =  anime["material_data"].get("all_status"),
            anime_status =  anime["material_data"].get("anime_status") 
            
        )
        try:
      
            db.add(anime_db)
            db.commit()
            db.refresh(anime_db)
            results.append(anime_db)
        except IntegrityError:
            db.rollback()
    return results

def add_anime_film(anime_data: dict, db: Session):
    results = []
    for anime in anime_data["results"]:
        exists = db.query(AnimeFilmBase.id).filter_by(title_orig=anime["title_orig"]).first()
        if exists:
            continue
       
        anime_db = AnimeFilmBase(
            id=anime["id"],
            type=anime.get("type"),
            link=anime.get("link"),
            title=anime["title"],
            title_orig=anime["title_orig"],
            year=anime["year"],
            kinopoisk_id=anime.get("kinopoisk_id"),
            imdb_id=anime.get("imdb_id"),
            worldart_link=anime.get("worldart_link"),
            shikimori_id=anime.get("shikimori_id"),
            quality=anime["quality"],
            camrip=anime["camrip"],
            lgbt=anime["lgbt"],
            blocked_countries=anime["blocked_countries"],
            created_at=anime["created_at"],
            updated_at=anime["updated_at"],
            material_data=anime["material_data"],
            screenshots=anime["screenshots"],
            premiere_world=anime["material_data"].get("premiere_world"),
            aired_at=anime["material_data"].get("aired_at"),
            released_at=anime["material_data"].get("released_at"),
            anime_studios = anime["material_data"].get("anime_studios"),
            countries = anime["material_data"].get("countries"),
            description = anime["material_data"].get("description"),
            anime_description = anime["material_data"].get("anime_description"),
            anime_kind = anime["material_data"].get("anime_kind"),
            poster_url = anime["material_data"].get("poster_url"),
            anime_poster_url = anime["material_data"].get("anime_poster_url")
        )
        try:
      
            db.add(anime_db)
            db.commit()
            db.refresh(anime_db)
            results.append(anime_db)
        except IntegrityError:
            db.rollback()
    return results





async def add_anime_film_al(anime_data: list, db: AsyncSession):
    results = []
    # print( anime_data, "ANIMEDATA")
    for anime in anime_data["data"]:
        # print(anime["name"], "=====================ANIMEDATA")
        # print("Обрабатывается аниме:", anime.get("name"), "ID:", anime.get("id_imdb"))

        anime_db = AnimeAllohaFilm(
            # id=anime["id_imdb"],
            # type=anime.get("type"),
            link=anime["iframe"],
            iframe = anime["iframe"],
            title=anime["name"],
            name=anime["name"],
            token_movie=anime["token_movie"],
            genre = anime[ "genre"],
            age_restrictions = anime["age_restrictions"],
            rating_kp = anime["rating_kp"],
            rating_imdb = anime["rating_imdb"],
            title_orig=anime["original_name"],
            year=int(anime["premiere"].split("-")[0]) if anime.get("premiere") else None,
            quality=anime["quality"],
            lgbt=anime["lgbt"],
            countries=anime["country"],
            description=anime["description"],
            poster_url=anime["poster"]
        )

        try:
            db.add(anime_db)
            await db.commit()
            await db.refresh(anime_db)
            results.append(anime_db)
        # except IntegrityError:
        except Exception as e:
            print("Ошибка при добавлении аниме:", anime.get("name"))
            print(e, "ОШИБКА")
            await db.rollback()
    return results




def add_anime_anons(anime_data: dict, db: Session):
    results = []
    for anime in anime_data["animes"]:
       
        anime_db = AnimeAnons(
            id=anime["id"],
            mal_id=anime["malId"],  # ID с MyAnimeList
            name=anime["name"],  # Название аниме
            russian_name=anime["russian"],  # Русское название
            english_name=anime.get("english"),  # Английское название
            japanese_name=anime["japanese"],  # Японское название
            kind=anime["kind"],  # Тип аниме (например, tv)
            rating=anime["rating"],  # Рейтинг (например, pg)
            score=anime["score"],  # Оценка
            status=anime["status"],  # Статус (например, "anons")
            episodes=anime["episodes"],  # Количество серий
            episodes_aired=anime["episodesAired"],  # Вышедшие серии
            duration=anime["duration"],  # Длительность серий
            aired_on=anime["airedOn"],  # Дата выхода (JSON)
            released_on=anime["releasedOn"],  # Дата релиза (JSON)
            url=anime["url"],  # Ссылка на аниме
            season=anime["season"],  # Сезон (например, весна, лето)
            poster=anime["poster"],  # Информация о постере (JSON)
            created_at=anime["createdAt"],  # Дата создания записи
            updated_at=anime["updatedAt"],  # Дата обновления записи
            next_episode_at=anime["nextEpisodeAt"],  # Дата выхода следующей серии
            is_censored=anime.get("isCensored", False),  # Наличие цензуры
            genres=anime["genres"],  # Жанры (JSON)
            studios=anime["studios"],  # Студии (JSON)
            videos=anime.get("videos", []),  # Видео (если есть)
            description=anime.get("description") # Описание аниме
        )
        try:
      
            db.add(anime_db)
            db.commit()
            db.refresh(anime_db)
            results.append(anime_db)
        except Exception as e:
                    db.rollback()
                    print(f"Ошибка при добавлении аниме: {str(e)}")
                    raise e
    return results

def add_anime_top(anime_data: dict, db: Session):
    results = []
    for anime in anime_data["results"]:
        exists = db.query(AnimeTopBase.id).filter_by(title_orig=anime["title_orig"]).first()
        
        if exists:
            
            continue
        print(anime["title"], "TUT")
        anime_db = AnimeTopBase(
            id=anime["id"],
            type=anime.get("type"),
            link=anime.get("link"),
            title=anime["title"],
            title_orig=anime["title_orig"],
            other_title=anime.get("other_title"),
            # translation_id=None,
            year=anime["year"],
            last_season=anime["last_season"],
            last_episode=anime["last_episode"],
            episodes_count=anime["episodes_count"],
            kinopoisk_id=anime.get("kinopoisk_id"),
            imdb_id=anime.get("imdb_id"),
            worldart_link=anime.get("worldart_link"),
            shikimori_id=anime["shikimori_id"],
            quality=anime["quality"],
            camrip=anime["camrip"],
            lgbt=anime["lgbt"],
            blocked_countries=anime["blocked_countries"],
            blocked_seasons=anime["blocked_seasons"],
            created_at=anime["created_at"],
            updated_at=anime["updated_at"],
            material_data=anime["material_data"],
            screenshots=anime["screenshots"],
            premiere_world=anime["material_data"].get("premiere_world"),
            aired_at=anime["material_data"].get("aired_at"),
            released_at=anime["material_data"].get("released_at"),
            countries=anime["material_data"].get("countries"),
            description=anime["material_data"].get("description"),
            anime_description =anime["material_data"].get("anime_description"),
            poster_url = anime["material_data"].get("poster_url"),
            anime_poster_url = anime["material_data"].get("anime_poster_url"),
            anime_studios = anime["material_data"].get("anime_studios"),
            next_episode_at = anime["material_data"].get("next_episode_at"),
            anime_genres = anime["material_data"].get("anime_genres"),
            # anime_kind = anime["material_data"].get("anime_kind"),
            all_status =  anime["material_data"].get("all_status"),
            anime_status =  anime["material_data"].get("anime_status"),
            episodes_total = anime["material_data"].get("episodes_total"),
            kinopoisk_rating = anime["material_data"].get("kinopoisk_rating"),
            shikimori_rating = anime["material_data"].get("shikimori_rating")
        )
        try:
      
            db.add(anime_db)
            db.commit()
            db.refresh(anime_db)
            results.append(anime_db)
        except Exception as e:
                    db.rollback()
                    print(f"Ошибка при добавлении аниме: {str(e)}")
                    raise e
    return results




def add_anime_search(anime_data: dict, db: Session):
    results = []
    not_add = []

    skip_ids, skip_titles = load_skip_from_log()

    for anime in anime_data["results"]:
        anime_genres = anime.get("material_data", {}).get("anime_genres", [])
        if isinstance(anime_genres, str):
            try:
                import json
                anime_genres = json.loads(anime_genres)
            except:
                anime_genres = []

        if anime["title"] in skip_titles:
            continue

        if any("хентай" in genre.lower() or "hentai" in genre.lower() for genre in anime_genres):
            print(f"Пропущен тайтл '{anime.get('title')}' — жанр содержит хентай.")
            continue
        # Запрос к базе данных, чтобы найти запись тайтла
        existing_anime = db.query(AnimeSearchTitle) \
            .filter(AnimeSearchTitle.title == anime["title"]) \
            .order_by(AnimeSearchTitle.updated_at.desc()) \
            .first()

        if existing_anime:
            # Сравнение количества вышедших эпизодов
            # if anime['episodes_count'] > existing_anime.episodes_count:
            episodes_count = anime.get("episodes_count")
            if isinstance(episodes_count, int) and existing_anime.episodes_count is not None and episodes_count > existing_anime.episodes_count:
                existing_anime.episodes_count = episodes_count
                # Обновление полей существующего аниме
                existing_anime.episodes_count = anime["episodes_count"]
                existing_anime.last_season = anime["last_season"]
                existing_anime.last_episode = anime["last_episode"]
                existing_anime.updated_at = anime["updated_at"]
                existing_anime.personupdate = datetime.now(timezone.utc)

                # Обновляем остальные поля
                existing_anime.type = anime.get("type")
                existing_anime.link = anime.get("link")
                existing_anime.title_orig = anime["title_orig"]
                existing_anime.year = anime["year"]
                existing_anime.kinopoisk_id = anime.get("kinopoisk_id")
                existing_anime.imdb_id = anime.get("imdb_id")
                existing_anime.worldart_link = anime.get("worldart_link")
                existing_anime.shikimori_id = anime.get("shikimori_id")
                existing_anime.quality = anime["quality"]
                existing_anime.camrip = anime["camrip"]
                existing_anime.lgbt = anime["lgbt"]
                existing_anime.blocked_countries = anime["blocked_countries"]
                existing_anime.blocked_seasons = anime["blocked_seasons"]
                existing_anime.created_at = anime["created_at"]
                existing_anime.material_data = anime["material_data"]
                existing_anime.screenshots = anime["screenshots"]
                existing_anime.premiere_world = anime["material_data"].get("premiere_world")
                existing_anime.aired_at = anime["material_data"].get("aired_at")
                existing_anime.released_at = anime["material_data"].get("released_at")
                existing_anime.countries = anime["material_data"].get("countries") if not existing_anime.countries else existing_anime.countries
                existing_anime.description = anime["material_data"].get("description")
                existing_anime.anime_description = anime["material_data"].get("anime_description")
                existing_anime.poster_url = anime["material_data"].get("poster_url")
                existing_anime.anime_poster_url = anime["material_data"].get("anime_poster_url")
                existing_anime.anime_studios = anime["material_data"].get("anime_studios")
                existing_anime.next_episode_at = anime["material_data"].get("next_episode_at")
                existing_anime.anime_genres = anime["material_data"].get("anime_genres")
                # existing_anime.anime_kind = anime["material_data"].get("anime_kind")
                existing_anime.all_status = anime["material_data"].get("all_status")
                existing_anime.anime_status = anime["material_data"].get("anime_status")
                existing_anime.episodes_total = anime["material_data"].get("episodes_total")
                existing_anime.kinopoisk_rating = anime["material_data"].get("kinopoisk_rating")
                existing_anime.shikimori_rating = anime["material_data"].get("shikimori_rating")

                try: 
                    db.commit() 
                    db.refresh(existing_anime) 
                    results.append(existing_anime) 
                    print(f"Тайтл '{existing_anime.title}' обновлен в базе данных.") 
                except IntegrityError as e: 
                    db.rollback() 
                    print(f"Ошибка: не удалось обновить тайтл '{existing_anime.title}' из-за конфликта целостности. {str(e)}")
            else:
                not_add.append(existing_anime.title)
                # print(f"Новых серий для '{existing_anime.title}' нет, обновление не требуется")
        else:
            # Если тайтл не найден, создаем новую запись
# Нормализация значений
               
            last_season = anime.get("last_season") if isinstance(anime.get("last_season"), int) else None
            last_episode = anime.get("last_episode") if isinstance(anime.get("last_episode"), int) else None

            blocked_seasons = anime.get("blocked_seasons")
            if isinstance(blocked_seasons, str):
                    blocked_seasons = None

            seasons = anime.get("seasons", {})
            if isinstance(seasons, str):
                    try:
                        import json
                        seasons = json.loads(seasons)
                    except:
                        seasons = {}

            material_data = anime.get("material_data")
            if isinstance(material_data, str):
                    try:
                        import json
                        material_data = json.loads(material_data)
                    except:
                        material_data = {}

            episodes_count = anime.get("episodes_count")
            if not isinstance(episodes_count, int):
                try:
                    episodes_count = int(episodes_count)
                except (TypeError, ValueError):
                    episodes_count = None


            new_anime = AnimeSearchTitle(
                id=anime["id"],
                type=anime.get("type"),
                link=anime.get("link"),
                title=anime["title"],
                title_orig=anime["title_orig"],
                year=anime["year"],
                last_season=anime.get("last_season"),
                # last_episode=anime.get("last_episode"),
                last_episode=last_episode,
                episodes_count=episodes_count,
                kinopoisk_id=anime.get("kinopoisk_id"),
                imdb_id=anime.get("imdb_id"),
                worldart_link=anime.get("worldart_link"),
                shikimori_id=anime.get("shikimori_id"),
                quality=anime["quality"],
                camrip=anime["camrip"],
                lgbt=anime["lgbt"],
                blocked_countries=anime["blocked_countries"],
                blocked_seasons=blocked_seasons,
                created_at=anime["created_at"],
                updated_at=anime["updated_at"],
                seasons=anime.get("seasons", {}),
                material_data=material_data,
                screenshots=anime["screenshots"],
                personupdate = datetime.now(timezone.utc),
                premiere_world=anime["material_data"].get("premiere_world"),
                aired_at=anime["material_data"].get("aired_at"),
                released_at=anime["material_data"].get("released_at"),
                countries=anime["material_data"].get("countries"),
                description=anime["material_data"].get("description"),
                anime_description =anime["material_data"].get("anime_description"),
                poster_url = anime["material_data"].get("poster_url"),
                anime_poster_url = anime["material_data"].get("anime_poster_url"),
                anime_studios = anime["material_data"].get("anime_studios"),
                next_episode_at = anime["material_data"].get("next_episode_at"),
                anime_genres = anime["material_data"].get("anime_genres"),
                anime_kind = anime["material_data"].get("anime_kind"),
                all_status =  anime["material_data"].get("all_status"),
                anime_status =  anime["material_data"].get("anime_status"),
                episodes_total = anime["material_data"].get("episodes_total"),
                kinopoisk_rating = anime["material_data"].get("kinopoisk_rating"),
                shikimori_rating = anime["material_data"].get("shikimori_rating")

            )
            try:
                db.add(new_anime)
                db.commit()
                db.refresh(new_anime)
                results.append(new_anime)
                print(f"Тайтл '{new_anime.title}' добавлен в базу данных.")
            except IntegrityError:
                db.rollback()
                print(f"Ошибка: не удалось добавить тайтл '{new_anime.title}' из-за конфликта целостности.")
 
    return results

async def add_alloha_ongoing(movies: list[dict]):
    async with AsyncSessionLocal() as session:
        for item in movies:
            token = item.get("token")
            if not token:
                continue

            stmt = select(AL_ONGOING).where(AL_ONGOING.token == token)
            result = await session.execute(stmt)
            movie = result.scalar_one_or_none()

            ids = item.get("ids", {}) or {}
            rating = item.get("rating", {}) or {}
            category = item.get("category", {}) or {}

            movie_data = {
                "token": token,
                "name": item.get("name"),
                "original_name": item.get("original_name"),
                "alternative_name": item.get("alternative_name"),
                "year": item.get("year"),
                "kp_id": ids.get("kp"),
                "imdb_id": ids.get("imdb"),
                "tmdb_id": ids.get("tmdb"),
                "world_art_id": ids.get("world_art"),
                "date": item.get("date"),
                "country": item.get("country"),
                "genre": item.get("genre"),
                "rating_kp": rating.get("kp"),
                "rating_imdb": rating.get("imdb"),
                "poster": item.get("poster"),
                "iframe": item.get("iframe"),
                "category_slug": category.get("slug"),
                "category_name": category.get("name"),
                "translations": item.get("translations"),
                "seasons": item.get("seasons"),
                "raw_data": item,
            }

            if movie:
                for key, value in movie_data.items():
                    setattr(movie, key, value)
            else:
                session.add(AL_ONGOING(**movie_data))

        await session.commit()