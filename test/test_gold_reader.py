import pytest


def test_bad_file(gold_vad):
    with pytest.raises(ValueError) as err:
        # joke stolen from Mathieu's shennong
        gold_vad.read_gold_dict('/spam/spam/with/eggs')
    assert 'File Not Found' in str(err.value)

    with pytest.raises(ValueError) as err:
        # joke stolen from Mathieu's shennong
        gold_vad.read_gold_intervalTree('/spam/spam/with/eggs')
    assert 'File Not Found' in str(err.value)


def test_phone_read_gold(gold_vad):
    phn_dict, ix2phn_dict, phn2ix_dict = (
        gold_vad.read_gold_dict(gold_vad.phn_path))
    assert len(ix2phn_dict) == 42, (
        "Not enough phones in phone dictionnary, should have 42")

    # all_phones = [phn_ for ix, phn_ in ix2phn]
    # assert "SIL" not in all_phones,

    phn_tree, trs, ix2phn_tree, phn2ix_tree, _ = (
        gold_vad.read_gold_intervalTree(gold_vad.phn_path))

    # assert ix2phn_dict == ix2phn_tree, "reading as dict or tree gave
    # different phones"
    assert len(ix2phn_tree) == len(ix2phn_dict), (
        "reading as dict or tree gave different number of phones")
    for phn in phn2ix_dict:
        assert phn in phn2ix_tree, (
            "phone {} not found when creating intervaltree".format(phn))

    for fname in phn_dict:
        assert len(phn_dict[fname]['start']) == len(phn_tree[fname]), (
            "not same number of intervals for file {} read as dict or as tree"
            .format(fname))
        assert not phn_tree[fname].is_empty(), (
            'interval tree for {} is empty'.format(fname))

        copied_tree = phn_tree[fname].copy()
        copied_tree.split_overlaps()
        assert phn_tree[fname] == copied_tree, (
            'interval tree for {} contains overlaps'.format(fname))


def test_phone_word_read_gold(gold_vad):
    phn_tree, _, ix2phn_tree, phn2ix_tree, _ = (
        gold_vad.read_gold_intervalTree(gold_vad.phn_path))
    wrd_tree, _, ix2wrd_tree, wrd2ix_tree, _ = (
        gold_vad.read_gold_intervalTree(gold_vad.wrd_path))

    for fname in wrd_tree:
        assert fname in phn_tree, '{} not in phone tree'.format(fname)
        starts = [on for on, off, phn in phn_tree[fname]]
        ends = [off for on, off, phn in phn_tree[fname]]
        for on, off, _ in wrd_tree[fname]:
            assert on in starts, (
                "word onset does not appear in phone alignment")
            assert off in ends, (
                "word offset does not appear in phone alignment")


def test_silences_tree():
    # TODO: compare overlaps between vad/phn/word and silence: should be
    # None...
    pass
