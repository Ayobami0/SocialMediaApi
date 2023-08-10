from pydantic import BaseModel

from .user_model import User


class PostBase(BaseModel):
    content: str | None = None


class PostComment(PostBase):
    owner_id: int
    id: int
    likes: int = 0
    owner: User


from .comments_model import Comment
class Post(PostComment):
    comments: list[Comment] | None = None

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostCreate):
    id: int


class PostUpdateLikes(PostCreate):
    id: int
