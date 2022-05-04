from sqlalchemy.orm import Session

from core.db.models import User
import schemas.user as schema


def create_user(db: Session, user: schema.User):
    user_db = User(**user.dict())
    db.add(user_db)
    db.commit()

    return user_db


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).one_or_none()


def update_user(db: Session, user_id: int, user: schema.User):
    user_db = db.query(User).filter(User.id == user_id).one_or_none()
    for param, value in user.dict().items():
        setattr(user_db, param, value)
    db.commit()

    return user_db


def delete_user(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
