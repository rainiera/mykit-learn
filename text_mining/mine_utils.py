__author__ = 'rainierababao'


import re
import math
import warnings
import pandas as pd


def get_word_ctx(sentence, target=''):
    """Pops `target` from `sentence` and converts into a bag of words representing the context of `word`.
    """
    orig = [word for word in re.compile('\w+').findall(sentence)]
    if target not in orig:
        warnings.warn("Target wasn't in sentence.", RuntimeWarning)
    new = [word for word in orig if word != target]
    return new


def tf(vocab, bag):
    """tf(w) = num times word appear in a document / total num words in document
    """
    tf_dict = {}
    lenbag = len(bag)
    for word, count in vocab.iteritems():
        tf_dict[word] = count / float(lenbag)
    return tf_dict


def idf(docs):
    """idf(w) = log(num documents / num documents that contain w)
    """
    M = len(docs)
    idf_dict = dict.fromkeys(docs[0].keys(), 0)
    for doc in docs:
        for word, val in doc.iteritems():
            if val > 0:
                idf_dict[word] += 1
    for word, val in idf_dict.iteritems():
        idf_dict[word] = math.log((M + 1) / float(val))
    return idf_dict


def get_tfidf_matrix(tfidf_bag_a, tfidf_bag_b):
    return pd.DataFrame([tfidf_bag_a, tfidf_bag_b])


def compute_tf_idf(tf_bag, idfs):
    tfidf = {}
    for word, val in tf_bag.iteritems():
        tfidf[word] = val * idfs[word]
    return tfidf


def bm25(bag):
    pass
