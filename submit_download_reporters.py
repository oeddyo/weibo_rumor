from rq import Queue

__author__ = 'eddiexie'

import config
from parse_reporters import download_reporter
from redis import Redis
import utils



if __name__ == "__main__":
    lines = set(open("report_page_urls.txt", 'r').readlines())
    redis_conn = Redis(config.redis_server)
    q = Queue(connection=redis_conn)

    my_db= utils.MongoInterface('rumor')
    cursor = my_db.connect_to_mongo('rumor_tweets')
    ids = set([tweet['reporter'] for tweet in cursor.find()  ])
    for my_id in ids:
        q.enqueue_call(func=download_reporter, args = (my_id,), timeout=572000)
