from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Person(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)

    tmdb_id: Mapped[int] = mapped_column(unique=True)

    name: Mapped[str]
    
    profile_path: Mapped[Optional[str]]