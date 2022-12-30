from gmt_random_test.test_unit.test_monobit import MonobitTest
from gmt_random_test.test_unit.test_cumulative_sums import CumulativeSumsTest
from gmt_random_test.test_unit.test_approximate_entropy import ApproximateEntropyTest
from gmt_random_test.test_unit.test_autocorrelation import AutocorrelationTest
from gmt_random_test.test_unit.test_binary_derivative import BinaryDerivativeTest
from gmt_random_test.test_unit.test_discrete_fourier_transform import DiscreteFourierTransformTest
from gmt_random_test.test_unit.test_frequency_within_block import FrequencyWithinBlockTest
from gmt_random_test.test_unit.test_longest_runs_in_a_block import LongestRunsInABlockTest
from gmt_random_test.test_unit.test_poker import PokerTest
from gmt_random_test.test_unit.test_runs import RunsTest
from gmt_random_test.test_unit.test_runs_distribution import RunsDistributionTest
from gmt_random_test.test_unit.test_serial import SerialTest

'''
        GM/T parameters for 20000bits binary sequences.
        This bits' size doesn't support Binary Matrix Rank Test, Universal Statistic Test, and Linear Complexity Test. 
'''
GMT_20000: dict = {
        "monobit": MonobitTest(),
        "frequency_within_block": FrequencyWithinBlockTest(1000),
        "poker_4": PokerTest(4),
        "poker_8": PokerTest(8),
        "serial_3": SerialTest(3),
        "serial_5": SerialTest(5),
        "runs": RunsTest(),
        "runs_distribution": RunsDistributionTest(20000),
        "longest_runs_in_a_block": LongestRunsInABlockTest(),
        "binary_derivative_3": BinaryDerivativeTest(3),
        "binary_derivative_7": BinaryDerivativeTest(7),
        "autocorrelation_2": AutocorrelationTest(2),
        "autocorrelation_8": AutocorrelationTest(8),
        "autocorrelation_16": AutocorrelationTest(16),
        "cumulative_sums": CumulativeSumsTest(),
        "approximate_entropy_2": ApproximateEntropyTest(2),
        "approximate_entropy_5": ApproximateEntropyTest(5),
        "discrete_fourier_transform": DiscreteFourierTransformTest()
}