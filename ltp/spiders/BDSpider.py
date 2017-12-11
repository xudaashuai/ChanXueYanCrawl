from scrapy import Spider, Request
import pymongo
import json
from aip import AipNlp

from ltp.settings import tdb
""" 你的 APPID AK SK """
APP_ID = '10209496'
API_KEY = 'MrUvMIK1x0kI2wsxZ5wrxZuU'
SECRET_KEY = 'at8ObT3K6ruzgB4tg2TIz9Tb8visZkY8'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
api_url='https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag'

class BDSpider(Spider):
    name = 'BD'

    def start_requests(self):
        comments = tdb.meituan_comment.find({'baidu_result': None})
        for item in comments:
            yield Request(url=api_url,method='POST',body={
                "text": "三星电脑电池不给力",
                "type": 13
            })



