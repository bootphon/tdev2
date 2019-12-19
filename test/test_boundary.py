
import os
import pytest
import numpy as np
import pkg_resources
import intervaltree as it

from collections import defaultdict
from WDE.measures.boundary import *
from WDE.readers.gold_reader import *
from WDE.readers.disc_reader import *
#from gold_reader import *
#from disc_reader import *

@pytest.fixture(scope='session')
def gold():
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.phn')

               
    return Gold(wrd_path=wrd_path,
                phn_path=phn_path)

@pytest.fixture(scope='session')
def disc(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/test_pairs')
    discovered = Disc(pairs_path)
    #discovered.read_clusters()
    discovered.intervals2txt(gold.phones)
    return discovered

@pytest.fixture(scope='session')
def disc_bigIntervals(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/bigger_interval.class')
    discovered = Disc(pairs_path)
    #discovered.read_clusters()
    discovered.intervals2txt(gold.phones)
    return discovered


def test_boundaries(gold):
    """
        Check that word boundaries are a subset of phone
        boundaries
    """
    _, _, _, _, phn_boundaries = gold.read_gold_intervalTree(gold.phn_path)
    _, _, _, _, wrd_boundaries = gold.read_gold_intervalTree(gold.wrd_path)

    all_phn_boundaries = defaultdict(set)
    all_wrd_boundaries = defaultdict(set)
    for fname in wrd_boundaries[0]:
        all_wrd_boundaries[fname] = wrd_boundaries[0][fname].union(wrd_boundaries[1][fname])
        all_phn_boundaries[fname] = phn_boundaries[0][fname].union(phn_boundaries[1][fname])

    for fname in all_wrd_boundaries:
        assert all_phn_boundaries[fname].intersection(all_wrd_boundaries[fname]) == all_wrd_boundaries[fname], ("boundaries"
         "are not the same in phone alignement and word alignement")
    #for fname in wrd_boundaries[1]:
    #    assert phn_boundaries[1][fname].intersection(wrd_boundaries[1][fname]) == wrd_boundaries[1][fname], ("boundaries"
    #     "are not the same in phone alignement and word alignement")


def test_big_intervals(gold, disc_bigIntervals):
     bound = Boundary(gold, disc_bigIntervals)
     bound.compute_boundary()
     assert bound.precision == 0.125, "should have found 2 boundaries"
     assert bound.recall == 1.0984062125855384e-05, "recall should be 1.0984062125855384e-05"

#def test_bad_boundary(gold):
#    """
#        No boundary found
#    """
#    bound = Boundary(gold, disc) 


 

