import pytest
import pkg_resources

from tde.readers.gold_reader import Gold
from tde.readers.disc_reader import Disc


@pytest.fixture(scope='session')
def gold():
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/buckeye.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/buckeye.phn')

    return Gold(wrd_path=wrd_path,
                phn_path=phn_path)


@pytest.fixture(scope='session')
def gold_vad():
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/buckeye.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/buckeye.phn')
    vad_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/buckeye.vad')

    return Gold(wrd_path=wrd_path,
                phn_path=phn_path,
                vad_path=vad_path)

@pytest.fixture(scope='session')
def mandarin_gold():
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/mandarin.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/mandarin.phn')

    return Gold(wrd_path=wrd_path,
                phn_path=phn_path)

@pytest.fixture(scope='session')
def kamper_disc(mandarin_gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/kamper_mandarin.class')
    discovered = Disc(pairs_path, mandarin_gold)
    return discovered 

@pytest.fixture(scope='session')
def ZR17_disc(mandarin_gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/ZR17_mandarin.class')
    discovered = Disc(pairs_path, mandarin_gold)
    return discovered 

@pytest.fixture(scope='session')
def gold_disc(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/gold.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def gold_disc_pairs(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/gold_pairs.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/test_pairs')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_bigIntervals(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/bigger_interval.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_goldIntervals(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/gold.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_clusters(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/group_clusters.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_pairs(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('tde'),
            'tde/share/group_pairs.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered
