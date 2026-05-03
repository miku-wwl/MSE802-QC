# Week 5: 量子逻辑门与多量子比特系统

## 知识点标题
- 单量子比特门深入：X, S, T, sqrt(NOT), 旋转门
- 多量子比特门：CNOT (CX), CCX (Toffoli), SWAP
- 张量积 (Tensor Product) 的实现与应用
- 量子纠缠 (Entanglement) 与 Bell 态
- 通用量子门集 (Universal Gate Set)

---

## 核心概念

### 1. 量子门分类
量子门分为两类：

| 类型 | 作用范围 | 示例 |
|------|---------|------|
| **单量子比特门** | 作用于单个量子比特 | X, Y, Z, H, S, T, Rx, Ry, Rz |
| **多量子比特门** | 作用于多个量子比特 | CNOT(CX), CZ, SWAP, CCX(Toffoli) |

**关键特性**: 所有量子门都是**可逆的**（幺正矩阵），即 $U^\dagger U = I$。

### 2. 单量子比特门详解

#### X门 (NOT门 / Pauli-X)
$$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$
作用: 比特翻转, $X|0\rangle = |1\rangle$, $X|1\rangle = |0\rangle$

#### sqrt(NOT) 门 ($\sqrt{X}$ 门)
$$\sqrt{X} = \frac{1}{2}\begin{pmatrix} 1+i & 1-i \\ 1-i & 1+i \end{pmatrix} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -i \\ -i & 1 \end{pmatrix}$$
特性: 连续两次应用等效于一次X门: $\sqrt{X} \cdot \sqrt{X} = X$
这是量子独有的——**没有经典的"平方根NOT"**

#### 旋转门 (Rotation Gates)
$$R_x(\theta) = \begin{pmatrix} \cos(\theta/2) & -i\sin(\theta/2) \\ -i\sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

$$R_y(\theta) = \begin{pmatrix} \cos(\theta/2) & -\sin(\theta/2) \\ \sin(\theta/2) & \cos(\theta/2) \end{pmatrix}$$

$$R_z(\theta) = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}$$

### 3. 多量子比特门详解

#### CNOT 门 ( Controlled-NOT / CX )
$$\text{CNOT} = \begin{pmatrix} 1&0&0&0 \\ 0&1&0&0 \\ 0&0&0&1 \\ 0&0&1&0 \end{pmatrix}$$

- **控制位 (Control)**: 决定是否执行操作
- **目标位 (Target)**: 被操作的位
- 操作规则: 当控制位为 $|1\rangle$ 时，对目标位执行 X 门

真值表:
| Control | Target | Target (out) |
|---------|--------|-------------|
| 0 | 0 | **0** |
| 0 | 1 | **1** |
| 1 | 0 | **1** |
| 1 | 1 | **0** |

#### CCX 门 ( Toffoli 门 ) 
- 两个**控制位**, 一个**目标位**
- 当两个控制位都为 $|1\rangle$ 时，对目标位执行 X 门
- **通用性**: Toffoli门 + 单量子比特门 = 通用量子计算

#### SWAP 门
交换两个量子比特的状态:
$$\text{SWAP} \cdot |ab\rangle = |ba\rangle$$

矩阵形式:
$$\text{SWAP} = \begin{pmatrix} 1&0&0&0 \\ 0&0&1&0 \\ 0&1&0&0 \\ 0&0&0&1 \end{pmatrix}$$

### 4. 量子纠缠 (Entanglement)
当多量子比特态**不能分解为单个量子比特态的张量积**时，称这些量子比特处于**纠缠态**。

#### Bell 态 (EPR对)
四个最大纠缠态（由H+CNOT生成）:

$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}} \quad \text{(H on q0 + CNOT q0→q1)}$$

$$|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}} \quad \text{(H + CNOT + Z)}$$

$$|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}} \quad \text{(H + CNOT + X on target)}$$

$$|\Psi^-\rangle = \frac{|01\rangle - |10\rangle}{\sqrt{2}} \quad \text{(H + CNOT + X + Z)}$$

**纠缠的关键特征**: 测量其中一个量子比特会**瞬间确定**另一个的状态，无论它们相距多远。

### 5. 张量积 (Tensor Product / Kronecker Product)
多量子比特系统的数学工具：

$$A \otimes B = \begin{pmatrix} a_{11}B & a_{12}B \\ a_{21}B & a_{22}B \end{pmatrix}$$

**应用场景**:
- 组合多个单量子比特门作用于多量子比特系统: $H \otimes I$ (只对第一个量子比特施H门)
- 描述多量子比特初态: $|0\rangle \otimes |0\rangle = |00\rangle$

---

## 公式汇总

### 通用量子门集
以下门集可以实现任意量子计算：
- **Clifford + T 集**: {H, S, CNOT, T} — 广泛用于容错量子计算
- **任意单量子比特 + CNOT**: 通用集
- **旋转 + CNOT**: {Rx, Ry, Rz, CNOT}

### 幺正性验证
$$U^\dagger U = U U^\dagger = I$$

例如验证X门:
$$X^\dagger = X, \quad X \cdot X = I$$

---

## 代码示例说明

### 示例1: X门（量子非门）

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(1, 1)
qc.x(0)        # 应用X门
qc.measure(0, 0)

simulator = AerSimulator()
result = simulator.run(qc, shots=1024).result()
counts = result.get_counts(qc)

