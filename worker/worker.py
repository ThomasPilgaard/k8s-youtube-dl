from redis import Redis
from rq import Queue, Worker, Connection
import downloader
import os

redis_path = os.getenv('REDIS_PATH')
redis_queue_name = os.getenv('YOUTUBE_QUEUE_NAME')

conn = Redis.from_url(redis_path)

if __name__ == '__main__':
    with Connection(conn):
        q = Queue(redis_queue_name, connection=conn)
        worker = Worker([q], connection=conn)
        worker.work()
