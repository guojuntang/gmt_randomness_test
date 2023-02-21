import numpy
# import our libs
from gmt_random_test.gmt_randomness_test import GmtRandomnessTest
from gmt_random_test.functions import pack_01str
from gmt_random_test.test import Result

if __name__ == "__main__":
    # create the test instance with the sample size
    # gmt_test: GmtRandomnessTest = GmtRandomnessTest(20000)
    # also you can choose other sizes 
    gmt_test: GmtRandomnessTest = GmtRandomnessTest(1000000)
    # gmt_test: GmtRandomnessTest = GmtRandomnessTest(100000000)

    # read binary sequences
    bits: numpy.ndarray = None
   #  with open("data/data_20000","rb") as f:
   #    bits = numpy.unpackbits(numpy.frombuffer(f.read(2500), dtype=numpy.uint8))
    e: str = ""
    with open("data/data.e", "rt") as f:
      e = f.read()
      f.close()
    bits = pack_01str(e)
   
    # run all tests   
    gmt_test.run_all_battery_with_bits(bits)
    # run tests by name
    gmt_test.run_by_name_with_bits(bits, "serial_3")
    gmt_test.run_by_name_with_bits(bits, "serial_5")
    # file as input
    gmt_test.run_all_battery_with_file("data/data_20000")
    # gmt_test.run_battery_by_names_with_file("data/data_20000", ["serial_3", "serial_5", "longest_runs_in_a_block", "cumulative_sums"])
