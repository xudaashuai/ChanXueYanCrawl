import pymongo

cloud_conn = pymongo.MongoClient('101.236.6.203',27017)

local_conn = pymongo.MongoClient('localhost',27017)
i = 0
for item in local_conn.meituan.comments.find({'hanlp_result':{'$ne':None}}).limit(10000).skip(i):
    cloud_conn.data.comment.insert(item)
