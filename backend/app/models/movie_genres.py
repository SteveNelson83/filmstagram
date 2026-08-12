from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MovieGenres(Base):
    __tablename__ = "movie_genres"
    __table_args__ = (
        PrimaryKeyConstraint("movie_id", "genre_id"),
    )

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))