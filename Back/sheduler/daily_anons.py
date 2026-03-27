import requests 

url = 'https://shikimori.one/api/graphql'

query = """
 {
  animes(limit: 100, kind: "tv", status: "anons") {
    id
    malId
    name
    russian
    english
    japanese
    kind
    rating
    score
    status
    episodes
    episodesAired
    duration
    airedOn { year month day date }
    releasedOn { year month day date }
    url
    season
    poster { id originalUrl mainUrl }
    createdAt
    updatedAt
    nextEpisodeAt
    isCensored
    genres { id name russian kind }
    studios { id name imageUrl }
    videos { id url name kind playerUrl imageUrl }
    description
  }
}
"""


headers = {
    "Content-Type": "application/json",
    "Authorization": "3j1Q3SCdzdV8JohsyZ6tLRopVUyoUuQWvtCIgm9dUA7YsBbxncgFP6MKU3q0MwcwDcKrWmhhit4wgl_K4fgIIw"
    }

response = requests.post(url, json={'query': query}, headers=headers)

# Обработка ответа
if response.status_code == 200:
    # Если запрос успешен, выводим данные
    data = response.json()
    print(data)
else:
    # Если произошла ошибка, выводим статус код
    print(f"Ошибка {response.status_code}: {response.text}")