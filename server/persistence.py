# we will save in Redis sorted set (sorted by root_id timestamp)

class PersistenceWriter:
    def __init__(self, conn):
        self.conn = conn

    def add_task(self, uuid, root_id):
        pass
