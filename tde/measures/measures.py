"""Implement class Measure.
   This class defines the object Measure, from which all measure inherit
   and that allows to store precision, recall and fscore.
   It also contains functions to pretty print, write into files...
"""
import os

class Measure():
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def __repr__(self):
        return 'metric: {}\nrecall: {}\nprecision: {}\nfscore: {}'.format(
                self.metric_name, self.recall, self.precision, self.fscore)

    @property
    def precision(self):
        raise NotImplementedError('Should not use Measure.precision directly')

    @property
    def recall(self):
        raise NotImplementedError('Should not use Measure.recall directly')

    @property
    def fscore(self):
        if not (self.recall is not None
                and self.precision is not None):
            raise ValueError('Attempting to compute fscore when precision'
                             ' and recall are not yet computed!')
        return 2 * (self.precision * self.recall) / (
            self.precision + self.recall)

    def write_score(self):
        if self.fscore is None:
            raise AttributeError('Attempting to print scores but fscore'
                                 ' is not yet computed!')
        with open(os.path.join(self.output_folder, self.metric_name), 'w') as fout:
            fout.write("metric: {}\n".format(self.metric_name))
            fout.write("precision: {}\n".format(self.precision))
            fout.write("recall: {}\n".format(self.recall))
            fout.write("fscore: {}\n".format(self.fscore))
