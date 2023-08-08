from pydantic import BaseModel, Field

from .comments_model import Comments


class Post(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)
    comments: Comments = Field(default=None)

    class Config:
        schema_extra = {
            "post_demo": {
                "title": "Some title on a topic",
                "content": "Some content to expand the title"
            }
        }
