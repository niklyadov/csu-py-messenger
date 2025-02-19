from sqlalchemy.orm import Session

from common.db.models import Message
from common.db.models import UserChat

import schemas.message as schema

from common.crud import chat as chat_crud


def create_message(db: Session, message: schema.Message):
    user_chat: UserChat = chat_crud.get_chat_by_ids(db=db, chat_id=message.chat_id, user_id=message.user_id)
    if user_chat is None:
        return False
    message_db = Message(user_chat_id=user_chat.id, text=message.text, edited=message.edited, read=message.read)
    db.add(message_db)
    db.commit()

    return schema.MessageInDB(id=message_db.id, user_id=message.user_id, chat_id=message.chat_id, text=message.text,
                              edited=message_db.edited, read=message_db.read)


def get_message_by_id(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).one_or_none()
    return map_message_to_db_message(db, message)


def get_all_messages_in_chat(db: Session, chat_id: int, limit=255, offset=0):
    messages = db.query(Message) \
        .filter(Message.user_chat_id == chat_id) \
        .limit(limit) \
        .all()

    return list(map(lambda message: map_message_to_db_message(db, message), messages))


def update_message(db: Session, message: Message):
    message_in_db = db.query(Message).filter_by(id=message.id).one_or_none()
    message_in_db.text = message.text
    message_in_db.media = message.media

    db.commit()
    db.refresh(message_in_db)

    return map_message_to_db_message(db, message_in_db)


def delete_message_by_id(db: Session, message_id: int):
    message_in_db = db.query(Message).filter_by(id=message_id).one_or_none()
    if not message_in_db.is_deleted:
        message_in_db.is_deleted = True
        db.commit()
        db.refresh(message_in_db)

    return map_message_to_db_message(db, message_in_db)


def mark_as_read(db: Session, message_id: int):
    message_in_db = db.query(Message).filter_by(id=message_id).one_or_none()
    if not message_in_db.read:
        message_in_db.read = True
        db.commit()
        db.refresh(message_in_db)

    return map_message_to_db_message(db, message_in_db)


def map_message_to_db_message(db: Session, message: Message):
    pair = chat_crud.get_chat_by_its_id(db, pair_id=message.user_chat_id)
    return schema.MessageInDB(id=message.id, user_id=pair.user_id, chat_id=pair.chat_id, text=message.text,
                              edited=message.edited, read=message.read)
