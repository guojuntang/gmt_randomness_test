import numpy
import scipy

class QValueCollector():

    '''
    Compute statistic value the Q values to estimate the uniformity of Q values.

    Args:
        q_values_list: A list of q values. Usually contain 1000 samples.
        intervals_num: The number of intervals. Usually equal to 10.

    Return:
        score: The threshold value. In GM/T, If this score is equal or greater than 0.0001, we consider it pass this test.
    '''
    @staticmethod 
    def compute_value(q_values_list: numpy.ndarray, intervals_num: int) -> float:
        samples_num: int = q_values_list.size
        frequencies: numpy.ndarray = numpy.histogram(q_values_list * intervals_num, intervals_num)[0]
        chi_square: float = numpy.sum((frequencies - samples_num / intervals_num) ** 2 / (samples_num / intervals_num))
        score: float = scipy.special.gammaincc((intervals_num - 1) / 2.0, chi_square / 2.0)
        return score
        