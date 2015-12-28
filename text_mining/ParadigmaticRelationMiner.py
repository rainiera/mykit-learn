__author__ = 'rainierababao'

"""Simple implementation of paradigmatic relation discovery by converting bags of words
into vectors and computing their similarities.

Keywords: paradigmatic relation discovery, bag of words, vector-space model (VSM),
expected overlap of words in context (EOWC), term frequency inverse document frequency (tf-idf)
"""


from collections import Counter
import numpy as np
from mine_utils import get_word_ctx


class ParadigmaticRelationMiner():


    def __init__(self, docs=[]):
        """Initialize a paradigmatic relation miner with an empty collection of documents.
        """
        self.docs = docs


    def seed_example_set(self):
        """Seed this miner instance's docs with a dummy set.
        """
        self.docs.append('My cat eats fish on Saturday.')
        self.docs.append('My dog eats turkey on Tuesday.')


    def get_sim_eowc(self, b1, b2):
        """Accepts two bags of words and computes their similarity using
        expected overlap of words [in context] (EOWC).

        Pattern is to call `get_word_ctx(sentence, target)` on bag initialization
        and pass the bags into this method.

        Disadvantages:
        i) favors matching one frequent term very well over matching more distinct terms
        ii) treats every word equally (overlaps on stop words like `the` are not very meaningful)
        """
        shared_vocab = set(b1).intersection(set(b2))
        cx, cy = Counter(b1), Counter(b2)
        lenx, leny = len(b1), len(b2)
        d1, d2 = [], []
        for wi in shared_vocab:
            xi, yi = float(cx[wi])/lenx, float(cy[wi])/leny
            d1.append(xi)
            d2.append(yi)
        d1 = np.asarray(d1)
        d2 = np.asarray(d2)
        sim = np.dot(d1, d2)
        return sim


if __name__ == '__main__':
    """Example usage to mine paradigmatic relations from a dummy set,
    first using raw expected overlap of words in context, then tf-idf.
    """
    prm = ParadigmaticRelationMiner()
    prm.seed_example_set()
    print prm.docs
    b1 = get_word_ctx(prm.docs[0], 'cat')
    b2 = get_word_ctx(prm.docs[1], 'dog')
    print b1, b2
    print prm.get_sim_eowc(b1, b2)
