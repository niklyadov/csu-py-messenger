import json
from datetime import datetime

from pydantic import BaseModel


class Chat(BaseModel):
    name: str
    type: str


class ChatCreate(Chat):
    created_date: datetime


class ChatInDB(Chat):
    id: int

    class Config:
        orm_mode = True


class ChatEvent:
    event_name: str
    event_data: str

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
