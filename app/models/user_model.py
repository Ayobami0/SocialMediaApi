from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email_address: EmailStr


class User(UserBase):
    id: int


class UserPost(User):
    id: int
    posts: list

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
