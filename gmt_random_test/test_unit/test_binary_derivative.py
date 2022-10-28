import numpy
import math


from gmt_random_test import Test, Result


class BinaryDerivativeTest(Test):
    def __init__(self, derivative: int = 1):
        # Generate base Test class
        self._derivative = derivative
        super(BinaryDerivativeTest, self).__init__("Binary Derivative", 0.01)

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

    def is_eligible(self,
                    bits: numpy.ndarray) -> bool:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # This test is always eligible for any sequence
        return True
