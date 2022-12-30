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

    def __init__(self, block_size:int  = 4):
        # Define specific test attributes
        self._max_block_size: int = 8
        self._sequence_size_min: int = 100
        self._default_block_size: int = block_size if block_size <= self._max_block_size else self._max_block_size
        # Define cache attributes
        self._last_bits_size: int = -1
        self._block_size: int = -1
        self._blocks_number: int = -1
        self._seq_size: int = -1
        self._patterns_num: int = -1
        # Generate base Test class
        super(PokerTest, self).__init__("Poker", 0.01)

    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # Reload values is cache is empty or no longer up-to-date
        # Otherwise, use cache
        if self._last_bits_size == -1 or self._last_bits_size != bits.size:
            # Get the number of blocks (N) with the default minimum block size (M)
            block_size: int = self._default_block_size
            blocks_number: int = int(bits.size // block_size)
            seq_size: int = block_size * blocks_number
            patterns_num: int = 2 ** block_size
            # Save in the cache
            self._last_bits_size = bits.size
            self._block_size = block_size
            self._blocks_number = blocks_number
            self._seq_size = seq_size
            self._patterns_num = patterns_num
        else:
            block_size: int = self._block_size
            blocks_number: int = self._blocks_number
            seq_size: int = self._seq_size
            patterns_num: int = self._patterns_num
        # Initialize a list of counting patterns (2 ^ block_size patterns in total)
        counter: numpy.ndarray = numpy.zeros(patterns_num, dtype=int)
        # reshape vectors discard the redundant bits
        poker_blocks: numpy.ndarray = numpy.reshape(bits.copy()[: seq_size], (blocks_number, block_size))
        # convert into uint8 patterns
        patterns: numpy.ndarray = numpy.packbits(poker_blocks, axis=1, bitorder='little')
        for i in range(blocks_number):
            # current pattern
            pattern: int = patterns[i]
            # Compute ones and save the fraction in the array
            counter[pattern] += 1
        # Compute Chi-square
        chi_square: float = (patterns_num / blocks_number) * numpy.sum((counter ** 2)) - blocks_number
        # Compute score (P-value) applying the lower incomplete gamma function
        score: float = scipy.special.gammaincc((patterns_num -1) / 2.0, chi_square / 2.0)
        # q_value = p_value
        q_value: float = score
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))


    def __repr__(self) -> str:
        return f'{self.name} (m={self._default_block_size})'

    def is_eligible(self,
                    bits: numpy.ndarray) -> bool:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # Check for eligibility
        if bits.size < self._sequence_size_min:
            return False
        return True