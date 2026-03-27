from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Response,  Response,File, UploadFile, Form, Query,  Body 
from sqlalchemy.orm import Session
from sqlalchemy import func, select,text, desc , extract , case , cast, Date, distinct
from typing import Generator, AsyncGenerator
from  database.database_user import  User,  Comment
from datetime import  timezone
from database.async_db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database_user import User, Comment


router = APIRouter()

async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session



@router.get("/api/getcomments/{id}")
async def get_comments(id: str, db: AsyncSession = Depends(get_db_async)):


    stmt = (
        select(
            Comment.content,
            User.username,
            User.avatars,
            Comment.id,
            Comment.created_at,
            Comment.parent_comment_id,
        )
        .join(User, User.id == Comment.user_id)
        .where(Comment.anime_id == id)
    )

    res = await db.execute(stmt)
    comments = res.all()  # список кортежей

    result = [
        {
            "content": content,
            "username": username,
            "avatars": avatars,
            "id": comment_id,
            "created_at": created_at,
            "parent_comment_id": parent_comment_id,
        }
        for content, username, avatars, comment_id, created_at, parent_comment_id in comments
    ]
    return result




@router.post("/api/comments/{id}")
async def add_comment(id: str, request: Request, db: AsyncSession = Depends(get_db_async)):
    body = await request.json()
    username = body.get("user")
    text = body.get("text")
    parent_id = body.get("parent_comment_id")

 

    # найти пользователя (async)
    stmt_user = select(User).where(User.username == username)
    res_user = await db.execute(stmt_user)
    user = res_user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # создать комментарий
    new_comment = Comment(
        anime_id=id,
        user_id=user.id,
        content=text,
        parent_comment_id=parent_id
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    created_at_iso = new_comment.created_at.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

    return {
        "id": new_comment.id,
        "anime_id": new_comment.anime_id,
        "content": new_comment.content,
        "parent_comment_id": new_comment.parent_comment_id,
        "username": user.username,
        "created_at": created_at_iso
    }

# Удалить комментарий

@router.delete("/api/deletecomments/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db_async)):
    stmt = select(Comment).where(Comment.id == comment_id)
    res = await db.execute(stmt)
    comment = res.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    await db.delete(comment)
    await db.commit()
    return {"message": "Комментарий удален"}

