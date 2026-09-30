from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (
        PrimaryKeyConstraint("follower_id", "following_id"),
        CheckConstraint("follower_id != following_id", name="no_self_follow"),
    )

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )