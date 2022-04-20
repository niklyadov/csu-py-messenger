from fastapi import APIRouter

from crud.user import user_database
from schemas.user import User, UserInDB


router = APIRouter(prefix="/user")


@router.get("/{user_id}")
async def get_user(user_id: int):
    """Получить пользователя по заданному user_id"""
    return user_database[user_id-1]


@router.post("/", response_model=UserInDB)
async def create_user(user: User):
    """Создать пользователя"""
    # Здесь происходит добавление пользователя в БД
    user_db = UserInDB(id=len(user_database)+1, **user.dict())
    return user_db


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user: User):
    user_db = user_database[user_id-1]
    for param, value in user.dict().items():
        user_db[param] = value

    # здесь изменения сохраняются в базу

    return user_db


@router.delete("/{user_id}")
async def update_user(user_id: int):
    db = list(user_database)
    del db[user_id-1]