from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.services.tmdb_client import TmdbClient


class GenreService:

    def __init__(self, db: Session):
        self.db = db

    def get_genres(self):
        return self.db.query(Genre).all()

    def seed_from_tmdb(self) -> list[Genre]:
        client = TmdbClient()
        response = client.get_genre_list()

        genres = []
        for tmdb_genre in response.genres:
            genre = (
                self.db.query(Genre)
                .filter(Genre.tmdb_id == tmdb_genre.id)
                .first()
            )

            if genre:
                genre.name = tmdb_genre.name
            else:
                genre = Genre(
                    tmdb_id=tmdb_genre.id,
                    name=tmdb_genre.name,
                )
                self.db.add(genre)

            genres.append(genre)

        self.db.commit()
        return genres

    def get_by_tmdb_id(self, tmdb_id: int) -> Genre | None:
        return (
            self.db.query(Genre)
            .filter(Genre.tmdb_id == tmdb_id)
            .first()
        )