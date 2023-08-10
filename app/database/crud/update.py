from sqlalchemy.orm import Session

from ..db_models import user_db, post_db


class UpdateRepository:
    def change_post_like(db: Session, post_id: int, like: bool):
        db.query(
            post_db.PostDB).filter(
            post_db.PostDB.id == post_id).update(
            {'likes': post_db.PostDB.likes + 1
             if like else post_db.PostDB.likes - 1})
        db.commit()
        post = db.query(post_db.PostDB).filter(
            post_db.PostDB.id == post_id).first()
        return post

    def update_post(
            db: Session,
            post_id: int,
            user_id: int,
            content: str
            ):

        db.query(
            post_db.PostDB
        ).filter(
            post_db.PostDB.owner_id == user_id,
            post_db.PostDB.id == post_db
        ).update(
            {'content': content}
        )
        db.commit()
        post = db.query(post_db.PostDB).filter(
            post_db.PostDB.id == post_id).first()
        return post
