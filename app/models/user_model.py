from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
    username: str
    email_address: EmailStr


class User(UserBase):
    id: int


class UserPost(User):
    id: int
    posts: List

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
