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
import scipy.special

# Import required src

from gmt_random_test import Test, Result


class PokerTest(Test):
    """
    Poker test is one of the tests in GM/T. However, this test is not included in NIST.
    The focus of Poker test is to check whether the number of 2^m subsequences with length m is close. 
    In a random binary sequence, the number of sequences should be close to each other.
    The significance value of the test is 0.01.
    """

    def __init__(self, seq_length: int, block_size: int  = 4):
        # Define attributes
        self._block_size: int = block_size
        self._blocks_number: int = seq_length // block_size
        self._seq_size: int = block_size * self._blocks_number
        self._patterns_num: int = 2 ** block_size
        # Generate base Test class
        super(PokerTest, self).__init__("Poker", 0.01, seq_length)

    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # Initialize a list of counting patterns (2 ^ block_size patterns in total)
        counter: numpy.ndarray = numpy.zeros(self._patterns_num, dtype=int)
        # reshape vectors discard the redundant bits
        poker_blocks: numpy.ndarray = numpy.reshape(bits.copy()[: self._seq_size], (self._blocks_number, self._block_size))
        # convert into uint8 patterns
        patterns: numpy.ndarray = numpy.packbits(poker_blocks, axis=1, bitorder='little')
        for i in range(self._blocks_number):
            # current pattern
            pattern: int = patterns[i]
            # Compute ones and save the fraction in the array
            counter[pattern] += 1
        # Compute Chi-square
        chi_square: float = (self._patterns_num / self._blocks_number) * numpy.sum((counter ** 2)) - self._blocks_number
        # Compute score (P-value) applying the lower incomplete gamma function
        score: float = scipy.special.gammaincc((self._patterns_num -1) / 2.0, chi_square / 2.0)
        # q_value = p_value
        q_value: float = score
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))


    def __repr__(self) -> str:
        return f'{self.name} (m={self._block_size})'
