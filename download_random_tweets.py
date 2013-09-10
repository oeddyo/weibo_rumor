__author__ = 'eddiexie'
import random
import pymongo
import time
from api_warpper import API
import config


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
    else:
        print 'Not in data'
    time.sleep(random.randint(10, 60))
