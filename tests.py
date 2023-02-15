import numpy
from gmt_random_test.functions import pack_01str, pack_sequence
from gmt_random_test.qvalues import QValueCollector
from gmt_random_test.test import Result
from gmt_random_test.test_unit.test_approximate_entropy import ApproximateEntropyTest
from gmt_random_test.test_unit.test_autocorrelation import AutocorrelationTest
from gmt_random_test.test_unit.test_binary_derivative import BinaryDerivativeTest
from gmt_random_test.test_unit.test_binary_matrix_rank import BinaryMatrixRankTest
from gmt_random_test.test_unit.test_cumulative_sums import CumulativeSumsTest
from gmt_random_test.test_unit.test_discrete_fourier_transform import DiscreteFourierTransformTest
from gmt_random_test.test_unit.test_frequency_within_block import FrequencyWithinBlockTest
from gmt_random_test.test_unit.test_linear_complexity import LinearComplexityTest
from gmt_random_test.test_unit.test_longest_runs_in_a_block import LongestRunsInABlockTest
from gmt_random_test.test_unit.test_maurers_universal import MaurersUniversalTest
from gmt_random_test.test_unit.test_monobit import MonobitTest
from gmt_random_test.test_unit.test_poker import PokerTest
from gmt_random_test.test_unit.test_runs import RunsTest
from gmt_random_test.test_unit.test_runs_distribution import RunsDistributionTest
from gmt_random_test.test_unit.test_serial import SerialTest

monobit_test_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
frequency_within_block_seq = "1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000"
runs_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
sums_seq = "1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000"
entropy_seq = "1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000"
fourier_seq = "1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000"
poker_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
auto_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
derivative_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
serial_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
runs_dist_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"
longest_runs_seq = "11001100000101010110110001001100111000000000001001001101010100010001001111010110100000001101011111001100111001101101100010110010"

q_values_list = [0.05, 0.05, 0.15, 0.15, 0.15, 0.15, 0.15, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.45, 0.45, 0.55, 0.55, 0.55, 0.55, 0.55, 0.65, 0.65, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.95, 0.95]


if __name__ == "__main__":
        result : Result = None
        time: int = 0

        '''
        Monobit test
        '''
        monobit_test: MonobitTest = MonobitTest(len(monobit_test_seq))
        result ,time = monobit_test.run(pack_01str(monobit_test_seq))
        print(result)

        '''
        Frequency within block test
        '''
        frequency_test: FrequencyWithinBlockTest = FrequencyWithinBlockTest(len(frequency_within_block_seq), 10)
        result, time = frequency_test.run(pack_01str(frequency_within_block_seq))
        print(result)

        '''
        Serial test
        '''
        serial_test: SerialTest = SerialTest(len(serial_seq), 2)
        result, time = serial_test.run(pack_01str(serial_seq))
        print(result)

        '''
        Poker test
        '''
        poker_test: PokerTest = PokerTest(len(poker_seq), 4)
        result, time = poker_test.run(pack_01str(poker_seq))
        print(result)

        '''
        Autocorrelation test
        '''
        auto_test: AutocorrelationTest = AutocorrelationTest(len(auto_seq), 1)
        result, time = auto_test.run(pack_01str(auto_seq))
        print(result)

        '''
        Autocorrelation test
        '''
        derivative_test: BinaryDerivativeTest = BinaryDerivativeTest(len(derivative_seq), 3)
        result, time = derivative_test.run(pack_01str(derivative_seq))
        print(result)

        '''
        Runs test
        '''
        runs_test: RunsTest = RunsTest(len(runs_seq))
        result, time = runs_test.run(pack_01str(runs_seq))
        print(result)

        '''
        Runs Distribution test
        '''
        runs_dist_test: RunsDistributionTest = RunsDistributionTest(len(runs_dist_seq), 128)
        result, time = runs_dist_test.run(pack_01str(runs_dist_seq))
        print(result)

        '''
        Longest runs in a block test
        '''
        longest_runs_test: LongestRunsInABlockTest = LongestRunsInABlockTest(len(longest_runs_seq))
        result, time = longest_runs_test.run(pack_01str(longest_runs_seq))
        print(result)

        '''
        cumulative sums test
        '''
        sums_test: CumulativeSumsTest = CumulativeSumsTest(len(sums_seq))
        result, time = sums_test.run(pack_01str(sums_seq))
        print(result)

        '''
        approximate entropy test
        '''
        entropy_test: ApproximateEntropyTest = ApproximateEntropyTest(len(entropy_seq), 2)
        result, time = entropy_test.run(pack_01str(entropy_seq))
        print(result)

        '''
        discrete fourier transform test
        '''
        fourier_test: DiscreteFourierTransformTest = DiscreteFourierTransformTest(len(fourier_seq))
        result, time = fourier_test.run(pack_01str(fourier_seq))
        print(result)

        e: str = ""
        with open("data/data.e", "rt") as f:
                e = f.read()
                f.close()
        
        #'''
        #Maurer's universal test
        #'''
        universal_test: MaurersUniversalTest = MaurersUniversalTest(len(e))
        result, time = universal_test.run(pack_01str(e))
        print(result)

        '''
        Linear Complexity test
        '''
        complexity_test: LinearComplexityTest = LinearComplexityTest(len(e), 1000)
        result, time = complexity_test.run(pack_01str(e))
        print(result)

        '''
        Binary matrix rank test
        '''
        matrix_test: BinaryMatrixRankTest = BinaryMatrixRankTest(len(e))
        result, time = matrix_test.run(pack_01str(e))
        print(result)

        '''
        q values test
        '''
        print(QValueCollector.compute_value(numpy.array(q_values_list), 10))
