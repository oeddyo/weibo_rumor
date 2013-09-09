import pymongo
import config
import random
__author__ = 'eddiexie'


class MongoInterface():
    def __init__(self, collection='pages'):
        self.mongo_collection = self.connect_to_mongo(collection)

    def connect_to_mongo(self, collection):
        mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
        mongo_db = mongo[config.db_name]
        mongo_collection = mongo_db[collection]
        return mongo_collection

    def get_random_page(self):
        self.connect_to_mongo.find_one({rnd: {'$gte': random()}})

    def get_all_pages(self):
        pages = self.mongo_collection.find(timeout=False).sort('_id')
        return pages

    def get_all_tweets(self):
        tweets = self.mongo_collection.find()
        return tweets

    def insert_into_collection(self, data):
        self.mongo_collection.insert(data)