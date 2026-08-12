from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator

class TmdbGenre(BaseModel):
    id: int
    name: str


class TmdbGenreListResponse(BaseModel):
    genres: list[TmdbGenre]


class TmdbMovie(BaseModel):
    id: int
    title: str
    adult: bool
    original_language: str
    overview: Optional[str] = None
    tagline: Optional[str] = None
    release_date: Optional[date] = None
    runtime: Optional[int] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    genres: list[TmdbGenre] = []

class TmdbDiscoverMovie(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    release_date: Optional[date] = None
    poster_path: Optional[str] = None


class TmdbDiscoverResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    results: list[TmdbDiscoverMovie]

@field_validator("release_date", mode="before")
@classmethod
def empty_string_to_none(cls, v):
    if v == "":
        return None
    return v