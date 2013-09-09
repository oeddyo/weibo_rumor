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



class Sampler():
    def __init__(self):
        mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
        mongo_db = mongo[config.db_name]

        self.mongo_collection = mongo_db.random_tweets
        self.api = API()

    def sample_and_save(self):
        # use api to sample tweets from streaming api
        try:
            data = self.api.get_api().get("statuses/public_timeline", count = 200 )
        except:
            return

        if 'statues' in data:
            for tweet in data['statuses']:
                tweet['_id'] = tweet['id']
                self.mongo_collection.insert(tweet)
            time.sleep(random.randint(10, 60))

if __name__ == '__main__':
    redis_conn = Redis(config.redis_server)
    q = Queue(connection=redis_conn)

    sampler = Sampler()

    while True:
        logging.debug("Submitting job...")
        q.enqueue_call(func=sampler.sample_and_save(), args = None, timeout=572000)
