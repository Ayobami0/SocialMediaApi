from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..db import Base


class CommentDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, ForeignKey("users.email_address"))
    content = Column(String, index=True)
    date_created = Column(DateTime, nullable=False)
    from_post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("PostDB", back_populates='comments')
