from tde.measures.grouping import Grouping


def test_same_pairs_and_class(disc_clusters, disc_pairs):
    """ results should be the same if given in pairs or in clusters"""
    group_clusters = Grouping(disc_clusters)
    group_pairs = Grouping(disc_pairs)

    group_clusters.compute_grouping()
    group_pairs.compute_grouping()

    assert group_clusters.precision == group_pairs.precision, (
        "grouping should have the same result if given in pairs or clusters")
    assert group_clusters.recall == group_pairs.recall, (
        "grouping should have the same result if given in pairs or clusters")

def test_weights(disc_clusters):
    good_pairs = [
        ((0, 0, 0, (1, 2, 'tambour'), ('tambour')),
         (0, 0, 0, (3, 4, 'tambour'), ('tambour'))),
        ((0, 0, 0, (4, 5, 'cassoulet'), ('cassoulet')),
         (0, 0, 0, (5, 6, 'cassoulet'), ('cassoulet'))),
        ((0, 0, 0, (6, 7, 'tambour'), ('tambour')),
         (0, 0, 0, (7, 8, 'tambour'), ('tambour')))]

    overlap_pairs = [
        ((0, 0, 0, (1, 2, 'tambour'), ('tambour')),
         (0, 0, 0, (3, 4, 'tambour'), ('tambour'))),
        ((0, 0, 0, (4, 5, 'cassoulet'), ('cassoulet')),
         (0, 0, 0, (5, 6, 'cassoulet'), ('cassoulet'))),
        ((0, 0, 0, (1, 2, 'tambour'), ('tambour')),
         (0, 0, 0, (5, 6, 'cassoulet'), ('cassoulet')))]

    group = Grouping(disc_clusters)

    weights_good, counter_good = group.get_weights(good_pairs)
    weights_overlap, counter_overlap = group.get_weights(overlap_pairs)

    assert counter_good['tambour'] == 4, (
        "'tambour' has 4 tokens in good_pairs")
    assert counter_overlap['tambour'] == 2, (
        "'tambour' has 2 tokens in overlap_pairs")
    assert weights_good['cassoulet'] == 1/3, (
        "'cassoulet' has 2 tokens out of 6 in pairs in good_pairs")
    assert weights_overlap['tambour'] == 2/4, (
        "'tambour' has 2 tokens out of 4 in overlap_pairs")
