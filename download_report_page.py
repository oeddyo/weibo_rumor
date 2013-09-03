__author__ = 'eddiexie'
import config
import requests
import logging
import pymongo
import random
import time
import credential


logging.basicConfig(filename = "./url_download.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')

def save_to_mongo(url, page):
    mongo = pymongo.Connection(config.mongo_host, config.mongo_port)
    mongo_db = mongo[config.db_name]
    mongo_collection = mongo_db.pages
    page_to_insert = {}
    page_to_insert['html'] = page
    page_to_insert['_id'] = url
    mongo_collection.insert(page_to_insert)

def download_and_save(url):
    logging.warn('Downloading url ' + str(url))
    try:
        res = requests.get(url, headers = {"cookie":credential.cookie}, timeout=30)
    except requests.exceptions.Timeout:
        logging.warn("Banned. Sleep for 10 minutes.")
        time.sleep(600)
        return False
    try:
        save_to_mongo(url, res.text)
    except Exception as e:
        logging.warn("Inserting to mongo-db error!" )
        return False
    time.sleep(random.randint(1, 20))
    return True

if __name__ == '__main__':
    download_and_save(u"http://service.account.weibo.com/show?rid=K1CaJ8Apd8q4m")
