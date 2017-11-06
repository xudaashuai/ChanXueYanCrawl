from scrapy import Spider, Request
import pymongo
import json

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
post = tdb.meituan_poi

shop_url = "http://meishi.meituan.com/i/api/channel/deal/list"
comment_url = "http://meishi.meituan.com/i/api/channel/deal/list"

headers = {
    'Host': 'meishi.meituan.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36',
    'Content-Type': 'application/json'
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
 oc=MHknbbsCLzAJ6ZoqbP6s56Rl6WB5v0UewnHqmyd_H35ZH_AQt3dg1WWQ6joDj_vN_ClWCJD-GSg4S9WMGued"""+\
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
cookies={}
for line in cookies_str.split(';'):
    # print line

    name, value = line.strip().split('=', 1)

    cookies[name] = value


class MTSpider(Spider):
    name = 'MT'

    def start_requests(self):
        for i in range(0,20000,49):
            para = {"offset": i, "limit": 50, "cateId": 1, "lineId": 0, "stationId": 0, "areaId": 0, "sort": "default",
                "deal_attr_23": "", "deal_attr_24": "", "deal_attr_25": "", "poi_attr_20043": "", "poi_attr_20033": ""}
        # print(i)
            yield Request(shop_url, method="POST", headers=headers, body=json.dumps(para), cookies=cookies, meta=para)

    def make_requests_from_url(self, url):
        # print(url)
        return Request(shop_url.format(url))

    def parse(self, response):
        result = json.loads(response.body_as_unicode())
        #print(result)
        print(response.meta['offset'],result['data']['poiList']['poiInfos'].__len__())
        for item in result['data']['poiList']['poiInfos']:
            item['_id']=str(item['poiid'])
            post.update({'_id':item['poiid']},item,True)



