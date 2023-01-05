## 1. 简介

本项目用于检测二进制序列随机性，遵循 GM/T 0005-2021 "随机性检测规范"。

我们可以通过本项目对伪随机数生成器进行检测：用伪随机数生成器生成若干个二进制序列并检测所生成的随机数是否符合检测标准从而判断该伪随机生成器是否合格。

该测试规范总共包含15个测试单项。在每个测试单项中，我们会对每个样本计算对应的p_value，然后若得出的值大于或等于**0.01**则认为该样本合格。每个单项总共会检测**1000**个样本，若合格样本大于等于981个，则认为通过测试。除此以外，我们也会对每个测试项统计q_value，若所得值大于或等于**0.0001**，则通过测试。

对于每个待检测的二进制序列长度，国标文档中均有要求，并给出了对应的推荐参数。

本项目暂时仅直持20000bits的检测，1000000和100000000的规模仍在调试当中。

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
    # 根据待测样本大小创建实例
    gmt_test: GmtRandomnessTest = GmtRandomnessTest(20000)

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

TODO data_20000 result 20000