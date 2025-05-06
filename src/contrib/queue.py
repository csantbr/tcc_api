from redis import Redis
from rq import Queue

from src.config import settings


class QueueManager:
    _instance = None
    _queue = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueueManager, cls).__new__(cls)
        return cls._instance

    @property
    def queue(self) -> Queue:
        if self._queue is None:
            redis_conn = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB
            )
            self._queue = Queue(settings.REDIS_QUEUE, connection=redis_conn)
        return self._queue

    def enqueue(self, func, *args, **kwargs):
        """Enqueue a job to be processed."""
        return self.queue.enqueue(func, *args, **kwargs)


queue_manager = QueueManager()