from xtp.Word import Word
from xtp.Sentence import Sentence
import pymongo, re

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
comments = tdb.comments


def test_by_rule(test_num, rule, debug=True):
    page = 1000
    num = [0, 0, 0, test_num]
    for i in range(test_num // page):
        print(i,num)
        for k, item in enumerate(comments.find({'hanlp_result': {'$ne': None}}).limit(page).skip(i * page)):
            hanlp_result = item['hanlp_result']
            t = item
            s = Sentence(hanlp_result)
            item = s.match_test(rule)
            num[0]+=1
            for it in item[1]:
                num[-2]+=len(it[1])
            num[-3]+=len(item[1])!=0
            # print(num)
            # print('\t',item[0])
            for item in item[1]:
                # print('\t',item)
                for item in item[1]:
                    yield (*item,str(t['score']))
