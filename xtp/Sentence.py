name = ['ID',
        'FORM',
        'LEMMA',
        'CPOSTAG',
        'POSTAG',
        'FEATS',
        'HEAD',
        'DEPREL',
        'PHEAD',
        'PDEPREL']

from xtp.Word import Word


class Sentence:
    def __init__(self, s):
        self.words = []
        for i, item in enumerate(s.split('\n')):
            if item == '': continue
            t = Word(item)
            self.words.append(t)

    def match(self, mss):
        result = []
        for mi, ms in enumerate(mss):
            for i in range(len(self.words) - len(ms)):
                for j, m in enumerate(ms):
                    if not self.words[i + j].match(m):
                        break
                    if j == len(ms) - 1:
                        result.append((mi, [self.words[i + t].FORM for t in range(len(ms))]))
        return result

    def match_test(self, rules):
        result = []
        for mi, rule in enumerate(rules):
            r = [i for i in rule(self)]
            if len(r)!=0:
                result.append((mi, r ))
        return (self.clear_str(),result)

    def str(self):
        return '#'.join([word.str() for word in self.words])

    def __str__(self):
        return '\n'.join(str(word) for word in self.words)

    def clear_str(self):
        return ' '.join([word.FORM for word in self.words])
