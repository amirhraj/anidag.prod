import requests
from datetime import datetime
import json

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Основной URL для API
base_url = f"{os.getenv('KODIK_URL')}/list"
token = os.getenv('TOKEN')
fastapi_url = f"{os.getenv('FASTP_API_URL')}/animeFilm"

# with open("/test.log", "a") as logfile:
#     logfile.write("Скрипт Обновления фильмов выполнен в: " + str(datetime.now()) + "\n")

# Функция для обработки и отправки данных
def process_data(url):
    # print(url)
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            # Преобразуем ответ в формат JSON
            data = response.json()

           
            # Отправляем данные на FastAPI
            results = data  # Здесь вы можете модифицировать, если нужно

            try:
                post_response = requests.post(fastapi_url, json=results)
                post_response.raise_for_status()  # Поднимет исключение для кодов ошибок
                print("Данные успешно отправлены в FastAPI:", post_response.json())
            except requests.exceptions.RequestException as e:
                print(f"Ошибка отправки данных: {e}")
            
            # Переход к следующему URL
            url = data.get('next_page')  # Получаем следующий URL
            print(url)
        else:
            print(f"Ошибка получения данных: {response.status_code}")
            break  # Выходим из цикла при ошибке

# Начальный запрос
years = [2026, 2025]

for year in years:
    print(f"Обрабатываем год: {year}")
    initial_url = f"{base_url}?token={token}&types=anime&with_material_data=true&year={year}"
    process_data(initial_url)
