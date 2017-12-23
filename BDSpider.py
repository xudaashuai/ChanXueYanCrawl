from scrapy import Spider, Request
import pymongo
import json, re
from aip import AipNlp

from ltp.settings import tdb

""" 你的 APPID AK SK """
APP_ID = '10209496'
API_KEY = 'MrUvMIK1x0kI2wsxZ5wrxZuU'
SECRET_KEY = 'at8ObT3K6ruzgB4tg2TIz9Tb8visZkY8'
keys = [
    ('10209496',
     'MrUvMIK1x0kI2wsxZ5wrxZuU',
     'at8ObT3K6ruzgB4tg2TIz9Tb8visZkY8'),
    ('10209495',
     'tLq4EO32EwjZVOtkZAeNY5nV',
     'OGxSBAWTlTv8Hhq83uLA70zCfkQUvh1V'),
    ('10209493',
     't1aFlIsV5FUwkvK1DY9gDbgr',
     '7kFLzCAqoZeb0mLqZwxSeiVag5E4guPF'),
    ('10029049', '4lqLUMNDQqcgw7yaS6SFiZ9G',
     'gk8pfmwGYWQ1meS4E92NtoGS91IuW8Xq'),
    ('10029045',
     'qO5PCgQIXr6H7PGPuMlPxRM2',
     'Wb5GrF8sqAYx7mAWBTAMNElLLSM1bQw1'),
    '10207132 jpmBMNurABuj8Vrxe9GS765S 2tu3zKmAOqXNK4bpBOFGGAb7T9ETlfRm'.split(),
    '10207130 Ts0GItUZOGIVSu8HAA1278zn dd8GU9Acam3Trc2N1RTA2RhHIBu6Xfco'.split(),
    '10207129 XHnLcvsF9ZUxLbEVLACNr56c HGlAg5xXEdGIGP6lPzjUgSIfRHYxC8jl'.split(),
    '10207128 gPfTmFqxtG1RVNG16qrTQSjP sNn6BpGPzByoIFg0CnRtG8V6qKPpR3xd'.split(),
    '9688683 wndZFKVBmUTM5cfMb7C8UaOA T80yWu0WAkbOFoKRVQ9p8lZMzj6rLq7S'.split(),

]
clients = [AipNlp(APP_ID, API_KEY, SECRET_KEY) for APP_ID, API_KEY, SECRET_KEY in keys]
api_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag'
t = 0
d = {'success': 0, 'error': 0}
clientID = 0
while True:
    t += 1
    clientID += 1
    clientID %= clients.__len__()
    for i, item in enumerate(tdb.meituan_comment.find({'baidu_result': None}).skip(t * 1000).limit(1000)):
        try:
            it = clients[clientID].commentTag(item['text'])
        except Exception as e:
            d['error'] += 1
            tdb.meituan_comment.update(item, {"$set": {"baidu_result": 'error'}})
            continue
        if 'error_code' in it:
            if it['error_code'] == 19:
                clients.pop(clientID)
            if it['error_msg'] not in d:
                d[it['error_msg']] = 0
            d[it['error_msg']] += 1
        else:
            d['success'] += 1
        if i % 100 == 0:
            print(d)
        tdb.meituan_comment.update(item, {
            "$set": {"baidu_result": [(ite['prop'], ite['adj']) for ite in it.get('items', [])]}})
