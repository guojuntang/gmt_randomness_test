# 1. Introduction

This repo is an implementation of GM/T 0005-2021, a randomness testing standard in China.

The Chinese version's document is available [here](README_CN.md).

We can use it to test a random number generator (RNG): if most random numbers generated by the RNG pass the test suite, we can consider this RNG reliable.

This work includes 15 test units. We will compute the p_value for each sample in each test unit, if the given value is equal or greater than **0.01**, we may consider this sample passes the test unit. Total, the number of samples is **1000**, and there should be more than **981** samples passing the test if the RNG is reliable. In addition, we also compute the q_value for each test unit, in which the significant value should be **0.0001**.

The GM/T document defines the recommended length for the sample bits and the corresponding parameters. Available sizes: 2 * 10^4, 10^6 and 10^8.

### 1.1 Test units


|| Test unit| |
|--|--| --|
| Monobit Test| Frequency Test within a block| Runs Test|
| Test for the longest Run of Ones in a block| Binary Matrix Rank Test| Discrete Fourier Transform  Test|
| Maurer's "Universal Statistical" Test| Linear Complexity Test| Serial Test|
| Approximate Entropy Test| Cumulative Test| Poker Test|
| Runs Distribution Test| Binary Derivative Test| Autocorrelation Test|


### 1.2 Difference between NIST and GM/T

Both the NIST standard and the GM/T standard require very similar test units. However, Poker test, Runs distribution test, Binary derivative test, and Autocorrelation test are only available in GM/T standard, while Excursion Test, Random Excursion Variant Test,Non-overlapping Template Matching Test, and Overlapping Template Matching Test are only available in NIST standards.


The GM/T standard also requires the q_value and the sample size.


Also, there are some different parameters in the discrete Fourier transform test and the test for the longest run of ones in a block. Please check comments in source codes for details.

### 1.3 References


https://github.com/dj-on-github/sp800_22_tests

https://github.com/InsaneMonster/NistRng

https://github.com/stevenang/randomness_testsuite

## 2. Usage

### Execution Environment

Python >= 3.9.0

### Requirements

```
pip install -r requirements.txt
```

### Generating tested samples

We need to generate tested random numbers and write them into a binary file before we run the script. Example here:

```python
import os 

with open("data_20000","wb") as f:
        for i in range(1000):
                f.write(os.urandom(2500))
                f.flush()
```

Users can use your own RNG.

### Execution

[Example](example.py)
```python
import numpy
# import our libs
from gmt_random_test.gmt_randomness_test import GmtRandomnessTest
from gmt_random_test.test import Result

if __name__ == "__main__":
    # create the test instance with the sample size
    gmt_test: GmtRandomnessTest = GmtRandomnessTest(20000)
    # also you can choose other sizes 
    # gmt_test: GmtRandomnessTest = GmtRandomnessTest(1000000)
    # gmt_test: GmtRandomnessTest = GmtRandomnessTest(100000000)

    # read binary sequences
    bits: numpy.ndarray = None
    with open("data/data_20000","rb") as f:
       bits = numpy.unpackbits(numpy.frombuffer(f.read(2500), dtype=numpy.uint8))
    # run all tests   
    gmt_test.run_all_battery_with_bits(bits)
    # run tests by name
    gmt_test.run_by_name_with_bits(bits, "serial_3")
    gmt_test.run_by_name_with_bits(bits, "serial_5")
    # file as input
    gmt_test.run_all_battery_with_file("data/data_20000")
```

#### Unit Test:

Please check the [test file](tests.py).

### 3. Results

[20000-bits](data/data_20000)

```
GMT randomness test (samples size: 1000)
Types of test:  Passes:         Distribution:
Monobit         992     0.19376653751100414
Frequency Within Block (m=1000)         993     0.6287904561747886
Poker (m=4)     992     0.9774801795691433
Poker (m=8)     983     0.010988016145239969
Runs)   989     0.5810821521175091
RunsDistribution)       989     0.6204652616810549
Binary Derivative (d=3)         994     0.8628831961771974
Binary Derivative (d=7)         989     0.35864134122843766
Autocorrelation (k=2)   987     0.5523828823144027
Autocorrelation (k=8)   990     0.5081718433121454
Autocorrelation (k=16)  991     0.004085375625386839
Approximate Entropy (m=2)       990     0.7791877161648364
Approximate Entropy (m=5)       996     0.5261047121948592
Discrete Fourier Transform                      991     0.12961959133276194
Serial (m=3)                    985     0.8891175958894987, 0.33768835649023937
Serial (m=5)                    984     0.03756608354257083, 0.6371194071693984
Longest Runs In A Block                         983     0.18555523463043544, 0.9929519746920032
Cumulative Sums                         991     0.8237245548918524, 0.4559371952206618
```