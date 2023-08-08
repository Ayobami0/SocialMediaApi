from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    username: str
    email_address: EmailStr = Field(default=None)

    class Config:
        schema_extra = {
            "user_demo": {
                "username": "@example",
                "email_address": "user@example.com"
            }
        }


class UserIn(User):
    password: EmailStr = Field(default=None)
