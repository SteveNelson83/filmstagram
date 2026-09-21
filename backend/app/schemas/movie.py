from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.schemas.genre import GenreResponse


class MovieResponse(BaseModel):
    id: int
    tmdb_id: int
    adult: bool
    title: str
    original_language: str
    overview: Optional[str] = None
    tagline: Optional[str] = None
    release_date: Optional[date] = None
    runtime: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    genres: list[GenreResponse] = []

    model_config = {
        "from_attributes": True
    }

class CastPreview(BaseModel):
    name: str
    character: str

class MoviePreviewResponse(BaseModel):
    id: int
    poster_path: str | None = None
    poster_url: str | None = None
    title: str
    release_year: int | None = None
    directors: list[str] = []
    top_cast: list[CastPreview] = []

class MovieSearchResult(BaseModel):
    id: int
    title: str
    release_year: int | None = None
    poster_path: str | None = None
    poster_url: str | None = None
    model_config = {"from_attributes": True}