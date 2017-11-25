from scrapy import Spider, Request
import pymongo
import json,re

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
poi_collection = tdb.dianping_poi
comment_collection = tdb.dianping_comment

api_url ="https://m.dianping.com/shop/{0}/map"
r = re.compile('"shopLat":([^,]+),"shopLng":([^,]+),')
headers = {
    'Host': 'm.dianping.com',
    'Origin': 'https://m.dianping.com',
    'Referer': 'https://m.dianping.com/shoplist/16/d/1/c/10/s/s_-1?from=m_nav_1_meishi',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
    'Content-Type': 'application/json'
}
cookies_str = """cy=16; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_cuid=15f90954844c8-064b2b34f04589-63181437-38400-15f90954844c8; _lxsdk=15f90954844c8-064b2b34f04589-63181437-38400-15f90954844c8; _hc.v=5fb22829-025e-930a-92ea-93d4c7e16bb7.1509959224; cityid=16; chwlsource=default; switchcityflashtoast=1; locallat=30.5236555; locallng=114.3934311; ___rl__test__cookies=1509959234062; OUTFOX_SEARCH_USER_ID_NCOO=2115534634.5516338; source=m_browser_test_33; pvhistory="6L+U5ZuePjo8L2dldGxvY2FsY2l0eWlkP2xhdD0zMC41MjM2NTU1JmxuZz0xMTQuMzkzNDMxMSZjb29yZFR5cGU9MSZjYWxsYmFjaz1XaGVyZUFtSTExNTA5OTU5MjM2NDA3Pjo8MTUwOTk1OTIzNjkzNl1fWw=="; m_flash2=1; msource=default; default_ab=index%3AA%3A1%7CshopList%3AA%3A1; _lxsdk_s=15f90954846-8a5-0e6-0e0%7C%7C13"""
cookies = {}
for line in cookies_str.split(';'):
    # print line

    name, value = line.strip().split('=', 1)

    cookies[name] = value

t =set()
t.add(1)
class MTSpider(Spider):
    name = 'DPP'

    def start_requests(self):
        for item in poi_collection.find():
            print(item)
            yield Request(api_url.format(item['_id']), method="GET", headers=headers, cookies=cookies, meta=item)

    def make_requests_from_url(self, url):
        # print(url)
        return Request(api_url.format(url))

    def parse(self, response):
        item = response.meta
        pos = r.findall(response.body_as_unicode())[0]
        item['pos']=pos
        poi_collection.update({'_id':item['_id']},item,False)
