from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    avatar_url: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserCardResponse(BaseModel):
    id: int
    username: str
    avatar_url: str | None = None
    is_following: bool = False

    model_config = ConfigDict(from_attributes=True)
    