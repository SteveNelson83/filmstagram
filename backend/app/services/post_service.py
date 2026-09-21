from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse
from app.models.user import User
from app.services.movie_service import MovieService


class PostService:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, user: User, data: PostCreate) -> Post:
        movie = MovieService(self.db).get_movie(data.movie_id)
        if movie is None:
            raise ValueError("Movie not found")

        post = Post(
            user_id=user.id,
            movie_id=data.movie_id,
            body=data.body.strip(),
            watch_if_you_enjoyed=data.watch_if_you_enjoyed,
            favourite_character=data.favourite_character,
            favourite_part=data.favourite_part,
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_post(self, post_id: int) -> Post | None:
        return self.db.get(Post, post_id)

    def build_response(self, post: Post) -> PostResponse:
        movie_preview = MovieService(self.db).get_movie_preview(post.movie_id)
        if movie_preview is None:
            raise ValueError("Movie not found")
        return PostResponse(
            id=post.id,
            body=post.body,
            watch_if_you_enjoyed=post.watch_if_you_enjoyed,
            favourite_character=post.favourite_character,
            favourite_part=post.favourite_part,
            created_at=post.created_at,
            author=post.user,
            movie=movie_preview,
        )