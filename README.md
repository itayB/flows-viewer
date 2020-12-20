### Installation
`pip install -r requirements.txt`


###Run locally
Start RabbitMQ as celery broker:

`docker-compose up -d`

Start celery worker (to simulate tasks):

`celery -A worker worker --loglevel=info`

Run `listener.py` to inspect tasks.

Run `flow_generator.py` to simulate tasks.

