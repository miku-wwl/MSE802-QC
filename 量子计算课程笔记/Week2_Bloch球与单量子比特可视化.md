# Week 2: Bloch球与单量子比特可视化

## 知识点标题
- Bloch球 (Bloch Sphere) 的几何表示
- 单量子比特在Bloch球上的可视化
- 单量子比特门的几何意义

---

## 核心概念

### 1. Bloch球是什么？
**Bloch球**是描述**单量子比特量子态**的三维几何表示法。任意单量子比特纯态都可以映射到单位球的表面上。

- **北极点**: 对应态 $|0\rangle$
- **南极点**: 对应态 $|1\rangle$
- **赤道上任意一点**: 对应等幅度的叠加态

### 2. Bloch球坐标表示

任意单量子比特态可表示为：
$$|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\phi}\sin\frac{\theta}{2}|1\rangle$$

其中：
- $\theta$ (**极角/polar angle**): 与+z轴的夹角, 范围 $[0, \pi]$
- $\phi$ (**方位角/azimuthal angle**): 在xy平面的投影角度, 范围 $[0, 2\pi)$

### 3. 重要特殊位置

| 位置 | $\theta$ | $\phi$ | 对应量子态 |
|------|----------|--------|-----------|
| 北极 | 0 | - | $|0\rangle$ |
| 南极 | $\pi$ | - | $|1\rangle$ |
| +x轴 | $\pi/2$ | 0 | $|+\rangle = \frac{|0\rangle+|1\rangle}{\sqrt{2}}$ |
| -x轴 | $\pi/2$ | $\pi$ | $|-\rangle = \frac{|0\rangle-|1\rangle}{\sqrt{2}}$ |
| +y轴 | $\pi/2$ | $\pi/2$ | $|+i\rangle = \frac{|0\rangle+i|1\rangle}{\sqrt{2}}$ |
| -y轴 | $\pi/2$ | $-\pi/2$ | $|-i\rangle = \frac{|0\rangle-i|1\rangle}{\sqrt{2}}$ |

---

## 公式

### Bloch球坐标到态向量的转换
$$|\psi\rangle = \begin{pmatrix} \cos(\theta/2) \\ e^{i\phi}\sin(\theta/2) \end{pmatrix}$$

### Bloch向量（密度矩阵表示中的实部）
$$\vec{r} = (\sin\theta\cos\phi,\; \sin\theta\sin\phi,\; \cos\theta)$$

满足 $|\vec{r}| = 1$（纯态情况）。

---

## 代码示例说明

### 示例1: 绘制Bloch球

```python
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt

# 绘制默认Bloch球
plot_bloch_vector([0, 0, 1])  # |0> 态, 指向北极
plt.show()

# |1> 态, 指向南极
plot_bloch_vector([0, 0, -1])
plt.show()
```

**说明**: `plot_bloch_vector()` 接受 `[x, y, z]` 三维坐标，绘制该方向上的量子态矢量。

### 示例2: 不同量子门在Bloch球上的效果

```python
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector

# |0> -> H -> |+> (指向+x)
qc_h = QuantumCircuit(1)
qc_h.h(0)          # Hadamard门绕Y轴旋转90度
state_h = Statevector.from_instruction(qc_h)

# |0> -> X -> |1>
qc_x = QuantumCircuit(1)
qc_x.x(0)          # X门绕X轴旋转180度
state_x = Statevector.from_instruction(qc_x)

# 可视化
plot_bloch_multivector(state_h)
plt.title("After H gate")
plot_bloch_multivector(state_x)
plt.title("After X gate")
```

**说明**:
- **H门**: 绕Y轴旋转180°（从|0⟩到|+⟩）
- **X门**: 绕X轴旋转180°（从|0⟩到|1⟩）
- **Z门**: 绕Z轴旋转180°（引入相位翻转）

### 示例3: 交互式探索Bloch球上的旋转

```python
import numpy as np
from qiskit.visualization import plot_bloch_vector

# 探索不同角度的量子态
theta = np.pi / 3    # 极角60度
phi = np.pi / 4       # 方位角45度

x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

plot_bloch_vector([x, y, z], title=f"θ={np.degrees(theta):.0f}°, φ={np.degrees(phi):.0f}°")
```

---

## 各量子门的几何意义

| 量子门 | 矩阵表示 | 几何操作 | Bloch球旋转轴 |
|--------|---------|----------|--------------|
| **I** (Identity) | $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ | 无变化 | 无 |
| **X** (Pauli-X) | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ | 比特翻转 | X轴旋转π |
| **Y** (Pauli-Y) | $\begin{pmatrix}0&-i\\i&0\end{pmatrix}$ | 比特+相位翻转 | Y轴旋转π |
| **Z** (Pauli-Z) | $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ | 相位翻转 | Z轴旋转π |
| **H** (Hadamard) | $\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ | 创建叠加态 | Y轴旋转π/再绕X轴旋转π/2 |
| **S** (Phase) | $\begin{pmatrix}1&0\\0&i\end{pmatrix}$ | π/2相位门 | Z轴旋转π/2 |
| **T** (T/π/8) | $\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$ | π/4相位门 | Z轴旋转π/4 |

---

## 课后练习要点

1. **手动计算Bloch坐标**: 给定一个量子态，计算其在Bloch球上的 $(x,y,z)$ 坐标
2. **验证门操作效果**: 用代码验证X、Y、Z、H门分别如何改变Bloch矢量
3. **理解全局相位**: 为什么 $e^{i\alpha}|\psi\rangle$ 和 $|\psi\rangle$ 在Bloch球上是同一个点？（提示：全局相位不可观测）
4. **叠加态的可视化**: 探索 $\theta=\pi/2$ 时不同 $\phi$ 值对应的量子态
5. **复合操作**: 连续应用多个门，观察Bloch矢量的最终位置
