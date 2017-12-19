from scrapy import Spider, Request
import pymongo
import json,re
from aip import AipNlp

from ltp.settings import tdb

""" 你的 APPID AK SK """
APP_ID = '10209496'
API_KEY = 'MrUvMIK1x0kI2wsxZ5wrxZuU'
SECRET_KEY = 'at8ObT3K6ruzgB4tg2TIz9Tb8visZkY8'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
api_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag'
t = 0
d = {'success': 0, 'error': 0}
while True:
    t +=1
    for i,item in enumerate(tdb.meituan_comment.find({'baidu_result': None}).skip(t*1000).limit(1000)):
        try:
            it = client.commentTag(item['text'])
        except Exception as e:
            d['error']+=1
            tdb.meituan_comment.update(item, {"$set": {"baidu_result": 'error'}})
            continue

        if 'error_code' in it:
            if it['error_code'] == 19:
                exit(0)
            if it['error_msg'] not in d:
                d[it['error_msg']]=0
            d[it['error_msg']]+=1
        else:
            d['success']+=1
        if i%100==0:
            print(d)

        tdb.meituan_comment.update(item, {"$set": {"baidu_result": [(ite['prop'],ite['adj']) for ite in it.get('items',[])]}})

