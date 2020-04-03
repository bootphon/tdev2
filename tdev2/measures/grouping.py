import numpy as np

from joblib import Parallel, delayed
from .measures import Measure
from itertools import combinations
from collections import defaultdict, Counter
from tdev2.utils import overlap


class Grouping(Measure):
    def __init__(self, disc, output_folder=None, njobs=1):
        self.metric_name = "grouping"
        self.output_folder = output_folder
        self.clusters = disc.clusters
        self.intervals = disc.intervals
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
        counter = Counter()
        gold_found_pairs = set()

        def _ngram_pairs(pair):
            # check if a pair should be kept as gold
            # and if it intersects with discovered pairs
            f1, f2 = pair

            # check if should be kept
            if (f1[0] == f2[0] and overlap((f1[1], f1[2]),
                                           (f2[1], f2[2]))[0] > 0):
                return (None, False)

            # check if discovered
            if (f1, f2) in self.found_pairs:
                intersection = True
            else:
                intersection = False

            return ((f1, f2), intersection)

        # get all discovered intervals
        same = defaultdict(set)
        for fname, disc_on, disc_off, token_ngram, ngram in self.intervals:
            # ngram = tuple(ph for on, off, ph in token_ngram)
            same[ngram].add((fname, disc_on, disc_off, token_ngram, ngram))
        # get all gold pairs
        seen_token = set()

        # parallelize over all possible pairs
        for ngram in same: 
            _gold_pairs_found = Parallel(n_jobs=self.njobs, backend="threading")(
                delayed(_ngram_pairs)(sorted((f1, f2),
                                    key=lambda f: (f[0], f[1])))
                                   for f1, f2 in combinations(same[ngram], 2))

            _gold_pairs = {pair for pair, found in _gold_pairs_found if pair is not None}
            if len(_gold_pairs) > 0: 
                self.gold_types.add(ngram)
            _intersection = {pair for pair, found in _gold_pairs_found if found == True}
            gold_found_pairs = gold_found_pairs.union(_intersection)

            # update counters
            for f1, f2 in _gold_pairs:
                if f1[3] not in seen_token:
                    counter.update((f1[4],))
                    # count token as seen
                    seen_token.add(f1[3])
                if f2[3] not in seen_token:
                    counter.update((f2[4],))
                    seen_token.add(f2[3])

        # compute weights for each n gram
        weights = {ngram: counter[ngram]/len(seen_token) for ngram in counter}
           
        return gold_found_pairs, counter, weights

    #def get_gold_pairs_buggy(self):
    #    """ Get all the gold pairs that can be created using the
    #        discovered intervals.
    #        The pairs are ordered by filename and onset.

    #        Input
    #        :param intervals: a list of all the discovered intervals, with
    #                          their transcription
    #        Output
    #        :param gold_pairs: a set of all the gold pairs created from the
    #                           discovered intervals
    #        :param gold_types: all the types (n-gram) that occur in gold_pairs
    #    """
    #    def _ngram_pairs(ngram_list):
    #        ngram_pairs = [tuple(sorted((f1, f2), key= lambda f:(f[0], f[1])))
    #                       for f1, f2 in combinations(ngram_list, 2)
    #                       if not (f1[0] == f2[0]
    #                               and overlap((f1[1], f1[2]),
    #                                           (f2[1], f2[2]))[0] > 0)]
    #        return ngram_pairs

    #    same = defaultdict(set)
    #    for fname, disc_on, disc_off, token_ngram, ngram in self.intervals:
    #        # ngram = tuple(ph for on, off, ph in token_ngram)
    #        same[ngram].add((fname, disc_on, disc_off, token_ngram, ngram))

    #    # add gold pair as tuple if both elements don't overlap
    #    gold_pairs = {
    #        tuple(sorted((f1, f2), key=lambda f: (f[0], f[1])))
    #        for ngram in same
    #        for f1, f2 in combinations(same[ngram], 2)
    #        if not (f1[0] == f2[0]
    #                and overlap((f1[1], f1[2]),
    #                            (f2[1], f2[2]))[0] > 0)}
    #    #gold_pairs = Parallel(n_jobs=15)(delayed(_ngram_pairs)(same[ngram]) for ngram in same)
    #    gold_types = {f1[4] for f1, f2 in self.gold_pairs}
    #    return gold_pairs, gold_types

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
        # get discovered pairs
        self.get_found_pairs()

        # get intersection of discovered pairs and gold pairs
        # and count occurences and weights for gold pairs
        gold_found_pairs, self.gold_counter, self.gold_weights = self.get_gold_pairs()

        # count occurences and weights for found pairs
        self.found_weights, self.found_counter = self.get_weights(
            self.found_pairs)

        # count occurences and weights for intersection of gold and 
        # found pairs
        _, self.found_gold_counter = self.get_weights(gold_found_pairs)

