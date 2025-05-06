import asyncio
import signal
import sys
from rq import Worker, Queue
from redis import Redis

from src.config import settings
from src.contrib.repository.mongodb_utils import connect_to_mongo


async def init():
    await connect_to_mongo()


def run_worker():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(init())

    redis_conn = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

    def shutdown(signum, _frame):
        print("Shutting down worker...")
        loop.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        queue = Queue(settings.REDIS_QUEUE, connection=redis_conn)
        worker = Worker([queue], connection=redis_conn)

        loop.run_until_complete(init())

        worker.work()
    except Exception as e:
        print(f"Worker error: {str(e)}")
        loop.close()
        sys.exit(1)


if __name__ == '__main__':
    run_worker()