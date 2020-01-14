#!/usr/bin/env python
"""Gold object contains a vad, a word alignment and a phone alignmenet

Each alignement can be represented either as an interval tree or a dictionnary,
depending on the usage (interval tree is fast for interval retrieval/ overal
detection)

"""

# TODO : ADD CHECK THAT ALIGNMENT CONTAINS NO SILENCES !!

import os
import pandas as pd
import intervaltree

from collections import defaultdict


class Gold():
    def __init__(self, vad_path=None, wrd_path=None, phn_path=None):
        """Object representing the gold.

        Contains the VAD,the word alignement and the phone alignment. The
        alignments can be stored as interval trees or as dictionnaries. The
        interval tree of the silences can also be stored.

        """
        # paths
        self.vad_path = vad_path
        self.wrd_path = wrd_path
        self.phn_path = phn_path

        # golds
        self.boundaries = None
        self.phones = None
        self.words = None

        # read alignments
        self.words, _, self.ix2wrd, self.wrd2ix, self.boundaries = (
            self.read_gold_intervalTree(self.wrd_path))

        if "SIL" in self.wrd2ix:
            print("WARNING: Word alignement contains silences, those will be counted as word by the evaluation.\n"
                  "You should keep them in the phone alignment but remove them from the word alignment.")

        self.phones, _, self.ix2phn, self.phn2ix, _ = (
            self.read_gold_intervalTree(self.phn_path))
        # self.boundaries = self.get_boundaries()

    # def get_boundaries(self):
    #    '''
    #    Get the gold boundaries by comparing phone and word alignments
    #    Return:
    #        :return: boundaries: dict, for each filename return a list
    #                             of tuples (lower boundary, upper boundary,
    #                                        lower phone, upper phone, word)
    #    '''
    #    if not os.path.isfile(self.phn_path):
    #        raise ValueError('{}: Phone Alignment Not Found'.format(self.phn_path))
    #    if not os.path.isfile(self.wrd_path):
    #        raise ValueError('{}: Word Alignment Not Found'.format(self.phn_path))

    #    # Read phone/word alignment using pandas
    #    phn = pd.read_table(self.phn_path, sep=' ', header=None, encoding='utf8',
    #            names=['file', 'start', 'end', 'symbol'])
    #    wrd = pd.read_table(self.phn_path, sep=' ', header=None, encoding='utf8',
    #            names=['file', 'start', 'end', 'symbol'])

    #    # get lower boundaries and upper boundaries by merging dataframes
    #    bound_low = pd.merge(phn, wrd, how='inner', on=['file', 'start'])
    #    bound_high = pd.merge(phn, wrd, how='inner', on=['file', 'end'])

    #    assert len(bound_low) == len(bound_high), ("phone and word alignement aren't"
    #            " correctly aligned, the timestamps should correspond for beginnings"
    #            " and endings of words")

    #    # output boundaries
    #    boundaries = dict()
    #    for fname in phn['file'].unique():
    #        lower = bound_low[bound_low['file'] == fname]['start'].values
    #        upper = bound_high[bound_high['file'] == fname]['end'].values
    #        #phn_low = bound_low[bound_low['file'] == fname]['symbol_x'].values
    #        #phn_up = bound_high[bound_high['file'] == fname]['symbol_x'].values
    #        #word = bound_low[bound_low['file'] == fname]['symbol_y'].values
    #        #boundaries[fname] = list(zip(lower,upper,phn_low, phn_up, word))
    #        boundaries[fname] = set(lower + upper)
    #    return boundaries

    def read_gold_dict(self, gold_path):
        """Read the gold phoneme file with fields: speaker/file start end annotation

        Returns a dict with the file/speaker as a key and the following
        structure:

        gold['speaker'] = [{'start': list(...)}, {'end': list(...), 'symbol': list(...)}]

        """
        if not os.path.isfile(gold_path):
            raise ValueError('{}: File Not Found'.format(gold_path))

        # Read phone alignment using pandas
        df = pd.read_table(
            gold_path, sep=' ', header=None, encoding='utf8',
            names=['file', 'start', 'end', 'symbol'])

        # sort the data by file and onsets and round the onsets/offsets
        df = df.sort_values(by=['file', 'start'])
        df['start'] = df['start'].round(decimals=4)
        df['end'] = df['end'].round(decimals=4)

        # # number of phones tokens in corpus
        # number_read_symbols = len(df['symbol'])

        # get the lexicon and translate to as integers
        symbols = list(set(df['symbol']))
        symbol2ix = {v: k for k, v in enumerate(symbols)}
        ix2symbols = dict((v, k) for k, v in symbol2ix.items())
        df['symbol'] = df['symbol'].map(symbol2ix)

        # timestamps in gold (start, end) must be in acending order for fast
        # search
        gold = {}
        verification_num_symbols = 0
        for k in df['file'].unique():
            start = df[df['file'] == k]['start'].values
            end = df[df['file'] == k]['end'].values
            symbols = df[df['file'] == k]['symbol'].values

            # check onsets/offsets are ordered
            # assert not any(np.greater_equal.outer(start[:-1] - start[1:], 0)), 'start in annotation file is not odered!!!'
            # assert not any(np.greater_equal.outer(end[:-1] - end[1:], 0)), 'end in annotation file is not odered!!!'

            gold[k] = {
                'start': list(start),
                'end': list(end),
                'symbol': list(symbols)}

            verification_num_symbols += len(gold[k]['symbol'])

        # logging.debug("%d symbolss read from %s (%d returned)", number_read_symbols,
        #         gold_path, verification_num_symbols)

        return gold, ix2symbols, symbol2ix

    def read_gold_intervalTree(self, gold_path):
        '''Read the gold alignment and build an interval tree (O( log(n) )).
        After that, take each found interval, search for its overlaps
        (O( log(n) + m), m being the number of results found),
        and check if we want to keep each interval.
        INPUT
        =====
        - phn_gold : the path to the gold alignment
        OUTPUT
        ======
        - gold: a dict {fname: intervaltree} which returns the interval tree
                of the gold phones for each file
        - ix2symbols: a dict that returns the symbols for each index of encoding
                      (to compute the ned, we assign numbers to symbols)
        '''
        if not os.path.isfile(gold_path):
            raise ValueError('{}: File Not Found'.format(gold_path))

        # read the gold and create a list of tuples for each filename, then create an interval
        # tree from this list of tuple.
        intervals = defaultdict(list)
        gold = dict()
        symbols = set() # create a set of all the available symbols
        transcription = dict() # create dict that returns the transcription for an interval
        boundaries_up = defaultdict(set)
        boundaries_down = defaultdict(set)

        with open(gold_path, 'r') as fin:
            ali = fin.readlines()

            for line in ali:
                try:
                    fname, on, off, symbol = line.strip('\n').split(' ')
                except:
                    raise ValueError(
                        'format of alignement should be:\n'
                        '\tfilename onset offset symbol\n'
                        'but alignment contains wrongly formated line:\n'
                        '{}'.format(line))
                transcription[(fname, float(on), float(off))] = symbol
                symbols.add(symbol)
                intervals[fname].append((float(on), float(off), symbol))
                boundaries_up[fname].add(float(off))
                boundaries_down[fname].add(float(on))

            # for each filename, create an interval tree
            for fname in intervals:
                gold[fname] = intervaltree.IntervalTree.from_tuples(
                    intervals[fname])

        # create a mapping index -> symbols for the phones
        symbol2ix = {v: k for k, v in enumerate(list(symbols))}
        ix2symbols = dict((v, k) for k, v in symbol2ix.items())

        # boundaries_down: contains all down boundaries,
        # boundaries_up: contains all up boundaries that do not already
        # occur un boundaries_down
        for fname in boundaries_up:
            boundaries_up[fname] = boundaries_up[fname].difference(
                    boundaries_up[fname].intersection(boundaries_down[fname]))

        return (gold, transcription, ix2symbols,
                symbol2ix, (boundaries_up, boundaries_down))

    def get_intervals(fname, on, off, gold, transcription):
        """ Given a filename and an interval, retrieve the list of
        covered intervals, and their transcription.
        This is done using intervaltree.search, which is supposed to
        work in O(log(n) + m), n being the number of intervals and m
        the number of covered intervals.
        """
        def overlap(a, b, interval):
            ov = (min(b, interval[1]) - max(a, interval[0])) \
                    / (interval[1] - interval[0])
            time = min(b, interval[1]) - max(a, interval[0])
            return ov, time

        # search interval tree
        _cov_int = gold[fname].overlap(on, off)
        cov_int = set()  # set of kept intervals
        cov_trs = []  # retrieved transcription

        # check each interval to see if we keep it or not.
        # In particular, check if found interval contains
        # more than 30 ms or more than 50% of phone.
        for interval in _cov_int:
            int_ov, time = overlap(on, off, interval)
            if round(int_ov, 4) >= 0.50 or round(time, 4) >= 0.03:
                cov_trs.append(
                    (interval[0], interval[1],
                     transcription[(fname, interval[0], interval[1])]))
                cov_int.add((interval[0], interval[1]))

        # finally, sort the transcription by onsets, because intervaltree
        # doesn't necessarily return the intervals in order...
        cov_trs.sort()
        trs = [t for b, e, t in cov_trs]

        return cov_int, trs

    def get_silence_intervals(self, vad):
        ''' Compute interval tree of silences '''
        pass
