# -*- coding: utf-8 -*-

__author__ = 'eddiexie'

""" This py file is used to generate the data of all the spreader's geo distribution """

import os
import sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))


import utils
import random

from collections import Counter

from province_mapping import province


def print_counter(counter):
    for item in counter.items():
        if item[0] not in province.keys():
            continue
        print province[item[0]]+'\t'+str(item[1])



mongo_rumor_tweets = utils.MongoInterface('rumor_tweets')
mongo_random_tweets = utils.MongoInterface('random_tweets')

rumor_tweets = mongo_rumor_tweets.get_all_tweets()
random_tweets = mongo_random_tweets.get_all_tweets()

num = 100000
cnt = 0

prov_counter_in_rumor_tweet = Counter()
prov_counter_for_spreader = Counter()

prov_counter_for_normal_tweeter = Counter()

for tweet in rumor_tweets[:num]:
    location = tweet['user']['location']
    prov = location.split()[0]
    prov_counter_for_spreader[prov] += 1

    for key in province.keys():
        if tweet['text'].find(key) != -1:
            cnt += 1
            prov_counter_in_rumor_tweet[key] += 1

print_counter(prov_counter_for_spreader)
print '\n\n'
print_counter(prov_counter_in_rumor_tweet)


for tweet in random_tweets[:50000]:
    if random.random()<=0.1:
        location = tweet['user']['location']
        prov = location.split()[0]
        prov_counter_for_normal_tweeter[prov] += 1


prov_counter_for_normal_tweeter_dic = dict(prov_counter_for_normal_tweeter)
all_sum = sum([c for c in prov_counter_for_normal_tweeter_dic.values()])


prov_counter_for_spreader_dic = dict(prov_counter_for_spreader)
prov_counter_in_rumor_tweet_dic = dict(prov_counter_in_rumor_tweet)

for key in province.keys():
    normalized_value = prov_counter_for_spreader_dic[key]*1.0/(prov_counter_for_normal_tweeter_dic[key]*1.0/all_sum)
    prov_counter_for_spreader_dic[key] = normalized_value


print 'Normalized counter for provinces...'

print_counter(prov_counter_for_spreader_dic)