# Week 3: 量子态向量、概率振幅与 Dirac 符号

## 知识点标题
- 态向量 (State Vector) 的数学表示
- Dirac 符号 (Ket-Bra Notation)
- 概率振幅 (Probability Amplitudes)
- 多量子比特系统与张量积

---

## 核心概念

### 1. 量子态向量
量子态是一个**归一化的复数向量**，属于希尔伯特空间 (Hilbert Space)。对于 $n$ 个量子比特的系统，态向量维度为 $2^n$。

### 2. Dirac 符号系统
Dirac符号（也称 bra-ket 符号）是量子力学中描述量子态的标准记号：

| 符号 | 名称 | 数学含义 | 示例 |
|------|------|---------|------|
| $\ket{\psi}$ | Ket（右矢/列向量） | 量子态本身 | $\ket{\psi} = \begin{pmatrix}\alpha \\ \beta\end{pmatrix}$ |
| $\bra{\psi}$ | Bra（左矢/行向量） | Ket的共轭转置 | $\bra{\psi} = (\alpha^*, \beta^*)$ |
| $\braket{\psi|\phi}$ | 内积 | 复数标量（概率振幅相关） | $\braket{0|1} = 0$ |
| $\ket{\psi}\bra{\phi}$ | 外积 | 算符/矩阵 | $\ket{0}\bra{1} = \begin{pmatrix}0&1\\0&0\end{pmatrix}$ |

### 3. 概率振幅
- 量子态展开式中每个基态前的**复系数**称为**概率振幅**
- 振幅的**模平方**等于测量得到对应结果的**概率**
- 振幅可以是负数或复数（包含**相位信息**）

### 4. 计算基 (Computational Basis)
对于 $n$ 量子比特系统，有 $2^n$ 个基态：

- 1量子比特: $\{|0\rangle, |1\rangle\}$
- 2量子比特: $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$
- 3量子比特: $\{|000\rangle, |001\rangle, ..., |111\rangle\}$

---

## 公式

### 单量子比特态的一般形式
$$\ket{\psi} = \alpha\ket{0} + \beta\ket{1} = \begin{pmatrix}\alpha \\ \beta\end{pmatrix}, \quad |\alpha|^2 + |\beta|^2 = 1$$

### 双量子比特态的一般形式（无纠缠）
$$\ket{\psi} = \alpha_{00}\ket{00} + \alpha_{01}\ket{01} + \alpha_{10}\ket{10} + \alpha_{11}\ket{11}$$

满足归一化: $\sum_i |\alpha_i|^2 = 1$

### 张量积 (Tensor Product / Kronecker Product)
两个量子系统的组合态用张量积表示：

$$\ket{\psi}_A \otimes \ket{\phi}_B = \ket{\psi\phi}_{AB}$$

具体例子:
$$\ket{0} \otimes \ket{1} = \ket{01} = \begin{pmatrix}1\\0\end{pmatrix} \otimes \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}0\\1\\0\\0\end{pmatrix}$$

$$\left(\frac{\ket{0}+\ket{1}}{\sqrt{2}}\right) \otimes \ket{0} = \frac{\ket{00}+\ket{10}}{\sqrt{2}}$$

### 内积的性质
- $\braket{i|j} = \delta_{ij}$ （正交归一性）
- $\braket{\psi|\psi} = 1$ （归一化）

---

## 代码示例说明

### 示例1: 获取和显示态向量

```python
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

# 创建|0>态
qc = QuantumCircuit(1)
state0 = Statevector.from_instruction(qc)
print("|0> 态向量:", state0.data)
# 输出: [1.+0.j 0.+0.j] 即 [1, 0]^T

# 应用H门后的态
qc.h(0)
state_plus = Statevector.from_instruction(qc)
print("|+> 态向量:", state_plus.data)
# 输出: [0.70710678+0.j 0.70710678+0.j] 即 [1/sqrt(2), 1/sqrt(2)]^T

# 绘制态向量（qsphere可视化）
from qiskit.visualization import plot_state_qsphere
plot_state_qsphere(state_plus)
```

**说明**: `Statevector.from_instruction()` 从电路中提取完整的量子态向量。`.data`属性返回numpy数组形式的振幅。

### 示例2: 概率与概率振幅的关系

```python
import numpy as np

# 手动定义一个量子态
amplitude_0 = 1/np.sqrt(3)
amplitude_1 = np.sqrt(2/3)   # 注意：也可以是复数，如 (1+1j)/sqrt(3)

psi = np.array([amplitude_0, amplitude_1])

probabilities = np.abs(psi)**2
print(f"振幅: {psi}")
print(f"概率: {probabilities}")     # [|α|², |β|²]
print(f"概率之和: {sum(probabilities)}")  # 必须等于1
```

### 示例3: 多量子比特系统的态向量

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# 两量子比特系统
qc2 = QuantumCircuit(2)
qc2.h(0)       # 第一个量子比特施加H门
qc2.h(1)       # 第二个量子比特也施加H门

state2 = Statevector.from_instruction(qc2)
print("两量子比特态向量 (维度=4):")
print(state2.data)
# 输出: [0.5, 0.5, 0.5, 0.5]
# 对应: 0.5|00> + 0.5|01> + 0.5|10> + 0.5|11>

print(f"概率分布:")
for i, amp in enumerate(state2.data):
    print(f"  |{format(i, '02b')}>: 振幅={amp:.4f}, 概率={abs(amp)**2:.4f}")
```

### 示例4: 使用 probs() 方法获取概率

```python
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)   # CNOT门，产生纠缠态

sv = Statevector.from_instruction(qc)
probs = sv.probabilities_dict()
print("测量概率:", probs)
# 对于Bell态 (|00>+|11>)/√2, 输出类似: {'00': 0.5, '11': 0.5}
```

---

## 课后练习要点

1. **手动计算内积**: 给定 $\ket{\psi} = \frac{1}{\sqrt{2}}(\ket{0} + \ket{1})$ 和 $\ket{\phi} = \frac{1}{\sqrt{2}}(\ket{0} - \ket{1})$，计算 $\braket{\psi|\phi}$
2. **张量积运算**: 计算 $(a\ket{0}+b\ket{1}) \otimes (c\ket{0}+d\ket{1})$ 展开结果
3. **验证归一化**: 对于任意量子态，验证所有概率振幅模平方和为1
4. **理解相位的影响**: 比较 $\frac{\ket{0}+\ket{1}}{\sqrt{2}}$ 和 $\frac{\ket{0}-\ket{1}}{\sqrt{2}}$ —— 概率相同但物理意义不同
5. **多量子比特维度**: 3个量子比特的态向量有多少维？4个呢？总结规律
6. **实验探索**: 使用Qiskit创建不同的量子电路，观察态向量的变化
