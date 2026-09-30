from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.services.follow_service import FollowService

from app.db.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCardResponse

def _follow_http_error(exc: ValueError) -> HTTPException:
    message = str(exc)
    if message == "User not found":
        return HTTPException(status_code=404, detail=message)
    return HTTPException(status_code=400, detail=message)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/suggestions", response_model=list[UserCardResponse])
def user_suggestions(
    limit: int = Query(default=3, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FollowService(db)
    users = service.get_suggestions(current_user, limit)
    following = service.following_ids(current_user.id, [u.id for u in users])
    return FollowService.to_user_cards(users, following)

@router.get("/search", response_model=list[UserCardResponse])
def search_users(
    query: str | None = Query(default=None, min_length=2),
    limit: int = Query(default=20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if query is None:
        return []
    service = FollowService(db)
    users = service.search_by_username(query, current_user, limit)
    following = service.following_ids(current_user.id, [u.id for u in users])
    return FollowService.to_user_cards(users, following)

@router.post("/{user_id}/follow", status_code=201)
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FollowService(db)
    try:
        service.follow(follower=current_user, target_user_id=user_id)
    except ValueError as e:
        raise _follow_http_error(e) from e


@router.delete("/{user_id}/follow", status_code=204)
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = FollowService(db)
    try:
        service.unfollow(follower=current_user, target_user_id=user_id)
    except ValueError as e:
        raise _follow_http_error(e) from e