import os
import sys
import ipdb
import numpy as np

from .measures import Measure
from itertools import combinations
from collections import defaultdict, Counter
from WDE.utils import overlap, check_boundary

class Grouping(Measure):
    def __init__(self, gold, disc):
        self.metric_name = "grouping"
        self.clusters = disc.clusters
        self.intervals = disc.transcription
        self.found_pairs = set()
        self.gold_pairs = set()
        self.found_types = set()
        self.gold_types = set()
        #self.

    def get_gold_pairs(self):
        """ given the intervals covered, get all the gold pairs"""
        same = defaultdict(set)
        for fname, disc_on, disc_off, token_ngram, ngram in self.intervals:
            #ngram = tuple(ph for on, off, ph in token_ngram)
            same[ngram].add((fname, disc_on, disc_off, token_ngram, ngram))
             
        # add gold pair if both elements don't overlap
        self.gold_pairs = { tuple(sorted((f1, f2), key = lambda f: (f[0], f[1]))) for ngram in same for f1, f2 in combinations(same[ngram], 2) if not (f1[0] == f2[0] and overlap((f1[1], f1[2]), (f2[1], f2[2]))[0] > 0)}
        self.gold_types = {f1[4] for f1, f2 in self.gold_pairs}

    def get_found_pairs(self):
        """ get all the pairs that were found """
        
        for class_nb in self.clusters:
            self.found_pairs = self.found_pairs.union(combinations(self.clusters[class_nb],2))
            self.found_types = self.found_types.union({ngram for _,_,_,token_ngram,ngram in self.clusters[class_nb]})
        # order found pairs
        self.found_pairs = {tuple(sorted((f1, f2), key = lambda f: (f[0], f[1]))) for f1, f2 in self.found_pairs}
        

    #def get_types(self, pairs):
    #    """ get all the types in a set of pairs and their weights"""

    #    pass

    def get_weights(self, pairs):
        """ for each type get its weight
        """
        # count occurences or each interval in pairs for frequency 
        counter = Counter()
        seen_token = set()
        for f1, f2 in pairs:
            if f1[3] not in seen_token:
                counter.update((f1[4],))
                # count token as seen
                seen_token.add(f1[3])
            if f2[4] != f1[4] and f2[3] not in seen_token:
                counter.update((f2[4],))
                seen_token.add(f2[3])
        
        #weights = {ngram: 1/counter[ngram] for ngram in counter}
        weights = {ngram: counter[ngram]/len(seen_token) for ngram in counter}
        return weights, counter

    def compute_grouping(self):
        self.get_gold_pairs()
        self.get_found_pairs()

        gold_found_pairs = self.found_pairs.intersection(self.gold_pairs)
        self.gold_weights, self.gold_counter = self.get_weights(self.gold_pairs)
        self.found_weights, self.found_counter = self.get_weights(self.found_pairs)
        _, self.found_gold_counter = self.get_weights(gold_found_pairs)


    def precision(self):
        if len(self.found_types) == 0:
            prec = np.nan
        else:
            prec = sum(self.found_weights[t] * self.found_gold_counter[t] / self.found_counter[t] for t in self.found_types)
        return prec

    def recall(self):
        if len(self.gold_types) == 0:
            rec = np.nan
        else:
            rec = sum(self.gold_weights[t] * self.found_gold_counter[t] / self.gold_counter[t] for t in self.gold_types)
        return rec
