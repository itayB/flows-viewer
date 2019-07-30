from celery_app import get_app


app = get_app()


@app.task
def add(x, y):
    return x + y
