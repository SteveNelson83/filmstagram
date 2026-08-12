from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)

    tmdb_id: Mapped[int] = mapped_column(unique=True)

    name: Mapped[str]