import pytest
import pkg_resources

from WDE.readers.gold_reader import Gold
from WDE.readers.disc_reader import Disc


@pytest.fixture(scope='session')
def gold():
    wrd_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.wrd')
    phn_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/english.phn')

    return Gold(wrd_path=wrd_path,
                phn_path=phn_path)


@pytest.fixture(scope='session')
def gold_vad():
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


@pytest.fixture(scope='session')
def gold_disc(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/gold.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def gold_disc_pairs(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/gold_pairs.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/test_pairs')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_bigIntervals(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/bigger_interval.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_goldIntervals(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/gold.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_clusters(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/group_clusters.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered


@pytest.fixture(scope='session')
def disc_pairs(gold):
    pairs_path = pkg_resources.resource_filename(
            pkg_resources.Requirement.parse('WDE'),
            'WDE/share/group_pairs.class')
    discovered = Disc(pairs_path, gold)
    # discovered.read_clusters()
    # discovered.intervals2txt(gold.phones)
    return discovered
