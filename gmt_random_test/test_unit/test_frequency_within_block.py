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


class FrequencyWithinBlockTest(Test):
    """
    Frequency within block test is one of the tests in GM/T.
    You can also refer to NIST paper: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf
    The focus of the test is the proportion of ones within M-bit blocks. The purpose of this test is to determine whether the frequency of
    ones in an M-bit block is approximately M/2, as would be expected under an assumption of randomness.
    For block size M=1, this test degenerates to the Frequency (Monobit) test.
    The significance value of the test is 0.01.
    """

    def __init__(self, seq_length: int, block_size: int = 20):
        # Define attributes
        self._block_size: int = block_size
        self._blocks_number: int = seq_length // self._block_size
        # Generate base Test class
        super(FrequencyWithinBlockTest, self).__init__("Frequency Within Block", 0.01, seq_length)

    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # Initialize a list of fractions
        block_fractions: numpy.ndarray = numpy.zeros(self._blocks_number, dtype=float)
        for i in range(self._blocks_number):
            # Get the bits in the current block
            block: numpy.ndarray = bits[i * self._block_size:((i + 1) * self._block_size)]
            # Compute ones and save the fraction in the array
            block_fractions[i] = numpy.count_nonzero(block) / self._block_size
        # Compute Chi-square
        chi_square: float = numpy.sum(4.0 * self._block_size * ((block_fractions[:] - 0.5) ** 2))
        # Compute score (P-value) applying the lower incomplete gamma function
        score: float = scipy.special.gammaincc((self._blocks_number / 2.0), chi_square / 2.0)
        # q_value = p_value
        q_value: float = score
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))

    def __repr__(self) -> str:
        return f'{self.name} (m={self._block_size})'
