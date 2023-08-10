from sqlalchemy.orm import Session

from ..db_models import user_db, post_db


class ReadRepository:
    def get_user(db: Session, user_id: int):
        return db.query(user_db.UserDB).filter(
            user_db.UserDB.id == user_id).first()

    def get_post(db: Session, post_id: int):
        return db.query(post_db.PostDB).filter(
            post_db.PostDB.id == post_id).first()

    def get_users(db: Session, skip: int = 0, limit: int = 10):
        return db.query(user_db.UserDB).offset(skip).limit(limit).all()

    def get_users_by_email(db: Session,
                           email_address: str,):
        return db.query(user_db.UserDB).filter(
            user_db.UserDB.email_address == email_address).first()

    def get_users_by_username(db: Session,
                              username: str, skip: int = 0, limit: int = 10):
        return db.query(user_db.UserDB).offset(skip).limit(limit).all()

    def get_posts(db: Session, skip: int = 0, limit: int = 10):
        return db.query(post_db.PostDB).offset(skip).limit(limit).all()
