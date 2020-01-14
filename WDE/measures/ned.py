import os
import numpy as np
import editdistance

from .measures import Measure
from itertools import combinations


class Ned(Measure):
    def __init__(self, disc, output_folder=None):
        self.metric_name = "ned"
        self.output_folder = output_folder
        self.disc = disc.clusters

        # measures
        self.ned = None

    @staticmethod
    def pairwise_ned(s1, s2):
        return float(editdistance.eval(s1, s2)) / max(len(s1), len(s2))

    def compute_ned(self):
        """ compute edit distance over all discovered pairs and average across
            all pairs

            Input:
            :param disc:  a dictionnary containing all the discovered clusters.
                          Each key in the dict is a class, and its value is
                          all the intervals in this cluster.
            Output:
            :param ned:   the average edit distance of all the pairs
        """
        overall_ned = []

        for class_nb in self.disc:
            for discovered1, discovered2 in combinations(
                    self.disc[class_nb], 2):
                fname1, disc_on1, disc_off1, token_ngram1, ngram1 = discovered1
                fname2, disc_on2, disc_off2, token_ngram2, ngram2 = discovered2

                pair_ned = self.pairwise_ned(ngram1, ngram2)
                overall_ned.append(pair_ned)
        self.ned = np.mean(overall_ned)

    def write_score(self):
        if not self.ned:
            raise AttributeError('Attempting to print scores but score'
                                 ' is not yet computed!')
        with open(os.path.join(self.output_folder, self.metric_name), 'w') as fout:
            fout.write("metric: {}\n".format(self.metric_name))
            fout.write("score: {}\n".format(self.ned))
