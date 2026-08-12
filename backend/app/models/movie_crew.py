from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MovieCrew(Base):
    __tablename__ = "movie_crew"
    __table_args__ = (
        PrimaryKeyConstraint("movie_id", "person_id", "job"),
    )

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    person_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    job: Mapped[str]
    department: Mapped[str]