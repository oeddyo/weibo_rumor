__author__ = 'eddiexie'
import pymongo
from api_warpper import API
import config
import pprint

def download_tweet_comments_and_save(tweet_id):
    mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
    mongo_db = mongo[config.db_name]

    mongo_collection = mongo_db.comments
    api = API()
    my_cursor = -1L
    my_page = 1
    while True:
        try:
            print 'at my_cursor %d'%(my_cursor)
            data = api.get_api().get("comments/show", id=tweet_id, count=200, page=my_page)
            my_page += 1
            for comment in data['comments']:
                mongo_collection.insert(comment)
        except :
            return

if __name__ == "__main__":
    download_tweet_comments_and_save(3616370703252156L)
    pass