print(counts)  # {'1': 1024} — 确定性输出1
plot_histogram(counts)
```

**说明**: X门将 $|0\rangle$ 翻转为 $|1\rangle$，测量结果确定性为1。

### 示例2: CNOT 门 — 从叠加到纠缠

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# 不纠缠的情况: 两个独立量子比特都在叠加态
qc_no_entangle = QuantumCircuit(2, 2)
qc_no_entangle.h(0)
qc_no_entangle.h(1)
qc_no_entangle.measure([0,1], [0,1])

result1 = AerSimulator().run(qc_no_entangle, shots=4096).result()
print("不纠缠:", result1.get_counts())
# 约 {'00':~1024, '01':~1024, '10':~1024, '11':~1024}

# 纠缠的情况: Bell态
qc_entangle = QuantumCircuit(2, 2)
qc_entangle.h(0)         # 叠加
qc_entangle.cx(0, 1)     # 纠缠!
qc_entangle.measure([0,1], [0,1])

result2 = AerSimulator().run(qc_entangle, shots=4096).result()
print("纠缠(Bell态):", result2.get_counts())
# 只出现 {'00':~2048, '11':~2048}
```

**关键对比**: 不纠缠时四种结果均匀分布；纠缠后只有 `00` 和 `11` 出现——**两个比特的结果完全关联**。

### 示例3: sqrt(NOT) 门

```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import SXGate  # sqrt(X) gate
from qiskit.quantum_info import Operator, Statevector
import numpy as np

qc = QuantumCircuit(1)

# 应用两次sqrt(X)
sx = SXGate()
qc.append(sx, [0])   # 第一次 sqrt(X)
qc.append(sx, [0])   # 第二次 sqrt(X)

# 验证两次sqrt(X) = X
op = Operator(qc)
print("SX * SX 矩阵:")
print(np.round(op.data, 3))
# 应该接近 [[0, 1], [1, 0]] 即 X 门矩阵

# 验证态的变化
qc_test = QuantumCircuit(1)
qc_test.x(0)           # 直接X门
op_x = Operator(qc_test)
print("\n直接X门矩阵:")
print(np.round(op_x.data, 3))
```

### 示例4: Toffoli 门 (CCX)

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Toffoli: 两个控制位控制一个目标位
qc = QuantumCircuit(3, 3)

# 设置初始态 |110> (q0=1, q1=1, q2=0)
qc.x(0)
qc.x(1)

# 施加Toffoli门: control=q0,q1, target=q2
qc.ccx(0, 1, 2)

qc.measure([0, 1, 2], [0, 1, 2])

result = AerSimulator().run(qc, shots=1024).result()
print(result.get_counts())  # {'111': 1024}
# 因为两个控制位都是1, 目标位被翻转 0->1
```

### 示例5: 旋转门的使用

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import numpy as np

# 绕X轴旋转45度
qc_rx = QuantumCircuit(1)
qc_rx.rx(np.pi/4, 0)   # θ = π/4 = 45°

state_rx = Statevector.from_instruction(qc_rx)
plot_bloch_multivector(state_rx)
# Bloch矢量从北极(0,0,1)向X轴方向偏移45度

# 绕Z轴旋转
qc_rz = QuantumCircuit(1)
qc_rz.h(0)             # 先转到赤道
qc_rz.rz(np.pi/3, 0)   # 再绕Z旋转60度

state_rz = Statevector.from_instruction(qc_rz)
plot_bloch_multivector(state_rz)
```

### 示例6: 张量积的实现

```python
import numpy as np
from qiskit.quantum_info import Operator

# 单量子比特门的张量积
H = Operator.from_label('H').data      # 2x2 矩阵
I = Operator.from_label('I').data      # 2x2 矩阵

# H ⊗ I: 只作用于第一个量子比特
HI = np.kron(H, I)
print(f"H⊗I 维度: {HI.shape}")  # (4, 4)

# I ⊗ H: 只作用于第二个量子比特
IH = np.kron(I, H)
print(f"I⊗H 维度: {IH.shape}")  # (4, 4)

# 验证: H⊗I ≠ I⊗H (顺序很重要!)
print("H⊗I == I⊗H?", np.allclose(HI, IH))  # False
```

---

## 课后练习要点

1. **验证门的可逆性**: 对每个学过的门U，验证 $U^\dagger U = I$
2. **构建Bell态**: 用不同方式构造全部四个Bell态，并用Statevector验证
3. **CNOT真值表**: 构建所有4种输入组合(|00>, |01>, |10>, |11>)下的CNOT电路，验证输出
4. **sqrt(NOT)的幂**: 计算 $(\sqrt{X})^4$ 的结果是什么？
5. **旋转门的连续应用**: 连续多次小角度旋转的效果是什么？
6. **SWAP门的替代实现**: 用3个CNOT门实现一个SWAP门（提示: CNOT(a,b), CNOT(b,a), CNOT(a,b)）
7. **通用门集实践**: 仅使用 {H, T, CNOT} 构造一个任意的单量子比特旋转
8. **纠缠验证**: 编写程序检测给定两量子比特态是否纠缠（检查是否可分离/separable）

---

## 本周知识体系总览

```
量子门体系
├── 单量子比特门 (2×2 幺正矩阵)
│   ├── Pauli门: X, Y, Z
│   ├── Clifford门: H, S
│   └── 非Clifford门: T (π/8), 旋转门 Rx/Ry/Rz
│
├── 多量子比特门
│   ├── CNOT (2-qubit, 通用)
│   ├── CZ (2-qubit)
│   ├── SWAP (2-qubit)
│   └── CCX/Toffoli (3-qubit)
│
├── 核心概念
│   ├── 幺正性 (可逆性)
│   ├── 张量积 (组合系统)
│   └── 纠缠 (不可分离态)
│
└── 通用性定理
    └── {任意单量子比特门} + CNOT = 通用量子计算
```
