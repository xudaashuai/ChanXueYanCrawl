import requests

from xtp import Sentence

url = "http://api.ltp-cloud.com/analysis/?api_key={api_key}&pattern={pattern}&text={text}&format={format}"
api_key = 'z1L4K6O9L74CBdFDLxsywSxSjLmwTfSxhdYqTgjc'
debug = True


def crawl(item):
    """
    爬取 item 中 文本的词性标注和 依存句法分析结果
    :param item:
    :return:
    """
    f = open('1.txt', 'w+',encoding='utf-8')
    args = {
        'api_key': api_key,
        'text': item,
        'pattern': 'all',
        'format': 'conll'
    }
    result = requests.get(url.format(**args))
    if result.status_code == 200:
        t = result.content.decode('utf-8')
        tt = []
        for i,line in enumerate(t.split('\n')):
            items = line.split()
            items[0] = str(i+1)
            items[6] = str(int(items[6])+1)
            tt .append( '\t'.join(items[:10]))

        tt='\n'.join(tt)
        s = Sentence(tt)
        print(s)
        f.write(tt)
        f.close()
        # post.update_one(item, {'$set': {'ltp_result': t}})
        # content = json.loads(result.content)
        # print(content)
        return 1
    else:
        print(result.content)
        return 0


crawl('感觉有些退步，可能主要是期待值过高')
"""
1	忠实	忠实	a	a	_	2	定中关系	_	_
2	粉丝	粉丝	n	nf	_	15	主谓关系	_	_
3	！	！	wp	w	_	2	标点符号	_	_
4	***	***	wp	w	_	2	标点符号	_	_
5	，	，	wp	w	_	2	标点符号	_	_
6	***	***	wp	w	_	2	标点符号	_	_
7	，	，	wp	w	_	2	标点符号	_	_
8	自	自	p	p	_	15	状中结构	_	_
9	***	***	wp	w	_	8	标点符号	_	_
10	金	金	b	b	_	12	定中关系	_	_
11	的	的	u	ude1	_	10	右附加关系	_	_
12	时候	时候	n	n	_	8	介宾关系	_	_
13	，	，	wp	w	_	12	标点符号	_	_
14	才	才	d	d	_	15	状中结构	_	_
15	知道	知道	v	v	_	0	核心关系	_	_
16	积分	积分	n	n	_	18	定中关系	_	_
17	的	的	u	ude1	_	16	右附加关系	_	_
18	重要	重要	a	a	_	15	动宾关系	_	_
19	。	。	wp	w	_	15	标点符号	_	_
20	***	***	wp	w	_	15	标点符号	_	_
21	了	了	u	ule	_	15	右附加关系	_	_
22	，	，	wp	w	_	15	标点符号	_	_
23	走到	走到	v	vf	_	15	并列关系	_	_
24	哪	哪	r	ry	_	23	动宾关系	_	_
25	，	，	wp	w	_	23	标点符号	_	_
26	复制到	复制到	v	v	_	23	并列关系	_	_
27	哪	哪	r	ry	_	26	动宾关系	_	_
28	，	，	wp	w	_	26	标点符号	_	_
29	***	***	wp	w	_	23	标点符号	_	_
30	，	，	wp	w	_	23	标点符号	_	_
31	还	还	d	d	_	33	状中结构	_	_
32	非常	非常	d	d	_	33	状中结构	_	_
33	省事	省事	a	a	_	23	并列关系	_	_
34	；	；	wp	w	_	33	标点符号	_	_
35	特别	特别	d	d	_	36	状中结构	_	_
36	是	是	v	vshi	_	40	定中关系	_	_
37	不用	不用	d	d	_	40	定中关系	_	_
38	认真	认真	a	ad	_	40	定中关系	_	_
39	的	的	u	ude1	_	38	右附加关系	_	_
40	评论	评论	n	n	_	23	并列关系	_	_
41	了	了	u	ule	_	40	右附加关系	_	_
42	，	，	wp	w	_	40	标点符号	_	_
43	又	又	d	d	_	44	状中结构	_	_
44	健康	健康	a	a	_	40	并列关系	_	_
45	快乐	快乐	a	a	_	44	并列关系	_	_
46	能	能	v	v	_	44	并列关系	_	_
47	么么哒	么么哒	nz	nz	_	46	动宾关系	_	_
48	。	。	wp	w	_	15	标点符号	_	_
49	不错	不错	a	a	_	15	并列关系	_	_
50	！	！	wp	w	_	15	标点符号	_	_
51	！	！	wp	w	_	15	标点符号	_	_
"""