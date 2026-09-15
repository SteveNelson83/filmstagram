from sqlalchemy.orm import Session, joinedload

from app.models.movie import Movie
from app.models.movie_cast import MovieCast
from app.models.movie_crew import MovieCrew
from app.schemas.tmdb import TmdbCastMember, TmdbMovie
from app.services.genre_service import GenreService
from app.services.person_service import PersonService
from app.services.tmdb_client import TmdbClient

TOP_CAST_COUNT = 5
DIRECTOR_JOB = "Director"


class MovieService:

    def __init__(self, db: Session):
        self.db = db

    def import_from_tmdb(self, tmdb_id: int) -> Movie:
        client = TmdbClient()
        tmdb_movie = client.get_movie(tmdb_id)

        movie = (
            self.db.query(Movie)
            .filter(Movie.tmdb_id == tmdb_movie.id)
            .first()
        )

        if movie:
            self._update_movie_from_tmdb(movie, tmdb_movie)
        else:
            movie = self._create_movie_from_tmdb(tmdb_movie)
            self.db.add(movie)

        genre_service = GenreService(self.db)
        movie.genres = []

        for tmdb_genre in tmdb_movie.genres:
            genre = genre_service.get_by_tmdb_id(tmdb_genre.id)
            if genre:
                movie.genres.append(genre)

        self.db.flush()
        self._import_credits(movie, tmdb_movie)

        self.db.commit()
        self.db.refresh(movie)
        return movie

    def _import_credits(self, movie: Movie, tmdb_movie: TmdbMovie) -> None:
        if not tmdb_movie.credits:
            return

        self.db.query(MovieCast).filter(MovieCast.movie_id == movie.id).delete()
        self.db.query(MovieCrew).filter(MovieCrew.movie_id == movie.id).delete()

        person_service = PersonService(self.db)

        cast_by_person: dict[int, TmdbCastMember] = {}
        for member in tmdb_movie.credits.cast:
            existing = cast_by_person.get(member.id)
            if existing is None or member.order < existing.order:
                cast_by_person[member.id] = member

        top_cast = sorted(cast_by_person.values(), key=lambda m: m.order)[
            :TOP_CAST_COUNT
        ]

        for member in top_cast:
            person = person_service.get_or_create(
                tmdb_id=member.id,
                name=member.name,
                profile_path=member.profile_path,
            )
            self.db.flush()
            self.db.add(
                MovieCast(
                    movie_id=movie.id,
                    person_id=person.id,
                    character=member.character or "",
                    order=member.order,
                )
            )

        seen_directors: set[int] = set()
        for member in tmdb_movie.credits.crew:
            if member.job != DIRECTOR_JOB:
                continue

            person = person_service.get_or_create(
                tmdb_id=member.id,
                name=member.name,
                profile_path=member.profile_path,
            )
            self.db.flush()

            if person.id in seen_directors:
                continue
            seen_directors.add(person.id)

            self.db.add(
                MovieCrew(
                    movie_id=movie.id,
                    person_id=person.id,
                    job=member.job,
                    department=member.department,
                )
            )

    def _create_movie_from_tmdb(self, tmdb_movie) -> Movie:
        return Movie(
            tmdb_id=tmdb_movie.id,
            title=tmdb_movie.title,
            adult=tmdb_movie.adult,
            original_language=tmdb_movie.original_language,
            overview=tmdb_movie.overview,
            tagline=tmdb_movie.tagline,
            release_date=tmdb_movie.release_date,
            runtime=tmdb_movie.runtime,
            poster_path=tmdb_movie.poster_path,
            backdrop_path=tmdb_movie.backdrop_path,
        )

    def _update_movie_from_tmdb(self, movie: Movie, tmdb_movie) -> None:
        movie.title = tmdb_movie.title
        movie.adult = tmdb_movie.adult
        movie.original_language = tmdb_movie.original_language
        movie.overview = tmdb_movie.overview
        movie.tagline = tmdb_movie.tagline
        movie.release_date = tmdb_movie.release_date
        movie.runtime = tmdb_movie.runtime
        movie.poster_path = tmdb_movie.poster_path
        movie.backdrop_path = tmdb_movie.backdrop_path

    def get_movies(self):
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.genres))
            .all()
        )

    def get_movie(self, movie_id: int):
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.genres))
            .filter(Movie.id == movie_id)
            .first()
        )

    def search_movies(self, query: str):
        return (
            self.db.query(Movie)
            .options(joinedload(Movie.genres))
            .filter(Movie.title.ilike(f"%{query}%"))
            .all()
        )

    def exists_by_tmdb_id(self, tmdb_id: int) -> bool:
        return (
            self.db.query(Movie.id)
            .filter(Movie.tmdb_id == tmdb_id)
            .first()
            is not None
        )
