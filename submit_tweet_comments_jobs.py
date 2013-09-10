__author__ = 'eddiexie'
from redis import Redis
from rq import Queue

__author__ = 'eddiexie'


import config
import logging
import time
import pymongo
from api_warpper import API
from download_tweet_comments import download_tweet_comments_and_save

logging.basicConfig(filename = "./log/download_comments.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')



if __name__ == '__main__':
    print 'begin'
    logging.warn("Begin...")
    redis_conn = Redis(config.redis_server)
    q = Queue(connection=redis_conn)

    mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
    mongo_db = mongo[config.db_name]

    mongo_collection = mongo_db.rumor_tweets
    api = API()

    for tweet in mongo_collection.find():
        tweet_id = tweet['id']
        logging.warn("Submitting job...")
        print 'Submitting...'
        q.enqueue_call(func=download_tweet_comments_and_save, args = tweet_id, timeout=572000)
        time.sleep(1)