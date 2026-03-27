
from  database.database_user import User, Token
from fastapi import APIRouter , HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from jwt import  ExpiredSignatureError   
from sqlalchemy.orm import Session
from hashPassFunction.util import get_password_hash , verify_password
from auth.auth_jwt import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token, decode_access
from models.ongoing_model import  UserCreate, LoginRequest
from database.sync_db import SessionLocal
import secrets
import smtplib
from email.mime.text import MIMEText
import os
import ssl
from datetime import datetime, timezone


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    

    # Проверка существующего пользователя
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже существует")
    
    db_user_username = db.query(User).filter(User.username == user.username).first()
    if db_user_username:
        raise HTTPException(status_code=400, detail="Login уже существует")

    hashed_password = get_password_hash(user.password)
    verification_token = secrets.token_urlsafe(16)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        verification_token=verification_token,  # Добавляем токен в БД
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    send_verification_email(user.email, verification_token)

    access_token = create_access_token(data={"sub": str(db_user.id), "email": db_user.email , 'login':db_user.username})
    refresh_token = create_refresh_token(data={"sub": str(db_user.id), "email": db_user.email , 'login':db_user.username})
    db_token = Token(
        refresh_token=refresh_token,
        user_id=db_user.id
    )
    db.add(db_token)
    db.commit()
    response = Response()
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer" , "registration": True, "message": "Проверьте почтовый ящик"})
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response





