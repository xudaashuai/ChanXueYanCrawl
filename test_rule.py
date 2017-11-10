from xtp import *
import re
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


s = '([^ ^#]+) n.? \d+ 主谓关系(?:#([^ ]+) d.? \d+ [^#]+)*#([^ ]+) a.? [^ ]+ [^#]+'
r = re.compile(s)

test_by_dict(1000,ms,False)
