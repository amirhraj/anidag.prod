
from hashlib import sha256
from fastapi import APIRouter , FastAPI, HTTPException, Depends, Request, Response,  Response,File, UploadFile, Form, Query,  Body 
from sqlalchemy import func, select,text, desc , extract , case , cast, Date, distinct
from auth.auth_jwt import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token, decode_access
from datetime import datetime, timezone, timedelta
from  database.database_setup_ongoing  import  AnimeSchemaBase, Like, View
from database.sync_db import SessionLocal
import asyncio
router = APIRouter()

def get_ip_hash(ip: str) -> str:
    return sha256(ip.encode()).hexdigest()


@router.post("/api/like/{anime_id}") 
async def like(anime_id: str, request: Request): 
    ip = request.headers.get("X-Forwarded-For")
    # ip = request.client.host dev
    ip_hash = get_ip_hash(ip) 
    body = await request.json()
    title = body.get("title")    
    user_id = body.get("user_id")


    # if not user_id:
    #     return {"error": "user_id is required"}


    
    session = SessionLocal() 
    # existing_like = session.query(Like).filter_by(ip_hash=ip_hash, anime_id=anime_id).first() 
    # anime = session.query(AnimeSchemaBase).filter_by(id=anime_id).first()
    anime = session.query(AnimeSchemaBase).filter_by( title_orig=title).first()
    # existing_like = session.query(Like).filter_by(ip_hash=ip_hash, title=title).first()
    # existing_like = session.query(Like).filter_by(user_id=user_id, title=title).first()
    if user_id:
        existing_like = session.query(Like).filter_by(user_id=user_id, title=title).first()
    else:
        existing_like = session.query(Like).filter_by(ip_hash=ip_hash, title=title).first()

    # print(f"Anime ID: {anime_id}")
    # print(f"Existing Like: {existing_like}")
    # print(f"Anime: {anime}")

    # if not anime:
    #     raise HTTPException(status_code=404, detail="Anime not found")

    if existing_like: 
        if existing_like.is_like: 
            pass
            # raise HTTPException(status_code=400, detail="You have already liked this anime.")
            # like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar() 
            # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
            # return {"like_count": like_sum , 
            #         "dislike_count": dislike_sum } 
        else: 
            existing_like.is_like = True
            # existing_like.title = title
            # existing_like.like_count += 1
            # existing_like.dislike_count = max(0, existing_like.dislike_count - 1)
            # existing_like.is_like = True
            # anime.like_count += 1
            # anime.dislike_count -= 1
            session.commit()
            # like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar() 
            # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
            # return {"message": "Dislike changed to like", 
            #         "like_count": anime.like_count ,
            #         "dislike_count": anime.dislike_count }
            # return {"message": "Dislike changed to like", 
            #         "like_count": like_sum , 
            #         "dislike_count": dislike_sum
            #           }
    else: 
        # new_like = Like(ip_hash=ip_hash, anime_id=anime_id, is_like=True)
        # session.add(new_like)
        # anime.like_count += 1
        # session.commit()
        # return {"message": "Anime liked successfully", "like_count": anime.like_count , "dislike_count": anime.dislike_count  }
        # new_like = Like(ip_hash=ip_hash, anime_id=anime_id , is_like=True, title=title, like_count= 1)
        # session.add(new_like)
        # existing_like.like_count += 1
        # session.commit()

        new_like = Like(ip_hash=ip_hash, anime_id=anime_id, user_id=user_id,  title=title, is_like=True)
        session.add(new_like)
        session.commit()

    like_count = session.query(func.count(Like.is_like)).filter_by(title=title, is_like=True).scalar()
    dislike_count = session.query(func.count(Like.is_like)).filter_by(title=title, is_like=False).scalar()
    return {
        "message": "Like processed",
        "like_count": like_count,
        "dislike_count": dislike_count
    }
        # like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar() 
        # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
        # return {"message": "Anime liked successfully", 
        #         "like_count": like_sum  ,  
        #         "dislike_count": dislike_sum }

    

