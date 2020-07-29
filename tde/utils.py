"""Set of functions used by the metrics.

   check_boundary: check if a phone is covered by checking
                   if the discovered interval overlaps with
                   at least either 50% of the phone duration
                   or 30ms of the phone duration.

   overlap:        return the percentage of overlap and the
                   duration (in seconds) of the overlap
                   between two intervals.
                   The percentage is computed w.r. to the
                   second interval (i.e. if the first completely
                   overlaps the second one, even if the first is bigger,
                   ov=1.0)
"""
import numpy as np 

def check_boundary(gold_times, disc_times):
    """ Consider phone discovered if the found interval overlaps
        with either more thant 50% or more than 30ms of the
        gold phone.

        Input
        :param gold_times: tuples, contains the timestamps of the gold phone
        :type gold_times:  tuples of float
        :param disc_times: tuples: contains the timestamps of the
                                   discovered phone
        :type disc_times:  tuples of float

        Output
        :return:           Bool, True if phone is considered discovered,
                           False otherwise
    """
    gold_dur = round(gold_times[1] - gold_times[0], 3)
    ov, ov_time = overlap(disc_times, gold_times)

    # if gold phone is over 60 ms, rule is phone is considered if
    # overlap is over 30ms. Else, rule is phone considered if
    # overlap is over 50% of phone duration.
    if ((gold_dur >= 0.060 and ov_time >= 0.030) or
       (gold_dur < 0.060 and ov >= 0.5)):
        return True
    elif ((gold_dur >= 0.060 and ov_time < 0.030) or
          (gold_dur < 0.060 and ov < 0.5)):
        return False

def overlap(disc, gold):
    ov = (np.min([disc[1], gold[1]]) - np.max([disc[0], gold[0]])) \
        / (gold[1] - gold[0])
    time = round(np.min([disc[1], gold[1]]) - np.max([disc[0], gold[0]]), 3)
    return ov, time
