from tde.measures.coverage import Coverage


def test_gold_coverage(gold, gold_disc):
    cov = Coverage(gold, gold_disc)

    cov.compute_coverage()
    assert cov.coverage == 1, "gold should have 100% coverage"

def test_coverage_max(mandarin_gold, kamper_disc):
    cov = Coverage(mandarin_gold, kamper_disc)
    cov.compute_coverage()
    assert cov.coverage <= 1.0, "Coverage can't be greater than 1"
