import numpy as np

from .measures import Measure

class Coverage(Measure):
    def __init__(self, gold, disc):
       
        #self.all_intervals = set()
        self.n_phones = 0
        for fname in gold.phones:
            self.n_phones += len(gold.phones[fname])
            #self.all_intervals = self.all_intervals.union(set((fname, on, off) for on, off, phn inf gold.phones[fname]))

        self.covered_phn = set((fname, phn_on, phn_off) for fname, disc_on, disc_off, ngram in disc.transcription for phn_on, phn_off, phn in ngram )
        self.coverage = 0
        
    def compute_cov(self):
        #for fname, phn_on, phn_off in self.covered_phn:
        #    if (fname, phn_on, phn_off) in self.all_intervals:
        #        self.all_intervals.remove((fname, phn_on, phn_off))
        self.coverage = len(self.covered_phn) / self.n_phones
        return self.coverage
