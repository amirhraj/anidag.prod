import requests
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Основной URL для API
base_url = f"{os.getenv('KODIK_URL')}/list"
token = os.getenv('TOKEN')
# fastapi_url = f"{os.getenv('ANI_URL')}/api/animeMainTitles"
fastapi_url = f"{os.getenv('FASTP_API_URL')}/animeMainTitles"
# Лог-файл для проверки запуска
# with open("/test.log", "a") as logfile:
#     logfile.write("Скрипт выполнен main titles в: " + str(datetime.now()) + "\n")


def process_data(url):
    """
    Получает данные от Kodik API и отправляет в FastAPI,
    пока есть next_page в ответе.
    """
    while url:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Отправляем весь JSON в FastAPI
            results = data  

            try:
                post_response = requests.post(fastapi_url, json=results)
                post_response.raise_for_status()
                print("✅ Данные успешно отправлены в FastAPI:", post_response.status_code)
            except requests.exceptions.RequestException as e:
                print(f"❌ Ошибка отправки данных: {e}")

            # Берём ссылку на следующую страницу
            url = data.get('next_page')
        else:
            print(f"❌ Ошибка получения данных: {response.status_code}")
            break


# Список годов для обхода
years = [2026,2025]

for year in years:
    print(f"\n📌 Обрабатываем год: {year}")
    initial_url = (
        f"{base_url}?token={token}"
        f"&types=anime-serial"
        f"&with_material_data=true"
        f"&with_seasons=true"
        f"&year={year}"
        f"&lgbt=false"
    )
    process_data(initial_url)

