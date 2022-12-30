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

    def __init__(self, block_size: int = 20):
        # Define specific test attributes
        self._sequence_size_min: int = 100
        self._default_block_size: int = block_size
        # Define cache attributes
        self._last_bits_size: int = -1
        self._block_size: int = -1
        self._blocks_number: int = -1
        # Generate base Test class
        super(FrequencyWithinBlockTest, self).__init__("Frequency Within Block", 0.01)

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
            # Save in the cache
            self._last_bits_size = bits.size
            self._block_size = block_size
            self._blocks_number = blocks_number
        else:
            block_size: int = self._block_size
            blocks_number: int = self._blocks_number
        # Initialize a list of fractions
        block_fractions: numpy.ndarray = numpy.zeros(blocks_number, dtype=float)
        for i in range(blocks_number):
            # Get the bits in the current block
            block: numpy.ndarray = bits[i * block_size:((i + 1) * block_size)]
            # Compute ones and save the fraction in the array
            block_fractions[i] = numpy.count_nonzero(block) / block_size
        # Compute Chi-square
        chi_square: float = numpy.sum(4.0 * block_size * ((block_fractions[:] - 0.5) ** 2))
        # Compute score (P-value) applying the lower incomplete gamma function
        score: float = scipy.special.gammaincc((blocks_number / 2.0), chi_square / 2.0)
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