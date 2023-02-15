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


class LongestRunsInABlockTest(Test):
    """
    Longest run ones in a block test is one of the tests in GM/T.
    You can also refer to NIST paper: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf
    In GM/T 005-2021, this test will also check runs of ones and zeros. And it also uses different probabilities from NIST (see _probabilities). 
    The focus of the test is the longest run of ones(zeroes) within M-bit blocks. The purpose of this test is to determine whether
    the length of the longest run of ones (zeroes) within the tested sequence is consistent with the length of the longest run of
    ones (zeroes) that would be expected in a random sequence. 
    The significance value of the test is 0.01.
    """

    def __init__(self, seq_length: int):
        # Define attributes
        block_size: int = 10000
        if seq_length < 6272:
            block_size: int = 8
        elif seq_length < 750000:
            block_size: int = 128
        # Set the block number and K depending on the block size
        k: int = 6
        if block_size == 8:
            k: int = 3
        elif block_size == 128:
            k: int = 5
        self._block_size: int = block_size
        self._blocks_number: int = seq_length // block_size
        self._k: int = k
        # Generate base Test class
        super(LongestRunsInABlockTest, self).__init__("Longest Runs In A Block", 0.01, seq_length)

    def _cal_longest_runs(self, block: numpy.ndarray):
        prev_bit: int = block[0]
        counter: int = 0
        longest_ones_run_length: int = 0
        longest_zeroes_run_length: int = 0
        for bit in block:
            if bit == prev_bit:
                counter += 1
            else:
                if prev_bit == 0:
                    longest_zeroes_run_length = counter if counter > longest_zeroes_run_length else longest_zeroes_run_length
                else:
                    longest_ones_run_length = counter if counter > longest_ones_run_length else longest_ones_run_length
                counter = 1
            prev_bit = bit
        # deal with the last bit
        if prev_bit == 0:
                longest_zeroes_run_length = counter if counter > longest_zeroes_run_length else longest_zeroes_run_length
        else:
                longest_ones_run_length = counter if counter > longest_ones_run_length else longest_ones_run_length
        return longest_ones_run_length, longest_zeroes_run_length


    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # Define the array of frequencies
        ones_frequencies: numpy.ndarray = numpy.zeros(7, dtype=int)
        zeroes_frequencies: numpy.ndarray = numpy.zeros(7, dtype=int)
        # Find longest run length in each block
        for i in range(self._blocks_number):
            block: numpy.ndarray = bits[i * self._block_size:((i + 1) * self._block_size)]
            run_length: int = 0
            # Count the length of each adjacent bits group (runs) in the current block and update the max length of them
            longest_ones_run_length, longest_zeroes_run_length  = self._cal_longest_runs(block)
            # Update the list of frequencies
            if self._block_size == 8:
                ones_frequencies[min(3, max(0, longest_ones_run_length - 1))] += 1
                zeroes_frequencies[min(3, max(0, longest_zeroes_run_length - 1))] += 1
            elif self._block_size == 128:
                ones_frequencies[min(5, max(0, longest_ones_run_length - 4))] += 1
                zeroes_frequencies[min(5, max(0, longest_zeroes_run_length - 4))] += 1
            else:
                ones_frequencies[min(6, max(0, longest_ones_run_length - 10))] += 1
                zeroes_frequencies[min(6, max(0, longest_zeroes_run_length - 10))] += 1
        # Compute Chi-square
        zeroes_chi_square: float = 0.0
        ones_chi_square: float = 0.0
        for i in range(self._k + 1):
            zeroes_chi_square += ((zeroes_frequencies[i] - self._blocks_number * self._probabilities(self._block_size, i)) ** 2) / (self._blocks_number * self._probabilities(self._block_size, i))
            ones_chi_square += ((ones_frequencies[i] - self._blocks_number * self._probabilities(self._block_size, i)) ** 2) / (self._blocks_number * self._probabilities(self._block_size, i))
        # Compute score (P-value)
        score_1: float = scipy.special.gammaincc(self._k / 2.0, zeroes_chi_square / 2.0)
        score_2: float = scipy.special.gammaincc(self._k / 2.0, ones_chi_square / 2.0)
        # Compute q-value
        q_value_1: float = score_1
        q_value_2: float = score_2
        # Return result
        if score_1 >= self.significance_value and score_2 >= self.significance_value:
            return Result(self.name, True, numpy.array([score_1, score_2]), numpy.array([q_value_1, q_value_2]))
        return Result(self.name, False, numpy.array([score_1, score_2]), numpy.array([q_value_1, q_value_2]))


    def __repr__(self) -> str:
        return f'{self.name}'

    @staticmethod
    def _probabilities(size_of_block: int, index: int) -> float:
        """
        Returns a probability at the given index in the array or probabilities defined for the block of the given size. (using different parameters from NIST)
        :param size_of_block: can be 8, 128, 512, 1000 and in any other case will fallback on 10000
        :param index: the index of the probability
        :return: the probability at the given index
        """
        if size_of_block == 8:
            return [0.2148, 0.3672, 0.2305, 0.1875][index]
        elif size_of_block == 128:
            return [0.1174, 0.2430, 0.2494, 0.1752, 0.1027, 0.1124][index]
        elif size_of_block == 1000:
            return [0.086632, 0.208201, 0.248419, 0.193913, 0.121458, 0.068011, 0.073366][index]
        else:
            return [0.086632, 0.208201, 0.248419, 0.193913, 0.121458, 0.068011, 0.073366][index]