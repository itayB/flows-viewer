import time
from functools import partial
from celery.result import AsyncResult
from celery.events import EventReceiver
from celery_app import get_app
from node import Node

app = get_app()

try_interval = 1

root = None
nodes = []


def on_event(event):
    # Call EventsState.event in ioloop thread to avoid synchronization
    if event.get('type') != 'worker-heartbeat':
        print(event)
        uuid = event.get('uuid')
        print(uuid)
        res = AsyncResult(uuid)
        task_name = event.get('name')
        args = event.get('args')
        root_id = event.get('root_id')
        parent = res.parent
        node = Node(uuid, task_name, args, root_id, parent)
        if node not in nodes:
            nodes.append(node)
        print('size:{}'.format(len(nodes)))
        print(res)
    # self.io_loop.add_callback(partial(self.state.event, event))


while True:
    try:
        app.control.enable_events()
        try_interval *= 2

        with app.connection() as conn:
            recv = EventReceiver(conn,
                                 handlers={"*": on_event},
                                 app=app)
            try_interval = 1
            recv.capture(limit=None, timeout=None, wakeup=True)

    except (KeyboardInterrupt, SystemExit):
        try:
            import _thread as thread
        except ImportError:
            import thread
        thread.interrupt_main()
    except Exception as e:
        print("Failed to capture events: '{}', trying again in {} seconds.".format(e, try_interval))
        print(e)
        time.sleep(try_interval)
