from sqlalchemy import Column, ForeignKey, Integer, String

from ..db import Base


class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    content = Column(String, index=True)
    from_post_id = Column(Integer, ForeignKey("posts.id"))
