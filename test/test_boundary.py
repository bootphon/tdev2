from collections import defaultdict
from tde.measures.boundary import Boundary


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
        all_wrd_boundaries[fname] = wrd_boundaries[0][fname].union(
            wrd_boundaries[1][fname])
        all_phn_boundaries[fname] = phn_boundaries[0][fname].union(
            phn_boundaries[1][fname])

    for fname in all_wrd_boundaries:
        wrd_boundary = all_wrd_boundaries[fname]
        assert all_phn_boundaries[fname].intersection(
            wrd_boundary) == wrd_boundary, (
                "boundaries are not the same in phone and word alignements")

    # for fname in wrd_boundaries[1]:
    #    assert phn_boundaries[1][fname].intersection(wrd_boundaries[1][fname]) == wrd_boundaries[1][fname], ("boundaries"
    #     "are not the same in phone alignement and word alignement")


def test_big_intervals(gold, disc_bigIntervals):
    bound = Boundary(gold, disc_bigIntervals)
    bound.compute_boundary()
    assert bound.precision == 0.125, "should have found 2 boundaries"
    assert bound.recall == 1.0984062125855384e-05, (
        "recall should be 1.0984062125855384e-05")



def test_disc_is_gold(gold, disc_goldIntervals):
    """ Test boundary result when discovered intervals are gold"""
    bound = Boundary(gold, disc_goldIntervals)
    bound.compute_boundary()
    assert bound.precision == 1.0, "should have 100% precision"
    assert bound.recall == 1.0, "should have 100% recall"

def test_ZR17Disc_subpart(mandarin_gold, ZR17_disc):
    bound = Boundary(mandarin_gold, ZR17_disc)
    bound.compute_boundary()

    assert bound.n_discovered_boundary == 12, ("should have found "
            "13 boundaries in those pairs")
