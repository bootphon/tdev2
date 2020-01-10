
import os
import pytest
import numpy as np
import pkg_resources
import intervaltree as it

from WDE.measures.token_type import *
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

@pytest.fixture(scope='session')
def disc_goldIntervals(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/gold.class')
    discovered = Disc(pairs_path)
    #discovered.read_clusters()
    discovered.intervals2txt(gold.phones)
    return discovered


def test_TokenType_init(gold, disc):
    gold_phn, _, _, _, _ = gold.read_gold_intervalTree(gold.phn_path)
    gold_wrd, _, _, _, _ = gold.read_gold_intervalTree(gold.wrd_path)
    print(type(gold_phn)) 
    _init = TokenType(gold_phn, gold_wrd, disc)

    assert len(_init.all_type) == 4538, "wrong number of type detected"
    assert _init.n_token == 69543, "wrong number of token detected"

def test_TokenType(gold, disc):

    gold_phn, _, _, _, _ = gold.read_gold_intervalTree(gold.phn_path)
    gold_wrd, _, _, _, _ = gold.read_gold_intervalTree(gold.wrd_path)
    
    disc.intervals2txt(gold_phn)
    #disc_int = disc.transcription
    tokenType = TokenType(gold_phn, gold_wrd, disc)
    tokenType.compute_token_type()

    #token_hit 6924
    #n_discovered 84218
    #n_token 86065
    #type_hit 766
    #type_covered 11117
    #n_type 4540

    assert len(tokenType.type_seen) == 14111, "should cover 14109 types, found {}".format(len(tokenType.type_seen))
    assert len(tokenType.type_hit) == 740, "should have hit 740 types, found {}".format(len(tokenType.type_hit))
    


def test_bad_tokens(gold):
    pass

def test_unknown_filename(disc):
    gold_wrd_intervals = [(1.0, 2.0, 'tambour'), (3.0, 4.0 , 'cassoulet')]
    gold_phn_intervals = gold_wrd_intervals 
    
    gold_wrd = {'s01': intervaltree.IntervalTree.from_tuples(gold_wrd_intervals)}
    gold_phn = {'s01': intervaltree.IntervalTree.from_tuples(gold_phn_intervals)}

    # test that only one discovered token is counted, not two
    disc.transcription = [('s06', 1.0, 1.69, ((1.0, 2.0,'tambour'),), 
                          ('tambour',))]

    with pytest.raises(ValueError) as err:
        tokenType = TokenType(gold_phn, gold_wrd, disc)
        tok_prec, tok_rec, typ_prec, typ_rec = tokenType.compute_token_type()
    assert 'file not found' in str(err.value)

def test_token_count_once(disc):
    gold_wrd_intervals = [(1.0, 2.0, 'tambour'), (3.0, 4.0 , 'cassoulet')]
    gold_phn_intervals = gold_wrd_intervals 
    
    gold_wrd = {'s01': intervaltree.IntervalTree.from_tuples(gold_wrd_intervals)}
    gold_phn = {'s01': intervaltree.IntervalTree.from_tuples(gold_phn_intervals)}

    # test that only one discovered token is counted, not two
    disc.transcription = [('s01', 1.0, 1.69, ((1.0, 2.0,'tambour'),),
                          ('tambour',)), ('s01', 1.02, 1.69, ((1.0, 2.0,'tambour'),), ('tambour',))]

    tokenType = TokenType(gold_phn, gold_wrd, disc)

    tokenType.compute_token_type()
    tok_prec, typ_prec = tokenType.precision
    tok_rec, typ_rec = tokenType.recall

    assert (tok_prec == 0.5 and tok_rec == 0.5), ("token precision should be"
           " 0.5, discovered the same token twice should be counted only once")
    assert (typ_prec == 1.0 and typ_rec == 0.5), ("type precision should be"
           " 1.0, and type recall 0.5, as all covered types were discovered")

def test_gold_intervals(gold, disc_goldIntervals):
    tokenType = TokenType(gold.phones, gold.words, disc_goldIntervals)
    tokenType.compute_token_type()

    tok_prec, typ_prec = tokenType.precision
    tok_rec, typ_rec = tokenType.recall

    assert (tok_prec == 1.0 and tok_rec == 1.0), ("token precision should be"
           " 1.0, discovered the same token twice should be counted only once")
    assert (typ_prec == 1.0 and typ_rec == 0.9858968708682239), ("type precision should be"
           " 1.0, and type recall ~0.98 (because of homophones),"
           "as all covered types were discovered")

