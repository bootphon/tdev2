#!/usr/bin/env python
""" Gold object contains a vad, a word alignment and a phone alignmenet.
    Each alignement can be represented either as an interval tree or 
    a dictionnary, depending on the usage (interval tree is fast 
    for interval retrieval/ overal detection)
"""


import os
import sys
import ipdb
import argparse
import numpy as np
import pandas as pd
import intervaltree

from collections import defaultdict

class Gold():
    def __init__(self, vad_path=None, wrd_path=None, phn_path=None):
        """ Object representing the gold.
            Contains the VAD,the word alignement and the phone 
            alignment.
            The alignments can be stored as interval trees or as 
            dictionnaries.
            The interval tree of the silences can also be stored
        """
        self.vad_path = vad_path
        self.wrd_path = wrd_path
        self.phn_path = phn_path

    def read_gold_dict(self, gold_path):
        ''' 
        Read the gold phoneme file with fields : speaker/file start end annotation,
        returns a dict with the file/speaker as a key and the following structure
        
        gold['speaker'] = [{'start': list(...)}, {'end': list(...), 'symbol': list(...)}]
        '''
        if not os.path.isfile(gold_path):
            raise ValueError('{}: File Not Found'.format(gold_path))

        # Read phone alignment using pandas
        df = pd.read_table(gold_path, sep='\s+', header=None, encoding='utf8',
                names=['file', 'start', 'end', 'symbol'])
        
        # sort the data by file and onsets and round the onsets/offsets
        df = df.sort_values(by=['file', 'start'])
        df['start'] = df['start'].round(decimals=4)
        df['end'] = df['end'].round(decimals=4)
    
        # number of phones tokens in corpus
        number_read_symbols = len(df['symbol'])
    
        # get the lexicon and translate to as integers
        symbols = list(set(df['symbol']))
        symbol2ix = {v: k for k, v in enumerate(symbols)}
        ix2symbols = dict((v,k) for k,v in symbol2ix.items())
        df['symbol'] = df['symbol'].map(symbol2ix)
    
        # timestamps in gold (start, end) must be in acending order for fast search
        gold = {}
        verification_num_symbols = 0
        for k in df['file'].unique():
            start = df[df['file'] == k]['start'].values
            end = df[df['file'] == k]['end'].values
            symbols = df[df['file'] == k]['symbol'].values
    
            # check onsets/offsets are ordered
            #assert not any(np.greater_equal.outer(start[:-1] - start[1:], 0)), 'start in annotation file is not odered!!!'
            #assert not any(np.greater_equal.outer(end[:-1] - end[1:], 0)), 'end in annotation file is not odered!!!'
    
            gold[k] = {'start': list(start), 'end': list(end), 'symbol': list(symbols)} 
            verification_num_symbols += len(gold[k]['symbol'])
    
        #logging.debug("%d symbolss read from %s (%d returned)", number_read_symbols,
        #        gold_path, verification_num_symbols) 

        return gold, ix2symbols, symbols2ix
    
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
        symbols = list() # create a set of all the available symbols
        transcription = dict() # create dict that returns the transcription for an interval
        with open(gold_path, 'r') as fin:
            ali = fin.readlines()

            for line in ali:
                fname, on, off, symbol = line.strip('\n').split(' ')
                transcription[(fname, float(on), float(off))] = symbol
                symbols.append(symbol)
                intervals[fname].append((float(on), float(off), symbol))

            # for each filename, create an interval tree
            for fname in intervals:
                gold[fname] = intervaltree.IntervalTree.from_tuples(intervals[fname])

            # create a mapping index -> symbols for the phones
        symbol2ix = {v: k for k, v in enumerate(symbols)}
        ix2symbols = dict((v,k) for k,v in symbol2ix.items())

        return gold, transcription, ix2symbols, symbol2ix

    def get_intervals(fname, on, off, gold, transcription):
        """ Given a filename and an interval, retrieve the list of 
        covered intervals, and their transcription.
        This is done using intervaltree.search, which is supposed to 
        work in O(log(n) + m), n being the number of intervals and m 
        the number of covered intervals.
        """
        def overlap(a, b, interval):
            ov = (min(b, interval[1]) - max(a, interval[0]))\
                    /(interval[1] - interval[0])
            time = min(b, interval[1]) - max(a, interval[0])
            return ov, time
    
        # search interval tree
        _cov_int = gold[fname].overlap(on, off)
        cov_int = set() # set of kept intervals
        cov_trs = [] # retrieved transcription
    
        # check each interval to see if we keep it or not.
        # In particular, check if found interval contains
        # more than 30 ms or more than 50% of phone.
        for interval in _cov_int:
            int_ov, time = overlap(on, off, interval)
            if round(int_ov, 4) >= 0.50 or round(time,4) >= 0.03:
                cov_trs.append((interval[0], interval[1], transcription[(fname, interval[0], interval[1])]))
                cov_int.add((interval[0], interval[1]))
        
        # finally, sort the transcription by onsets, because intervaltree
        # doesn't necessarily return the intervals in order...
        cov_trs.sort()
        trs = [t for b, e, t in cov_trs]
    
        return cov_int, trs
    

    def get_silence_intervals(self, vad):
        ''' Compute interval tree of silences '''
        pass

    @staticmethod
    def check_phn_boundaries(gold_bg, gold_ed, gold, classes, elem):
        ''' check boundaries of discovered phone.
            If discovered "word" contains 50% of a phone, or more than
            30ms of a phone, we consider that phone discovered.
            INPUT
            gold_elem : tuplet, gold element (onset, offset, annotation)

            disc_elem : tuplet, discovered element (onset, offset, annotation)

            OUTPUT
            check: bool, true if gold element is discovered.
        '''
        # get discovered phones timestamps
        spkr, disc_bg, disc_ed = classes[elem]
        # get first phone timestamps
        first_ph_bg = gold[spkr]['start'][max(gold_bg-1,0)] # avoid taking last element if gold_bg = 0
        first_ph_ed = gold[spkr]['end'][max(gold_bg-1,0)] # avoid taking last element if gold_bg = 0
        first_ph_len = first_ph_ed - first_ph_bg
        first_ph_ov = float(first_ph_ed - disc_bg)/first_ph_len

        # get last phone timestamps
        last_ph_bg = gold[spkr]['start'][min(gold_ed,len(gold[spkr]['start'])-1)]
        last_ph_ed = gold[spkr]['end'][min(gold_ed,len(gold[spkr]['start'])-1)]
        last_ph_len = last_ph_ed - last_ph_bg
        last_ph_ov = float(disc_ed - last_ph_bg)/last_ph_len

        #ipdb.set_trace()
        # check overlap between first phone in transcription and discovered word
        # Bugfix : when reading alignments, pandas approximates float values
        # and it can lead to problems when th difference between the two compared 
        # values is EXACTLY 0.03, so we have to round the values to 0.0001 precision ! 
        if (round(first_ph_len,4) >= 0.060 and round((first_ph_ed - disc_bg),4) >= 0.030) or \
           (round(first_ph_len,4) < 0.060 and first_ph_ov >= 0.5) and \
           (gold_bg !=0 or disc_bg >first_ph_bg):
            # avoid substracting - 1 when already first phone in Gold
            first_ph_pos = gold_bg - 1 if gold_bg > 0 else 0 
            
        elif (gold_bg == 0 and disc_bg <= round(first_ph_bg,4)):
            first_ph_pos = gold_bg
        else:
            first_ph_pos = gold_bg
        
        # check overlap between last phone in transcription and discovered word
        # Bugfix : when reading alignments, pandas approximates float values
        # and it can lead to problems when th difference between the two compared 
        # values is EXACTLY 0.03, so we have to round the values to 0.0001 precision ! 
        if (round(last_ph_len,4) >= 0.060 and round((disc_ed - last_ph_bg),4) >= 0.030) or \
           (round(last_ph_len,4) < 0.060 and last_ph_ov >= 0.5):
            # avoid adding + 1 if already last phone in Gold
            last_ph_pos = gold_ed + 1 if gold_ed < len(gold[spkr]['end']) - 1  else gold_ed
        else:
            last_ph_pos = gold_ed
        return first_ph_pos, last_ph_pos

