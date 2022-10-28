import numpy
import scipy

class QValueCollector():

    @staticmethod 
    def compute_value(q_values_list: numpy.ndarray, intervals_num: int, samples_num: int) -> float:
        frequencies: numpy.ndarray = numpy.histogram(q_values_list * intervals_num, intervals_num)[0]
        chi_square: float = numpy.sum((frequencies - samples_num / intervals_num) ** 2 / (samples_num / intervals_num))
        score: float = scipy.special.gammaincc((intervals_num - 1) / 2.0, chi_square / 2.0)
        return score
        