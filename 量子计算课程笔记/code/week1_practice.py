"""
Week 1: 量子计算入门与 Qiskit 基础 - 实践代码
运行方式: python week1_practice.py
"""

import sys, os
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Week 1: 量子计算入门与 Qiskit 基础")
print("=" * 60)

# ============================================================
# 环境检查
# ============================================================
print("\n[1] 环境检查...")
try:
    import qiskit
    print(f"   Qiskit 版本: {qiskit.__version__}")
except ImportError:
    print("   错误: 请先安装 Qiskit: pip install qiskit qiskit-aer qiskit-visualization")
    exit(1)

try:
    from qiskit_aer import AerSimulator
    print("   AerSimulator: OK")
except ImportError:
    print("   错误: 请安装 qiskit-aer: pip install qiskit-aer")
    exit(1)

from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# ============================================================
# 示例1: 最简单的量子电路 — 测量 |0> 态
# ============================================================
print("\n" + "=" * 60)
print("[2] 示例1: 最简单的量子电路 — 测量 |0> 态")
print("=" * 60)

qc1 = QuantumCircuit(1, 1)          # 1个量子比特, 1个经典比特
qc1.measure(0, 0)                   # 将量子比特0测量到经典比特0

print("\n电路图:")
print(qc1.draw())

simulator = AerSimulator()
job = simulator.run(qc1, shots=1024)
result = job.result()
counts1 = result.get_counts(qc1)

print(f"\n测量结果 (shots=1024): {counts1}")
print("预期结果: {'0': 1024} — 初始态|0>测量后始终为0")
assert counts1.get('0', 0) == 1024, "示例1失败!"
print("✓ 验证通过!")

# ============================================================
# 示例2: Hadamard门 — 创建叠加态
# ============================================================
print("\n" + "=" * 60)
print("[3] 示例2: Hadamard门 — 创建叠加态")
print("=" * 60)

qc2 = QuantumCircuit(1, 1)
qc2.h(0)                            # Hadamard门 -> 叠加态 (|0>+|1>)/√2
qc2.measure(0, 0)

print("\n电路图:")
print(qc2.draw())

simulator = AerSimulator()
job = simulator.run(qc2, shots=1024)
result = job.result()
counts2 = result.get_counts(qc2)

print(f"\n测量结果 (shots=1024): {counts2}")
p0 = counts2.get('0', 0) / 1024
p1 = counts2.get('1', 0) / 1024
print(f"  P(0) = {p0:.3f}  (预期 ≈ 0.500)")
print(f"  P(1) = {p1:.3f}  (预期 ≈ 0.500)")
if abs(p0 - 0.5) < 0.1 and abs(p1 - 0.5) < 0.1:
    print("✓ 验证通过! 分布接近50%-50%")
else:
    print("! 结果偏差较大（量子随机性正常）")

fig, ax = plt.subplots(figsize=(5, 3))
plot_histogram(counts2, ax=ax)
ax.set_title("Hadamard门后的测量分布")
plt.tight_layout()
plt.savefig('week1_hadamard.png', dpi=100, bbox_inches='tight')
print("   直方图已保存: week1_hadamard.png")

# ============================================================
# 示例3: X门（量子NOT门）
# ============================================================
print("\n" + "=" * 60)
print("[4] 示例3: X门（量子NOT门 / Pauli-X门）")
print("=" * 60)

qc3a = QuantumCircuit(1, 1)
qc3a.x(0)                           # X门: |0> -> |1>
qc3a.measure(0, 0)

job3a = simulator.run(qc3a, shots=1024)
counts3a = job3a.result().get_counts(qc3a)
print(f"\nX门作用于|0>: {counts3a}")
assert counts3a.get('1', 0) == 1024, "X门验证失败!"
print("✓ 验证通过! |0> 经X门后变为 |1>")

qc3b = QuantumCircuit(1, 1)
qc3b.x(0)
qc3b.x(0)                           # 两次X = 恒等操作
qc3b.measure(0, 0)

job3b = simulator.run(qc3b, shots=1024)
counts3b = job3b.result().get_counts(qc3b)
print(f"两次X门作用于|0>: {counts3b}")
assert counts3b.get('0', 0) == 1024, "X²验证失败!"
print("✓ 验证通过! XX = I (两次翻转还原)")

# ============================================================
# 示例4: H + X 组合实验
# ============================================================
print("\n" + "=" * 60)
print("[5] 示例4: H + X 组合 — 先翻转再叠加")
print("=" * 60)

qc4 = QuantumCircuit(1, 1)
qc4.x(0)                           # 先翻转为|1>
qc4.h(0)                           # 再叠加: H|1> = (|0>-|1>)/√2
qc4.measure(0, 0)

job4 = simulator.run(qc4, shots=4096)
counts4 = job4.result().get_counts(qc4)

print(f"\n电路: |0> --X--> |1> --H--> (|0>-|1>)/√2 --> measure")
print(f"测量结果 (shots=4096): {counts4}")
print("注意: 概率仍为~50%-50%, 但相位不同!")
fig2, ax2 = plt.subplots(figsize=(5, 3))
plot_histogram(counts4, ax=ax2)
ax2.set_title("|1> 经 H门 后的测量")
plt.tight_layout()
plt.savefig('week1_x_then_h.png', dpi=100, bbox_inches='tight')
print("   直方图已保存: week1_x_then_h.png")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("Week 1 实践总结")
print("=" * 60)
print("""
关键知识点:
  ✓ 量子比特初始态为 |0>
  ✓ Hadamard(H)门 创建叠加态 → 测量结果概率50-50%
  ✓ X 门是量子NOT门, 翻转|0> <-> |1>
  ✓ 两次X门等于恒等操作 (XX = I)
  ✓ shots 参数控制重复测量的次数
""")

plt.close('all')
print("所有实践代码执行完毕!")
