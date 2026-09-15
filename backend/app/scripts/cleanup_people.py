import app.models  # noqa: F401

from app.db.database import SessionLocal
from app.models.person import Person
from app.services.person_service import PersonService


def main() -> None:
    db = SessionLocal()
    try:
        before = db.query(Person).count()
        removed = PersonService(db).delete_orphans()
        after = db.query(Person).count()
        print(f"Removed {removed} orphaned people ({before} → {after})")
    finally:
        db.close()


if __name__ == "__main__":
    main()
