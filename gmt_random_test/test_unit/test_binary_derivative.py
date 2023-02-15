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


from gmt_random_test import Test, Result


class BinaryDerivativeTest(Test):
    """
    Binary derivative test is one of the tests in GM/T. However, this test is not included in NIST.
    The focus of this test is to check  whether the numbers of 0 and 1 in the nth binary derivation sequence are close to the same. 
    For a binary initial sequence with a length of n, two adjacent bits in the initial sequence are sequentially XORed to obtain
    a binary derivation sequence of the sequence with a length of n-1. By performing the above operations n times in sequence, 
    an n-time binary derivation sequence of the initial sequence can be obtained, with a length of n-k. For a random sequence,
    no matter how many derivations are performed, the number of 0 and 1 should be close to the same.
    The significance value of the test is 0.01.
    """
    def __init__(self, seq_length: int, derivative: int = 1):
        # Generate base Test class
        self._derivative = derivative
        super(BinaryDerivativeTest, self).__init__("Binary Derivative", 0.01, seq_length)

    def _execute(self,
                 bits: numpy.ndarray):
        """
        Overridden method of Test class: check its docstring for further information.
        """
        v0: numpy.ndarray = bits.copy()
        for i in range(self._derivative):
            original_vector : numpy.ndarray = v0[:bits.size - 1]
            shifted_vector: numpy.ndarray = numpy.roll(v0, -1)[:bits.size - 1]
            v0 = numpy.bitwise_xor(original_vector, shifted_vector)
        # Compute ones int result vector
        v0 = v0[:bits.size - self._derivative]
        ones: int = numpy.count_nonzero(v0)
        zeroes: int = v0.size - ones
        difference: int = (ones - zeroes)
        # Compute score
        score: float = math.erfc(float(abs(difference)) / (math.sqrt(float(v0.size)) * math.sqrt(2.0)))
	# Compute q_value
        q_value: float = math.erfc(float(difference) / (math.sqrt(float(v0.size)) * math.sqrt(2.0))) / 2.0
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))

    def __repr__(self) -> str:
        return f'{self.name} (d={self._derivative})'

