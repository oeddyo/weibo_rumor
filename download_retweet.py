__author__ = 'eddiexie'
import pymongo
from api_warpper import API
import config
import logging
logging.basicConfig(filename = "./log/download_repost.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')


def download_retweets_and_save(tweet_id):
    mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
    mongo_db = mongo[config.db_name]

    mongo_collection = mongo_db.reposts
    api = API()
    my_page = 1
    while True:
        try:
            logging.warn('at my_cursor %d'%(my_page) )
            data = api.get_api().get("statuses/repost_timeline", id=tweet_id, count=200, page=my_page)
            my_page += 1
            for repost in data['reposts']:
                mongo_collection.insert(repost)
        except :
            return

if __name__ == "__main__":
    download_retweets_and_save(3616370703252156L)
    pass