@router.post("/api/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == login_data.email).first()
 
    if not db_user:
        raise HTTPException(status_code=400, detail="Нет такого пользователя")
    
    if verify_password(login_data.password, db_user.hashed_password):
        
        # db_refressh_token = db.query(Token).filter(Token.user_id == db_user.id).first()
        
        # if db_refressh_token is None:
            new_access_token = create_access_token(data={
                "sub": str(db_user.id), 
                "email": db_user.email , 
                'login':db_user.username, 
                'role': db_user.role})
            new_create_refresh = create_refresh_token(data={
                "sub": str(db_user.id), 
                "email": db_user.email , 
                'login':db_user.username, 
                'role': db_user.role})
            
            # ✅ ВАЖНО: удаляем все старые refresh-токены этого пользователя
            db.query(Token).filter(Token.user_id == db_user.id).delete()
            db.commit()
            
            # Сохраняем новый токен
            db_token = Token(
                    refresh_token= new_create_refresh,
                    user_id=db_user.id,
                    login_at=datetime.now(timezone.utc)
                )
            
            db.add(db_token)
            db.commit()

            response = Response()
            response = JSONResponse(content={
                    "access_token": new_access_token,
                    "token_type": "bearer",
                    "user_id": db_user.id,
                    "email": db_user.email,
                    'login':db_user.username,
                    "avatar_url" :db_user.avatars
                    
                })
            response.set_cookie(key="refresh_token", value=new_create_refresh, httponly=True, samesite="lax", path='/')
            return response
    else:
        raise HTTPException(status_code=400, detail="Не верный пароль")   
  


    
    
@router.get("/api/check-token/")
def check_token(request: Request):
    authorization: str = request.headers.get("Authorization")
    # print(authorization, 'AUTO')
    refresh_token = request.cookies.get("refresh_token")
    # print(refresh_token, "REFRESH")
    if authorization:
        token = authorization.split(" ")[1]  # Извлекаем токен из заголовка Authorization
        # print(token)

        try:
            check_token_access = decode_access_token(token=token)
            if check_token_access is None:
                raise HTTPException(status_code=401, detail="Invalid access token")
            # print(check_token_access)
            # print(f"Access Token: {check_token_access}")
            return JSONResponse(content={"status": "Access token received", "token": token})
        except Exception as e:
            print(f"Token decoding failed: {e}")
            raise HTTPException(status_code=401, detail="Invalid access token")

    else:
         raise HTTPException(status_code=401, detail="Access token is missing")
    






@router.post("/api/refreshAccessToken/")
def refresh_access_token(request: Request, db: Session = Depends(get_db)):
    # print("🔁 Запрос на /api/refreshAccessToken/")

    # 1. Получаем access token из заголовка Authorization
    authorization: str = request.headers.get("Authorization")
    # print(f"🔐 Заголовок Authorization: {authorization}")

    if not authorization:
        # print("❌ Нет заголовка Authorization")
        raise HTTPException(status_code=401, detail="Не залогинен")

    try:
        token = authorization.split(" ")[1]
        # print(f"✅ Access-токен получен: {token[:15]}...")  # не печатаем весь токен
    except Exception as e:
        # print("❌ Ошибка при разборе токена из заголовка:", e)
        raise HTTPException(status_code=401, detail="Неверный формат токена")

    # 2. Декодируем access token без проверки срока годности
    try:
        decoded_access = decode_access(token=token)
        # print("✅ Access-токен декодирован:", decoded_access)
    except Exception as e:
        # print("❌ Ошибка при декодировании access токена:", e)
        raise HTTPException(status_code=401, detail="Неверный access токен")

    user_email = decoded_access.get('email')
    # print(f"📧 Email из токена: {user_email}")

    if not user_email:
        # print("❌ Email отсутствует в токене")
        raise HTTPException(status_code=401, detail="Не найден email в токене")

    # 3. Получаем пользователя из БД
    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        # print(f"❌ Пользователь с email {user_email} не найден в БД")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    print(f"👤 Пользователь найден: id={db_user.id}, email={db_user.email}")

    # 4. Получаем refresh token из БД
    db_refresh_token = db.query(Token).filter(Token.user_id == db_user.id).first()
    if not db_refresh_token:
        # print(f"❌ Refresh токен для пользователя id={db_user.id} не найден")
        raise HTTPException(status_code=401, detail="Нет токена")

    # print(f"✅ Refresh токен из БД: {db_refresh_token.refresh_token[:15]}...")

    # 5. Проверяем refresh token
    try:
        check_refresh = decode_refresh_token(token=db_refresh_token.refresh_token)
        # print("✅ Refresh токен валиден:", check_refresh)
    except ExpiredSignatureError:
        # print("❌ Refresh токен истёк")
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except Exception as e:
        # print("❌ Ошибка при декодировании refresh токена:", e)
        raise HTTPException(status_code=401, detail="Неверный refresh токен")

    # 6. Генерируем новый access token
    new_access_token = create_access_token(data={
        "sub": str(db_user.id), 
        "email": db_user.email, 
        "login" : db_user.username, 
        'role': db_user.role})
    # print("🔑 Новый access-токен создан")

    # 7. Отправляем ответ с кукой
    response = JSONResponse(content={
        "access_token": new_access_token,
        "token_type": "bearer",
    })
    response.set_cookie(
        key="refresh_token",
        value=db_refresh_token.refresh_token,
        httponly=True,
        secure=True,  # Для HTTPS
        samesite="lax",
        max_age=30*24*60*60,  # 30 дней
        path="/"
    )
    # print("✅ Новый access-токен отправлен в ответе")
    return response







@router.get("/api/logout")
def logout_user(request: Request, db: Session = Depends(get_db)):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Не авторизован")

    token = authorization.split(" ")[1]  # Извлекаем токен из заголовка Authorization

    try:
        decoded_access = decode_access(token=token)
    except Exception:
        raise HTTPException(status_code=401, detail="Неверный access токен")

    user_email = decoded_access.get('email')
    if not user_email:
        raise HTTPException(status_code=400, detail="Не найден email в токене")

    db_user = db.query(User).filter(User.email == user_email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Удаляем все refresh токены пользователя
    user_tokens = db.query(Token).filter(Token.user_id == db_user.id).all()

    if user_tokens:
        for token_record in user_tokens:
            db.delete(token_record)
        db.commit()

    # Создаем ответ и удаляем куки
    response = JSONResponse(content={"message": "Разлогирован успешно", "status": 200})
    response.delete_cookie(key="access_token", path='/')
    response.delete_cookie(key="refresh_token", path='/')

    return response




SMTP_HOST = "smtp.beget.com"
SMTP_PORT = 2525
SMTP_USER = "anidag@anidag.ru"
SMTP_PASS = "3gMsLRTbQjVSZkdqa5dOKrHy0XiCz-sx_"


def send_verification_email(email: str, token: str) -> None:
    link = f"Для подтверждения почты перейдите по ссылке: https://anidag.ru/verify/{token}"

    msg = MIMEText(link, "plain", "utf-8")
    msg["Subject"] = "Подтверждение почты"
    msg["From"] = SMTP_USER
    msg["To"] = email

    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


@router.get("/api/verify/{token}")
def verify_user(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Неверный или устаревший токен")

    user.is_verified = True
    user.verification_token = None  # Удаляем временный токен
    db.commit()

    return {"message": "Email подтвержден"}
