from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import hash_password


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def create_user(self, data: UserCreate) -> User:
        if self.get_by_email(data.email):
            raise ValueError("Email already registered")

        existing_username = (
            self.db.query(User)
            .filter(User.username == data.username)
            .first()
        )
        if existing_username:
            raise ValueError("Username already taken")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
