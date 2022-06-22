import json
from datetime import datetime
from os import getenv
import pytz

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from common.broker.celery_inst import celery_app
from common.broker.redis_inst import redis

router = APIRouter()

security = HTTPBasic()


@router.get("/")
async def home():
    """HTML chats"""
    import os
    path = os.getcwd()
    with open(path + "/static/home.html", "r") as html:
        return HTMLResponse(html.read())


@router.post("/send_celery_task")
def send_celery_task(begin_datetime: datetime):
    timezone = pytz.timezone(getenv("TZ"))
    dt_with_timezone = timezone.localize(begin_datetime)

    celery_app.send_task("queue.test", eta=dt_with_timezone)


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    if chat_id is None:
        return

    await websocket.accept()
    pub_sub = redis.pubsub()
    await pub_sub.subscribe(f"chat-{chat_id}")

    while True:
        message = await pub_sub.get_message(ignore_subscribe_messages=True)

        if message:
            json_obj = json.dumps(message["data"])
            await websocket.send_text(json_obj)

