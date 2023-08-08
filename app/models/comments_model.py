from pydantic import BaseModel, Field

from .user_model import User


class Comments(BaseModel):
    id: int = Field(default=None)
    creator: User = Field(default=None)
    initial_comment: str = Field(default=None)
    content: str = Field(default=None)
    reply_comments: list[User, str] = Field(default=None)