from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.movie_service import MovieService

from app.db.dependencies import get_db
from app.schemas.movie import MovieResponse

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
    response_model=list[MovieResponse]
)
def search_movies(
    query: str,
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    return service.search_movies(query)

# Get a movie by ID
@router.get(
    "/movies/{movie_id}",
    response_model=MovieResponse
)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    service = MovieService(db)
    movie = service.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie