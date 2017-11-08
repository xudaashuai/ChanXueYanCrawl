from xtp import *
import pymongo

connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
comments = tdb.comment
ms = [
    {
        'POSTAG': 'n.?',
        'HEAD': '1'
    }, {
        'POSTAG': 'a.?'
    }
]

for i in range(100):
    for item in comments.find().limit(10).skip(i * 10):
        hanlp_result = item['hanlp_result']
        s = Sentence(hanlp_result)
        print(s.match(ms))
