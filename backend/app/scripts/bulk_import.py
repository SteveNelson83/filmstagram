import argparse
import time

import app.models  # noqa: F401

from app.db.database import SessionLocal
from app.services.movie_service import MovieService
from app.services.tmdb_client import TmdbClient

def parse_countries(value: str | None) -> str | None:
    if not value:
        return None
     # TMDB uses pipe for OR: US|GB|FR
    return "|".join(c.strip().upper() for c in value.split(","))

def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk import movies from TMDB Discover")
    parser.add_argument("--from-date", default="2000-01-01", help="primary_release_date.gte (YYYY-MM-DD)")
    parser.add_argument("--to-date", help="primary_release_date.lte (YYYY-MM-DD)")
    parser.add_argument("--countries", help="Comma-separated ISO codes, e.g. US,GB,FR")
    parser.add_argument("--language", help="Original language ISO 639-1, e.g. en")
    parser.add_argument("--min-votes", type=int, default=100, help="vote_count.gte")
    parser.add_argument("--max-pages", type=int, default=5, help="Pages of discover results (20 per page)")
    parser.add_argument("--sleep", type=float, default=0.3, help="Seconds between movie imports")
    parser.add_argument("--skip-existing", action="store_true", default=True)
    args = parser.parse_args()

    filters: dict = {
        "primary_release_date.gte": args.from_date,
        "vote_count.gte": args.min_votes,
        "include_adult": False,
        "sort_by": "popularity.desc",
    }

    if args.to_date:
        filters["primary_release_date.lte"] = args.to_date

    countries = parse_countries(args.countries)
    if countries:
        filters["with_origin_country"] = countries

    if args.language:
        filters["with_original_language"] = args.language

    client = TmdbClient()
    db = SessionLocal()
    movie_service = MovieService(db)

    imported = 0
    skipped = 0
    failed = 0

    try:
        for page in range(1, args.max_pages + 1):
            response = client.discover_movies(page=page, **filters)
            print(f"Page {page}/{min(args.max_pages, response.total_pages)} - {len(response.results)} results")

            if not response.results:
                break

            for item in response.results:
                if args.skip_existing and movie_service.exists_by_tmdb_id(item.id):
                    print(f"  Skip (exists): {item.title} [{item.id}]")
                    skipped += 1
                    continue

                try:
                    movie = movie_service.import_from_tmdb(item.id)
                    print(f"  Imported: {movie.title} [{movie.tmdb_id}]")
                    imported += 1
                    time.sleep(args.sleep)
                except Exception as e:
                    print(f"  Failed: {item.title} [{item.id}] — {e}")
                    failed += 1

            if page >= response.total_pages:
                break

        print(f"\nDone. Imported: {imported}, Skipped: {skipped}, Failed: {failed}")
    finally:
        db.close()

if __name__ == "__main__":
    main()