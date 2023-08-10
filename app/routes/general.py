from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.user_model import User
from models.post_model import Post
from database.crud.read import ReadRepository
from database.db import get_db

general_route = APIRouter()


@general_route.get("all/posts/", response_model=list[Post])
async def get_all_posts(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    post_db = ReadRepository.get_posts(db, skip, limit)
    return post_db


@general_route.get("all/user", responses=list[User])
async def get_all_users(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    users_db = ReadRepository.get_users(db, skip, limit)
    return users_db
