#
# Copyright (C) Guojun Tang 2022
#
# Inspired by the work of David Johnston (C) 2017: https://github.com/dj-on-github/sp800_22_tests
#   and Luca Pasqualini (C) 2019: https://github.com/InsaneMonster/NistRng
#
# This work is licensed under a BSD 3-Clause.
#
# You should have received a copy of the license along with this
# work. If not, see <https://opensource.org/licenses/BSD-3-Clause>.

# Import packages

import numpy
import scipy
import math

# Import required src

from gmt_random_test import Test, Result


class RunsDistributionTest(Test):
    """
    Runs distribution test is one of the tests in GM/T. However, this test is not included in NIST.
    The focus of this test is to check the uniformity of runs' distribution. In a random binary sequence, 
    the number of runs of the same length should be approximately the same.
    The significance value of the test is 0.01.
    """

    # require bits length to pre-compute the table
    def __init__(self, seq_length: int, bits_length: int = 100):
        self._bits_length = bits_length
        self._table: numpy.ndarray = None
        self._k: int = -1
        super(RunsDistributionTest, self).__init__("RunsDistribution", 0.01, seq_length)

    def _compute_table(self):
        self._table = numpy.zeros(self._bits_length, dtype=float) 
        for i in range(self._bits_length):
            self._table[i] = (self._bits_length - i + 3) / 2 ** (i + 2)
            if self._table[i] >= 5:
                   self._k = i

    def _cal_runs(self,
                  bits: numpy.ndarray, ones_runs: numpy.ndarray, zeroes_runs: numpy.ndarray):
        prev_bit: int = bits[0]
        counter: int = 0
        for bit in bits:
            if bit == prev_bit:
                counter += 1
            else:
                counter = counter if counter <= self._k else self._k
                if prev_bit == 0:
                    zeroes_runs[counter] += 1
                else:
                    ones_runs[counter] += 1
                counter = 1
            prev_bit = bit
        # deal with the last bit
        counter = counter if counter <= self._k else self._k
        if prev_bit == 0:
                zeroes_runs[counter] += 1
        else:
                ones_runs[counter] += 1

    def _compute_runs_table(self, total: int) -> numpy.ndarray:
        result: numpy.ndarray = numpy.zeros(self._k + 1)
        result[0] = 1
        for i in range(1, self._k):
            result[i] = total / 2 ** (i + 1)
        result[self._k] = total / 2 ** (self._k)
        return result

    def _execute(self,
                 bits: numpy.ndarray):
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # pre-compute the table and save in cache
        if self._table is None:
            self._compute_table()
        zeroes_runs: numpy.ndarray = numpy.zeros(self._k + 1, dtype=int)
        ones_runs: numpy.ndarray = numpy.zeros(self._k + 1, dtype=int)
        self._cal_runs(bits, ones_runs, zeroes_runs)
        total: int = numpy.sum(zeroes_runs + ones_runs)
        runs_table: numpy.ndarray = self._compute_runs_table(total)
        tmp_1: numpy.ndarray = (zeroes_runs - runs_table) ** 2 / runs_table
        tmp_2: numpy.ndarray = (ones_runs - runs_table) ** 2 / runs_table
        tmp_1[0] = 0
        tmp_2[0] = 0
        chi_square: float = numpy.sum(tmp_1) + numpy.sum(tmp_2)

        # Compute score (P-value) applying the lower incomplete gamma function
        score: float = scipy.special.gammaincc(self._k - 1, chi_square / 2.0)
        # q_value = p_value
        q_value: float = score
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))

    def __repr__(self) -> str:
        return f'{self.name}'
