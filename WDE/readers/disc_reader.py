#!/usr/bin/env python
"""handles reading of discovered elements from a Term Discovery system output

Discovered object contains dictionnary of clusters with all the intervals (for
ned and grouping), and list of all the found intervals (cov, token, type,
boundary)

class file format is:

    Class 1:
    wav1 on1 off1
    wav2 on2 off2


:class: `Disc` represents all the discovered intervals.

The discovered elements can be represented in 3 ways, depending on the usage:
:param intervals: a list of all the discovered intervals
:param intervals_tree: an interval tree containing all the discovered intervals
:param clusters: a dictionary where all the keys are class numbers, and the
    values are all the intervals for that class

"""


import os
import codecs
import intervaltree

from WDE.utils import check_boundary


class Disc():
    def __init__(self, disc_path=None, gold=None):

        if not os.path.isfile(disc_path):
            raise ValueError('{}: File Not Found'.format(disc_path))
        self.disc_path = disc_path
        self.clusters = None
        self.intervals = None
        self.gold_phn = gold.phones
        # self.transcription = None
        self.intervals_tree = None
        # set intervals
        self.read_clusters()

    def __repr__(self):
        return '\n'.join(
           '{} {} {}'.format(fname, t0, t1)
           for (fname, t0, t1) in self.intervals)

    # def get_interval_transcription(self, fname, on, off):
    #    """ Return the transcription of an interval """

    #    #if (fname, on, off) not in self.intervals:
    #    #    raise ValueError('Requested interval not in discovered intervals')
    #    interval_trs = [ngram for fn, disc_on, disc_on, token_ngram, ngram
    #                          in self.intervals
    #                          if (fn == fname and disc_on == on
    #                              and disc_off == off)]
    #    if len(interval_trs) == 0:
    #        raise ValueError('Requested interval not in discovered intervals')

    #    return ' '.join(interval_trs)

    def read_clusters(self):
        """ Read discovered clusters """
        classes = []
        discovered = dict()
        intervals = set()
        # file is decoded line by line and ned statistics are computed in
        # a streaming to avoid using a high amount of memory
        with codecs.open(self.disc_path, encoding='utf8') as cfile:
            for lines in cfile:
                line = lines.strip()

                # check what type of line is being read, either it begins with
                # "Class", so it's the start of a new cluster or it contains an
                # interval, so add it to current cluster or it is empty, so the
                # previous cluster has been read entirely
                if line[:5] == 'Class':  # class + number + ngram if available
                    class_number = line.strip().split(' ')[1]
                    pass
                elif len(line.split(' ')) == 3:
                    fname, start, end = line.split(' ')
                    disc_on, disc_off = float(start), float(end)

                    # get the phone transcription for current interval
                    token_ngram, ngram = self.get_transcription(
                        fname, disc_on, disc_off, self.gold_phn)

                    intervals.add(
                        (fname, disc_on, disc_off, token_ngram, ngram))
                    classes.append(
                        (fname, disc_on, disc_off, token_ngram, ngram))
                elif len(line) == 0:
                    # empty line means that the class has ended
                    # add class to discovered dict.
                    # if entry already exists, exit with an error
                    assert class_number not in discovered, (
                        "Two Classes have the same name in discovered classes")
                    discovered[class_number] = classes

                    # re-initialize classes
                    classes = list()
                else:
                    print("Line in discovered classes has wrong format")
                    print("{}".format(line))

        self.clusters = discovered
        self.intervals = list(intervals)

        print("{} unique intervals".format(len(self.intervals)))

    def read_intervals_tree(self):
        """ Read discovered intervals as interval tree"""
        self.intervals_tree = dict()
        for fname in self.intervals:
            self.intervals_tree[fname] = intervaltree.IntervalTree.from_tuples(
                self.intervals[fname])

    @staticmethod
    def get_transcription(fname, disc_on, disc_off, gold_phn):
        """ Given an interval, get its phone transcription"""

        # Get all covered phones
        covered = sorted(
            [phn for phn
             in gold_phn[fname].overlap(disc_on, disc_off)],
            key=lambda times: times[0])

        # Check if first and last phones are discovered
        keep_first = check_boundary(
            (covered[0][0], covered[0][1]),
            (disc_on, covered[0][1]))
        keep_last = check_boundary(
            (covered[-1][0], covered[-1][1]),
            (covered[-1][0], disc_off))

        if keep_first:
            token_ngram = [
                (covered[0][0], covered[0][1], covered[0][2])]
            ngram = [covered[0][2]]
        else:
            token_ngram = []
            ngram = []

        token_ngram += [(on, off, phn) for on, off, phn in covered[1:-1]]
        ngram += [phn for on, off, phn in covered[1:-1]]

        if keep_last and len(covered) > 1:
            token_ngram += [
                (covered[-1][0], covered[-1][1], covered[-1][2])]
            ngram += [covered[-1][2]]

        return tuple(token_ngram), tuple(ngram)

    # def intervals2txt(self, gold_phn):
    #    """ For each interval, check which gold phones are covered
    #        and phonetically transcribe the intervals to phones.
    #    """

    #    token_ngram = []
    #    ngram = []
    #    intervals_transcription = []
    #    #ipdb.set_trace()
    #    #for fname, disc_on, disc_off in self.intervals:
    #    for class_nb in self.clusters:
    #        class_trs = []
    #        for fname, disc_on, disc_off in self.clusters[class_nb]:

    #            # Get all covered phones
    #            covered = sorted([phn  for phn
    #                                  in gold_phn[fname].overlap(disc_on, disc_off)],
    #                                  key=lambda times: times[0])
    #            # Check if first and last phones are discovered
    #            keep_first = check_boundary((covered[0][0], covered[0][1]),
    #                                      (disc_on, covered[0][1]))
    #            keep_last = check_boundary((covered[-1][0], covered[-1][1]),
    #                                      (covered[-1][0], disc_off))

    #            if keep_first:
    #                token_ngram = [(covered[0][0], covered[0][1],
    #                          covered[0][2])]
    #                ngram = [covered[0][2]]
    #            else:
    #                token_ngram = []
    #                ngram = []

    #            token_ngram += [ (on, off, phn) for on, off, phn in covered[1:-1]]
    #            ngram += [phn for on, off, phn in covered[1:-1]]

    #            if keep_last and len(covered) > 1:
    #                token_ngram += [(covered[-1][0], covered[-1][1],
    #                          covered[-1][2])]
    #                ngram += [covered[-1][2]]
    #            intervals_transcription.append((fname, disc_on, disc_off, tuple(token_ngram), tuple(ngram)))
    #            class_trs.append((fname, disc_on, disc_off, tuple(token_ngram), tuple(ngram)))
    #        self.clusters[class_nb] = class_trs
    #    self.transcription = intervals_transcription
