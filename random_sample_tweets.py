from redis import Redis
from rq import Queue

__author__ = 'eddiexie'


import config
import logging
import time
from download_random_tweets import sample_and_save

logging.basicConfig(filename = "./random_sample.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')



if __name__ == '__main__':
    print 'begin'
    logging.warn("Begin...")
    redis_conn = Redis(config.redis_server)
    q = Queue(connection=redis_conn)

    while True:
        logging.warn("Submitting job...")
        print 'Submitting...'
        q.enqueue_call(func=sample_and_save, args=None, timeout=572000)
        time.sleep(1)