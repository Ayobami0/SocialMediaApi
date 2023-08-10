from datetime import datetime

from sqlalchemy.orm import Session

from ..db_models import user_db, post_db, comment_db
from models import user_model, post_model, comments_model
from auth.jwt_handlers import get_password_hash


class CreateRepository:
    def create_user(db: Session, user: user_model.UserCreate):
        db_user = user_db.UserDB(
            email_address=user.email_address,
            password=get_password_hash(user.password),
            username=user.username
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def create_post(db: Session, post: post_model.PostCreate, user_id: int):
        db_post = post_db.PostDB(
            **post.dict(),
            owner_id=user_id,
            date_posted=datetime.utcnow()
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    def create_comment(
            db: Session,
            comment: comments_model.CommentCreate,
            post_id: int
            ):
        db_comments = comment_db.CommentDB(
            **comment.dict(), from_post_id=post_id, date_created=datetime.utcnow())
        db.add(db_comments)
        db.commit()
        db.refresh(db_comments)
        return db_comments
