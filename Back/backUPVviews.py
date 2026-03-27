from datetime import datetime
from database.database_setup_ongoing import  View, Like
from database.sync_db import SessionLocal

# Явно создаём сессию
session = SessionLocal()

# Найдём все записи, где явно был просмотр
likes_with_views = session.query(Like).filter(Like.view_count != None).all()

total_created = 0

for like in likes_with_views:
    for _ in range(like.view_count or 1):
        view = View(
            user_id=like.user_id,
            ip_hash=like.ip_hash,
            anime_id=like.anime_id,
            title=like.title,
            viewed_at=like.created_at or datetime.utcnow()
        )
        session.add(view)
        total_created += 1

session.commit()
session.close()

print(f"✅ Перенесено {total_created} просмотров.")
