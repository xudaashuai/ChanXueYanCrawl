from xtp.Word import Word
from xtp.Sentence import Sentence
import pymongo, re

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data


def test_by_rule(test_num, rule, debug=True, attr='hanlp_result', db='comments'):
    comments = tdb[db]
    page = 1000
    num = [0, 0, 0, 0, 0, test_num]
    for i in range(test_num // page):
        for k, item in enumerate(comments.find({attr: {'$ne': None}}).limit(page).skip(i * page)):
            hanlp_result = item[attr]
            t = item

            s = Sentence(hanlp_result)
            item = s.match_test(rule)
            num[0] += 1
            for it in item[1]:
                num[1] += len(it[1])
            num[2] += len(item[1]) != 0
            # print(num)
            # print('\t',item[0])
            for item in item[1]:
                # print('\t',item)
                for item in item[1]:
                    yield (*item, str(t['score']))
                print(i, num, item, '1')

def save(test_num, debug=True, db='comments', save_maps=[]):
    comments = tdb[db]

    page = 1000
    files = [open(item[1],'w+',encoding='utf-8') for item in save_maps]
    for i in range(test_num // page):
        for k, item in enumerate(comments.find({'hanlp_result': {'$ne': None}}).limit(page).skip(i * page)):
            status = True
            for m in save_maps:
                if m[0] not in item:
                    status = False
            if not status:
                continue
            for i,file in enumerate(files):
                file.write(item[save_maps[i][0]])
                file.write('\n')
    for file in files:
        file.flush()
        file.close()
