from scrapy import Spider, Request
import pymongo
import json

connection = pymongo.MongoClient('localhost', 27017)
tdb = connection.meituan
post = tdb.comments

api_url = "https://api.ltp-cloud.com/analysis/?" \
          "api_key=z1L4K6O9L74CBdFDLxsywSxSjLmwTfSxhdYqTgjc&" \
          "pattern=all&" \
          "text={0}&" \
          "format=json"
api_key = 'z1L4K6O9L74CBdFDLxsywSxSjLmwTfSxhdYqTgjc'

class LtpSpider(Spider):
    name = 'Ltp'

    def start_requests(self):
        result = post.find({'ltp_result': None})
        for i in result:
            # print(i)
            yield Request(api_url.format(i['text']), meta={'item': i})

    def make_requests_from_url(self, url):
        # print(url)
        return Request(api_url.format(url))

    def parse(self, response):
        # print(response)
        if response.status == 200:
            t = response.body_as_unicode()
            post.update_one(response.meta['item'], {'$set': {'ltp_result': t}})
        else:
            # print(result.content)
            post.update_one(response.meta['item'], {'$set': {'ltp_result': 'error'}})



"""
2017-11-03 22:56:38 [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (301) to 
<GET
 https://api.ltp-cloud.com/analysis/?api_key=z1L4K6O9L74CBdFDLxsywSxSjLmwTfSxhdYqTgjc&pattern=all&text=%E5%BE%88%E5%A5%BD%E5%90%83%EF%BC%8C%E4%B8%9C%E8%A5%BF%E4%B9%9F%E8%BF%98%E8%9B%AE%E5%A4%9A%E7%9A%84%EF%BC%8C%E5%B0%B1%E6%98%AF%E4%BA%BA%E6%9C%89%E7%82%B9%E5%A4%9A%E3%80%82&format=json> from
 http://api.ltp-cloud.com/analysis/?api_key=z1L4K6O9L74CBdFDLxsywSxSjLmwTfSxhdYqTgjc&pattern=all&text=%E5%BE%88%E5%A5%BD%E5%90%83%EF%BC%8C%E4%B8%9C%E8%A5%BF%E4%B9%9F%E8%BF%98%E8%9B%AE%E5%A4%9A%E7%9A%84%EF%BC%8C%E5%B0%B1%E6%98%AF%E4%BA%BA%E6%9C%89%E7%82%B9%E5%A4%9A%E3%80%82&format=json>
"""
