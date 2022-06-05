"""Различные методы проверки функционала"""
from datetime import datetime

from fastapi import APIRouter

from core.broker.celery import celery_app


router = APIRouter(prefix="/utils")


@router.post("/send_celery_task")
def send_celery_task(begin_datetime: datetime):
    """Запускает выполнение задачи queue.test
    
    Args:
        begin_datetime: datetime, когда запустить задачу
    """
    celery_app.send_task("queue.test", eta=begin_datetime)
