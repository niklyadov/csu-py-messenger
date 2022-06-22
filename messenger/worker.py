from datetime import datetime

from common.broker.celery_inst import celery_app


@celery_app.task(name="queue.test")
def test():
    print(datetime.now())
