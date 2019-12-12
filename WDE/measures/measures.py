"""Implement class Measure.
   This class defines the object Measure, from which all measure inherit
   and that allows to store precision, recall and fscore. 
   It also contains functions to pretty print, write into files...
"""



class Measure():
    def __init__():
        pass

    def __repr__():
        pass

    @property
    def precision():
        pass

    @property
    def recall():
        pass

    @property
    def fscore():
        if not (self.recall and self.precision):
            raise ValueError('Attempting to compute fscore when precision'
                             ' and recall are not yet computed!')
        pass

    def write_score():
        if not self.fscore:
            raise AttributeError('Attempting to print scores but fscore'
                                 ' is not yet computed!')
        pass
