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
import math

# Import required src

from gmt_random_test import Test, Result


class MaurersUniversalTest(Test):
    """
    Maurers universal test as described in NIST paper: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf
    The focus of this test is the number of bits between matching patterns (a measure that is related to the length of a compressed sequence).
    The purpose of the test is to detect whether or not the sequence can be significantly compressed without loss of information.
    A significantly compressible sequence is considered to be non-random.
    The significance value of the test is 0.01.
    """

    def __init__(self, seq_length: int, pattern_length: int = 7, q_blocks: int = 1280):
        # Define specific test attributes
        # Note: tables from https://static.aminer.org/pdf/PDF/000/120/333/a_universal_statistical_test_for_random_bit_generators.pdf
        self._thresholds = [904960, 2068480, 4654080, 10342400, 22753280, 49643520, 107560960, 231669760, 496435200, 1059061760]
        self._expected_value_table  = [0, 0.73264948, 1.5374383, 2.40160681, 3.31122472, 4.25342659, 5.2177052, 6.1962507, 7.1836656, 8.1764248, 9.1723243, 10.170032, 11.168765, 12.168070, 13.167693, 14.167488, 15.167379]
        self._variance_table = [0, 0.690, 1.338, 1.901, 2.358, 2.705, 2.954, 3.125, 3.238, 3.311, 3.356, 3.384, 3.401, 3.410, 3.416, 3.419, 3.421]
        # Define cache attributes
        self._pattern_length: int = pattern_length
        self._q_blocks: int = q_blocks
        # Generate base Test class
        super(MaurersUniversalTest, self).__init__("Maurers Universal", 0.01, seq_length)

    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        blocks_number: int = int(bits.size // self._pattern_length)
        q_blocks: int = self._q_blocks
        k_blocks: int = blocks_number - q_blocks
        # Construct table of symbols all zeroed out at the beginning
        table: numpy.ndarray = numpy.zeros(2 ** self._pattern_length, dtype=int)
        # Mark final position in Q-blocks
        for i in range(q_blocks):
            # Get the pattern in the Q-block
            pattern: numpy.ndarray = bits[i * self._pattern_length:(i + 1) * self._pattern_length]
            # +1 to number indexes 1... (2 ** L) + 1 instead of 0... 2 ** L
            table[self._pattern_to_int(pattern)] = i + 1
        # Mark final position in K-blocks and compute the sum
        computed_sum: float = 0.0
        for i in range(q_blocks, blocks_number):
            # Get the pattern in the K-block
            pattern: numpy.ndarray = bits[i * self._pattern_length:(i + 1) * self._pattern_length]
            # Compute difference with respect to the current value in the table
            difference: int = i + 1 - table[self._pattern_to_int(pattern)]
            # Update the current value in the table
            table[self._pattern_to_int(pattern)] = i + 1
            # Update the computed sum
            computed_sum += math.log(difference, 2)
        # Compute the test statistic
        fn: float = computed_sum / k_blocks
        c: float = 0.7 - 0.8 / self._pattern_length + (4 + 32 / self._pattern_length) * (k_blocks ** (-3 / self._pattern_length) / 15)
        sigma: float = c * math.sqrt(self._variance_table[self._pattern_length] / k_blocks)
        # Compute magnitude
        magnitude: float = (fn - self._expected_value_table[self._pattern_length]) / sigma
        # Compute the score (P-value)
        score: float = math.erfc(abs(magnitude) / math.sqrt(2))
        q_value: float = math.erfc(magnitude / math.sqrt(2)) / 2.0
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))

    @staticmethod
    def _pattern_to_int(bit_pattern: numpy.ndarray) -> int:
        """
        Convert the given pattern of bits to an integer value.
        :param bit_pattern: the bit pattern to convert
        :return: the integer value identifying the pattern
        """
        result: int = 0
        for bit in bit_pattern:
            result = (result << 1) + bit
        return result

    def __repr__(self) -> str:
        return f'{self.name}'