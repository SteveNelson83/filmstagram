from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.genre_service import GenreService

from app.db.dependencies import get_db
from app.models.genre import Genre
from app.schemas.genre import GenreResponse

router = APIRouter()

# Get all genres
@router.get("/genres", response_model=list[GenreResponse])
def get_genres(
    db: Session = Depends(get_db)
):
    service = GenreService(db)
    return service.get_genres()