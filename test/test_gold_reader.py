
import numpy
import pytest
import pkg_resources

#from gold_reader import *
from WDE.measures.token_type import *
from WDE.readers.gold_reader import *

@pytest.fixture(scope='session')
def gold():
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.phn')
    vad_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.vad')

               
    return Gold(wrd_path=wrd_path,
                phn_path=phn_path,
                vad_path=vad_path)

def test_bad_file(gold):
    with pytest.raises(ValueError) as err:
        # joke stolen from Mathieu's shennong
        gold.read_gold_dict('/spam/spam/with/eggs')
    assert 'File Not Found' in str(err.value)

    with pytest.raises(ValueError) as err:
        # joke stolen from Mathieu's shennong
        gold.read_gold_intervalTree('/spam/spam/with/eggs')
    assert 'File Not Found' in str(err.value)

def test_phone_read_gold(gold):
    phn_dict, ix2phn_dict, phn2ix_dict =  gold.read_gold_dict(gold.phn_path)
    assert len(ix2phn_dict) == 42, "Not enough phones in phone dictionnary, should have 42"
    
    #all_phones = [phn_ for ix, phn_ in ix2phn]
    #assert "SIL" not in all_phones,
    
    phn_tree, trs, ix2phn_tree, phn2ix_tree = gold.read_gold_intervalTree(gold.phn_path)
    #assert ix2phn_dict == ix2phn_tree, "reading as dict or tree gave different phones"
    assert len(ix2phn_tree) == len(ix2phn_dict), "reading as dict or tree gave different number of phones"
    for phn in phn2ix_dict:
        assert phn in phn2ix_tree, "phone {} not found when creating intervaltree".format(phn)

    for fname in phn_dict:
        assert len(phn_dict[fname]['start']) == len(phn_tree[fname]), "not same number of intervals for file {} read as dict or as tree".format(fname)
        assert not phn_tree[fname].is_empty(), 'interval tree for {} is empty'.format(fname)
        
        copied_tree = phn_tree[fname].copy()
        copied_tree.split_overlaps()
        assert phn_tree[fname] == copied_tree, 'interval tree for {} contains overlaps'.format(fname)

def test_phone_word_read_gold(gold):
    phn_tree, _, ix2phn_tree, phn2ix_tree = gold.read_gold_intervalTree(gold.phn_path)
    wrd_tree, _, ix2wrd_tree, wrd2ix_tree = gold.read_gold_intervalTree(gold.wrd_path)

    for fname in wrd_tree:
        assert fname in phn_tree, '{} not in phone tree'.format(fname)
        starts = [on for on, off, phn in phn_tree[fname]]
        ends = [off for on, off, phn in phn_tree[fname]]
        for on, off, _ in wrd_tree[fname]:
            assert on in starts, "word onset does not appear in phone alignment"
            assert off in ends, "word offset does not appear in phone alignment"

def test_silences_tree():
    # TODO: compare overlaps between vad/phn/word and silence: should be None...
    pass   
