from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    author: str
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    author: str
    content: str
    from_post_id: int
    date_created: datetime

    class Config:
        orm_mode = True


from .post_model import PostComment
class CommentSourcePost(Comment):
    post: PostComment
