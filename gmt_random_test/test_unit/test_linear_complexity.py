#
# Copyright (C) Guojun Tang 2022
#
# Inspired by the work of David Johnston (C) 2017: https://github.com/dj-on-github/sp800_22_tests
#   and Luca Pasqualini (C) 2019: https://github.com/InsaneMonster/NistRng
#   and Steven Ang (C) 2017: https://github.com/stevenang/randomness_testsuite/blob/master/Complexity.py
#
# This work is licensed under a BSD 3-Clause.
#
# You should have received a copy of the license along with this
# work. If not, see <https://opensource.org/licenses/BSD-3-Clause>.

# Import packages

import numpy
import scipy.special

# Import required src

from gmt_random_test import Test, Result


class LinearComplexityTest(Test):
    """
    Linear complexity test as described in NIST paper: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf
    The focus of this test is the length of a linear feedback shift register (LFSR). The purpose of this test is to determine whether
    or not the sequence is complex enough to be considered random. Random sequences are characterized by longer LFSRs.
    An LFSR that is too short implies non-randomness.
    The significance value of the test is 0.01.
    """

    def __init__(self, seq_length: int, pattern_length = 1000):
        # Define specific test attributes
        self._pattern_length: int = pattern_length
        self._freedom_degrees: int = 6
        self._probabilities: numpy.ndarray = numpy.array([0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833])
        # Compute mean
        self._mu: float = (self._pattern_length / 2.0) + (((-1) ** (self._pattern_length + 1)) + 9.0) / 36.0 - ((self._pattern_length / 3.0) + (2.0 / 9.0)) / (2 ** self._pattern_length)
        # Define attributes
        self._blocks_number: int = seq_length // pattern_length
        # Generate base Test class
        super(LinearComplexityTest, self).__init__("Linear Complexity", 0.01, seq_length)

    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # Compute the linear complexity of the blocks
        blocks_linear_complexity: numpy.ndarray = numpy.zeros(self._blocks_number, dtype=int)
        for i in range(self._blocks_number):
            blocks_linear_complexity[i] = self.berlekamp_massey_algorithm(bits[(i * self._pattern_length) : ((i + 1) * self._pattern_length)])
        # Count the distribution over tickets
        tickets: numpy.ndarray =  ((-1) ** self._pattern_length) * (blocks_linear_complexity[:] - self._mu) + (2.0 / 9.0)
        # Compute frequencies depending on tickets
        # -1 * tickets to convert the bin edges
        frequencies: numpy.ndarray = numpy.histogram(-1 * tickets, bins=[numpy.NINF, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, numpy.Inf])[0][::-1]
        # Compute Chi-square using pre-defined probabilities
        chi_square: float = float(numpy.sum(((frequencies[:] - (self._blocks_number * self._probabilities[:])) ** 2.0) / (self._blocks_number * self._probabilities[:])))
        # Compute the score (P-value)
        score: float = scipy.special.gammaincc((self._freedom_degrees / 2.0), (chi_square / 2.0))
        q_value: float = score
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))


    @staticmethod
    def berlekamp_massey_algorithm(block_data):
           """
           An implementation of the Berlekamp Massey Algorithm. Taken from Wikipedia [1]
           [1] - https://en.wikipedia.org/wiki/Berlekamp-Massey_algorithm
           The Berlekamp-Massey algorithm is an algorithm that will find the shortest linear feedback shift register (LFSR)
           for a given binary output sequence. The algorithm will also find the minimal polynomial of a linearly recurrent
           sequence in an arbitrary field. The field requirement means that the Berlekamp-Massey algorithm requires all
           non-zero elements to have a multiplicative inverse.
           :param block_data:
           :return:
           """
           n = len(block_data)
           c = numpy.zeros(n)
           b = numpy.zeros(n)
           c[0], b[0] = 1, 1
           l, m, i = 0, -1, 0
           int_data = [int(el) for el in block_data]
           while i < n:
               v = int_data[(i - l):i]
               v = v[::-1]
               cc = c[1:l + 1]
               d = (int_data[i] + numpy.dot(v, cc)) % 2
               if d == 1:
                   temp = numpy.copy(c)
                   p = numpy.zeros(n)
                   for j in range(0, l):
                       if b[j] == 1:
                           p[j + i - m] = 1
                   c = (c + p) % 2
                   if l <= 0.5 * i:
                       l = i + 1 - l
                       m = i
                       b = temp
               i += 1
           return l


    def __repr__(self) -> str:
        return f'{self.name} (m={self._pattern_length})'