from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..db import Base


class PostDB(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    likes = Column(Integer, nullable=False, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    date_posted = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, default=None)

    owner = relationship("UserDB", back_populates="posts")

    comments = relationship("CommentDB", back_populates="post")
