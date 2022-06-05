"""Различные методы проверки функционала"""
from datetime import datetime

from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

from core.broker.celery import celery_app
from core.broker.redis import redis


router = APIRouter(prefix="/utils")


@router.post("/send_celery_task")
def send_celery_task(begin_datetime: datetime):
    """Запускает выполнение задачи queue.test
    
    Args:
        begin_datetime: datetime, когда запустить задачу
    """
    celery_app.send_task("queue.test", eta=begin_datetime)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8080/utils/ws/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/ws-page")
async def ws_page():
    return HTMLResponse(html)


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    if user_id is None:
        return

    await websocket.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"user-{user_id}")

    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)

        if message:
            await websocket.send_text(message["data"].decode())


@router.get("/ws-pubsub")
async def ws_pubsub(user_id: int, text: str = "test text"):
    await redis.publish(f"user-{user_id}", text)
