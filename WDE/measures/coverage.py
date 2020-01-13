import numpy as np

from .measures import Measure

class Coverage(Measure):
    def __init__(self, gold, disc):
        self.metric_name = "coverage" 
        #self.all_intervals = set()
        self.n_phones = 0
        for fname in gold.phones:
            ## TODO remove SIL here ? 
            self.n_phones += len([ph 
                for on, off, ph in gold.phones[fname]
                if (ph != "SIL" and ph != "SPN")])

        self.covered_phn = set((fname, phn_on, phn_off) 
                for fname, disc_on, disc_off, token_ngram, ngram
                    in disc.intervals
                for phn_on, phn_off, phn in token_ngram )
        self.coverage = 0
        
    def compute_cov(self):
        """ For coverage, simply compute the ratio of discovered phones over all phone
            
            Input:
            :param covered_phn:  a set containing all the covered phones

            Output:
            :param coverage:     the ratio of number of covered phones over 
                                 the overall number of phones in the corpus
        """
        self.coverage = len(self.covered_phn) / self.n_phones
