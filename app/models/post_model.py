from pydantic import BaseModel

from .comments_model import Comments
from .user_model import User


class PostBase(BaseModel):
    pass


class Post(PostBase):
    owner_id: int
    id: int
    comments: Comments | None = None
    likes: int = 0
    owner: User

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    content: str | None = None


class PostUpdateLikes(PostBase):
    likes: int


class PostCreate(PostBase):
    content: str | None = None
