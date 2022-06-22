from sqlalchemy.orm import Session

from common.db.models import Chat
from common.db.models import UserChat
from common.db.models import User
import schemas.chat as schema_c
import schemas.chat_user as schema_u


def create_chat(db: Session, user_id: int, chat: schema_c.Chat):
    chat_db = Chat(name=chat.name, type=chat.type)
    db.add(chat_db)
    db.commit()

    add_user_in_chat(db, schema_u.ChatUser(user_id=user_id, chat_id=chat_db.id))

    return chat_db


def add_user_in_chat(db: Session, chat_user: schema_u.ChatUser):
    user_chat_db = UserChat(user_id=chat_user.user_id, chat_id=chat_user.chat_id)
    db.add(user_chat_db)
    db.commit()
    return user_chat_db


def get_chat_by_id(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).one_or_none()


def get_chat_by_name(db: Session, name: str):
    return db.query(Chat).filter(Chat.name == name).one_or_none()


def get_chat_members(db: Session, chat_id: int):
    mem_ids = db.query(UserChat.user_id).filter(UserChat.chat_id == chat_id).all()
    mem_ids = [id[0] for id in mem_ids]
    result = db.query(User).filter(User.id.in_(mem_ids)).all()
    return result


def get_all_chats_of_user(db: Session, user_id: int):
    chat_ids = db.query(UserChat.chat_id).filter(UserChat.user_id == user_id).all()
    chat_ids = [id[0] for id in chat_ids]
    result = db.query(Chat).filter(Chat.id.in_(chat_ids)).all()
    return result


def get_all_chats_by_id(db: Session, chat_id: int):
    return db.query(UserChat).filter(UserChat.chat_id == chat_id).all()


def get_chat_by_ids(db: Session, user_id: int, chat_id: int):
    return db.query(UserChat).filter(UserChat.chat_id == chat_id and UserChat.user_id == user_id).one_or_none()


def get_chat_by_its_id(db: Session, pair_id: int):
    return db.query(UserChat).filter(UserChat.id == pair_id).one_or_none()


def update_chat(db: Session, chat_id: int, chat: schema_c.Chat):
    chat_db = db.query(Chat).filter(Chat.id == chat_id).one_or_none()
    for param, value in chat.dict().items():
        setattr(chat_db, param, value)
    db.commit()

    return chat_db


def delete_chat(db: Session, chat_id: int):  # DO NOT USE BCZ KEYS
    db.query(Chat).filter(Chat.id == chat_id).delete()
    db.commit()