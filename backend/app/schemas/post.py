from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.movie import MoviePreviewResponse
from app.schemas.user import UserResponse


class PostCreate(BaseModel):
    movie_id: int
    body: str = Field(min_length=1)
    watch_if_you_enjoyed: str | None = None
    favourite_character: str | None = None
    favourite_part: str | None = None


class PostResponse(BaseModel):
    id: int
    body: str
    watch_if_you_enjoyed: str | None = None
    favourite_character: str | None = None
    favourite_part: str | None = None
    created_at: datetime
    author: UserResponse
    movie: MoviePreviewResponse

    model_config = ConfigDict(from_attributes=True)