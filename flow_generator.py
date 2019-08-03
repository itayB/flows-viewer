from celery import group
from celery_app import get_app
from worker import add

app = get_app()

print('before')
res = group(add.si(1, 1), add.si(2, 2))
# res = add.si(1, 1) | add.si(2, 2) | group(add.si(3, 3), add.si(4, 4)) | add.si(5, 5)
# res = group(add.si(1, 1), add.si(2, 2), group(add.si(3, 3), add.si(4, 4)), add.si(5, 5)) | add.si(6, 6)

print('build')
a = res.apply_async()
print('run')
print(a)

