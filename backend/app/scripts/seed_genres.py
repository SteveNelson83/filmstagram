import app.models  # noqa: F401

from app.db.database import SessionLocal
from app.services.genre_service import GenreService

def main() -> None:
    db = SessionLocal()
    try:
        genres = GenreService(db).seed_from_tmdb()
        print(f"Seeded {len(genres)} genres")
    finally:
        db.close()

if __name__ == "__main__":
    main()