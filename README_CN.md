## 1. 简介

本项目用于检测二进制序列随机性，遵循 GM/T 0005-2021 "随机性检测规范"。

我们可以通过本项目对伪随机数生成器进行检测：用伪随机数生成器生成若干个二进制序列并检测所生成的随机数是否符合检测标准从而判断该伪随机生成器是否合格。

该测试规范总共包含15个测试单项。在每个测试单项中，我们会对每个样本计算对应的p_value，然后若得出的值大于或等于**0.01**则认为该样本合格。每个单项总共会检测**1000**个样本，若合格样本大于等于**981**个，则认为通过测试。除此以外，我们也会对每个测试项统计q_value，若所得值大于或等于**0.0001**，则通过测试。

对于每个待检测的二进制序列长度，国标文档中均有要求，并给出了对应的推荐参数。

检测的长度规模：2 * 10^4, 2 * 10^6, 2 * 10^8

### 1.1 测试单项
|| 测试项| |
|--|--| --|
| 单比特频数检测| 块内频数检测| 游程总数检测|
| 块内最大1游程检测| 矩阵秩检测| 离散傅里叶变换检测|
| Maurer通用统计检测| 线性复杂度检测| 重叠子序列检测|
| 近似熵检测| 累加和检测| 扑克检测|
| 游程分布检测| 二元推导检测| 自相关检测|

### 1.2 与NIST标准的不同

国标与NIST的随机数测试标准其实很多相似的地方，但也有不少不同的地方：

国标中的扑克检测，二元推导检测，自相关检测以及游程分布检测均为国标特有。而NIST中的Random Excursion Test， Random Excursion Variant Test，Non-overlapping Template Matching Test以及Overlapping Template Matching Test，在国标中均不作要求。

而且在最新版本的国标（GM/T 0005-2021）中，对q_value的计算以及样本规模都做了额外要求。

离散傅里叶变换检测和块内最大1游程检测，均在两个标准中。但是具体的参数变量有所不同，具体请参考源代码中的注释。

### 1.3 参考

https://github.com/dj-on-github/sp800_22_tests

https://github.com/InsaneMonster/NistRng

## 2. 如何使用

#### 运行环境： 

Python >= 3.9.0

#### 安装依赖：

```
pip install -r requirements.txt
```

#### 生成测试样例：

在进行测试前，我们需要准备好待测试的随机二进制序列。例如，我们现在需要检测**20000bits**的随机数，那么我们需要将**20000 * 1000**个bits写进二进制文件中。参考样例如下：

```python
import os 

with open("data_20000","wb") as f:
        for i in range(1000):
                f.write(os.urandom(2500))
                f.flush()
```

用户可自行替换所使用的伪随机数生成器。

#### 代码运行：

参考[样例](example.py)

```python
import numpy
# 导入测试库
from gmt_random_test.gmt_randomness_test import GmtRandomnessTest
from gmt_random_test.test import Result

if __name__ == "__main__":
    # 根据待测样本长度创建实例
    gmt_test: GmtRandomnessTest = GmtRandomnessTest(20000)
    # 选择不同的规模
    # gmt_test: GmtRandomnessTest = GmtRandomnessTest(1000000)
    # gmt_test: GmtRandomnessTest = GmtRandomnessTest(100000000)

    # 读取待测二进制串
    bits: numpy.ndarray = None
    with open("data/data_20000","rb") as f:
       bits = numpy.unpackbits(numpy.frombuffer(f.read(2500), dtype=numpy.uint8))
    # 运行所有测试
    gmt_test.run_all_battery_with_bits(bits)
    # 用测试名作为输入
    gmt_test.run_by_name_with_bits(bits, "serial_3")
    gmt_test.run_by_name_with_bits(bits, "serial_5")
    # 通过文件作为待测样本的输入
    gmt_test.run_all_battery_with_file("data/data_20000")
```

#### 单元测试：

详细参考[测试源文件](tests.py)

### 3. 测试样例

[20000bits](data/data_20000)样例：

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