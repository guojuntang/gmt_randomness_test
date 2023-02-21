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
from gmt_random_test.test_unit.test_linear_complexity import LinearComplexityTest
from gmt_random_test.test_unit.test_maurers_universal import MaurersUniversalTest
from gmt_random_test.test_unit.test_binary_matrix_rank import BinaryMatrixRankTest

'''
        GM/T parameters for 20000bits binary sequences.
        This size of tests doesn't support Binary Matrix Rank Test, Universal Statistic Test, and Linear Complexity Test. 
'''
GMT_20000: dict = {
        "monobit": MonobitTest(20000),
        "frequency_within_block": FrequencyWithinBlockTest(20000, 1000),
        "poker_4": PokerTest(20000, 4),
        "poker_8": PokerTest(20000, 8),
        "serial_3": SerialTest(20000, 3),
        "serial_5": SerialTest(20000, 5),
        "runs": RunsTest(20000),
        "runs_distribution": RunsDistributionTest(20000),
        "longest_runs_in_a_block": LongestRunsInABlockTest(20000),
        "binary_derivative_3": BinaryDerivativeTest(20000, 3),
        "binary_derivative_7": BinaryDerivativeTest(20000, 7),
        "autocorrelation_2": AutocorrelationTest(20000, 2),
        "autocorrelation_8": AutocorrelationTest(20000, 8),
        "autocorrelation_16": AutocorrelationTest(20000, 16),
        "cumulative_sums": CumulativeSumsTest(20000),
        "approximate_entropy_2": ApproximateEntropyTest(20000, 2),
        "approximate_entropy_5": ApproximateEntropyTest(20000, 5),
        "discrete_fourier_transform": DiscreteFourierTransformTest(20000)
}


GMT_1000000: dict = {
        "monobit": MonobitTest(1000000),
        "frequency_within_block": FrequencyWithinBlockTest(1000000, 10000),
        "poker_4": PokerTest(1000000, 4),
        "poker_8": PokerTest(1000000, 8),
        "serial_3": SerialTest(1000000, 3),
        "serial_5": SerialTest(1000000, 5),
        "runs": RunsTest(1000000),
        "runs_distribution": RunsDistributionTest(1000000),
        "longest_runs_in_a_block": LongestRunsInABlockTest(1000000),
        "binary_derivative_3": BinaryDerivativeTest(1000000, 3),
        "binary_derivative_7": BinaryDerivativeTest(1000000, 7),
        "autocorrelation_1": AutocorrelationTest(1000000, 1),
        "autocorrelation_2": AutocorrelationTest(1000000, 2),
        "autocorrelation_8": AutocorrelationTest(1000000, 8),
        "autocorrelation_16": AutocorrelationTest(1000000, 16),
        "cumulative_sums": CumulativeSumsTest(1000000),
        "approximate_entropy_2": ApproximateEntropyTest(1000000, 2),
        "approximate_entropy_5": ApproximateEntropyTest(1000000, 5),
        "discrete_fourier_transform": DiscreteFourierTransformTest(1000000),
        "linear_complexity_500": LinearComplexityTest(1000000, 500),
        "linear_complexity_1000": LinearComplexityTest(1000000, 1000),
        "maurers_universal": MaurersUniversalTest(1000000),
        "binary_matrix": BinaryMatrixRankTest(1000000)
}

# GMT_100000000: dict = {
#         "monobit": MonobitTest(100000000),
#         "frequency_within_block": FrequencyWithinBlockTest(100000000, 100000),
#         "poker_4": PokerTest(100000000, 4),
#         "poker_8": PokerTest(100000000, 8),
#         "serial_3": SerialTest(100000000, 3),
#         "serial_5": SerialTest(100000000, 5),
#         "serial_7": SerialTest(100000000, 7),
#         "runs": RunsTest(100000000),
#         "runs_distribution": RunsDistributionTest(100000000),
#         "longest_runs_in_a_block": LongestRunsInABlockTest(100000000),
#         "binary_derivative_3": BinaryDerivativeTest(100000000, 3),
#         "binary_derivative_7": BinaryDerivativeTest(100000000, 7),
#         "binary_derivative_15": BinaryDerivativeTest(100000000, 15),
#         "autocorrelation_1": AutocorrelationTest(100000000, 1),
#         "autocorrelation_2": AutocorrelationTest(100000000, 2),
#         "autocorrelation_8": AutocorrelationTest(100000000, 8),
#         "autocorrelation_16": AutocorrelationTest(100000000, 16),
#         "autocorrelation_32": AutocorrelationTest(100000000, 32),
#         "cumulative_sums": CumulativeSumsTest(100000000),
#         "approximate_entropy_5": ApproximateEntropyTest(100000000, 5),
#         "approximate_entropy_7": ApproximateEntropyTest(100000000, 7),
#         "discrete_fourier_transform": DiscreteFourierTransformTest(100000000),
#         "linear_complexity": LinearComplexityTest(100000000, 5000),
#         "maurers_universal": MaurersUniversalTest(100000000),
#         "binary_matrix": BinaryMatrixRankTest(100000000)
# }