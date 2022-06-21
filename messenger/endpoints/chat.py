from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from deps import get_db, get_current_user
import crud.chat as crud
from schemas.chat import Chat, ChatInDB
from schemas.user import UserInDB

router = APIRouter(prefix="/chat")


@router.post("/", response_model=ChatInDB)
async def create_chat(chat: Chat, user_id=Depends(get_current_user), db=Depends(get_db)):
    """Creates new chat"""
    result = crud.create_chat(db=db, user_id=user_id, chat=chat)

    return result


@router.get("/", response_model=ChatInDB)
async def get_chat(chat_id, db=Depends(get_db)):
    """Get chat with ID"""
    chat = crud.get_chat_by_id(db=db, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return chat


@router.get("/members", response_model=List[UserInDB])
async def get_chat_members(chat_id: int, db=Depends(get_db)):
    """Get all chat members"""
    chat = crud.get_chat_members(db=db, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return chat


@router.get("/my", response_model=List[ChatInDB])
async def get_user_chat(user_id=Depends(get_current_user), db=Depends(get_db)):
    """Get chats for authorized user"""
    chat = crud.get_all_chats_of_user(db=db, user_id=user_id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return chat
