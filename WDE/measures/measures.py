"""Implement class Measure.
   This class defines the object Measure, from which all measure inherit
   and that allows to store precision, recall and fscore. 
   It also contains functions to pretty print, write into files...
"""

class Measure():
    def __init__():
        pass

    def __repr__(self):
        return 'metric: {}\nrecall: {}\nprecision: {}\nfscore: {}'.format(
                self.metric_name, self.recall, self.precision, self.fscore)

    @property
    def precision(self):
        raise  NotImplementedError('Should not use Measure.precision directly')

    @property
    def recall(self):
        raise  NotImplementedError('Should not use Measure.recall directly')


    @property
    def fscore(self):
        if not (self.recall and self.precision):
            raise ValueError('Attempting to compute fscore when precision'
                             ' and recall are not yet computed!')
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

    def write_score(self):
        if not self.fscore:
            raise AttributeError('Attempting to print scores but fscore'
                                 ' is not yet computed!')
        with open(self.output_folder, 'w') as fout:
            fout.write("metric: {}\n".format(self.metric_name))
            fout.write("precision: {}\n".format(self.precision))
            fout.write("recall: {}\n".format(self.recall))
            fout.write("fscore: {}\n".format(self.fscore))
