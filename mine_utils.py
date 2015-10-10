__author__ = 'rainierababao'

import re
import warnings

def get_word_ctx(sentence, target=''):
    """Pops `target` from `sentence` and converts into a bag of words representing the context of `word`.
    """
    orig = [word for word in re.compile('\w+').findall(sentence)]
    if target not in orig:
        warnings.warn("Target wasn't in sentence.", RuntimeWarning)
    new = [word for word in orig if word != target]
    return new

def tfidf(bag):
    pass

def bm25(bag):
    pass
