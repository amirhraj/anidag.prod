from sqlalchemy import String, Integer, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from database.async_db import Base


class AL_ONGOING(Base):
    __tablename__ = "al_ongoing"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    token: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(500))
    original_name: Mapped[str | None] = mapped_column(String(500))
    alternative_name: Mapped[str | None] = mapped_column(String(500))
    year: Mapped[int | None] = mapped_column(Integer)

    kp_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    imdb_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tmdb_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    world_art_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    date: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(255))
    genre: Mapped[str | None] = mapped_column(Text)

    rating_kp: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating_imdb: Mapped[float | None] = mapped_column(Float, nullable=True)

    poster: Mapped[str | None] = mapped_column(Text)
    iframe: Mapped[str | None] = mapped_column(Text)

    category_slug: Mapped[str | None] = mapped_column(String(100))
    category_name: Mapped[str | None] = mapped_column(String(255))

    translations: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    seasons: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)




#     CREATE TABLE al_ongoing (
#     id SERIAL PRIMARY KEY,

#     token VARCHAR(255) UNIQUE,
#     name VARCHAR(500),
#     original_name VARCHAR(500),
#     alternative_name VARCHAR(500),
#     year INTEGER,

#     kp_id INTEGER,
#     imdb_id VARCHAR(100),
#     tmdb_id INTEGER,
#     world_art_id INTEGER,

#     date VARCHAR(100),
#     country VARCHAR(255),
#     genre TEXT,

#     rating_kp FLOAT,
#     rating_imdb FLOAT,

#     poster TEXT,
#     iframe TEXT,

#     category_slug VARCHAR(100),
#     category_name VARCHAR(255),

#     translations JSON,
#     seasons JSON,
#     raw_data JSON
# );


# CREATE INDEX idx_al_ongoing_token ON al_ongoing(token);


#  select * from anime_schema t 
 
 
# CREATE EXTENSION IF NOT EXISTS pgcrypto;


# CREATE TABLE public.al_ongoing_anime_schema (
#     id SERIAL PRIMARY KEY,

#     al_ongoing_id INTEGER,
#     anime_schema_id VARCHAR,

#     common_uid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),

#     CONSTRAINT fk_al_ongoing
#         FOREIGN KEY (al_ongoing_id)
#         REFERENCES public.al_ongoing(id),

#     CONSTRAINT fk_anime_schema
#         FOREIGN KEY (anime_schema_id)
#         REFERENCES public.anime_schema(id),

#     CONSTRAINT uq_pair
#         UNIQUE (al_ongoing_id, anime_schema_id)
# );


# truncate al_ongoing_anime_schema

# select * from al_ongoing_anime_schema

# select ao.original_name, ao."name"   from al_ongoing ao 

# select t.title_orig , t.title, a."name"   from   al_ongoing_anime_schema ao 
# join  anime_schema t  on t.id = ao.anime_schema_id
# join al_ongoing a  on a.id = ao.al_ongoing_id
# where true



# SELECT column_name
# FROM information_schema.columns
# WHERE table_name = 'al_ongoing';

# SELECT column_name, data_type, character_maximum_length
# FROM information_schema.columns
# WHERE table_name = 'anime_schema'
#   AND column_name = 'id';