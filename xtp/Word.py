name = 'ID   FORM    LEMMA   CPOSTAG POSTAG  FEATS   HEAD    DEPREL  PHEAD   PDEPREL'.split()
import re

class Word:
    def __init__(self, s):
        self.data = {}
        for i, item in enumerate(s.split()):
            self.data[name[i]] = item

    def match(self, m):
        for item in m:
            if item == 'HEAD':
                if int(self.HEAD) - int(self.ID) != int(m['HEAD']):
                    return False
                else:
                    continue
            if not re.match('^'+m[item]+'$', self.data[item]):
                return False
        return True

    def __getattr__(self, item):
        if item in name:
            return self.data[item]

    def __str__(self):
        return '\t'.join(self.data[i] for i in name)
