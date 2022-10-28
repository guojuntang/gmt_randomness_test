import numpy
import math

# Import required src

from gmt_random_test import Test, Result


class AutocorrelationTest(Test):
    def __init__(self, shift: int = 1):
        # Generate base Test class
        self._shift = shift
        super(AutocorrelationTest, self).__init__("Autocorrelation", 0.01)

    def _execute(self,
                 bits: numpy.ndarray):
        """
        Overridden method of Test class: check its docstring for further information.
        """
        original_vector : numpy.ndarray = bits[:bits.size - self._shift]
        shifted_vector: numpy.ndarray = numpy.roll(bits, -self._shift)[:bits.size - self._shift]
        result_vector: numpy.ndarray = numpy.bitwise_xor(original_vector, shifted_vector)
        # Compute ones int result vector
        ones: int = numpy.count_nonzero(result_vector)

        tmp: float = 2 * (ones - (bits.size - self._shift) / 2.0)  / math.sqrt(bits.size - self._shift)
        # Compute score
        score: float = math.erfc(abs(tmp) / (math.sqrt(2.0)))
	    # Compute q_value
        q_value: float = math.erfc(tmp / (math.sqrt(2.0))) / 2.0
        # Return result
        if score >= self.significance_value:
            return Result(self.name, True, numpy.array([score]), numpy.array([q_value]))
        return Result(self.name, False, numpy.array([score]), numpy.array([q_value]))

    def is_eligible(self,
                    bits: numpy.ndarray) -> bool:
        """
        Overridden method of Test class: check its docstring for further information.
        """
        # This test is always eligible for any sequence
        return True

    def __repr__(self) -> str:
        return f'{self.name} (k={self._shift})'
