from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.services.movie_service import MovieService

from app.db.dependencies import get_db
from app.schemas.movie import MoviePreviewResponse, MovieResponse, MovieSearchResult

router = APIRouter()

# Get all movies
@router.get(
    "/movies",
    response_model=list[MovieResponse]
)
def get_movies(
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return service.get_movies()

# Search for movies
@router.get(
    "/movies/search",
    response_model=list[MovieSearchResult]
)
def search_movies(
    query: str | None = Query(
        default=None,
        min_length=3,
        description="Movie title search term (min 3 characters)"),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    if query is None:
        return []
    return MovieService(db).search_movies(query, limit=limit)

# Get a movie preview
@router.get(
    "/movies/{movie_id}/preview",
    response_model=MoviePreviewResponse,
)
def get_movie_preview(
    movie_id: int,
    db: Session = Depends(get_db),
):
    preview = MovieService(db).get_movie_preview(movie_id)
    if preview is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return preview

# Get a movie by ID
@router.get(
    "/movies/{movie_id}",
    response_model=MovieResponse
)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie = MovieService(db).get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie