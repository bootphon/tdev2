import os
import numpy as np
import editdistance
from .measures import Measure
from itertools import combinations


class Ned(Measure):
    """NED measure

    The NED (Normalized Edit Distance) measures how close each
    pair of word found is. For 1 pair of intervals found, a
    NED of 1 means all the phonemes are different, and a NED of 0 means
    they contain the exact same phonemes in the same order.
    See https://docs.cognitive-ml.fr/tde/measures/index.html
    for a summary of all measures.

    Input
    :param disc: Discovered Object, contains the discovered phonemes
    :param output_folder: string, path to the output folder

    Output
    :param coverage: NED
    """

    def __init__(self, disc, output_folder=None):
        self.metric_name = "ned"
        self.output_folder = output_folder
        self.disc = disc.clusters

        # measures
        self.n_pairs = None
        self.ned = None

    @staticmethod
    def pairwise_ned(s1, s2):
        s1 = tuple(phn for phn in s1 if phn != "SIL")
        s2 = tuple(phn for phn in s2 if phn != "SIL")
        if max(len(s1), len(s2)) > 0:
            return float(editdistance.eval(s1, s2)) / max(len(s1), len(s2))
        else:
            return 1.0

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

        # get number of pairs and ned value
        self.n_pairs = len(overall_ned)
        self.ned = np.mean(overall_ned)

    def write_score(self):
        if self.ned is None:
            raise AttributeError('Attempting to print scores but score'
                                 ' is not yet computed!')
        with open(os.path.join(self.output_folder, self.metric_name), 'w') as fout:
            fout.write("metric: {}\n".format(self.metric_name))
            fout.write("score: {}\n".format(self.ned))
