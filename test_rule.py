from xtp import *


def rule1(sentence):
    for word in sentence.words:
        adv = ''
        if word.DEPREL == '主谓关系':
            adj = sentence.words[int(word.HEAD) - 1]
            if 'a' in adj.CPOSTAG:
                for word2 in sentence.words:
                    if word2.HEAD == adj.ID and word2.DEPREL == '状中结构' and 'd' in word2.CPOSTAG:
                        adv = word2.FORM
                yield (word.FORM, adv, adj.FORM)


with open('res.txt','w+',encoding='utf-8') as f:
    for item in test_by_rule(1000, [rule1]):
        f.write(str('-'.join(item)))
        f.write('\n')
