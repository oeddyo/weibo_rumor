__author__ = 'eddiexie'
import pymongo
from api_warpper import API
import config

def download_tweet_comments_and_save(tweet_id):
    mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
    mongo_db = mongo[config.db_name]

    mongo_collection = mongo_db.comments
    api = API()
    cursor = 0

    while True:
        try:
            data = api.get_api().get("comments/show", id = tweet_id, count = 200)
            next_cursor = data['next_cursor']
            for comment in data['comments']:
                mongo_collection.insert(comment)
            if cursor == next_cursor:
                break
            else:
                cursor = next_cursor
        except:
            return

if __name__ == "__main__":
    download_tweet_comments_and_save(3531965485117180L)
    pass
