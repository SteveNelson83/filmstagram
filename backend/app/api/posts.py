from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse, status_code=201, response_model_exclude_none=True)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PostService(db)
    try: 
        post = service.create_post(current_user, data)
        return service.build_response(post)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}", response_model=PostResponse, response_model_exclude_none=True)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    service = PostService(db)
    post = service.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        return service.build_response(post)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))