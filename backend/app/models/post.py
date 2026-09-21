from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.user import User
from app.models.movie import Movie


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), index=True)

    body: Mapped[str] = mapped_column(Text, nullable=False)
    watch_if_you_enjoyed: Mapped[str | None] = mapped_column(Text, nullable=True)
    favourite_character: Mapped[str | None] = mapped_column(Text, nullable=True)
    favourite_part: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User")
    movie: Mapped["Movie"] = relationship("Movie")