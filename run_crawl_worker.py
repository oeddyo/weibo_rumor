__author__ = 'eddiexie'

from rq import Queue, Worker, Connection
from redis import Redis
import config

if __name__ == '__main__':
    redis_conn = Redis(config.redis_server)
    with Connection(connection=redis_conn):
        q = Queue()
        Worker(q).work()