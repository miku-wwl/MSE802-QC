# Week 4: 复向量空间 (Complex Vector Spaces)

## 知识点标题
- 向量空间的公理化定义
- 复数的代数性质与几何解释
- 希尔伯特空间 (Hilbert Space)
- 内积 (Inner Product) 与范数 (Norm)
- 正交性与正交归一基

---

## 核心概念

### 1. 什么是向量空间？
**向量空间**（或称线性空间）是满足以下8条公理的集合 $V$，配备加法和标量乘法：

**加法公理（对任意 $\vec{u}, \vec{v}, \vec{w} \in V$）：**
1. 封闭性: $\vec{u} + \vec{v} \in V$
2. 结合律: $(\vec{u} + \vec{v}) + \vec{w} = \vec{u} + (\vec{v} + \vec{w})$
3. 交换律: $\vec{u} + \vec{v} = \vec{v} + \vec{u}$
4. 零元存在: 存在 $\vec{0} \in V$ 使 $\vec{v} + \vec{0} = \vec{v}$
5. 逆元存在: 对每个$\vec{v}$，存在$-\vec{v}$使$\vec{v}+(-\vec{v})=\vec{0}$

**标量乘法公理（对标量$a,b$和向量$\vec{u},\vec{v}$）：**
6. 封闭性: $a\vec{v} \in V$
7. 分配律I: $a(\vec{u}+\vec{v}) = a\vec{u} + a\vec{v}$
8. 分配律II: $(a+b)\vec{v} = a\vec{v} + b\vec{v}$
9. 结合律: $a(b\vec{v}) = (ab)\vec{v}$
10. 单位元: $1 \cdot \vec{v} = \vec{v}$

### 2. 复数域 $\mathbb{C}$
量子力学中使用的是**复向量空间**（标量为复数）：

- 复数: $z = a + bi$，其中 $a,b \in \mathbb{R}$, $i^2 = -1$
- 共轭: $z^* = a - bi$
- 模长: $|z| = \sqrt{zz^*} = \sqrt{a^2+b^2}$
- 欧拉公式: $e^{i\theta} = \cos\theta + i\sin\theta$
- 极坐标: $z = re^{i\theta}$，其中$r = |z|$, $\theta = \arg(z)$

### 3. 希尔伯特空间
**完备的内积空间**称为希尔伯特空间。量子态就生活在希尔伯特空间中：

- 完备性: 所有柯西序列都收敛于空间内的元素
- 内积: 定义了"角度"和"长度"的概念
- 有限维希尔伯特空间同构于 $\mathbb{C}^n$

### 4. 内积 (Inner Product)
对于复向量空间 $\mathbb{C}^n$，内积定义为：

$$\braket{\vec{u}|\vec{v}} = \sum_{i=1}^{n} u_i^* v_i$$

**重要性质**:
- 共轭对称: $\braket{u|v} = \braket{v|u}^*$
- 第一线性: $\braket{au+bw|v} = a^*\braket{u|v} + b^*\braket{w|v}$
- 第二线性: $\braket{u|av+bw} = a\braket{u|v} + b\braket{u|w}$
- 正定性: $\braket{v|v} \geq 0$，等号成立当且仅当$v=0$

### 5. 范数 (Norm)
$$\|\vec{v}\| = \sqrt{\braket{v|v}} = \sqrt{\sum_i |v_i|^2}$$

量子态要求**归一化**: $\|\ket{\psi}\| = 1$

### 6. 正交与正交归一基
- **正交**: $\braket{u|v} = 0$
- **正交归一基**: 一组基 $\{e_i\}$ 满足 $\braket{e_i|e_j} = \delta_{ij}$
- 计算基 $\{|0\rangle, |1\rangle, ...\}$ 就是正交归一基

---

## 公式汇总

### 复数运算
$$z_1 \cdot z_2 = (a_1+ib_1)(a_2+ib_2) = (a_1a_2-b_1b_2) + i(a_1b_2+a_2b_1)$$

$$\frac{z_1}{z_2} = \frac{z_1 z_2^*}{|z_2|^2}$$

