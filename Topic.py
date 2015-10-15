__author__ = 'rainierababao'


from collections import defaultdict


class Topic():


    def __init__(self):
        self.dists = defaultdict(str)


    def add_dist(self, word, p):
        self.dists[word] = p


