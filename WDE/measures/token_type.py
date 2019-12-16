import os
import sys
import ipdb
import numpy as np

from .measures import Measure
from WDE.utils import overlap, check_boundary

class TokenType(Measure):
    def __init__(self, gold_phn, gold_wrd, disc):
        self.metric_name = "token type"
        # get gold as interval trees
        self.gold_phn = gold_phn
        assert type(gold_phn) == dict, ("gold_phn should be a dict "
           "of intervaltree objects but is {} ".format(type(gold_phn)))
        self.gold_wrd = gold_wrd
        assert type(gold_wrd) == dict, ("gold_phn should be a dict "
           "of intervaltree objects but is {} ".format(type(gold_wrd)))
        self.all_type = set()
        self.n_token = 0
        for fname in self.gold_wrd:
            self.all_type.update(set([word for on, off, word 
                                   in self.gold_wrd[fname]]))
            self.n_token += len(self.gold_wrd[fname])
        self.n_type = len(self.all_type)

        # get discovered as list of intervals
        self.disc = disc

        # measures
        self.n_discovered_words = 0
        self.type_hit = set()
        self.token_hit = 0
        self.type_seen = set()
        self.token_seen = set()
        self.token_prec = None
        self.token_rec = None
        self.type_prec = None
        self.type_rec = None

    @property
    def precision(self):
        """Return Token and Type precision"""
        # Token precision/recall
        if len(self.disc) == 0:
            self.token_prec = np.nan
        else:
            self.token_prec = self.token_hit / len(self.disc)

        # Types precision/recall
        if len(self.type_seen) == 0:
            self.type_prec = np.nan
        else:
            self.type_prec = len(self.type_hit) / len(self.type_seen)

        return self.token_prec, self.type_prec

    @property
    def recall(self):
        """Return Token and Type recall"""
        if self.n_token == 0:
            self.token_rec = np.nan
        else:
            self.token_rec = self.token_hit / self.n_token
        # type recall
        if self.n_type == 0:
            self.type_rec = np.nan
        else:
            self.type_rec = len(self.type_hit) / self.n_type

        return self.token_rec, self.type_rec

    @property
    def fscore(self):
        """Return Token and Type fscore"""
        assert self.token_prec, ("Attempting to compute token fscore"
                " when token precision is not computed yet.")
        assert self.token_rec, ("Attempting to compute token fscore"
                " when token recall is not computed yet.")
        self.token_fscore = 2 * (self.token_prec * self.token_rec) / (self.token_prec + self.token_rec)
        self.type_fscore = 2 * (self.type_prec * self.type_rec) / (self.type_prec + self.type_rec)
        return self.token_fscore, self.type_fscore

    def compute_token_type(self):
        """ Loop over all intervals and compute token
            type measure.

            The Token measure is computed by 
            counting all the gold words discovered by the
            system. 
            The Type measure is computed by counting all 
            the unique type of gold words discovered by the 
            system.


            Input:
            :param gold_phn: the gold phone alignment
                             stored as an interval tree
            :type gold_phn:  Interval Tree
            :param gold_wrd: the gold word alignment
                             stored as an interval tree
            :type gold_wrd:  Interval Tree
            :param disc:     a list of all the discovered
                             intervals
            :type disc:      list of tuples
            Output:
            :return:         The Token Type measure
        """
        for fname, disc_on, disc_off, ngram in self.disc:
            if fname not in self.gold_wrd:
                raise ValueError('{}: file not found in gold'.format(fname))

            overlap_wrd = self.gold_wrd[fname].overlap(disc_on, disc_off)
           
            ngram = tuple(phn for _, _, phn in ngram)
            # get type by getting ngram covered
            self.type_seen.add(tuple(ngram))

            # switch cases.
            # if interval overlaps with less than 1 word
            # don't count
            # if overlapped word is not fully discovered, i.e. 
            # onset and offset are less than 30ms or 50% away
            # from border phone boundaries, then don't count
            if len(overlap_wrd) < 1:
                continue
            elif len(overlap_wrd) > 1:
                # choose word with the most overlap
                current_overlap = 0
                for wrd_on, wrd_off, wrd in overlap_wrd:
                    ov, _ = overlap((disc_on, disc_off), (wrd_on, wrd_off))
                    if ov > current_overlap:
                        current_overlap = ov
                        chosen = (wrd_on, wrd_off, wrd)

                overlap_wrd = chosen

            else:
                # Get word and add it to types seen (not necessarily hit)
                overlap_wrd = overlap_wrd.pop()
            gold_wrd_on, gold_wrd_off, gold_wrd_token = overlap_wrd
            gold_wrd_trs = sorted([phn for phn 
                              in self.gold_phn[fname].overlap(gold_wrd_on,
                                                              gold_wrd_off)])

            gold_wrd_trs = tuple([phn for phn_on, phn_off, phn 
                              in gold_wrd_trs])
            if ((gold_wrd_trs == ngram) and 
                not ((fname, gold_wrd_on, 
                      gold_wrd_off, gold_wrd_token) in self.token_seen)):
                self.token_hit +=1
                self.token_seen.add((fname, gold_wrd_on, 
                      gold_wrd_off, gold_wrd_token))

            if ((gold_wrd_trs == ngram) and 
                not ngram in self.type_hit):
                self.type_hit.add(ngram)

