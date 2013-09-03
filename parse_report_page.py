# coding=utf-8
import logging

__author__ = 'eddiexie'


from BeautifulSoup import BeautifulSoup
from api_warpper import API
import utils

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
    return soup.find('a', attrs={'suda-uatrack':'key=tblog_service_account&value=original_text'})


def parse_pages_and_download():
    """Get pages from mongo db and download data from API. Store data into MongoDB"""
    api = API()

    mongo_interface_read_pages = utils.MongoInterface('pages')
    mongo_interface_insert_data = utils.MongoInterface('rumor_tweets')

    for page_index, page in  enumerate(mongo_interface_read_pages.get_all_pages()):
        logging.debug('Working on %d th page'%(page_index))
        tweet_url_object = parse(page['html'])
        if tweet_url_object is None:
            continue
        else:
            tweet_url = str(tweet_url_object['href'])
            tweet_id =  string_to_tweet_id(tweet_url[(len(tweet_url) - tweet_url[::-1].index("/")):])
            try:
                data = api.get_api().get("statuses/show", id=tweet_id)
            except:
                logging.warn("Exception when fetching data. Continue")
                continue
            data['_id'] = page['_id']  # use the id of report page url as tweet url
            soup = BeautifulSoup(page['html'])
            judge = soup.find('p', attrs={'class':'p'})

            try:
                if judge.text.find(u"不予受理")!=-1:
                    data['approved_report'] = 1
                else:
                    data['approved_report'] = 0
            except:
                logging.warn("Excpetion in deciding report.")
                continue
            mongo_interface_insert_data.insert_into_collection(data)

parse_pages_and_download()
