# import asyncio
# import httpx
# import json

# url = "https://apbugall.org/v2/movies/"

# headers = {
#     "Authorization": "Bearer 899a35e7762f75cf7c31c3d23a8050",
#     "Accept": "application/json",
#     "Content-Type": "application/json"
# }

# payload = {
#     "category": ["anime-serial"],
#     "year": [2026]
# }


# async def main():
#     current_url = url
#     all_data = []

#     async with httpx.AsyncClient(timeout=30.0) as client:
#         while current_url:
#             response = await client.request(
#                 "GET",
#                 current_url,
#                 headers=headers,
#                 json=payload
#             )

#             response.raise_for_status()

#             data = response.json()

#             print(f"Страница: {data['meta']['current_page']}")
#             print(f"URL: {current_url}")

#             all_data.extend(data.get("data", []))

#             current_url = data.get("links", {}).get("next")

#     with open("response.json", "w", encoding="utf-8") as f:
#         json.dump(all_data, f, indent=4, ensure_ascii=False)

#     print(f"Все страницы сохранены. Всего записей: {len(all_data)}")


# if __name__ == "__main__":
#     asyncio.run(main())
import asyncio
import httpx
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = FastAPI()

API_URL = f"{os.getenv('AL_URL')}/v2/movies/"
# LOCAL_API_URL = f"{os.getenv('ANI_URL')}/api/addallohaongoing"
LOCAL_API_URL = "http://backend:8001/api/addallohaongoing"
#  curl -X POST https://anidag.ru/api/match-alloha-anime  запрос чтобы смерджить две бд


HEADERS = {
    "Authorization": f"Bearer {os.getenv('AL_TOKEN')}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

PAYLOAD = {
    "category": ["anime-serial"],
    "year": [2026, 2025]
}




async def fetch_movies():
    current_url = API_URL
    all_data = []

    async with httpx.AsyncClient(timeout=30.0) as client:
        while current_url:
            response = await client.request(
                "GET",
                current_url,
                headers=HEADERS,
                json=PAYLOAD
            )
            response.raise_for_status()

            data = response.json()

            print(f"Страница: {data['meta']['current_page']}")
            print(f"URL: {current_url}")

            all_data.extend(data.get("data", []))
            current_url = data.get("links", {}).get("next")

    return all_data


async def send_to_api():
    movies = await fetch_movies()


    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            LOCAL_API_URL,
            json=movies
        )
        response.raise_for_status()

        print("Ответ API:")
        print(response.json())

        return response.json()


@app.post("/api/run-alloha-parser")
async def run_alloha_parser():
    try:
        result = await send_to_api()
        return {
            "status": "success",
            "result": result
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


if __name__ == "__main__":
    asyncio.run(send_to_api())
