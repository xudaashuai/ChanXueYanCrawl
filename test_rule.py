from xtp import *
import pymongo,re
connection = pymongo.MongoClient('101.236.6.203', 27017)
tdb = connection.data
comments = tdb.comments
ms = [[
    {
        'POSTAG': 'n.?',
        'HEAD': '1',
        'DEPREL':'主谓关系'
    }, {
        'POSTAG': 'a.?'
    }
],[
    {
        'POSTAG': 'n.?',
        'HEAD': '2',
        'DEPREL':'主谓关系'
    }, {
        'POSTAG': 'd.?'
    }, {
        'POSTAG': 'a.?'
    }
],[
{
        'POSTAG': 'n.?',
        'HEAD': '3',
        'DEPREL':'主谓关系'
    }, {
        'POSTAG': 'd.?'
    }, {
        'POSTAG': 'd.?'
    }, {
        'POSTAG': 'a.?'
    }
]]

test_num = 10000
page = 10
num = 0

s = '([^ ^#]+) n.? \d+ 主谓关系(?:#([^ ]+) d.? \d+ [^#]+)*#([^ ]+) a.? [^ ]+ [^#]+'
r = re.compile(s)


for i in range(test_num//page):
    for k,item in enumerate(comments.find({'hanlp_result':{'$ne':None}}).limit(page).skip(i * page)):
        hanlp_result = item['hanlp_result']
        s = Sentence(hanlp_result)
        result = r.findall(s.str())
        num += len(result)!=0
        print(num,'/',i*page+k,'/',10000,)
        print(s.clear_str(),'\n',*result,*s.match(ms))
