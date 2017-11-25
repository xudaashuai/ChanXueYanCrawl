from scrapy import Spider, Request
import pymongo
import json
from bs4 import BeautifulSoup
import math

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
poi_collection = tdb.meituan_poi
comment_collection = tdb.meituan_comment

shop_url = "http://meishi.meituan.com/i/api/channel/deal/list"
comment_url = "https://i.meituan.com/poi/{poi_id}/feedbacks/page_{page_num}"
comment_url_start = "https://i.meituan.com/poi/{poi_id}/feedbacks"

headers = {
    'Host': 'meishi.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
    'Content-Type': 'application/json'
}
referer = 'https://i.meituan.com/poi/{poi_id}/feedbacks'
comment_header = {
    'Host': 'i.meituan.com',
    'Referer': referer,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
cookies_str = """___rl__test__cookies=1509955890260;
 mtcdn=K; lsu=; _lxsdk=15f8cb3cb4fc8-06c3a0e6deea94-3f63450e-144000-15f8cb3cb4fc8; 
 rvct=57; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; 
 _lxsdk_cuid=15f90575b8cc8-0472c4ef1c013d-3f63450e-144000-15f90575b8dc8; 
 IJSESSIONID=qhl6fkbkj6j91tkkny4mk1pm0; 
 iuuid=A350FB1FAF048CDCC84D42357FA79A19A477717530339AAB8F17DDD57D4976E8; 
 webp=1; OUTFOX_SEARCH_USER_ID_NCOO=323071973.9155836; 
 _hc.v=1f801222-aa91-a94e-87ae-0a3306333dc4.1509955205; 
 pcstyle=1; __mta=247757368.1509955172389.1509955177836.1509955948840.3; 
 uuid=00f0b2fc6ed245308768.1509893578.1.0.0; 
 oc=MHknbbsCLzAJ6ZoqbP6s56Rl6WB5v0UewnHqmyd_H35ZH_AQt3dg1WWQ6joDj_vN_ClWCJD-GSg4S9WMGued""" + \
              """JAW3YwK1TeYWiiVzxe1ffq3yfkVUKH7Eeee2SiZ2c_Z9TKtpkCs_tlK42TrmluRe3QVYIlBFuM_OFoPdJxitfSM; 
 latlng=; __utma=74597006.64054930.1509956006.1509956006.1509956006.1; 
 __utmb=74597006.2.9.1509956008060; __utmc=74597006; 
 __utmz=74597006.1509956006.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); 
 i_extend=C_b1Gimthomepagecategory11H__a; ci=57; 
 cityname="%E6%AD%A6%E6%B1%89"; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; 
 client-id=7159301c-65ce-4121-98c5-032b0d11f725;
  __mta=50044569.1509955206118.1509955862707.1509956009745.4; 
  _lxsdk_s=15f90575b8e-1a4-ce4-77a%7C%7C30
"""
cookies = {}
for line in cookies_str.split(';'):
    # print line

    name, value = line.strip().split('=', 1)

    cookies[name] = value


class MTSpider(Spider):
    name = 'NM'

    def start_requests(self):
        i=0
        para = {
                'origina': 'https://chi.nuomi.com/gaiya/food/getInfo?type=31&cityId=400010000&location=0%2C0&fid=2093&pn=1&v=7.1.0&deviceType=1&compV=3.1.5&cuid=187bc228caeaacec4c0269ef5ea096a9&terminal=3&category=326&categoryName=%E7%BE%8E%E9%A3%9F&sub_category_id=0&area_type=0&parent_area_id=1&area_id=0',
                'type': 'get', 'extra': '{"compid":"cuisine-home"}'
            }
        # print(i)
        yield Request('https://m.nuomi.com/webapp/bnjs/request', method="POST", headers=headers, body=json.dumps(para),
                      meta=para)

    def make_requests_from_url(self, url):
        # print(url)
        return Request(shop_url.format(url))

    def parse(self, response):
        result = json.loads(response.body_as_unicode())
        print(result)

    def parse_comment(self, response):
        meta = response.meta
        # print(meta,response.url)
        t = BeautifulSoup(response.body_as_unicode(), "html.parser")
        if meta['page_num'] == 1:
            comment_count= int(t.find('span',{'class':'header-tab-count'}).text)
            for i in range(2,int(math.ceil(comment_count/15))):
                meta['page_num']=i
                yield Request(comment_url.format(**meta), callback=self.parse_comment, headers=comment_header,
                              cookies=cookies, meta=meta)
        comments = t.find_all('div', {'class': 'feedbackCard'})
        for item in comments:
            comment_item = {'username': item.find('weak', {'class': 'username'}).text,
                            'text': item.find('div', {'class': 'comment'}).text,
                            'time': item.find('weak', {'class': 'time'}).text.replace('\n',''),
                            'pic': ['http:' + span['data-src'] for span in
                                    item.findAll('span', {'class': 'pic-container imgbox'})], 'poi_id': meta['poi_id'],
                            'score': item.findAll('i', {'class': 'text-icon icon-star'}).__len__()}
            comment_item['_id'] = comment_item['username'] + comment_item['poi_id'] + comment_item['time']
            comment_collection.update({'_id': comment_item['_id']}, comment_item, True)