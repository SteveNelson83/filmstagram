import app.models  # noqa: F401

from app.db.database import SessionLocal
from app.schemas.user import UserCreate
from app.services.user_service import UserService


def main() -> None:
    db = SessionLocal()
    service = UserService(db)

    created = 0
    skipped = 0

    try:
        for i in range(1, 11):
            data = UserCreate(
                username=f"steve{i}",
                email=f"steve{i}@example.com",
                password="password123",
            )

            try:
                user = service.create_user(data)
                print(f"Created: {user.username} ({user.email})")
                created += 1
            except ValueError as e:
                print(f"Skipped: steve{i} — {e}")
                skipped += 1

        print(f"\nDone. Created: {created}, Skipped: {skipped}")
    finally:
        db.close()


if __name__ == "__main__":
    main()