import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Основной URL для API
base_url = "https://api.apbugall.org/"
token = os.getenv('TOKENAL')
fastapi_url = "http://localhost:8000/api/animeFilmal/"

def process_data(url):
    total_count = 0  # общий счётчик
    page = 1
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get("data", []))
            total_count += count
            print(f"📄 Страница {page}: найдено {count} объектов, всего собрано {total_count}")

            # Отправляем данные на FastAPI
            try:
                post_response = requests.post(fastapi_url, json=data)
                post_response.raise_for_status()
                print("✅ Данные успешно отправлены в FastAPI:", post_response.status_code)
                # print(post_response.text)
            except requests.exceptions.RequestException as e:
                print(f"❌ Ошибка отправки данных: {e}")

            # Проверяем есть ли next_page
            next_page = data.get("next_page")
            if next_page:
                url = f"{base_url}?token={token}&list=anime&page={next_page}"
                print(f"➡ Переход на следующую страницу: {url}")
                page += 1
            else:
                break
        else:
            print(f"❌ Ошибка получения данных: {response.status_code}")
            break

# Запуск
initial_url = f"{base_url}?token={token}&list=anime"
process_data(initial_url)

