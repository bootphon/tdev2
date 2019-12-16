import os
import sys
import ipdb
import numpy as np

from .measures import Measure
from WDE.utils import overlap, check_boundary

class Boundary(Measure):
    def __init__(self, gold, disc):
        self.metric_name = "boundary"
        # get gold as interval trees
        self.gold_boundaries = gold.boundaries
        self.gold_wrd = gold.words
        assert type(self.gold_wrd) == dict, ("gold_phn should be a dict "
           "of intervaltree objects but is {} ".format(type(gold_wrd)))

        # get all discovered boundaries
        bounds = [(fname, ngram[0][0]) 
                for fname, _, _, ngram in disc.transcription]
        bounds += [(fname, ngram[-1][1]) 
                for fname, _, _, ngram in disc.transcription]
        self.disc = set(bounds)


        # measures
        self.boundaries = dict()
        self.n_correct_disc_boundary = 0
        self.n_all_disc_boundary = len(self.disc)
        self.n_gold_boundary = 0
        self.n_discovered_boundary = 0
        for fname in self.gold_boundaries:
            self.n_gold_boundary += len(self.gold_boundaries[fname])
            #self.n_all_disc_boundary += 2 * len(self.disc)


    @property
    def precision(self):
        """Return Token and Type precision"""
        # Token precision/recall
        if self.n_all_disc_boundary == 0:
            boundary_prec = np.nan
        else:
            boundary_prec = self.n_discovered_boundary / self.n_all_disc_boundary

        return boundary_prec

    @property
    def recall(self):
        """Return Token and Type recall"""
        if self.n_gold_boundary == 0:
            boundary_rec = np.nan
        else:
            boundary_rec = self.n_discovered_boundary / self.n_gold_boundary

        return boundary_rec

    #@property
    #def fscore(self):
    #    """Return Token and Type fscore"""
    #    assert self.token_prec, ("Attempting to compute token fscore"
    #            " when token precision is not computed yet.")
    #    assert self.token_rec, ("Attempting to compute token fscore"
    #            " when token recall is not computed yet.")
    #    self.token_fscore = 2 * (self.token_prec * self.token_rec) / (self.token_prec + self.token_rec)
    #    self.type_fscore = 2 * (self.type_prec * self.type_rec) / (self.type_prec + self.type_rec)
    #    return self.token_fscore, self.type_fscore


    def compute_boundary(self):
        """Create intervaltree containing only boundary phones"""
        for fname, disc_time in self.disc:
            if fname not in self.gold_boundaries:
                raise ValueError('{}: file not found in gold'.format(fname))

            if disc_time in self.gold_boundaries[fname]:
                self.n_discovered_boundary += 1
            #if (len(ngram) > 1 
            #and (ngram[-1][1], ngram[-1][2]) in self.gold_boundaries[fname]):
            #    self.n_discovered_boundary += 1



    def compute_boundary_score(self):
        """Count how many unique boundaries were discovered"""