@router.post("/api/dislike/{anime_id}")
async def dislike(anime_id: str, request: Request):
    ip = request.headers.get("X-Forwarded-For")
    # ip = request.client.host dev
    ip_hash = get_ip_hash(ip)
    body = await request.json()
    title = body.get("title")
    user_id = body.get("user_id")


    # if not user_id:
    #     return {"error": "user_id is required"}
    
    session = SessionLocal()
    # existing_like = session.query(Like).filter_by(ip_hash=ip_hash, anime_id=anime_id).first()
    # anime = session.query(AnimeSchemaBase).filter_by(id=anime_id).first()

    anime = session.query(AnimeSchemaBase).filter_by(title_orig=title).first()
    # existing_like = session.query(Like).filter_by(ip_hash=ip_hash, title=title).first()
    # existing_like = session.query(Like).filter_by(user_id=user_id, title=title).first()
    if user_id:
        existing_like = session.query(Like).filter_by(user_id=user_id, title=title).first()
    else:
        existing_like = session.query(Like).filter_by(ip_hash=ip_hash, title=title).first()

    if existing_like:
        if existing_like.is_like is False:
            pass
            # existing_like.is_like = False
            # existing_like.like_count = max(0, existing_like.dislike_count - 1)
            # existing_like.dislike_count += 1
            # session.commit()
            # like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar() 
            # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
            # return {"message": "is_like null", "dislike_count": dislike_sum }
        # elif not existing_like.is_like:
        #     # raise HTTPException(status_code=400, detail="You have already disliked this anime.")
        #     like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar() 
        #     dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
        #     return {"message": "Like changed to dislike (none)", 
        #             "like_count": like_sum, 
        #             "dislike_count": dislike_sum 
        #               }
        else:
            existing_like.is_like = False
            # anime.like_count -= 1
            # anime.dislike_count += 1
            # session.commit()
            # return {"message": "Like changed to dislike", "dislike_count": anime.dislike_count, "like_count": anime.like_count}
            # existing_like.is_like = False
            # existing_like.like_count = max(0, existing_like.dislike_count - 1)
            # existing_like.dislike_count += 1
            session.commit()
            # like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar() 
            # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
            # return {"message": "Like changed to dislike", 
            #         "dislike_count": dislike_sum, 
            #         "like_count": like_sum }
    else:
        new_dislike = Like(ip_hash=ip_hash, anime_id=anime_id, user_id=user_id, title=title, is_like=False)
        session.add(new_dislike)
        session.commit()

    like_count = session.query(func.count(Like.is_like)).filter_by( title=title, is_like=True).scalar()
    dislike_count = session.query(func.count(Like.is_like)).filter_by( title=title, is_like=False).scalar()

    return {
        "message": "Dislike processed",
        "like_count": like_count,
        "dislike_count": dislike_count
    }
        # new_like = Like(ip_hash=ip_hash, anime_id=anime_id, is_like=False)
        # session.add(new_like)
        # anime.dislike_count += 1
        # session.commit()
        # return {"message": "Anime disliked successfully", "dislike_count": anime.dislike_count , "like_count": anime.like_count }
        # new_like = Like(ip_hash=ip_hash, anime_id=anime_id, is_like=False, dislike_count = 1, title=title)
        # session.add(new_like)
        # existing_like.dislike_count += 1
        # session.commit()
        # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
        # return {"message": "Anime disliked successfully", "dislike_count": dislike_sum}



@router.post("/api/status/{anime_id}")
async def get_status(anime_id: str, request: Request):
    body = await request.json()
    title = body.get("title") 
    session = SessionLocal()

    existing_like = session.query(Like).filter_by(title=title).first()
    if existing_like:
        like_sum = session.query(func.count(Like.id)).filter(Like.title == title, Like.is_like == True).scalar()
        dislike_sum = session.query(func.count(Like.id)).filter(Like.title == title, Like.is_like == False).scalar()
        view_count = session.query(func.count(View.id)).filter_by(title=title).scalar()
        # like_sum = session.query(func.sum(Like.like_count)).filter_by(title=title).scalar()
        # dislike_sum = session.query(func.sum(Like.dislike_count)).filter_by(title=title).scalar()
        # view_count = session.query(func.sum(Like.view_count)).filter_by(title=title).scalar()
        return {
            "like_count": like_sum,
            "dislike_count": dislike_sum ,
            "view_count": view_count
        }
    else:
        return {
            "message" : 'Нет совпадений'
        }
    # anime = session.query(AnimeSchemaBase).filter_by(id=anime_id).first()

    # if not anime:
    #     raise HTTPException(status_code=404, detail="Anime not found")

    # return {
    #     "like_count": anime.like_count,
    #     "dislike_count": anime.dislike_count,
    #     "view_count": anime.view_count
    # }



@router.post("/api/view/{anime_id}")
async def view_anime(anime_id: str, request: Request):
    body = await request.json()
    title = body.get("title")
    # ip = request.client.host
    ip = request.headers.get("X-Forwarded-For") 
    # ip = request.client.host dev
    ip_hash = get_ip_hash(ip)
    session = SessionLocal()

    auth_header = request.headers.get("Authorization")
    user_id = None

    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            dec = decode_access(token)
            user_id = int(dec.get("sub"))
        except Exception as e:
            print(f"Ошибка при декодировании токена: {e}")

    # Всегда создаем новую запись — даже если тот же пользователь/тайтл
    # new_view = Like(
    #     ip_hash=ip_hash,
    #     anime_id=anime_id,
    #     title=title,
    #     view_count=1,
    #     is_like=None,
    #     user_id=user_id,
    #     created_at=datetime.now()
    # )
    new_view = View(
        ip_hash=ip_hash,
        anime_id=anime_id,
        title=title,
        user_id=user_id,
        viewed_at=datetime.now()
    )
    session.add(new_view)
    session.commit()

    # Суммируем общее количество просмотров для тайтла
    # view_count = session.query(func.sum(Like.view_count)).filter_by(title=title).scalar() or 0
    view_count = session.query(func.count(View.id)).filter_by(title=title).scalar() or 0
    like_count = session.query(func.count()).filter(Like.title == title, Like.is_like == True).scalar()
    dislike_count = session.query(func.count()).filter(Like.title == title, Like.is_like == False).scalar()

    return {
        "message": "New view recorded",
        "view_count": view_count,
        "like_count": like_count,
        "dislike_count": dislike_count
    }
