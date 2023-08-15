from typing import List

from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.jwt_handlers import get_current_user
from models.user_model import User
from models.post_model import Post, PostUpdate, PostCreate
from models.comments_model import Comment, CommentCreate
from database.crud.read import ReadRepository
from database.crud.create import CreateRepository
from database.crud.update import UpdateRepository
from database.db import get_db

user_route = APIRouter(prefix="/user/me", tags=['logged in'])


@user_route.get("/", response_model=User)
async def me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@user_route.get("/posts", response_model=List[Post])
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


@user_route.post("/post/create", response_model=Post)
async def create_post(
    post: PostCreate,
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db),
):
    post_db = CreateRepository.create_post(db, post, current_user.id)
    print(post_db.owner.email_address)
    return post_db


@user_route.patch("/post/edit", response_model=Post)
async def edit_post(
    post: PostUpdate,
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db),
):
    print(post.content)
    post_db = UpdateRepository.update_post(
        db,
        post_id=post.id,
        user_id=current_user.id,
        content=post.content
    )
    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {post.id}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return post_db


@user_route.patch("/post/like", response_model=Post)
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


@user_route.patch("/post/unlike", response_model=Post)
async def unlike_post(
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user),],
    db: Session = Depends(get_db)
):
    post_db = ReadRepository.get_post(db, post_id).likes
    if post_db == 0:
        return post_db
    post_db = UpdateRepository.change_post_like(
        db,
        post_id,
        like=False)

    return post_db


@user_route.post("/post/comment/", response_model=Comment)
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
