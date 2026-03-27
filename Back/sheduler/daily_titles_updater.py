import requests
from datetime import datetime
import json
import time
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Основной URL для API
base_url = f"{os.getenv('KODIK_URL')}/list"
token = os.getenv('TOKEN')
fastapi_url = f"{os.getenv('ANI_URL')}/api/anime"

# чтобы запустить нужно удалить базу будет падать по не уникальному ключу 


# test.py
# with open("/test.log", "a") as logfile:
#     logfile.write("Скрипт обновления онгоингов: " + str(datetime.now()) + "\n")


# # Функция для обработки и отправки данных
# def process_data(url):
#     # print(url)
#     while url:
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             # Преобразуем ответ в формат JSON
#             data = response.json()

           
#             # Отправляем данные на FastAPI
#             results = data  # Здесь вы можете модифицировать, если нужно

#             try:
#                 post_response = requests.post(fastapi_url, json=results)
#                 post_response.raise_for_status()  # Поднимет исключение для кодов ошибок
#                 # print("Данные успешно отправлены в FastAPI:", post_response.json())
#             except requests.exceptions.RequestException as e:
#                 print(f"Ошибка отправки данных: {e}")
            
#             # Переход к следующему URL
#             url = data.get('next_page')  # Получаем следующий URL
#             print(url)
#             # time.sleep(3)
#         else:
#             print(f"Ошибка получения данных: {response.status_code}")
#             break  # Выходим из цикла при ошибке

# # Начальный запрос
# initial_url = f"{base_url}?token={token}&updated_at=updated_at&types=anime-serial&with_material_data=true&year=2025&with_seasons=true"
# process_data(initial_url)



# Функция для обработки и отправки данных
def process_data(url):
    while url:
        response = requests.get(url)
        
        if response.status_code == 200:
            # Преобразуем ответ в формат JSON
            data = response.json()

            # Отправляем данные на FastAPI
            results = data  # Можно модифицировать по необходимости

            try:
                # print("Отправляем данные на FastAPI, пример первых 500 символов:", results)
                # with open("/var/www/html/Back/update_title.json", "a") as logfile:
                #     logfile.write(json.dumps(results, ensure_ascii=False) + "\n")
                post_response = requests.post(fastapi_url, json=results)
                post_response.raise_for_status()  # Поднимет исключение для кодов ошибок
                print("Данные успешно отправлены в FastAPI:", post_response.status_code)
                print(post_response)
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP ошибка при отправке: {http_err}")
                print(post_response)
                if http_err.response is not None:
                    print("Статус код:", http_err.response.status_code)
                    # print("Тело ответа:", http_err.response.text)
                    # print("Заголовки ответа:", http_err.response.headers)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка запроса при отправке данных: {e}")
            
            # Переход к следующему URL
            url = data.get('next_page')  # Получаем следующий URL
            print("Следующая страница:", url)
        else:
            print(f"Ошибка получения данных: {response.status_code}")
            print("Тело ответа:", response.text)
            break  # Выходим из цикла при ошибке

# def process_data(url):
#     while url:
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             # Преобразуем ответ в формат JSON
#             data = response.json()

#             # Отправляем данные на FastAPI
#             results = data  # Здесь вы можете модифицировать, если нужно

#             try:
#                 post_response = requests.post(fastapi_url, json=results)
#                 post_response.raise_for_status()  # Поднимет исключение для кодов ошибок
#                 print("Данные успешно отправлены в FastAPI:", post_response.status_code)
#             except requests.exceptions.RequestException as e:
#                 print(f"Ошибка отправки данных: {e}")
            
#             # Переход к следующему URL
#             url = data.get('next_page')  # Получаем следующий URL
#         else:
#             print(f"Ошибка получения данных: {response.status_code}")
#             break  # Выходим из цикла при ошибке

# Список годов для обхода
years = [2026,2025, 2024]

# Проход по каждому году
for year in years:
    print(f"Обрабатываем год: {year}")
    initial_url = f"{base_url}?token={token}&updated_at=updated_at&types=anime-serial&with_material_data=true&year={year}&with_seasons=true&lgbt=false"
    process_data(initial_url)




