import argparse
import time

import app.models  # noqa: F401

from app.db.database import SessionLocal
from app.models.movie import Movie
from app.models.movie_cast import MovieCast
from app.models.movie_crew import MovieCrew
from app.services.movie_service import MovieService
from app.services.person_service import PersonService


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Re-import all movies from TMDB to refresh metadata and credits"
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.3,
        help="Seconds between TMDB requests",
    )
    args = parser.parse_args()

    db = SessionLocal()
    movies = db.query(Movie).order_by(Movie.id).all()
    service = MovieService(db)

    updated = 0
    failed = 0

    try:
        print(f"Re-importing {len(movies)} movies...")
        for movie in movies:
            title = movie.title
            tmdb_id = movie.tmdb_id
            try:
                result = service.import_from_tmdb(tmdb_id)
                cast_count = (
                    db.query(MovieCast)
                    .filter(MovieCast.movie_id == result.id)
                    .count()
                )
                crew_count = (
                    db.query(MovieCrew)
                    .filter(MovieCrew.movie_id == result.id)
                    .count()
                )
                print(
                    f"  Updated: {result.title} [{result.tmdb_id}] "
                    f"— {cast_count} cast, {crew_count} crew"
                )
                updated += 1
                time.sleep(args.sleep)
            except Exception as e:
                db.rollback()
                print(f"  Failed: {title} [{tmdb_id}] — {e}")
                failed += 1

        removed = PersonService(db).delete_orphans()
        print(f"\nDone. Updated: {updated}, Failed: {failed}")
        print(f"Removed {removed} orphaned people")
    finally:
        db.close()


if __name__ == "__main__":
    main()
