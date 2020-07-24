from tde.measures.ned import Ned


def test_gold_pairs(gold, gold_disc_pairs):
    n = Ned(gold_disc_pairs)
    n.compute_ned()
    assert n.ned == 0, "gold pairs should have a ned of 0"
