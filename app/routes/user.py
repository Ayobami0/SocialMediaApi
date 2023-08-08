from typing import Annotated

from fastapi import APIRouter, Depends

from auth.jwt_handlers import get_current_user
from models.user_model import User
from models.post_model import Post

user_route = APIRouter()


@user_route.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@user_route.get("/users/me/posts", response_model=list[Post])
async def get_posts(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return []


@user_route.get("/users/me/posts", response_model=list[Post])
async def get_post(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user),]
):
    return []
