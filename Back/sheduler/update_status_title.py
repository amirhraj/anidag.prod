from sqlalchemy.orm import Session
import os
from sqlalchemy import create_engine, update
from datetime import datetime
# from ..database.database_setup_ongoing import AnimeOngoingBase
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database')))

from database_setup_ongoing import AnimeSchemaBase



# Создаем движок базы данных
engine = create_engine(f"postgresql+psycopg2://{os.getenv('BD_ADMIN')}:{os.getenv('BD_PASS')}@localhost:5435", echo=True)

with open("/test.log", "a") as logfile:
    logfile.write("Скрипт меняет статус выполнен выполнен в: " + str(datetime.now()) + "\n")

session = Session(bind=engine)

# Функция для обновления статуса аниме
def update_anime_status():
    animes = session.query(AnimeSchemaBase).all()
    
    for anime in animes:
        print(anime)
        if anime.material_data['episodes_total'] == anime.episodes_count:
            stmt = (
                update(AnimeSchemaBase)
                .where(AnimeSchemaBase.id == anime.id)
                .values(anime_status='released')
            )
            session.execute(stmt)
    session.commit()

# Запускаем обновление статусов
update_anime_status()