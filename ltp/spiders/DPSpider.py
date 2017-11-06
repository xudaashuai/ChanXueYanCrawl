from scrapy import Spider, Request
import pymongo
import json

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
poi_collection = tdb.dianping_poi
comment_collection = tdb.dianping_comment

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
        for i in range(0, 7000, 40):
            para = {"pageEnName": "shopList", "moduleInfoList": [{"moduleName": "mapiSearch", "query": {
                "search": {"start": i, "categoryid": 10, "locatecityid": 16, "limit": 50, "sortid": "0", "cityid": 16,
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
        t = result['data']['moduleInfoList'][0]['moduleData']['data']['listData']['list']
        print(response.meta['moduleInfoList'][0]['query']['search']['start'], t.__len__())
        for item in t:
            para = {"uuid": "5fb22829-025e-930a-92ea-93d4c7e16bb7.1509959224", "platform": 3, "partner": 150,
                    "originUrl": "https://m.dianping.com/shop/92519558/review_all", "pageEnName": "shopreviewlist",
                    "moduleInfoList": [
                        {
                            "moduleName": "header",
                            "query": {
                                "shopId": str(item['id']), "pageDomain": "m.dianping.com",
                                "pageReferer": "https://m.dianping.com/shop/" + str(item[
                                                                                        'id']) + "?from=shoplist&shoplistqueryid=76cf01c2-b94d-4b39-a627-946e1fd31df7"
                            }
                        },
                        {
                            "moduleName": "reviewlist",
                            "query": {"shopId": str(item['id']), "page": 1, "type": 1, "attr": None,
                                      "hit": None,
                                      "keyword": "全部"}}, {"moduleName": "bottom-app",
                                                          "query": {"shopId": str(item['id']),
                                                                    "pageDomain": "m.dianping.com"},
                                                          "config": {"support_system": "all",
                                                                     "bottomapp_link_ios": "https://link.dianping.com/universal-link?originalUrl=https%3A%2F%2Fevt.dianping.com%2Fsynthesislink%2F10195.html%3FshopId%3D{shopId}&schema=dianping%3A%2F%2Fshopinfo%3Fid%3D{shopId}%26utm%3D@utm@",
                                                                     "bottomapp_utm": "ulink_reviewbutton",
                                                                     "setSyntheticalLink": "https://evt.dianping.com/synthesislink/10195.html",
                                                                     "setDownloadLink": "http://m.dianping.com/download/redirect?id=6922",
                                                                     "bottomapp_link_android": "https://evt.dianping.com/synthesislink/10195.html?shopId={shopId}",
                                                                     "pos": "bottom"}},
                        {"moduleName": "autoopenapp", "query": {}}]}
            item['_id'] = str(item['id'])
            poi_collection.update({'_id': str(item['id'])}, item, True)
            yield Request(api_url, callback=self.parse_comment, method="POST", headers=headers, body=json.dumps(para),
                          cookies=cookies, meta=para)

    def parse_comment(self, response):
        j = json.loads(response.body_as_unicode())
        data = j['data']['moduleInfoList'][1]['moduleData']['data']
        para = response.meta
        if data['hasNextPage']:
            para['moduleInfoList'][1]['query']['page']+=1
            yield Request(api_url, callback=self.parse_comment, method="POST", headers=headers, body=json.dumps(para),
                          cookies=cookies, meta=para)
        for item in data['reviewList']:
            item['_id'] = str(item['reviewId'])
            comment_collection.update({'_id': str(item['reviewId'])}, item, True)
