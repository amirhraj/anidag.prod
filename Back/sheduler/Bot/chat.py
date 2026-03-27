import requests
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from datetime import datetime

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = '@anidagHD'

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Подключение к БД
# engine = create_engine(f"postgresql+psycopg2://{os.getenv('BD_ADMIN')}:{os.getenv('BD_PASS')}@localhost:5435", echo=False)
engine = create_engine(f"postgresql+psycopg2://{os.getenv('BD_ADMIN')}:{os.getenv('BD_PASS')}@213.139.210.103", echo=True)


with open("/test.log", "a") as logfile:
    logfile.write("Скрипт по обновлению серий в телеграмм выполнен в: " + str(datetime.now()) + "\n")
# Получить время последней отправки
try:
    with open("last_sent.txt", "r") as f:
        last_sent_time = datetime.fromisoformat(f.read().strip())
except FileNotFoundError:
    last_sent_time = datetime.min  # самый ранний возможный

# Найти записи новее
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT id, title, personupdate, description, poster_url FROM public.anime_schema
        WHERE personupdate > :last_sent
        ORDER BY personupdate ASC
    """), {"last_sent": last_sent_time}).fetchall()


for row in result:
    # Формируем текст
    title = row.title
    description = row.description or "Описание отсутствует."
    poster_url = row.poster_url
    # https://www.anidag.ru/card/serial-65974/cardOngoing
    series_link = f"https://www.anidag.ru/card/{row.id}/cardOngoing"

    # Отправка фото с подписью
    payload = {
        'chat_id': CHANNEL_USERNAME,
        'photo': poster_url,
        'caption': f"<b>{title}</b>\n\n{description}\n\n👉 <a href=\"{series_link}\">Смотреть</a>",
        'parse_mode': 'HTML'
    }

    response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data=payload)

    if response.ok:
        print(f"✅ Отправлено: {title}")
    else:
        print(f"❌ Ошибка при отправке {title}: {response.text}")

    # Обновить время последней отправки
    latest_time = max(row.personupdate for row in result)
    with open("last_sent.txt", "w") as f:
        f.write(latest_time.isoformat())
else:
    print("🔕 Нет новых серий.")
