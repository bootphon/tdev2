
import os
import pytest
import numpy as np
import pkg_resources
import intervaltree as it

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
def disc():
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/test_pairs')
    discovered = Disc(pairs_path)
    discovered.read_clusters()
    return discovered

def test_boundaries(gold):
    """
        Check that word boundaries are a subset of phone
        boundaries
    """
    _, _, _, _, phn_boundaries = gold.read_gold_intervalTree(gold.phn_path)
    _, _, _, _, wrd_boundaries = gold.read_gold_intervalTree(gold.wrd_path)

    for fname in wrd_boundaries:
        assert phn_boundaries[fname].intersection(wrd_boundaries[fname]) == wrd_boundaries[fname], ("boundaries"
         "are not the same in phone alignement and word alignement")

def test_bad_boundary(gold):
    """
        No boundary found
    """
    


 

