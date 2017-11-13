from xtp import *
import pymongo, re,json

def rule1(sentence):
    for word in sentence.words:
        if word.DEPREL == '主谓关系':
            yield (word.FORM,sentence.words[int(word.HEAD)-1].FORM)

test_by_rule(1000,[rule1])