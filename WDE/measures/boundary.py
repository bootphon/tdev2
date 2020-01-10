import os
import sys
import ipdb
import numpy as np

from .measures import Measure
from collections import defaultdict
from WDE.utils import overlap, check_boundary

class Boundary(Measure):
    def __init__(self, gold, disc):
        self.metric_name = "boundary"
        # get gold as interval trees
        self.gold_boundaries_up = gold.boundaries[0]
        self.gold_boundaries_down = gold.boundaries[1]
        self.gold_wrd = gold.words
        assert type(self.gold_wrd) == dict, ("gold_phn should be a dict "
           "of intervaltree objects but is {} ".format(type(gold_wrd)))

        # get all discovered boundaries
        bounds_down = [(fname, ngram[0][0]) 
                for fname, _, _, ngram,_ in disc.transcription]
        bounds_up = [(fname, ngram[-1][1]) 
                for fname, _, _, ngram,_ in disc.transcription]
        self.disc_down = set(bounds_down)
        self.disc_up = set(bounds_up).difference(
                set(bounds_up).intersection(self.disc_down))
        

        # measures
        self.boundaries = dict()
        self.boundaries_seen = set()
        self.n_correct_disc_boundary = 0

        self.n_all_disc_boundary = len(self.disc_up) + len(self.disc_down)
        self.n_gold_boundary = 0
        self.n_discovered_boundary = 0
        for fname in self.gold_boundaries_up:
            self.n_gold_boundary += len(self.gold_boundaries_up[fname])
            self.n_gold_boundary += len(self.gold_boundaries_down[fname])


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

    def compute_boundary(self):
        """ Create intervaltree containing only boundary phones.
            Here we discriminate upward and downward boundaries, 
            because if a word is followed by a silence, the upward 
            boundary should be counted if discovered as upward, but not
            if discovered as downward.
            
            Input
            :param disc_down:  a list of all the downward boundaries of 
                               discovered segments
            :param disc_up:    a list of all the upward boundaries of
                               discovered segments
            :gold_boundaries_down: a set of all the downward gold boundaries
            :gold_boundaries_up:   a set of all the upward gold boundaries
        """
        # downward boundaries
        for fname, disc_time in self.disc_down:
            if fname not in self.gold_boundaries_down:
                raise ValueError('{}: file not found in gold'.format(fname))

            if disc_time in self.gold_boundaries_down[fname]:
                self.n_discovered_boundary += 1

        # upward boundaries
        for fname, disc_time in self.disc_up:
            if fname not in self.gold_boundaries_up:
                raise ValueError('{}: file not found in gold'.format(fname))

            if (disc_time in self.gold_boundaries_up[fname]
                and not (fname, disc_time) in self.boundaries_seen):
                self.n_discovered_boundary += 1
                self.boundaries_seen.add((fname, disc_time))

