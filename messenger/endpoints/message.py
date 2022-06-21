from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db
import crud.message as crud
from schemas.message import Message, MessageInDB
from core.broker.redis_inst import redis

router = APIRouter(prefix="/message")


@router.post("/", response_model=MessageInDB)
async def create_message(message: Message, db=Depends(get_db)):
    result = crud.create_message(db=db, message=message)
    await redis.publish(f"chat-{message.chat_id}", message.toJSON())

    return result


@router.get("/", response_model=MessageInDB)
async def get_message(message_id, db=Depends(get_db)):
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message


@router.get("/chat", response_model=list[MessageInDB])
async def get_chat_messages(chat_id: int, db=Depends(get_db)):
    messages = crud.get_all_messages_in_chat(db=db, chat_id=chat_id)
    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return messages
