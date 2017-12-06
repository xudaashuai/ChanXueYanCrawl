from scrapy import Spider, Request
import pymongo
import json

from ltp.settings import *

api_url = "https://m.dianping.com/isoapi/module"

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


class MTSpider(Spider):
    name = 'DP'

    def start_requests(self):
        for i in range(0, 10000, 50):
            para = {"pageEnName": "shopList", "moduleInfoList": [{"moduleName": "mapiSearch", "query": {
                "search": {"start": i, "categoryid": 10, "locatecityid": 16, "limit": 1000, "sortid": "0", "cityid": 16,
                           "range": -1, "mylat": "30.5236555", "mylng": "114.3934311", "maptype": 0},
                "loaders": ["list"]}}]}
            # print(i)
            yield Request(api_url, method="POST", headers=headers, body=json.dumps(para), cookies=cookies, meta=para)

    def make_requests_from_url(self, url):
        # print(url)
        return Request(api_url.format(url))

    def parse(self, response):
        # print(response.body_as_unicode())
        result = json.loads(response.body_as_unicode())
        # print(result)
        try:
            t = result['data']['moduleInfoList'][0]['moduleData']['data']['listData']['list']
        except:
            return
        print(response.meta['moduleInfoList'][0]['query']['search']['start'], t.__len__())

        for item in t:
            item['_id'] = str(item['id'])
            tdb.dianping_poi.update({'_id': str(item['id'])}, item, True)
            para = {"pageEnName": "shopreviewlist", "moduleInfoList": [{"moduleName": "reviewlist",
                                                                        "query": {"shopId": item['_id'], "page": 1,
                                                                                  "type": 1,
                                                                                  "keyword": "全部"}},
                                                                       ]}
            yield Request(api_url, callback=self.parse_comment, method="POST", headers=headers, body=json.dumps(para),
                          cookies=cookies, meta=para)

    def parse_comment(self, response):
        j = json.loads(response.body_as_unicode())
        data = j['data']['moduleInfoList'][0]['moduleData']['data']
        para = response.meta
        if data['hasNextPage']:
            para['moduleInfoList'][0]['query']['page'] += 1
            yield Request(api_url, callback=self.parse_comment, method="POST", headers=headers, body=json.dumps(para),
                          cookies=cookies, meta=para)
        for item in data['reviewList']:
            item['_id'] = str(item['reviewId'])
            tdb.dianping_comment.update({'_id': str(item['reviewId'])}, item, True)
