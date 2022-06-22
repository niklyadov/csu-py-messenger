from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db, get_current_user
import common.crud.user as crud
from schemas.user import User, UserInDB

router = APIRouter(prefix="/user")


@router.get("/", response_model=UserInDB)
async def get_user(user_id=Depends(get_current_user), db=Depends(get_db)):
    user = crud.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

@router.put("/", response_model=UserInDB)
async def update_user(user: User, user_id=Depends(get_current_user), db=Depends(get_db)):
    user_db = crud.update_user(db=db, user_id=user_id, user=user)

    return user_db


@router.delete("/")
async def delete_user(user_id=Depends(get_current_user), db=Depends(get_db)):
    crud.delete_user(db=db, user_id=user_id)
