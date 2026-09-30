from sqlalchemy.orm import Session

from app.models.user import User
from app.models.follow import Follow
from app.schemas.user import UserCardResponse

class FollowService:

    def __init__(self, db: Session):
        self.db = db

    def get_suggestions(self, current_user: User, limit: int = 3) -> list[User]:
        return (
            self.db.query(User)
            .filter(User.id != current_user.id, User.is_active.is_(True))
            .order_by(User.id)
            .limit(limit)
            .all()
        )

    def search_by_username(self, query: str, current_user: User, limit: int = 20) -> list[User]:
        trimmed = query.strip()
        if not trimmed:
            return []
        return (
            self.db.query(User)
            .filter(
                User.username.ilike(f"%{trimmed}%"),
                User.id != current_user.id,
                User.is_active.is_(True),
            )
            .order_by(User.username)
            .limit(limit)
            .all()
        )

    def following_ids(self, follower_id: int, user_ids: list[int]) -> set[int]:
        if not user_ids:
            return set()
        rows = (
            self.db.query(Follow.following_id)
            .filter(Follow.follower_id == follower_id, Follow.following_id.in_(user_ids))
            .all()
        )
        return {r[0] for r in rows}

    @staticmethod
    def to_user_cards(users: list[User], following: set[int]) -> list[UserCardResponse]:
        return [
            UserCardResponse(
                id=u.id,
                username=u.username,
                avatar_url=u.avatar_url,
                is_following=u.id in following,
            )
            for u in users
        ]

    def is_following(self, follower_id: int, following_id: int) -> bool:
        return (
            self.db.query(Follow.following_id)
            .filter(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
            .first()
            is not None
        )

    def follow(self, follower: User, target_user_id: int) -> None:
        if follower.id == target_user_id:
            raise ValueError("Cannot follow yourself")
        target = self.db.get(User, target_user_id)
        if not target or not target.is_active:
            raise ValueError("User not found")
        if self.is_following(follower.id, target_user_id):
            raise ValueError("Already following")
        self.db.add(Follow(follower_id=follower.id, following_id=target_user_id))
        self.db.commit()

    def unfollow(self, follower: User, target_user_id: int) -> None:
        target = self.db.get(User, target_user_id)
        if not target or not target.is_active:
            raise ValueError("User not found")
        row = (
            self.db.query(Follow)
            .filter(
                Follow.follower_id == follower.id,
                Follow.following_id == target_user_id,
            )
            .first()
        )
        if not row:
            raise ValueError("Not following this user")
        self.db.delete(row)
        self.db.commit()