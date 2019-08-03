"""
we will save in Redis sorted set (sorted by root_id timestamp)
"""
import time
import redis


class PersistenceWriter:
    def __init__(self, host=None, port=None):
        self.host = host if host is not None else 'localhost'
        self.port = port if port is not None else 6379
        self.conn = None

    def connect(self):
        try:
            self.conn = redis.StrictRedis(host=self.host, port=self.port)
            self.conn.ping()
            print('Connected!')
        except Exception as ex:
            print('Error:', ex)
            exit('Failed to connect, terminating.')

    def _update_task(self, uuid, root_id):
        pass

    def update_task(self, uuid, root_id):
        current_timestamp_in_millisecond = int(time.time()*1000)
        self.conn.zadd('tasks', current_timestamp_in_millisecond, uuid)