### Schmidt分解（两体纯态）
任意双量子比特纯态可以写成：
$$\ket{\psi}_{AB} = \lambda_0 \ket{e_0}_A \otimes \ket{f_0}_B + \lambda_1 \ket{e_1}_A \otimes \ket{f_1}_B$$

其中 $\lambda_i \geq 0$ 且 $\lambda_0^2 + \lambda_1^2 = 1$。

---

## 代码示例说明

### 示例1: 复数向量与内积计算

```python
import numpy as np

# 定义两个复数向量
u = np.array([1+0j, 0+1j])      # = |0> + i|1>
v = np.array([1/np.sqrt(2), 1/np.sqrt(2)])  # = (|0>+|1>)/sqrt(2)

# 计算内积 <u|v> = u† · v
inner_product = np.vdot(u, v)   # vdot自动取第一个参量的共轭
print(f"<u|v> = {inner_product}")

# 计算范数
norm_u = np.linalg.norm(u)
norm_v = np.linalg.norm(v)
print(f"||u|| = {norm_u:.4f}")
print(f"||v|| = {norm_v:.4f}")

# 归一化
u_normalized = u / norm_u
print(f"归一化后的u: {u_normalized}")
print(f"归一化范数: {np.linalg.norm(u_normalized):.4f}")  # 应为1.0
```

### 示例2: 验证正交性

```python
import numpy as np

# 计算基态 |0> 和 |1>
ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)

# 验证正交归一性
print(f"<0|0> = {np.vdot(ket0, ket0)}")   # 应为1
print(f"<1|1> = {np.vdot(ket1, ket1)}")   # 应为1
print(f"<0|1> = {np.vdot(ket0, ket1)}")   # 应为0

# |+> 和 |-> 也是正交归一基
ket_plus = np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex)
ket_minus = np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex)

print(f"<+|-> = {np.vdot(ket_plus, ket_minus)}")  # 应为0
```

### 示例3: 希尔伯特空间的维度

```python
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

for n in range(1, 5):
    qc = QuantumCircuit(n)
    sv = Statevector.from_instruction(qc)
    dim = len(sv.data)
    print(f"{n}个量子比特 -> 态向量维度 = {dim} = 2^{n}")
    
# 输出:
# 1个量子比特 -> 态向量维度 = 2 = 2^1
# 2个量子比特 -> 态向量维度 = 4 = 2^2
# 3个量子比特 -> 态向量维度 = 8 = 2^3
# 4个量子比特 -> 态向量维度 = 16 = 2^4
```

### 示例4: 复数相位的可视化影响

```python
import numpy as np
import matplotlib.pyplot as plt

# 三个不同的态，概率相同但相位不同
states = {
    r'$\frac{|0\rangle+|1\rangle}{\sqrt{2}}$': np.array([1, 1])/np.sqrt(2),
    r'$\frac{|0\rangle-|1\rangle}{\sqrt{2}}$': np.array([1, -1])/np.sqrt(2),
    r'$\frac{|0\rangle+i|1\rangle}{\sqrt{2}}$': np.array([1, 1j])/np.sqrt(2),
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, (name, state) in zip(axes, states.items()):
    # 显示复平面上的振幅
    for i, amp in enumerate(state):
        ax.quiver(0, 0, amp.real, amp.imag, angles='xy', scale_units='xy', scale=1,
                   color='blue' if i==0 else 'red')
        ax.scatter(amp.real, amp.imag, s=100, color='blue' if i==0 else 'red')
        ax.text(amp.real, amp.imag, f'|{i}>', fontsize=12)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_title(name)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 课后练习要点

1. **验证向量空间公理**: 选择一组具体向量，逐一验证10条公理
2. **手算内积**: 给定向量 $\vec{u} = (1+i, 2)$ 和 $\vec{v} = (3, 1-i)$，计算 $\braket{u|v}$
3. **Gram-Schmidt正交化**: 将一组线性无关的正交化为正交归一基
4. **理解为什么需要复数**: 如果只用实数，哪些量子现象无法描述？（提示：干涉效应）
5. **希尔伯特空间维度爆炸**: 30个量子比特的态向量有多少维？这说明了什么问题？
6. **编程练习**: 用numpy实现一个函数判断给定的复向量组是否构成正交归一基
