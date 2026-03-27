from datetime import datetime, timedelta, timezone
from jwt import PyJWTError, ExpiredSignatureError   
import jwt
import os
from fastapi import HTTPException
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
SECRET_REFRESH_KEY = os.getenv('SECRET_REFRESH_KEY')
ALGORITHM = os.getenv('ALGORITHM')

if not SECRET_ACCESS_KEY or not SECRET_REFRESH_KEY or not ALGORITHM:
    raise ValueError("Не удалось загрузить переменные окружения")

# def create_access_token(data: dict, expires_delta: timedelta = timedelta(seconds=8)):
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_ACCESS_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def create_access_token(data: dict, expires_delta: timedelta = timedelta(seconds=900)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_ACCESS_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def decode_access_token(token: str):
#     try:
#         decoded_token = jwt.decode(token, SECRET_ACCESS_KEY, algorithms=[ALGORITHM])
#         return decoded_token if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp() else None
#     except jwt.PyJWTError:
#         return None

# def decode_access_token(token: str):
#     try:
#         decoded_token = jwt.decode(
#             token,
#             SECRET_ACCESS_KEY,
#             algorithms=[ALGORITHM],
#            options={"verify_exp": False}  # Отключаем авто-проверку
           
#         )
#         exp = decoded_token.get("exp")
#         if exp is None:
#             raise HTTPException(status_code=401, detail="Invalid token structure (no exp field)")
#         if exp < datetime.now(timezone.utc).timestamp():
#             raise HTTPException(status_code=401, detail="Access token expired")
#         return decoded_token
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid access token")

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_ACCESS_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")


# def decode_refresh_token(token: str):
#         # print(token, "DECODEEE TOKEN===========")
#     # try:
#         decoded_token = jwt.decode(token, SECRET_REFRESH_KEY, algorithms=[ALGORITHM])
#         print(decoded_token, "DECODEEE TOKEN===========")
#         return decoded_token if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp() else None
#     # except jwt.PyJWTError:
#     #     return None

# def decode_refresh_token(token: str):
    
#     try:
#         decoded_token = jwt.decode(token, SECRET_REFRESH_KEY, algorithms=[ALGORITHM])
        
#         return decoded_token if decoded_token["exp"] >= datetime.now(timezone.utc).timestamp() else None
#     except jwt.PyJWTError as e:
#         print(f"Error decoding token: {e}")
#         return None

def decode_refresh_token(token: str):
    try:
        decoded_token = jwt.decode(
            token,
            SECRET_REFRESH_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}  # <--- вот это КЛЮЧ
        )
        return decoded_token
    except ExpiredSignatureError:
        print("Refresh token expired (внутри decode_refresh_token)")
        raise  # прокидываем дальше для обработки наверху
    except PyJWTError as e:
        print(f"Error decoding token: {e}")
        raise


def decode_access(token: str):
        decoded_token = jwt.decode(token, SECRET_ACCESS_KEY, algorithms=[ALGORITHM],options={"verify_exp": False})
        print(decoded_token, "TOKEN DECODER ================")
        return decoded_token
