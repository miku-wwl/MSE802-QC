# Week 1: 量子计算入门与 Qiskit 基础

## 知识点标题
- 量子计算简介 (Introduction to Quantum Computing)
- Qiskit 环境搭建与基本使用
- 量子比特 (Qubit) 与量子电路 (Quantum Circuit)

---

## 核心概念

### 1. 什么是量子计算？
量子计算是一种利用**量子力学原理**（如叠加态和纠缠态）进行信息处理的计算范式。与传统经典计算的比特（0或1）不同，**量子比特（Qubit）**可以同时处于0和1的**叠加态（Superposition）**。

### 2. Qiskit 简介
Qiskit 是 IBM 开发的开源 **Python 量子计算框架**，用于：
- 构建**量子电路**
- 在**模拟器**或**真实量子计算机**上运行
- 可视化和分析量子态

### 3. 量子比特 vs 经典比特

| 特征 | 经典比特 | 量子比特 |
|------|---------|---------|
| 取值 | 0 或 1 | $|0\rangle$, $|1\rangle$ 或其叠加 |
| 测量 | 确定性 | 概率性 |
| 并行性 | 无 | 天然并行 |

### 4. 量子电路的基本组成
- **QuantumRegister**: 量子寄存器，存储量子比特
- **ClassicalRegister**: 经典寄存器，存储测量结果
- **QuantumCircuit**: 量子电路对象
- **Gate**: 量子门操作（如 H, X, Y, Z 门）
- **Measurement**: 测量操作

---

## 公式

### 量子态的一般形式（单量子比特）
$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

其中 $\alpha, \beta \in \mathbb{C}$（复数），且满足**归一化条件**：
$$|\alpha|^2 + |\beta|^2 = 1$

$|\alpha|^2$ 表示测量得到 $|0\rangle$ 的概率，$|\beta|^2$ 表示测量得到 $|1\rangle$ 的概率。

### 基态的向量表示
$$|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad |1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$$

---

## 代码示例说明

### 示例1: 创建第一个量子电路

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 创建量子电路: 1个量子比特, 1个经典比特
qc = QuantumCircuit(1, 1)

# 测量
qc.measure(0, 0)

# 绘制电路图
print(qc.draw())

# 使用Aer模拟器运行
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts(qc)

print("测量结果:", counts)
plot_histogram(counts)
plt.show()
```

**说明**: 此例创建最简单的量子电路，初始态为 $|0\rangle$，测量后始终得到 `'0'`。

### 示例2: Hadamard门 — 创建叠加态

```python
qc = QuantumCircuit(1, 1)

# 应用Hadamard门, 将|0>变为 (|0>+|1>)/sqrt(2)
qc.h(0)

qc.measure(0, 0)

simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts(qc)

print("测量结果:", counts)  # 预期约 {'0': ~512, '1': ~512}
plot_histogram(counts)
```

**说明**: H门将量子比特从基态变为**等概率叠加态**，测量结果接近50%-50%分布。

### 示例3: X门（量子非门 / Pauli-X）

```python
qc = QuantumCircuit(1, 1)

# X门将|0>变为|1>, 类似经典NOT门
qc.x(0)

qc.measure(0, 0)

# 运行并显示结果...
```

**说明**: X门的作用等同于经典的**NOT门**，翻转量子比特状态。

---

## 课后练习要点

1. **理解量子叠加态**: 为什么Hadamard门作用后的量子比特测量结果是随机的？
2. **Qiskit环境配置**: 成功安装Qiskit和Aer模拟器
3. **shots参数含义**: 理解`shots=1024`表示重复测量的次数，影响统计结果的精度
4. **绘制电路图**: 学会使用 `qc.draw()` 和 `draw(output='mpl')`
5. **直方图解读**: 理解`plot_histogram`输出的含义

---

## 关键术语表

| 术语 | 英文 | 含义 |
|------|------|------|
| 量子比特 | Qubit | 量子信息的基本单位 |
| 叠加态 | Superposition | 同时处于多个状态 |
| 量子门 | Quantum Gate | 对量子比特的操作 |
| 测量 | Measurement | 坍缩量子态获得经典结果 |
| 量子电路 | Quantum Circuit | 由量子门组成的计算流程 |
| 模拟器 | Simulator | 经典计算机上模拟量子行为 |
