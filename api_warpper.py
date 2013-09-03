import logging

__author__ = 'eddiexie'
import random
import time
import credential
from weibo import Client
logging.basicConfig(filename = "./API.log",
                    level=logging.DEBUG,format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s ')

class API():
    def __init__(self):
        self.tokens = credential.tokens
        self.api_keys = credential.api_keys
        self.api_secrest = credential.api_secrest
        self.authorazation_url = "http://www.rutgers.edu"
        self.clients = []
        for i in range(len(self.tokens)):
            logging.debug("Connecting to api number %d"%(i))
            c = Client(self.api_keys[i],
                       self.api_secrest[i],
                       self.authorazation_url, self.tokens[i])
            self.clients.append(c)

    def get_api(self):
        index = random.randint(0, len(self.clients) - 1)
        while True:
            remaining_hits = self.clients[index].get("account/rate_limit_status")['remaining_user_hits']
            if remaining_hits <= 10:
                logging.debug("Remain API = %d for index %d. Wait..."%(remaining_hits, index))
                time.sleep(5)
                continue
            logging.debug("Using API index %d, remains = %d"%(index, remaining_hits))
            return self.clients[index]
