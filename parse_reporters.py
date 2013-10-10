# coding=utf-8
import logging

__author__ = 'eddiexie'


from BeautifulSoup import BeautifulSoup
from api_warpper import API
import utils
import re

logging.basicConfig(filename = "./API.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')


def base62_decode(string):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return str(num)


def string_to_tweet_id(hashed_id):
    return "".join(base62_decode(hashed_id[0]) + base62_decode(hashed_id[1:5]) + base62_decode(hashed_id[5:]))


def parse(html):
    soup = BeautifulSoup(html)
    return soup.find('a', attrs={'target':'_blank'})


def parse_reporters():
    """Get pages from mongo db and parse the reporters, download the profiles of those reporters"""
    api = API()

    mongo_interface_read_pages = utils.MongoInterface('pages')
    mongo_interface_insert_data = utils.MongoInterface('rumor')
    cursor = mongo_interface_insert_data.connect_to_mongo('reporters')

    counter = {}
    for page_index, page in  enumerate(mongo_interface_read_pages.get_all_pages()):
        logging.debug('Working on %d th page'%(page_index))
        page_url = page['_id']
        pattern = r"[0-9].*"

        tweet_reporter_object = parse(page['html'])
        reporter = re.findall(pattern, tweet_reporter_object['href'])[0]
        cursor.update({'_id': page_url}, {"$set": {"reporter": reporter}})
        print page_url, reporter
        if reporter in counter:
            counter[reporter] += 1
        else:
            counter[reporter] = 1

def download_reporter(user_id):
    mongo_interface_insert_data = utils.MongoInterface('rumor')
    cursor = mongo_interface_insert_data.connect_to_mongo('reporters')
    api = API()
    data = api.get_api().get("users/show", uid=user_id)
    cursor.insert(data)


#download_reporter(1856687980L)