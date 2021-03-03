import os

from .measures import Measure


class Coverage(Measure):
    """Coverage measure

    The coverage measures how many 'Gold' phonemes were found.
    See https://docs.cognitive-ml.fr/tde/measures/index.html
    for a summary of all measures.

    Input
    :param disc: Discovered Object, contains the discovered phonemes
    :param gold: Gold object, contains all the gold phonemes
    :param output_folder: string, path to the output folder

    Output
    :param coverage: Coverage
    """

    def __init__(self, gold, disc, output_folder=None):
        self.metric_name = "coverage"
        self.output_folder = output_folder

        # self.all_intervals = set()
        self.n_phones = 0

        for fname in gold.phones:
            # TODO remove SIL here ?
            self.n_phones += len([
                ph for on, off, ph in gold.phones[fname]
                if (ph != "SIL" and ph != "SPN")])

        self.covered_phn = set(
            (fname, phn_on, phn_off, phn)
            for fname, disc_on, disc_off, token_ngram, ngram
            in disc.intervals
            for phn_on, phn_off, phn in token_ngram
            if (phn != "SIL" and phn != "SPN"))

        self.coverage = 0

    def compute_coverage(self):
        """ For coverage, simply compute the ratio of discovered phones over all phone

            Input:
            :param covered_phn:  a set containing all the covered phones

            Output:
            :param coverage:     the ratio of number of covered phones over
                                 the overall number of phones in the corpus
        """
        self.coverage = len(self.covered_phn) / self.n_phones

    def write_score(self):
        if not self.coverage:
            raise AttributeError('Attempting to print scores but score'
                                 ' is not yet computed!')
        with open(os.path.join(self.output_folder, self.metric_name), 'w') as fout:
            fout.write("metric: {}\n".format(self.metric_name))
            fout.write("coverage: {}\n".format(self.coverage))
