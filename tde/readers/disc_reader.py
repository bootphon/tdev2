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

from tde.utils import check_boundary


class Disc():
    """ Read the discovered intervals

    Attributes
    ----------
    :param disc_path: Path to the 'Discovered" file, to be evaluated
    :param intervals: a list of all the discovered intervals
    :param intervals_tree: an interval tree containing all the discovered 
                           intervals
    :param clusters: a dictionary where all the keys are class numbers, and the
        values are all the intervals for that class


    Raises
    ------
    AssertionError 
        - if incorrect interval found (offset greater than onset)
        - if two classes have the same class number
    ValueError
        - if discovered file is not found
        - if discovered file is is wrong format
    """
    def __init__(self, disc_path=None, gold=None):

        if not os.path.isfile(disc_path):
            raise ValueError('{}: File Not Found'.format(disc_path))
        self.disc_path = disc_path
        self.clusters = None
        self.intervals = None
        if gold:
            self.gold_phn = gold.phones
        else:
            print("Warning: discovered file is read"
                  " without gold, so no transcription is given")
            self.gold_phn = None
        self.intervals_tree = None
        self.read_clusters()

    def __repr__(self):
        return '\n'.join(
           '{} {} {}'.format(fname, t0, t1)
           for (fname, t0, t1) in self.intervals)

    def read_clusters(self):
        """ Read discovered clusters
        
        Returns a dictionnary { class_number : [intervals_found]} that gives
        a list of the intervals for each class_number as key.
        The intervals are represented as a tuple:
            (fname: str, name of the speaker
            disc_on: float, onset of the interval
            disc_off: float, offset of the interval
            token_ngram: tuple, each discovered phone from the interval, with 
                         their onset and offsets,
            ngram: tuple, each)

        Raises
        ------
        AssertionError 
            - if incorrect interval found (offset greater than onset)
            - if two classes have the same class number
        ValueError
            - if a line is badly formated
        """
        classes = []
        discovered = dict()
        intervals = set()
        # file is decoded line by line and ned statistics are computed in
        # a streaming to avoid using a high amount of memory
        with open(self.disc_path) as fin:
            cfile = fin.readlines()

            # check that last line is empty
            assert cfile[-1] == '\n', ("discovered class file should end with"
                                     " and empty line")
            for lines in cfile:
                line = lines.strip()

                # check what type of line is being read, either it begins with
                # "Class", so it's the start of a new cluster or it contains an
                # interval, so add it to current cluster or it is empty, so the
                # previous cluster has been read entirely
                if line[:5] == 'Class':  # class + number + ngram if available
                    class_number = line.strip().split(' ')[1]
                elif len(line.split(' ')) == 3:
                    fname, start, end = line.split(' ')
                    disc_on, disc_off = float(start), float(end)

                    # check that timestamps are correct
                    assert disc_off > disc_on, ("timestamps are not"
                     " correct\n {} {} {}\n".format(fname, disc_on, disc_off))

                    # get the phone transcription for current interval
                    if self.gold_phn:
                        token_ngram, ngram = (self.get_transcription(
                         fname, disc_on, disc_off, self.gold_phn))

                        # throw away interval if outside of transcription
                        if len(token_ngram) == 0:
                            continue
                    else:
                        token_ngram, ngram = None, None

                    intervals.add(
                        (fname, disc_on, disc_off, token_ngram, ngram))
                    classes.append(
                        (fname, disc_on, disc_off, token_ngram, ngram))
                elif len(line) == 0:
                    # empty line means that the class has ended
                    # add class to discovered dict.
                    # if entry already exists, exit with an error
                    assert class_number not in discovered, (
                        "Two Classes have the same number {}"
                        " in discovered classes".format(class_number))
                    #assert len(classes) > 0, (
                    #        'class {} if empty'.format(class_number))
                    if len(classes) > 0:
                        discovered[class_number] = classes

                    # re-initialize classes
                    classes = list()
                else:
                    raise ValueError('Line in discovered classes has wrong'
                            ' format\n {}\n'.format(line))

        self.clusters = discovered
        self.intervals = list(intervals)

        print("Discovered Class file read\n")
        print("{} unique intervals found".format(len(self.intervals)))

    def read_intervals_tree(self):
        """ Read discovered intervals as interval tree"""
        self.intervals_tree = dict()
        for fname in self.intervals:
            self.intervals_tree[fname] = intervaltree.IntervalTree.from_tuples(
                self.intervals[fname])

    @staticmethod
    def get_transcription(fname, disc_on, disc_off, gold_phn):
        """ Given an interval, get its phone transcription

        Parameters
        ----------
        fname: str, name of the speaker on the interval
        disc_on: float, onset of the interval
        disc_off: float, offset of the interval
        gold_phn: intervaltree, contains the gold phones

        Returns
        -------
        token_ngram: list of tuples, list of all the 
                     (onset, offset, phone) covered by request interval
        ngram:       list, list of all the phones covered by request interval
        """
        # Get all covered phones
        covered = sorted(
            [phn for phn
             in gold_phn[fname].overlap(disc_on, disc_off)],
            key=lambda times: times[0])

        if len(covered) == 0:
            return tuple(), tuple()

        # Check if first and last phones are discovered
        #keep_first = check_boundary(
        #    (covered[0][0], covered[0][1]),
        #    (disc_on, covered[0][1]))

        #keep_last = check_boundary(
        #    (covered[-1][0], covered[-1][1]),
        #    (covered[-1][0], disc_off))

        keep_first = check_boundary(
            (covered[0][0], covered[0][1]),
            (disc_on, disc_off))

        keep_last = check_boundary(
            (covered[-1][0], covered[-1][1]),
            (disc_on, disc_off))

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

