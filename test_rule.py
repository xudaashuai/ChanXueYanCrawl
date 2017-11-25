from xtp import *

t = open('1.txt', 'w+', encoding='utf-8')


def rule1(sentence):
    t.write(sentence.__str__())
    t.write('\n\n')
    t.flush()
    for word in sentence.words:
        adv = ''
        if word.CPOSTAG[0] == 'n' and word.DEPREL == 'SBV' or word.DEPREL == '主谓关系':
            adj = sentence.words[int(word.HEAD) - 1]
            if 'a' in adj.CPOSTAG:
                for word2 in sentence.words:
                    if word2.HEAD == adj.ID and (word2.DEPREL == '状中结构' or word2.DEPREL == 'ADV' ) and 'd' in word2.CPOSTAG.lower():
                        adv = word2.FORM
                yield (word.FORM, adv, adj.FORM)

with open('res2.txt', 'w+', encoding='utf-8') as f:
    for item in test_by_rule(100000, [rule1], attr='hanlp_crf_result',db='comment_t'):
        f.write(str('-'.join(item)))
        f.write('\n')
t.close()
