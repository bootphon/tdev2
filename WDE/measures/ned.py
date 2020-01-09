





import numpy as np
import editdistance 

from .measures import Measure
from itertools import combinations






class ned(Measure):
    def __init__(self, disc):
        self.metric_name = "ned"
        self.disc = disc.clusters
    
        # measures
        self.ned = None
    
    @staticmethod
    def pairwise_ned(s1, s2):
        return float(editdistance.eval(s1, s2)) / max(len(s1), len(s2))

    def compute_ned(self):
        overall_ned = []

        for class_nb in self.disc:
            for discovered1, discovered2 in combinations(self.disc[class_nb], 2):
                fname1, disc_on1, disc_off1, token_ngram1, ngram1 = discovered1
                fname2, disc_on2, disc_off2, token_ngram2, ngram2 = discovered2
                
                pair_ned = self.pairwise_ned(ngram1, ngram2)
                overall_ned.append(pair_ned)
        self.ned = np.mean(overall_ned)
