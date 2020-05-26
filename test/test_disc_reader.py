def test_unique_intervals():
    pass


def test_interval_over_SIL():
    """Decide what to do when interval overlaps with silence"""


def test_get_transcription(disc, gold):
    token_ngram, ngram = disc.get_transcription(
            's2301b', 232.849, 233.929,
            gold.phones)

    gold_ngram = ('n', 'aa', 't', 'k', 'l', 'ae', 'm',
                  'ah', 'r', 'ih', 'ng', 'f', 'ow')

    assert (ngram == gold_ngram), (
        'Wrong ngram found, shoud have found\n '
        '{}\n but found\n {}\n'.format(gold_ngram, ngram))


def test_30ms(disc, gold):
    token_ngram_notbeg, ngram_notbeg = disc.get_transcription(
        's3202b', 295.498, 295.767, gold.phones)
    token_ngram_notend, ngram_notend = disc.get_transcription(
        's3202b', 295.428, 295.736, gold.phones)
    token_ngram_good, ngram_good = disc.get_transcription(
        's3202b', 295.496, 295.737, gold.phones)
    assert ngram_notbeg == ('l', 'uh', 'k', 'ow'), (
        'should not have found first phone because took less than 30ms of it')
    assert ngram_notend == ('ay', 'l', 'uh', 'k'), (
        'should not have found last phone because took less than 30ms of it')
    assert ngram_good == ('ay', 'l', 'uh', 'k', 'ow'), (
        'should have found last phone because took more than 30ms of it')


def test_50percent(disc, gold):
    token_ngram_notbeg, ngram_notbeg = disc.get_transcription(
        's3303b', 542.875, 542.949, gold.phones)
    token_ngram_notend, ngram_notend = disc.get_transcription(
        's3303b', 542.83, 542.873, gold.phones)
    token_ngram_good, ngram_good = disc.get_transcription(
        's3303b', 542.83, 542.875, gold.phones)
    assert ngram_notbeg == ('hh', 'ah'), (
        'should not have found first phone because took less than 50% of it')
    assert ngram_notend == ('ah',), (
        'should not have found last phone because took less than 50% of it')
    assert ngram_good == ('ah', 'n'), (
        'should have found last phone because took more thant 50% of it')

def test_tiny_interval(disc, gold):
    token_ngram, ngram = disc.get_transcription(
        's0101a', 77.276, 77.278 , gold.phones)
    assert len(ngram) == 0, (
        'Discovered transcription should be empty, but '
        'found {} as transcription'.format(ngram))
