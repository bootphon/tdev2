import numpy as np

#from joblib import Parallel, delayed
from .measures import Measure
from itertools import combinations
from collections import defaultdict, Counter
from tde.utils import overlap


class Grouping(Measure):
    """Grouping measure
    
    The grouping measures how pure the found clusters are, and
    is close to the 'purity' measure in clustering.
    See https://docs.syntheticlearner.net/tde/measures/index.html
    for a summary of all measures.

    .. note::
        The grouping computation requires to create the set of all "gold
        pairs" from the found pairs. This step is in "n choose 2" for each
        type found and take too much memory and cpu time.
        To fix this, we convert here all timestamps in seconds (in float),
        to timestamps in milliseconds (as integers), and manage dictionaries
        of integers.

    Input
    :param disc: Discovered Object, contains the discovered elements
    :param output_folder: string, path to the output folder
    :param njobs: Number of cpus to be used.

    Output
    :param precision: Grouping Precision
    :param recall: Grouping Recall

    """
    def __init__(self, disc, output_folder=None, njobs=1):
        print('inside grouping')
        self.metric_name = "grouping"
        self.output_folder = output_folder
        #self.clusters = disc.clusters
        # set timestamps as int in milliseconds
        self.clusters = dict()
        for key in disc.clusters:
            self.clusters[key] = [(fname, int(disc_on * 1000), int(disc_off * 1000),
              token_ngram, ngram) for fname, disc_on, disc_off, token_ngram, ngram in disc.clusters[key]]

        self.intervals = list()
        for fname, disc_on, disc_off, token_ngram, ngram in disc.intervals:
            self.intervals.append((fname, int(disc_on * 1000), int(disc_off * 1000), token_ngram, ngram))

        #self.intervals = disc.intervals
        self.njobs = njobs
        self.found_pairs = set()
        self.gold_pairs = set()
        self.found_types = set()
        self.gold_types = set()

    @property
    def precision(self):
        if len(self.found_types) == 0:
            prec = np.nan
        else:
            prec = sum(self.found_weights[t] * self.found_gold_counter[t]
                       / self.found_counter[t] for t in self.found_types)
        return prec

    @property
    def recall(self):
        if len(self.gold_types) == 0:
            rec = np.nan
        else:
            rec = sum(self.gold_weights[t] * self.found_gold_counter[t]
                      / self.gold_counter[t] for t in self.gold_types)
        return rec

    def get_gold_pairs(self):
        """ Get all the gold pairs that can be created using the
            discovered intervals.
            The pairs are ordered by filename and onset.

            Input
            :param intervals: a list of all the discovered intervals, with
                              their transcription
            Output
            :param gold_pairs: a set of all the gold pairs created from the
                               discovered intervals
            :param gold_types: all the types (n-gram) that occur in gold_pairs
        """
        print('testing with dict')
        same = defaultdict(set)
        same_int = dict()
        self.int_same = dict()
        same_int_idx = 0
        for fname, disc_on, disc_off, token_ngram, ngram in self.intervals:
            # ngram = tuple(ph for on, off, ph in token_ngram)
            #same[ngram].add((fname, disc_on, disc_off, token_ngram, ngram))
            if (fname, disc_on, disc_off, token_ngram, ngram) not in same_int:
                same_int[(fname, disc_on, disc_off, token_ngram, ngram)] = same_int_idx
                self.int_same[same_int_idx] = (fname, disc_on, disc_off, token_ngram, ngram)
                same_int_idx += 1
            same[ngram].add(same_int[(fname, disc_on, disc_off, token_ngram, ngram)])

        # add gold pair as tuple if both elements don't overlap

        #self.gold_pairs = {
        #    tuple(sorted((f1, f2), key=lambda f: (f[0], f[1])))
        #    for ngram in same
        #    for f1, f2 in combinations(same[ngram], 2)
        #    if not (f1[0] == f2[0]
        #            and overlap((f1[1], f1[2]),
        #                        (f2[1], f2[2]))[0] > 0)}
        self.gold_pairs = {
            tuple(sorted((f1, f2), key=lambda f: (self.int_same[f][0], self.int_same[f][1])))
            for ngram in same
            for f1, f2 in combinations(same[ngram], 2)
            if not (self.int_same[f1][0] == self.int_same[f2][0]
                    and overlap((self.int_same[f1][1], self.int_same[f1][2]),
                                (self.int_same[f2][1], self.int_same[f2][2]))[0] > 0)}


        self.gold_types = {self.int_same[f1][4] for f1, f2 in self.gold_pairs}
        # count occurences or each interval in pairs for frequency
        counter = Counter()
        seen_token = set()
        for f1, f2 in self.gold_pairs:
            if self.int_same[f1][3] not in seen_token:
                counter.update((self.int_same[f1][4],))
                # count token as seen
                seen_token.add(self.int_same[f1][3])
            if self.int_same[f2][3] not in seen_token:
                counter.update((self.int_same[f2][4],))
                seen_token.add(self.int_same[f2][3])

        weights = {ngram: counter[ngram]/len(seen_token) for ngram in counter}
        return weights, counter


    def get_found_pairs(self):
        """ Get all the pairs that were found.
            The pairs are ordered by filename and onset.

            Input
            :param clusters: a dict of all the clusters found. the keys
                             are the clusters names, the values are
                             a list of the intervals in this cluster
            Output
            :param found_pairs: a set of all the discovered pairs
        """
        for class_nb in self.clusters:
            self.found_pairs = self.found_pairs.union(
                set(combinations(self.clusters[class_nb], 2)))

            # count type only if clusters has two elements
            if len(self.clusters[class_nb]) > 1 :
                self.found_types = self.found_types.union(
                    {ngram for _, _, _, token_ngram, ngram
                    in self.clusters[class_nb]})

        # order found pairs
        self.found_pairs = {
            tuple(sorted((f1, f2), key=lambda f: (f[0], f[1])))
            for f1, f2 in self.found_pairs}

    @staticmethod
    def get_weights(pairs):
        """ For each type get its weight

            Input
            :params pairs:  a set containing pairs of intervals, stored
                            as (filename, onset, offset, token_ngram, ngram),
                            where token_ngram is the ngram with the timestamps
                            of each of its phone, and ngram is just a tuple of
                            all the phones
            Output
            :return:        weights, a dict that for each type (i.e. ngram)
                            gives its weight, which is computed as
                            number_of_tokens(ngram)/total_number_of_seen_tokens
                            counter, a dict that for each type (i.e. ngram)
                            gives the number of tokens of this ngram in the
                            pairs.
        """
        # count occurences or each interval in pairs for frequency
        counter = Counter()
        seen_token = set()
        for f1, f2 in pairs:
            if f1[3] not in seen_token:
                counter.update((f1[4],))
                # count token as seen
                seen_token.add(f1[3])
            if f2[3] not in seen_token:
                counter.update((f2[4],))
                seen_token.add(f2[3])

        weights = {ngram: counter[ngram]/len(seen_token) for ngram in counter}
        return weights, counter

    def compute_grouping(self):
        """ Compute the grouping by essentially counting the number of tokens
            of each type in three sets: the set of gold pairs, the set of
            found pairs, and the intersection of gold pairs and found pairs
        """
        self.gold_weights, self.gold_counter = self.get_gold_pairs()
        self.get_found_pairs()

        gold_found_pairs = self.found_pairs.intersection(self.gold_pairs)
        #self.gold_weights, self.gold_counter = self.get_weights(
        #    self.gold_pairs)
        ## get intersection of discovered pairs and gold pairs
        ## and count occurences and weights for gold pairs
        #gold_found_pairs, self.gold_counter, self.gold_weights = self.get_gold_pairs()

        # count occurences and weights for found pairs
        self.found_weights, self.found_counter = self.get_weights(
            self.found_pairs)

        # count occurences and weights for intersection of gold and 
        # found pairs
        _, self.found_gold_counter = self.get_weights(gold_found_pairs)

