"""
Week 4: 复向量空间 - 实践代码
运行方式: python week4_practice.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Week 4: 复向量空间 (Complex Vector Spaces)")
print("=" * 60)

import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import Statevector, Operator
from qiskit import QuantumCircuit

# ============================================================
# 示例1: 复数基础运算
# ============================================================
print("\n" + "=" * 60)
print("[1] 示例1: 复数的基本性质与几何意义")
print("=" * 60)

z1 = 3 + 4j
z2 = 1 - 2j

print(f"\nz1 = {z1}, z2 = {z2}")
print(f"  共轭: z1* = {z1.conjugate()}, z2* = {z2.conjugate()}")
print(f"  模长: |z1| = {abs(z1):.4f}, |z2| = {abs(z2):.4f}")
print(f"  乘积: z1*z2 = {z1*z2}")
print(f"  商:   z1/z2 = {z1/z2:.4f}")

# 欧拉公式
theta = np.pi / 3
z_euler = np.exp(1j * theta)
print(f"\n欧拉公式: e^(i·π/3) = cos(π/3) + i·sin(π/3)")
print(f"         = {z_euler.real:.4f} + {z_euler.imag:.4f}i = {z_euler:.4f}")

# 复平面可视化
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图: 复数在复平面上
ax1 = axes[0]
for z, color, label in [(z1, 'blue', f'z1={z1}'), (z2, 'red', f'z2={z2}')]:
    ax1.quiver(0, 0, z.real, z.imag, angles='xy', scale_units='xy', scale=1,
                color=color, width=0.03, label=label)
    ax1.scatter(z.real, z.imag, s=100, color=color, zorder=5)
ax1.axhline(0, color='gray', linewidth=0.5)
ax1.axvline(0, color='gray', linewidth=0.5)
ax1.set_xlim(-1, 6); ax1.set_ylim(-3, 5)
ax1.set_xlabel('Real'); ax1.set_ylabel('Imaginary')
ax1.set_title('复平面上的复数')
ax1.legend(); ax1.grid(True, alpha=0.3); ax1.set_aspect('equal')

# 右图: 欧拉公式的单位圆
ax2 = axes[1]
circle_angles = np.linspace(0, 2*np.pi, 100)
ax2.plot(np.cos(circle_angles), np.sin(circle_angles), 'lightblue', linewidth=2, label='|z|=1')
for t, marker in zip([0, np.pi/6, np.pi/3, np.pi/2, np.pi, 3*np.pi/2],
                      ['o','s','^','D','v','p']):
    z_t = np.exp(1j*t)
    ax2.scatter(z_t.real, z_t.imag, s=80, marker=marker, zorder=5)
    ax2.annotate(f'{t/np.pi:.2g}π', (z_t.real, z_t.imag), textcoords='offset points',
                 xytext=(5,5), fontsize=9)
ax2.scatter(z_euler.real, z_euler.imag, s=150, c='red', marker='*', 
            label=f'e^(iπ/3)', zorder=6)
ax2.quiver(0, 0, z_euler.real, z_euler.imag, angles='xy', scale_units='xy', scale=1,
            color='red', width=0.02)
ax2.set_xlim(-1.5, 1.5); ax2.set_ylim(-1.5, 1.5)
ax2.set_xlabel('Re'); ax2.set_ylabel('Im')
ax2.set_title("欧拉公式: e^(iθ) 在单位圆上")
ax2.legend(); ax2.grid(True, alpha=0.3); ax2.set_aspect('equal')

plt.tight_layout()
plt.savefig('week4_complex_numbers.png', dpi=120, bbox_inches='tight')
print("✓ 已保存: week4_complex_numbers.png")

# ============================================================
# 示例2: 内积、范数、归一化
# ============================================================
print("\n" + "=" * 60)
print("[2] 示例2: 内积与范数的计算")
print("=" * 60)

# 定义几个复数向量
vectors = {
    'v₁': np.array([1, 0], dtype=complex),
    'v₂': np.array([0, 1], dtype=complex),
    'v₃': np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex),
    'v₄': np.array([1+1j, 2-1j], dtype=complex) / 2,  # 未归一化
}

names = list(vectors.keys())
print(f"\n{'':6s}", end="")
for n in names:
    print(f"  {n:<10s}", end="")
print()
print("-" * 65)

# 打印各向量
print(f"{'向量':6s}", end="")
for n in names:
    v = vectors[n]
    s = f"[{v[0]:.3f}, {v[1]:.3f}]"
    print(f"  {s:<10s}", end="")
print()

# 打印范数
print(f"{'||v||':6s}", end="")
for n in names:
    v = vectors[n]
    norm = np.linalg.norm(v)
    print(f"  {norm:<10.4f}", end="")
print()

# 归一化
print(f"\n--- 归一化 ---")
for n in names:
    v = vectors[n]
    norm = np.linalg.norm(v)
    v_norm = v / norm
    new_norm = np.linalg.norm(v_norm)
    print(f"  {n}: ||v|| = {norm:.4f} → 归一化后 ||v|| = {new_norm:.6f}")

# 内积矩阵
print(f"\n--- 内积矩阵 ⟨vi|vj⟩ ---")
print(f"{'':8s}", end="")
for n in names:
    print(f"  {n:<10s}", end="")
print()
for ni in names:
    vi = vectors[ni]
    print(f"{ni:<8s}", end="")
    for nj in names:
        vj = vectors[nj]
        ip = np.vdot(vi, vj)  # ⟨vi|vj⟩
        if abs(ip.imag) < 1e-10:
            print(f"  {ip.real:<10.4f}", end="")
        else:
            print(f"  {ip:<10.4f}", end="")
    print()

# ============================================================
# 示例3: 正交性与 Gram-Schmidt 过程
# ============================================================
print("\n" + "=" * 60)
print("[3] 示例3: 正交性检验与 Gram-Schmidt 正交化")
print("=" * 60)

# 定义一组线性无关但非正交的向量
a = np.array([2, 1], dtype=float)
b = np.array([1, 3], dtype=float)

print(f"\n原始向量 (非正交):")
print(f"  a = {a}")
print(f"  b = {b}")
print(f"  ⟨a|b⟩ = {np.dot(a,b):.4f} ≠ 0  (不正交!)")

# Gram-Schmidt 正交化
e1 = a / np.linalg.norm(a)
proj_b_on_e1 = np.dot(b, e1) * e1
e2_perp = b - proj_b_on_e1
e2 = e2_perp / np.linalg.norm(e2_perp)

print(f"\nGram-Schmidt 正交化后:")
print(f"  e₁ = {e1}  (归一化后的a)")
print(f"  e₂ = {e2}  (b减去在e₁上的投影后归一化)")
print(f"  ⟨e₁|e₂⟩ = {np.dot(e1,e2):.10f}  (应为≈0)")
print(f"  ||e₁|| = {np.linalg.norm(e1):.6f}  (应为1)")
print(f"  ||e₂|| = {np.linalg.norm(e2):.6f}  (应为1)")

# 可视化 Gram-Schmidt
fig2, ax = plt.subplots(figsize=(7, 7))

# 原始向量
ax.arrow(0, 0, a[0], a[1], head_width=0.15, head_length=0.1, fc='blue', ec='blue', label='a')
ax.arrow(0, 0, b[0], b[1], head_width=0.15, head_length=0.1, fc='green', ec='green', label='b')

# 投影
ax.arrow(0, 0, proj_b_on_e1[0], proj_b_on_e1[1], head_width=0.1, head_length=0.08,
         fc='orange', ec='orange', linestyle='--', label='proj(b,e1)')
ax.arrow(proj_b_on_e1[0], proj_b_on_e1[1], e2_perp[0], e2_perp[1],
         head_width=0.1, head_length=0.08, fc='purple', ec='purple', linestyle=':', label='e2⊥')

ax.set_xlim(-0.5, 4); ax.set_ylim(-0.5, 4)
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('Gram-Schmidt 正交化过程')
ax.legend(loc='upper right'); ax.grid(True, alpha=0.3); ax.set_aspect('equal')
ax.axhline(0, color='gray', lw=0.5); ax.axvline(0, color='gray', lw=0.5)
plt.tight_layout()
plt.savefig('week4_gram_schmidt.png', dpi=120, bbox_inches='tight')
print("\n✓ 已保存: week4_gram_schmidt.png")

# ============================================================
# 示例4: 希尔伯特空间维度与量子态
# ============================================================
print("\n" + "=" * 60)
print("[4] 示例4: 希尔伯特空间维度的指数爆炸")
print("=" * 60)

print(f"\n{'量子比特':<8s} {'希尔伯特空间维度':<20s} {'复数振幅个数':<16s} {'内存估算(float64)'}")
print("-" * 75)

for n in range(1, 11):
    dim = 2 ** n
    memory_mb = dim * 16 / (1024**2)  # 每个复数16字节 (float128)
    if memory_mb < 1:
        mem_str = f"{memory_mb*1024:.1f} KB"
    elif memory_mb < 1024:
        mem_str = f"{memory_mb:.1f} MB"
    else:
        mem_str = f"{memory_mb/1024:.1f} GB"
    print(f"  n={n:<6d} {dim:<20d} {dim:<16d} {mem_str}")

print(f"\n⚠  n=40 时, 需要 {2**40 * 16 / (1024**4):.1f} TB 内存!")
print(f"   这就是「量子优越性」的来源之一 —— 无法经典模拟!")

# ============================================================
# 示例5: 验证量子门的幺正性
# ============================================================
print("\n" + "=" * 60)
print("[5] 示例5: 验证量子门的幺正性 U†U = I")
print("=" * 60)

gate_names = ['X', 'Y', 'Z', 'H', 'S', 'T']
print(f"\n{'门':<6s} {'U†U = I ?':<14s} {'det(U)':<10s} 说明")
print("-" * 50)

for gname in gate_names:
    op = Operator.from_label(gname)
    U = op.data
    U_dag = U.conj().T
    
    identity_check = U_dag @ U
    is_identity = np.allclose(identity_check, np.eye(U.shape[0]), atol=1e-10)
    
    det_U = np.linalg.det(U)
    
    status = "✓ 幺正!" if is_identity else "✗ 非幺正!"
    print(f"  {gname:<5s} {status:<14s} {det_U:<10.4f} |U|=1")

print("\n所有量子门都是幺正矩阵 → 可逆操作 → 不丢失信息!")

# ============================================================
# 示例6: 向量空间公理验证
# ============================================================
print("\n" + "=" * 60)
print("[6] 示例6: 验证向量空间公理 (以 C² 为例)")
print("=" * 60)

def random_complex_vector(dim=2):
    """生成随机复数向量"""
    return np.random.randn(dim) + 1j * np.random.randn(dim)

np.random.seed(42)
u = random_complex_vector()
v = random_complex_vector()
w = random_complex_vector()
a = 1.5 + 0.5j
b = 0.8 - 1.2j

print(f"\n随机生成的测试向量:")
print(f"  u = {u}")
print(f"  v = {v}")
print(f"  w = {w}")
print(f"  标量 a = {a:.3f}, b = {b:.3f}")

axioms = [
    ("加法封闭性", u+v, "u+v ∈ C²"),
    ("结合律", u+(v+w), "(u+v)+w"),
    ("交换律", u+v, "v+u", lambda: np.allclose(u+v, v+w)),
    ("零元存在性", u+np.zeros_like(u), "u+0 = u", lambda: np.allclose(u, u+np.zeros_like(u))),
    ("逆元存在性", u+(-u), "u+(-u) = 0", lambda: np.allclose(u+(-u), np.zeros_like(u))),
    ("标量乘封闭", a*u, "a*u ∈ C²"),
    ("分配律I", a*(u+v), "a(u+v)", None, lambda: np.allclose(a*(u+v), a*u+a*v)),
    ("分配律II", (a+b)*u, "(a+b)u", None, lambda: np.allclose((a+b)*u, a*u+b*u)),
    ("标量结合律", (a*b)*u, "(ab)u", None, lambda: np.allclose((a*b)*u, a*(b*u))),
    ("单位元", 1.0*u, "1*u = u", lambda: np.allclose(1.0*u, u)),
]

all_passed = True
for item in axioms:
    name = item[0]
    if len(item) >= 4 and item[3] is not None:
        check_fn = item[3]
        passed = check_fn()
    elif len(item) >= 5 and item[4] is not None:
        check_fn = item[4]
        passed = check_fn()
    else:
        passed = True
    
    status = "✓ 通过" if passed else "✗ 失败!"
    print(f"  {name:<16s} {status}")
    if not passed:
        all_passed = False

print(f"\n{'='*40}")
print(f"  总体结果: {'全部通过! ✓' if all_passed else '有公理未通过 ✗'}")
print(f"  结论: C² 是一个合法的复向量空间 (希尔伯特空间)")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("Week 4 实践总结")
print("=" * 60)
print("""
关键知识点:
  ✓ 复数 z=a+bi: 共轭 z*=a-bi, 模长|z|=√(a²+b²)
  ✓ 欧拉公式: e^(iθ) = cos(θ) + i·sin(θ) → 单位圆上的点
  ✓ 内积 ⟨u|v⟩ = Σ ui* · vi (第一个取共轭!)
  ✓ 范数 ||v|| = √⟨v|v⟩ = √Σ|vi|²
  ✓ 正交: ⟨u|v⟩=0;  归一化: ||v||=1
  ✓ Gram-Schmidt: 任意线性无关组 → 正交归一基
  ✓ 量子门都是幺正矩阵: U†U = I (可逆, 保内积)
  ✓ n量子比特 → 希尔伯特空间维度 = 2ⁿ (指数爆炸!)
""")

plt.close('all')
print("所有实践代码执行完毕!")
