# -*- coding: utf-8 -*-
__author__ = 'eddiexie'

import codecs
from collections import Counter
import re

class LIWC():
    def __init__(self):
        '''Load dictory'''
        self._construct_category()
        self._read_mapping()

        #print self.mapping.keys()
    def analyze(self, text):
        LIWC_result = Counter()

        #print 'max = ', max(self.mapping.keys())
        text_length = len(text)

        for key in self.mapping.keys():
            pattern = re.compile(key)
            #print 'checking '+key
            for word in text:
                if len(word)<len(key):
                    continue
                result = re.findall(pattern, word)
                for index in self.mapping[key]:
                    LIWC_result[index] += len(result)

        for key in LIWC_result.keys():
            LIWC_result[key] = LIWC_result[key]*1.0/(text_length+1)
        #print LIWC_result.most_common(5)
        return LIWC_result

    def get_dominant(self, text, top_k):
        LIWC_result = self.analyze(text)

        idx = LIWC_result.most_common(top_k)
        ans = []
        for a, b in idx:
            ans.append(self.cate_dic[a])
        return ans

    def _read_mapping(self):
        lines = codecs.open('textmind.txt', 'r', 'utf-8').readlines()
        self.mapping = {}
        for line in lines:
            line = line.replace(u'*', u'')

            t = line.strip().split("	")
            self.mapping[t[0]] = []
            for v in t[1:]:
                self.mapping[t[0]].append(int(v))



    def get_catedic(self):
        return self.cate_dic


    def _construct_category(self):
        lines = """1	funct
2	pronoun
3	ppron
4	i
5	we
6	you
7	shehe
8	they
9	ipron
11	verb
12	auxverb
16	adverb
17	preps
18	conj
19	negate
20	quant
21	number
22	swear
31	youpl
32	PrepEnd
33	SpecArt
34	QuanUnit
35	Interjunction
36	MultiFun
41	TenseM
42	PastM
43	PresentM
44	FutureM
45	ProgM
121	social
122	family
123	friend
124	humans
125	affect
126	posemo
127	negemo
128	anx
129	anger
130	sad
131	cogmech
132	insight
133	cause
134	discrep
135	tentat
136	certain
137	inhib
138	incl
139	excl
140	percept
141	see
142	hear
143	feel
146	bio
147	body
148	health
149	sexual
150	ingest
250	relativ
251	motion
252	space
253	time
354	work
355	achieve
356	leisure
357	home
358	money
359	relig
360	death
462	assent
463	nonfl
464	filler"""
        self.cate_dic = {}
        for line in lines.split(u'\n'):
            tmp = line.strip().split(u'	')
            self.cate_dic[int(tmp[0])] = tmp[1]




#liwc = LIWC()
#liwc.analyze([u'今天', u'要', u'回家', u'上床睡觉', u'上床'])
#print liwc.get_dominant([u'今天', u'要', u'回家', u'上床睡觉', u'上床'], 15)