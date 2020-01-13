
import os
import pytest
import numpy as np
import pkg_resources
import intervaltree as it

from collections import defaultdict
from WDE.measures.ned import *
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
def gold_disc(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/gold_pairs.class')
    discovered = Disc(pairs_path, gold)
    #discovered.read_clusters()
    #discovered.intervals2txt(gold.phones)
    return discovered

def test_gold_pairs(gold, gold_disc):
    n = ned(gold_disc)

    n.compute_ned()

    assert n.ned==0, "gold pairs should have a ned of 0"

