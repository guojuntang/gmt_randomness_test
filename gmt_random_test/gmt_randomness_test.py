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

import numpy
import math
import os
from gmt_random_test.qvalues import QValueCollector

from gmt_random_test.test import Result, Test
from .config import *
class GmtRandomnessTest():

    def __init__(self, bits_length: int, intervals_num: int=10):
        self._bits_length = bits_length
        self._intervals_num = intervals_num
        if bits_length == 20000:
            self._battery = GMT_20000
        elif bits_length == 1000000:
            self._battery = GMT_1000000
        elif bits_length == 100000000:
            self._battery == GMT_100000000
        else:
            raise RuntimeError("inapplicable bits length.")

    def _run_single_test(self, bits: numpy.ndarray, test_unit: Test):
        return test_unit.run(bits)

    def run_by_name_with_bits(self, bits: numpy.ndarray, name: str):
        result: Result = None
        time: int = 0

        try:
            test_unit: Test = self._battery[name]
        except:
            print("Unknown test name.")

        print(f'Test name: {test_unit}')
        result, time = self._run_single_test(bits, test_unit)
        print(result)
        

    def run_all_battery_with_bits(self, bits: numpy.ndarray):
        result: Result = None
        time: int = 0
        for test_unit in self._battery.values():
            print(f'Test name: {test_unit}')
            result, time = self._run_single_test(bits, test_unit)
            print(result)
    
    def _read_sequences_from_file(self, file_name: str, sample_size: int):
        buffer_size: int = self._bits_length // 8
        f = open(file_name, "rb")
        sequences = []
        for i in range(sample_size):
            sequences.append(numpy.frombuffer(f.read(buffer_size), dtype=numpy.uint8))
        f.close()
        return sequences

    def run_battery_by_names_with_file(self, file_name: str, test_names):
        file_size: int = os.path.getsize(file_name)
        samples_size: int = file_size // (self._bits_length // 8)
        sequences = self._read_sequences_from_file(file_name, samples_size)
        battery: dict = {k: v for k, v in self._battery.items() if k in test_names}
        self._run_battery(sequences, battery)

    def _run_battery(self, sequences, battery: dict):
        result: Result = None
        time: int = 0
        samples_size: int = len(sequences)
        # TODO print format
        print(f'GMT randomness test (samples size: {samples_size})')
        print("Types of test: \t\t\tPasses: \tDistribution:")
        for test_unit in battery.values():
            # todo two q value lists
            q_value_list = []
            q_value_list1 = []
            passes: int = 0
            for seq in sequences:
                bits: numpy.ndarray = numpy.unpackbits(seq)
                result, time = self._run_single_test(bits, test_unit)
                passes += 1 if result.passed else 0
                if result.q_value.size == 2:
                    q_value_list.append(result.q_value[0])
                    q_value_list1.append(result.q_value[1])
                else:
                    q_value_list.append(result.q_value[0])

            if q_value_list1 != []:
                q_value_score1: float = QValueCollector.compute_value(numpy.array(q_value_list1), self._intervals_num, samples_size)
                q_value_score: float = QValueCollector.compute_value(numpy.array(q_value_list), self._intervals_num, samples_size)
                print(f'{test_unit} \t\t\t{passes} \t{q_value_score}, {q_value_score1}')
            else:
                q_value_score: float = QValueCollector.compute_value(numpy.array(q_value_list), self._intervals_num, samples_size)
                print(f'{test_unit} \t\t\t{passes} \t{q_value_score}')


    
    def run_all_battery_with_file(self, file_name: str):
        file_size: int = os.path.getsize(file_name)
        samples_size: int = file_size // (self._bits_length // 8)
        sequences = self._read_sequences_from_file(file_name, samples_size)
        self._run_battery(sequences, self._battery)
