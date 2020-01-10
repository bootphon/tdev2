
import os
import pytest
import numpy as np
import pkg_resources
import intervaltree as it

from collections import defaultdict
from WDE.measures.coverage import *
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
            'WDE/share/gold.class')
    discovered = Disc(pairs_path)
    #discovered.read_clusters()
    discovered.intervals2txt(gold.phones)
    return discovered

def test_gold_coverage(gold, gold_disc):
    cov = Coverage(gold, gold_disc)

    res = cov.compute_cov()
    print(res)

    assert res == 1, "gold should have 100% coverage"
    
