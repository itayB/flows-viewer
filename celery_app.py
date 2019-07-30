from celery import Celery


def get_app():
    return Celery(
        'worker',
        broker='pyamqp://localhost/vhost',
        backend='redis://localhost/0'
    )
