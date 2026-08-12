from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MovieCast(Base):
    __tablename__ = "movie_cast"
    __table_args__ = (
        PrimaryKeyConstraint("movie_id", "person_id"),
    )

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    character: Mapped[str]
    order: Mapped[int]