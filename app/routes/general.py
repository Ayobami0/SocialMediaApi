from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.user_model import User, UserCreate
from models.post_model import Post
from database.crud.read import ReadRepository
from database.crud.create import CreateRepository
from database.db import get_db

general_route = APIRouter(prefix='/all', tags=['general'])


@general_route.get("/posts", response_model=list[Post])
async def get_all_posts(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    post_db = ReadRepository.get_posts(db, skip, limit)
    return post_db


@general_route.get("/user", response_model=list[User])
async def get_all_users(
    skip: int = 0, limit: int = 10,
    db: Session = Depends(get_db)
):
    users_db = ReadRepository.get_users(db, skip, limit)
    return users_db


@general_route.post("/create/", response_model=User)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = ReadRepository.get_users_by_email(db, user.email_address)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with the email address already exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = CreateRepository.create_user(db, user)
    return db_user
