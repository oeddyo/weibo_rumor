from redis import Redis
from rq import Queue

__author__ = 'eddiexie'


import pymongo
import config
import logging
import time
import random
from api_warpper import API

logging.basicConfig(filename = "./random_sample.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')




def sample_and_save():
    # use api to sample tweets from streaming api
    mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
    mongo_db = mongo[config.db_name]

    mongo_collection = mongo_db.random_tweets
    api = API()

    try:
        data = api.get_api().get("statuses/public_timeline", count = 200 )
    except:
        return

    if 'statuses' in data:
        for tweet in data['statuses']:
            tweet['_id'] = tweet['id']
            mongo_collection.insert(tweet)
    time.sleep(random.randint(10, 60))
    mongo_collection.close()

if __name__ == '__main__':
    print 'begin'
    logging.warn("Begin...")
    redis_conn = Redis(config.redis_server)
    q = Queue(connection=redis_conn)

    while True:
        logging.warn("Submitting job...")
        q.enqueue_call(func=sample_and_save(), timeout=572000)
        time.sleep(1)