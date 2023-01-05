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

def pack_sequence(sequence: numpy.ndarray) -> numpy.ndarray:
    """
    Pack a sequence of signed integers to its binary 8-bit representation using numpy.
    :param sequence: the integer sequence to pack (in the form of a numpy array, ndarray)
    :return: the sequence packed in 8-bit integer in the form of a numpy array (ndarray)
    """
    return numpy.unpackbits(numpy.array(sequence, dtype=numpy.uint8)).astype(numpy.int8)

def pack_01str(sequence: numpy.ndarray) -> numpy.ndarray:
    return numpy.fromstring(sequence ,'u1') - ord('0')