import time
from celery_app import get_app


app = get_app()


@app.task
def add(x, y):
    time.sleep(2)
    return x + y
