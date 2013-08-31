#coding=utf8

import re
import requests
import time
import random
import config

import logging


from BeautifulSoup import BeautifulSoup

"""
Login to Sina Weibo with cookie
"""



COOKIE = config.cookie
HEADERS = {"cookie": COOKIE}

# logger setting
logger = logging.getLogger('TopPagesCrawler')
hdlr = logging.FileHandler('./top_page_crawler.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


def iterate_pages():
    top_page_url_base = u'http://service.account.weibo.com/index?type=5&status=4&page='
    each_page_base = u'http://service.account.weibo.com'
    urls = []
    output_file = file("report_page_urls.txt", 'a')
    for page_number in range(173, 579):
        top_page_url = top_page_url_base + str(page_number)
        try:
            res = requests.get(top_page_url, headers=HEADERS)
        except:
            time.sleep(300)
            logger.warn("Exception! Sleep 300s")
            time.sleep(300)

        if res.status.code != 200:
            logger.warn("Banned. Sleep 300s")
            time.sleep(300)

        logger.warn("Crawling top page url "+top_page_url)
        soup = BeautifulSoup(res.text)
        logger.warn("First item on this page is "+str(soup.findAll('div', attrs={"class":"m_table_tit"})[2]))
        logger.warn("Code = "+str(res.status.code))


        for ele in soup.findAll(href=re.compile("show\?rid")):
            _url = each_page_base + ele['href']
            output_file.write(_url + '\n')
        time.sleep(random.randint(1,5))
        logger.warn("Sleeping...")


if __name__ == '__main__':
    iterate_pages()
