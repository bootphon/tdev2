import pytest
import intervaltree

from tde.measures.token_type import TokenType


def test_TokenType_init(gold, disc):
    #gold_phn, _, _, _, _ = gold.read_gold_intervalTree(gold.phn_path)
    #gold_wrd, _, _, _, _ = gold.read_gold_intervalTree(gold.wrd_path)
    #print(type(gold_phn))
    _init = TokenType(gold, disc)

    assert len(_init.all_type) == 4538, "wrong number of type detected"
    assert _init.n_token == 69543, "wrong number of token detected"

def test_gold_intervals(gold, disc_goldIntervals):
    tokenType = TokenType(gold, disc_goldIntervals)
    tokenType.compute_token_type()

    tok_prec, typ_prec = tokenType.precision
    tok_rec, typ_rec = tokenType.recall

    assert (tok_prec == 1.0 and tok_rec == 1.0), (
        "token precision should be"
        " 1.0, discovered the same token twice should be counted only once")

    assert (typ_prec == 1.0 and typ_rec == 0.9858968708682239), (
        "type precision should be"
        " 1.0, and type recall ~0.98 (because of homophones),"
        "as all covered types were discovered")

# TODO make this test more robust/checked
#def test_TokenType(gold, disc):
#    #gold_phn, _, _, _, _ = gold.read_gold_intervalTree(gold.phn_path)
#    #gold_wrd, _, _, _, _ = gold.read_gold_intervalTree(gold.wrd_path)
#
#    # disc.intervals2txt(gold_phn)
#    # disc_int = disc.transcription
#    tokenType = TokenType(gold, disc)
#    tokenType.compute_token_type()
#    assert len(tokenType.type_seen) == 14111, (
#        "should cover 14109 types, found {}".format(len(tokenType.type_seen)))
#    assert len(tokenType.type_hit) == 740, (
#        "should have hit 740 types, found {}".format(len(tokenType.type_hit)))

def test_unknown_filename(gold, disc):
    gold_wrd_intervals = [(1.0, 2.0, 'tambour'), (3.0, 4.0 , 'cassoulet')]
    gold_phn_intervals = gold_wrd_intervals 
    
    gold.words = {
        's01': intervaltree.IntervalTree.from_tuples(gold_wrd_intervals)}
    gold.phones = {
        's01': intervaltree.IntervalTree.from_tuples(gold_phn_intervals)}

    # test that only one discovered token is counted, not two
    disc.intervals = [
        ('s06', 1.0, 1.69, ((1.0, 2.0, 'tambour'),), ('tambour',))]

    with pytest.raises(ValueError) as err:
        tokenType = TokenType(gold, disc)
        tok_prec, tok_rec, typ_prec, typ_rec = tokenType.compute_token_type()
    assert 'file not found' in str(err.value)

def test_token_count_once(gold, disc):
    gold_wrd_intervals = [(1.0, 2.0, 'tambour'), (3.0, 4.0 , 'cassoulet')]
    gold_phn_intervals = gold_wrd_intervals 
    
    gold.words = {
        's01': intervaltree.IntervalTree.from_tuples(gold_wrd_intervals)}
    gold.phones = {
        's01': intervaltree.IntervalTree.from_tuples(gold_phn_intervals)}

    # test that only one discovered token is counted, not two
    disc.intervals = [
        ('s01', 1.0, 1.69, ((1.0, 2.0,'tambour'),), ('tambour',)),
        ('s01', 1.02, 1.69, ((1.0, 2.0, 'tambour'),), ('tambour',))]

    tokenType = TokenType(gold, disc)

    tokenType.compute_token_type()
    tok_prec, typ_prec = tokenType.precision
    tok_rec, typ_rec = tokenType.recall

    assert (tok_prec == 0.5 and tok_rec == 0.5), (
        "token precision should be"
        " 0.5, discovered the same token twice should be counted only once")
    assert (typ_prec == 1.0 and typ_rec == 0.5), (
        "type precision should be"
        " 1.0, and type recall 0.5, as all covered types were discovered")



