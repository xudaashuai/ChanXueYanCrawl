from ltp.settings import *
import jieba
with open('r.txt','w+',encoding='utf-8') as f:
        for i,item in enumerate(comment_collection.find({'baidu_result': {'$ne': None}})):
            if i%100==0:
                print(i)
            baidu_result = item['baidu_result']
            if baidu_result == 'error':
                continue
            for it in baidu_result:
                if len(it[1]) == 0:
                    it = [itt for itt in jieba.cut(it[0])]
                if len(it) != 2:
                    continue
                f.write('-'.join(it)+'-'+str(item['score']))
                f.write('\n')
            f.flush()
