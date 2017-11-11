from xtp.Word import Word
from xtp.Sentence import Sentence
import pymongo, re

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
comments = tdb.comments

def test_by_dict(test_num, rule, debug=True):
    page = 1000
    num = 0
    for i in range(test_num // page):
        for k, item in enumerate(comments.find({'hanlp_result': {'$ne': None}}).limit(page).skip(i * page)):
            hanlp_result = item['hanlp_result']
            s = Sentence(hanlp_result)
            result = s.match(rule)
            num += len(result) != 0
            if debug:
                print(num, '/', i * page + k + 1, '/', test_num)
                print('\t', s.clear_str())
                print('\t', *result)
            else:
                print(num, '/', i * page + k + 1, '/', test_num)
