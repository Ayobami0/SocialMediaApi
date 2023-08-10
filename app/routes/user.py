from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.jwt_handlers import get_current_user
from models.user_model import User, UserCreate
from models.post_model import Post, PostUpdate, PostCreate
from models.comments_model import Comment, CommentCreate
from database.crud.read import ReadRepository
from database.crud.create import CreateRepository
from database.crud.update import UpdateRepository
from database.db import get_db

user_route = APIRouter()


@user_route.post("/users/create/", response_model=User)
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


@user_route.get("/users/me/", response_model=User)
async def me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@user_route.get("/users/me/posts", response_model=list[Post])
async def get_posts_by_user(
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db),
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_db = ReadRepository.get_user(db, user_id=current_user.id)

    if user_db:
        user_posts = user_db.posts
        return user_posts


@user_route.post("/users/me/post/create", response_model=Post)
async def create_post(
    post: PostCreate,
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db),
):
    post_db = CreateRepository.create_post(db, post, current_user.id)
    print(post_db.owner.email_address)
    return post_db


@user_route.patch("/users/me/post/edit", response_model=Post)
async def edit_post(
    post: PostUpdate,
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db),
):
    post_db = UpdateRepository.update_post(
        db,
        post.id,
        current_user.id,
        post.content
    )
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {post.id}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return post_db


@user_route.patch("/users/me/post/like", response_model=Post)
async def like_post(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db)
):
    post_db = UpdateRepository.change_post_like(
        db,
        post_id,
        like=True)

    return post_db


@user_route.post("/users/me/post/comment/", response_model=Comment)
async def write_comment(
    comment: CommentCreate,
    current_user: Annotated[User, Depends(get_current_user),],
    post_id: int,
    db: Session = Depends(get_db)
):
    post_db = ReadRepository.get_post(db, post_id)

    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {post_id}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    comment_db = CreateRepository.create_comment(db, comment, post_id)
    return comment_db
