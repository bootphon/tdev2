from WDE.measures.coverage import Coverage


def test_gold_coverage(gold, gold_disc):
    cov = Coverage(gold, gold_disc)

    cov.compute_cov()
    print(cov.coverage)

    assert cov.coverage == 1, "gold should have 100% coverage"
