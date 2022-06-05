from datetime import datetime
from enum import Enum


class ChatType(str, Enum):
    public = "public"
    private = "private"
    group = "group"


chat_database = [
    {
        "id": 1,
        "name": "Чат 1",
        "created_date": datetime(2022, 4, 20, 19, 39, 0),
        "type": ChatType.group,
    }
]

user_chat_database = [
    {
        "user_id": 1,
        "chat_id": 1
    },
    {
        "user_id": 2,
        "chat_id": 1
    },
]