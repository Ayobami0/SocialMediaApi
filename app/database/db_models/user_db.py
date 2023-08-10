from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Integer, index=True)
    email_address = Column(String, unique=True, index=True, nullable=False)
    password = Column(String)

    posts = relationship("PostDB", back_populates="owner")
