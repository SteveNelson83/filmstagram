from sqlalchemy.orm import Session

from app.models.movie_cast import MovieCast
from app.models.movie_crew import MovieCrew
from app.models.person import Person


class PersonService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(
        self,
        tmdb_id: int,
        name: str,
        profile_path: str | None = None,
    ) -> Person:
        person = (
            self.db.query(Person)
            .filter(Person.tmdb_id == tmdb_id)
            .first()
        )

        if person:
            person.name = name
            person.profile_path = profile_path
            return person

        person = Person(
            tmdb_id=tmdb_id,
            name=name,
            profile_path=profile_path,
        )
        self.db.add(person)
        return person

    def delete_orphans(self) -> int:
        cast_ids = {row[0] for row in self.db.query(MovieCast.person_id).distinct()}
        crew_ids = {row[0] for row in self.db.query(MovieCrew.person_id).distinct()}
        referenced_ids = cast_ids | crew_ids

        if not referenced_ids:
            deleted = self.db.query(Person).delete(synchronize_session=False)
        else:
            deleted = (
                self.db.query(Person)
                .filter(Person.id.notin_(referenced_ids))
                .delete(synchronize_session=False)
            )

        self.db.commit()
        return deleted
