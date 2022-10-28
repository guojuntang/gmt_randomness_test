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