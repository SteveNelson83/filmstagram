from datetime import date
from typing import Optional

from app.models.genre import Genre
from app.models.movie_genres import MovieGenres
from sqlalchemy import Boolean, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)

    tmdb_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
        nullable=False,
    )

    adult: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    overview: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    tagline: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    release_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    runtime: Mapped[Optional[int]]

    poster_path: Mapped[Optional[str]]

    backdrop_path: Mapped[Optional[str]]

    genres: Mapped[list[Genre]] = relationship(
        "Genre",
        secondary=MovieGenres.__table__,
    )