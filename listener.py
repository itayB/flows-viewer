import sys
import time
import logging
from celery.result import AsyncResult, GroupResult
from celery.events import EventReceiver
from celery_app import get_app
from node import Node
from server.persistence import PersistenceWriter
from celery.utils.log import get_task_logger

LOG_FORMAT = '%(asctime)-15s %(process)-6d %(levelname)-7s %(message)s [file: %(filename)s, line: %(lineno)d]'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = get_task_logger(__name__)


class Events:
    def __init__(self):
        self.counter = 0
        self.root = None
        self.nodes = []
        # self.persist = PersistenceWriter()
        self.group_set_id = None

    def _on_event(self, event):
        if event.get('type') == 'worker-heartbeat':
            return
        self.counter += 1
        logger.info('%s events handled', self.counter)
        logger.info(event)
        uuid = event.get('uuid')
        res = AsyncResult(uuid)
        task_name = event.get('name')
        args = event.get('args')
        root_id = event.get('root_id')
        # if root_id is not None:
        #     logger.info("root: {}".format(root_id))
            # self.persist.update_task(uuid, '')
        # else:
        # logger.info('graph:\n' + repr(res.graph))
        logger.info("")
        # print("root: {}".format(root_id))
        parent = res.parent
        node = Node(uuid, task_name, args, root_id, parent)
        if node not in self.nodes:
            self.nodes.append(node)

        logger.info('self.group_set_id: %s', self.group_set_id)
        if res.result == 8:
            pass

        if uuid is not None and uuid == self.group_set_id:
            pass

        if res.children is None:
            pass

        if res.children and len(res.children) > 0 and isinstance(res.children[0], GroupResult):
            self.group_set_id = res.children[0]
            pass
        # print('size:{}'.format(len(nodes)))
        # print(res)
        # self.io_loop.add_callback(partial(self.state.event, event))

    def start(self):
        self.app = get_app()

    def run(self):
        logger.info('starting listening to celery events..')
        try_interval = 1
        while True:
            try:
                self.app.control.enable_events()
                try_interval *= 2

                with self.app.connection() as conn:
                    recv = EventReceiver(conn, handlers={"*": self._on_event}, app=self.app)
                    try_interval = 1
                    recv.capture(limit=None, timeout=None, wakeup=True)
            except (KeyboardInterrupt, SystemExit):
                try:
                    import _thread as thread
                except ImportError:
                    import thread
                thread.interrupt_main()
            except Exception as e:
                logger.error("Failed to capture events: '%s', "
                             "trying again in %s seconds.",
                             e, try_interval)
                logger.debug(e, exc_info=True)
            time.sleep(try_interval)


def main():
    events = Events()
    events.start()
    events.run()


if __name__ == "__main__":
    sys.exit(main())
