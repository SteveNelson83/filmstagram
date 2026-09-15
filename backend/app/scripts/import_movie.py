import argparse

import app.models  # noqa: F401

from app.db.database import SessionLocal
from app.models.movie_cast import MovieCast
from app.models.movie_crew import MovieCrew
from app.services.movie_service import MovieService

def main() -> None:
    parser = argparse.ArgumentParser(description="Import a movie from TMDB by ID")
    parser.add_argument("tmdb_id", type=int, help="TMDB movie ID (e.g. 550 for Fight Club)")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        movie = MovieService(db).import_from_tmdb(args.tmdb_id)
        genre_names = ", ".join(g.name for g in movie.genres) or "none"
        cast_count = db.query(MovieCast).filter_by(movie_id=movie.id).count()
        crew_count = db.query(MovieCrew).filter_by(movie_id=movie.id).count()
        print(f"Imported: {movie.title} (id={movie.id}, tmdb_id={movie.tmdb_id})")
        print(f"Genres: {genre_names}")
        print(f"Credits: {cast_count} cast, {crew_count} crew")
    finally:
        db.close()

if __name__ == "__main__":
    main()