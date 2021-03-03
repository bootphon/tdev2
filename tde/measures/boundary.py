import numpy as np
from .measures import Measure


class Boundary(Measure):
    """Boundary measure

    The boundary measures how many 'Gold' boundaries were found.
    See https://docs.cognitive-ml.fr/tde/measures/index.html for
    a summary of all measures.

    Input
    :param disc: Discovered Object, contains the discovered boundaries
    :param gold: Gold object, contains all the gold boundaries
    :param output_folder: string, path to the output folder

    Output
    :param precision: Boundary Precision
    :param recall: Boundary Recall
    """

    def __init__(self, gold, disc, output_folder=None):
        self.metric_name = "boundary"
        self.output_folder = output_folder

        # get gold as interval trees
        self.gold_boundaries_up = gold.boundaries[0]
        self.gold_boundaries_down = gold.boundaries[1]
        self.gold_wrd = gold.words
        assert type(self.gold_wrd) == dict, (
            "gold_phn should be a dict "
            "of intervaltree objects but is {} ".format(type(self.gold_wrd)))

        # get all discovered boundaries
        bounds_down = [(fname, ngram[0][0])
                       for fname, _, _, ngram, _ in disc.intervals
                       if len(ngram) > 0]
        bounds_up = [(fname, ngram[-1][1])
                     for fname, _, _, ngram, _ in disc.intervals
                     if len(ngram) > 0]
        self.disc_down = set(bounds_down)
        self.disc_up = set(bounds_up)

        # measures
        self.boundaries = dict()
        self.boundaries_seen = set()
        self.n_correct_disc_boundary = 0

        # if boundary is discovered as up and down, only count it once
        self.n_all_disc_boundary = len(self.disc_up.difference(
            self.disc_up.intersection(self.disc_down))) + len(self.disc_down)
        self.n_gold_boundary = 0
        self.n_discovered_boundary = 0
        for fname in self.gold_boundaries_up:
            self.n_gold_boundary += len(
               self.gold_boundaries_up[fname].difference(
                self.gold_boundaries_up[fname].intersection(
                 self.gold_boundaries_down[fname])))
            self.n_gold_boundary += len(self.gold_boundaries_down[fname])

    @property
    def precision(self):
        """Return Token and Type precision"""
        # Token precision/recall
        if self.n_all_disc_boundary == 0:
            boundary_prec = np.nan
        else:
            boundary_prec = (
                self.n_discovered_boundary / self.n_all_disc_boundary)

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

            if (
                    disc_time in self.gold_boundaries_down[fname]
                    and not (fname, disc_time) in self.boundaries_seen
            ):

                self.n_discovered_boundary += 1
                self.boundaries_seen.add((fname, disc_time))

        # upward boundaries
        for fname, disc_time in self.disc_up:
            if fname not in self.gold_boundaries_up:
                raise ValueError('{}: file not found in gold'.format(fname))

            if (
                    disc_time in self.gold_boundaries_up[fname]
                    and not (fname, disc_time) in self.boundaries_seen
            ):
                self.n_discovered_boundary += 1
                self.boundaries_seen.add((fname, disc_time))
