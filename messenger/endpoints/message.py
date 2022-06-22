from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db
import common.crud.message as crud
from schemas.message import Message, MessageInDB
from schemas.chat import ChatEvent
from common.broker.redis_inst import redis

router = APIRouter(prefix="/message")


@router.post("/", response_model=MessageInDB)
async def create_message(message: Message, db=Depends(get_db)):
    result = crud.create_message(db=db, message=message)
    #
    # event = ChatEvent()
    # event.event_name = "create-message"
    # event.event_data = message.toJSON()

    await redis.publish(f"chat-{message.chat_id}", message.toJSON())

    return result


@router.get("/", response_model=MessageInDB)
async def get_message(message_id, db=Depends(get_db)):
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message


@router.put("/", response_model=MessageInDB)
async def update_message(message: Message, db=Depends(get_db)):
    message = crud.update_message(db=db, message=message)

    # event = ChatEvent()
    # event.event_name = "update-message"
    # event.event_data = message.toJSON()
    #
    # await redis.publish(f"chat-{message.chat_id}", event.toJSON())
    # if message is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message


@router.delete("/", response_model=MessageInDB)
async def delete_message(message_id: int, db=Depends(get_db)):
    message = crud.delete_message_by_id(db=db, message_id=message_id)

    # event = ChatEvent()
    # event.event_name = "delete-message"
    # event.event_data = message.toJSON()
    #
    # await redis.publish(f"chat-{message.chat_id}", event.toJSON())

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message


@router.get("/chat", response_model=list[MessageInDB])
async def get_chat_messages(chat_id: int, count=255, db=Depends(get_db)):
    messages = crud.get_all_messages_in_chat(db=db, chat_id=chat_id, limit=count, offset=0)
    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return messages


@router.put("/read", response_model=MessageInDB)
async def mark_as_read(message_id: int, db=Depends(get_db)):
    message = crud.mark_as_read(db=db, message_id=message_id)

    # event = ChatEvent()
    # event.event_name = "read-message"
    # event.event_data = message.toJSON()
    #
    # await redis.publish(f"chat-{message.chat_id}", event.toJSON())

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message
