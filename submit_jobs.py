from rq import Queue

__author__ = 'eddiexie'

import config
from download_report_page import download_and_save
from redis import Redis

if __name__ == "__main__":
    lines = set(open("report_page_urls.txt", 'r').readlines())
    redis_conn = Redis(config.redis_server)
    q = Queue(connection=redis_conn)

    for line in lines:
        q.enqueue_call(func=download_and_save(),args=((line,),), timeout=572000)