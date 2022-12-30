# Import packages

import numpy
import time


# Define result class

class Result:
    """
    Wrapper class for test results.
    Attributes:
        - name: the name of the test giving the result
        - passed: whether or not the test in hand was passed.
        - score: the score (p value) resulting from the test in hand (in some test, there will be more than one p values).
        - q_value: the q value result (in some test, there will be more than one q values).
    """

    def __init__(self,
                 test_name: str,
                 success: bool, score_list: numpy.ndarray, q_value_list: numpy.ndarray):
        self._test_name: str = test_name
        self._success: bool = success
        self._score_list: numpy.ndarray = score_list
        self._q_value_list: numpy.ndarray = q_value_list

    def __repr__(self) -> str:
        return f'name: {self.name}; score: {self._score_list}; q_value: {self._q_value_list}; pass: {self.passed}'

    @property
    def name(self) -> str:
        return self._test_name

    @property
    def passed(self) -> bool:
        return self._success

    @property
    def score(self) -> numpy.ndarray:
        return self._score_list

    @property
    def q_value(self) -> numpy.ndarray:
        return self._q_value_list


# Define base abstract test class

class Test:
    """
    Base test class to represent all test as described in the GM/T 005-2021.
    When run, the test returns one or multiple scores and a result flag wrapped in a Result object.
    Each score is a P-value, which is the probability that a true random number generator would produce a worse result in the test
    than the one computed on the sequence of bits given as parameter. If each P-value is greater than the significance value for the
    test it means that the sequence appears to be random.
    Attributes:
        - significance_value: represent the threshold value for the score.
    """

    def __init__(self,
                 name: str,
                 significance_value: float):
        self.name: str = name
        self.significance_value: float = significance_value

    def _execute(self,
                 bits: numpy.ndarray) -> Result:
        """
        Execute the test returning a Result object upon completion.
        :param bits: the sequence of bits on which to run the test, wrapped in a numpy array (ndarray)
        :return: a Result object stating the outcome of the test
        """
        # Abstract method, definition should be implemented on a child class basis
        raise NotImplementedError()

    def run(self,
            bits: numpy.ndarray):
        """
        Run the test on the given sequence of bits, returning a Result object and the elapsed time upon completion.
        :param bits: the sequence of bits on which to run the test, wrapped in a numpy array (ndarray)
        :return: a Result object stating the outcome of the test and the elapsed time in milliseconds
        """
        start_time: int = int(round(time.time() * 1000))
        result: Result = self._execute(bits)
        end_time: int = int(round(time.time() * 1000))
        return result, end_time - start_time

    def is_eligible(self,
                    bits: numpy.ndarray) -> bool:
        """
        Check whether or not the given sequence of bits is eligible for the test.
        :param bits: the sequence of bits for which to check test eligibility, wrapped in a numpy array (ndarray)
        :return: a boolean flag stating the eligibility or not of the test
        """
        # Abstract method, definition should be implemented on a child class basis
        raise NotImplementedError()