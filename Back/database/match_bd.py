from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from database.async_db import Base
import uuid


class AL_ONGOING_ANIME_SCHEMA(Base):
    __tablename__ = "al_ongoing_anime_schema"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    al_ongoing_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("al_ongoing.id"),
        nullable=True
    )

    anime_schema_id: Mapped[str | None] = mapped_column(
        String,
        ForeignKey("anime_schema.id"),
        nullable=True
    )

    common_uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )