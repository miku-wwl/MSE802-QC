"""
Week 5: 量子逻辑门与多量子比特系统 - 实践代码
运行方式: python week5_practice.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Week 5: 量子逻辑门与多量子比特系统")
print("=" * 60)

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit.library import SXGate
from qiskit.quantum_info import Statevector, Operator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_aer import AerSimulator

# ============================================================
# 示例1: X门 (Pauli-X / NOT门)
# ============================================================
print("\n" + "=" * 60)
print("[1] 示例1: X 门 — 量子 NOT 门")
print("=" * 60)

sim = AerSimulator()

# X|0> = |1>
qc_x0 = QuantumCircuit(1, 1)
qc_x0.x(0)
qc_x0.measure(0, 0)
r0 = sim.run(qc_x0, shots=1024).result().get_counts()
print(f"X|0⟩ → 测量: {r0}  (预期: {{'1': 1024}})")
assert r0.get('1', 0) == 1024

# X|1> = |0>
qc_x1 = QuantumCircuit(1, 1)
qc_x1.x(0); qc_x1.x(0)  # X*X = I
qc_x1.measure(0, 0)
r1 = sim.run(qc_x1, shots=1024).result().get_counts()
print(f"XX|0⟩ → 测量: {r1}  (预期: {{'0': 1024}})")
assert r1.get('0', 0) == 1024
print("✓ X门验证通过!")

# ============================================================
# 示例2: sqrt(NOT) 门 (SX / sqrt(X))
# ============================================================
print("\n" + "=" * 60)
print("[2] 示例2: √NOT 门 (√X / SX 门)")
print("=" * 60)

# 验证 SX * SX = X
qc_sx2 = QuantumCircuit(1)
sx = SXGate()
qc_sx2.append(sx, [0])
qc_sx2.append(sx, [0])
op_sx2 = Operator(qc_sx2)

op_x = Operator.from_label('X')

print(f"SX * SX 矩阵:\n{np.round(op_sx2.data, 4)}")
print(f"\nX 门矩阵:    \n{np.round(op_x.data, 4)}")
match = np.allclose(op_sx2.data, op_x.data)
print(f"\nSX × SX = X ? {'✓ 是!' if match else '✗ 否!'}")

# 三次SX = ?
qc_sx3 = QuantumCircuit(1)
qc_sx3.sx(0); qc_sx3.sx(0); qc_sx3.sx(0)
op_sx3 = Operator(qc_sx3)
print(f"\n(SX)³ = SX×X 矩阵:\n{np.round(op_sx3.data, 4)}")

print("\n→ 量子独有的特性: 没有'平方根NOT'的经典门!")

# ============================================================
# 示例3: CNOT 门真值表验证
# ============================================================
print("\n" + "=" * 60)
print("[3] 示例3: CNOT 门 — 完整真值表")
print("=" * 60)

print(f"\n{'输入':<8s} {'输出':<8s} {'Control':<10s} {'Target':<10s} 验证")
print("-" * 50)

for ctrl_val in [0, 1]:
    for tgt_val in [0, 1]:
        qc = QuantumCircuit(2, 2)
        if ctrl_val: qc.x(0)
        if tgt_val:  qc.x(1)
        qc.cx(0, 1)              # 控制位=0, 目标位=1
        qc.measure([0, 1], [0, 1])
        
        result = sim.run(qc, shots=100).result().get_counts()
        out_state = list(result.keys())[0][::-1]  # Qiskit顺序
        
        expected_tgt = tgt_val ^ ctrl_val  # XOR
        expected = f"{ctrl_val}{expected_tgt}"
        
        ok = out_state == expected
        symbol = "✓" if ok else "✗"
        
        print(f"  |{ctrl_val}{tgt_val}⟩ → |{out_state}⟩  "
              f"  C={ctrl_val}(不变)  T={tgt_val}→{expected_tgt}  {symbol}")

print("\nCNOT规则: 当Control=1时, Target翻转(XOR)")

# 可视化 (Qiskit 2.x compatible: save individual figures)
inputs = [(0,0),(0,1),(1,0),(1,1)]
for idx, (c, t) in enumerate(inputs):
    qc_v = QuantumCircuit(2)
    if c: qc_v.x(0)
    if t: qc_v.x(1)
    qc_v.cx(0, 1)
    sv = Statevector.from_instruction(qc_v)
    state_str = list(sv.probabilities_dict().keys())[0]
    fig_cnot = sv.draw("bloch")
    fig_cnot.suptitle("CNOT|%d%d> = |%s>" % (c, t, state_str))
    fig_cnot.savefig("week5_cnot_%d%d.png" % (c, t), dpi=120, bbox_inches='tight')
print("Saved: week5_cnot_*.png (4 files)")

# ============================================================
# 示例4: Bell 态 (纠缠态) 的构造与验证
# ============================================================
print("\n" + "=" * 60)
print("[4] 示例4: Bell 纠缠态的四种形式")
print("=" * 60)

bell_configs = [
    ("|Phi+> = (|00>+|11>)/sqrt(2)", ["h0","cx01"]),
    ("|Phi-> = (|00>-|11>)/sqrt(2)", ["h0","cx01","z0"]),
    ("|Psi+> = (|01>+|10>)/sqrt(2)", ["h0","cx01","x1"]),
    ("|Psi-> = (|01>-|10>)/sqrt(2)", ["h0","cx01","x1","z0"]),
]

def build_bell_circuit(gate_list):
    """Build a Bell state circuit from gate list."""
    qc = QuantumCircuit(2, 2)
    for g in gate_list:
        if g == "h0": qc.h(0)
        elif g == "cx01": qc.cx(0, 1)
        elif g == "z0": qc.z(0)
        elif g == "x1": qc.x(1)
    return qc

for idx, (name, gates) in enumerate(bell_configs):
    # Build without measurements for Statevector
    qc_bell_nomeas = build_bell_circuit(gates)
    sv_bell = Statevector.from_instruction(qc_bell_nomeas)
    probs = sv_bell.probabilities_dict()
    
    # Qiskit 2.x: plot_histogram returns Figure
    fig_hist = plot_histogram(probs, sort='asc')
    fig_hist.suptitle(name, fontsize=12)
    fig_hist.savefig("week5_bell_%d.png" % idx, dpi=120, bbox_inches='tight')
    
    # Build WITH measurements for simulator verification
    qc_bell_meas = build_bell_circuit(gates)
    qc_bell_meas.measure([0,1], [0,1])
    sim_result = sim.run(qc_bell_meas, shots=8192).result().get_counts()
    sorted_res = dict(sorted(sim_result.items()))
    print("  %28s  theory:%s  sim:%s" % (name, probs, sorted_res))

print("\nSaved: week5_bell_*.png (4 files)")

# ============================================================
# 示例5: Toffoli 门 (CCX)
# ============================================================
print("\n" + "=" * 60)
print("[5] 示例5: Toffoli 门 (CCX) — 双控制位")
print("=" * 60)

print(f"\n{'输入(c1,c2,t)':<18s} {'输出':<8s} 说明")
print("-" * 45)

for c1 in [0, 1]:
    for c2 in [0, 1]:
        for t in [0, 1]:
            qc_ccx = QuantumCircuit(3, 3)
            if c1: qc_ccx.x(0)
            if c2: qc_ccx.x(1)
            if t:  qc_ccx.x(2)
            qc_ccx.ccx(0, 1, 2)
            qc_ccx.measure([0,1,2], [0,1,2])
            
            res = sim.run(qc_ccx, shots=32).result().get_counts()
            out = list(res.keys())[0][::-1]  # 反转Qiskit位序
            
            both_ctrl = (c1 == 1 and c2 == 1)
            expected_t = t ^ (1 if both_ctrl else 0)
            expected = f"{c1}{c2}{expected_t}"
            
            ok = out == expected
            note = "目标翻转!" if both_ctrl else "目标不变"
            print(f"  |{c1}{c2}{t}⟩ → |{out}⟩{'✓' if ok else '✗':<4s}  {note}")

print("\nToffoli: 仅当两个控制位都为1时, 目标位才翻转")

# ============================================================
# 示例6: SWAP 门
# ============================================================
print("\n" + "=" * 60)
print("[6] 示例6: SWAP 门 — 交换两个量子比特")
print("=" * 60)

test_inputs = [(0,1), (1,0), ('+', '-')]
for inp_a, inp_b in test_inputs:
    qc_swap = QuantumCircuit(2, 2)
    
    if isinstance(inp_a, str):
        if inp_a == '+':
            qc_swap.h(0)
        elif inp_a == '-':
            qc_swap.x(0); qc_swap.h(0)
    elif inp_a == 1:
        qc_swap.x(0)
        
    if isinstance(inp_b, str):
        if inp_b == '+':
            qc_swap.h(1)
        elif inp_b == '-':
            qc_swap.x(1); qc_swap.h(1)
    elif inp_b == 1:
        qc_swap.x(1)
    
    qc_swap.swap(0, 1)
    qc_swap.measure([0, 1], [0, 1])
    
    res = sim.run(qc_swap, shots=256).result().get_counts()
    print(f"  SWAP|{inp_a}{inp_b}⟩ = {res}")

# 用CNOT实现SWAP: CNOT(a,b), CNOT(b,a), CNOT(a,b)
print("\n验证: SWAP = CNOT(a,b) · CNOT(b,a) · CNOT(a,b)")
qc_swap_manual = QuantumCircuit(2, 2)
qc_swap_manual.x(0)  # |10>
qc_swap_manual.cx(0, 1)  # |11>
qc_swap_manual.cx(1, 0)  # |01>
qc_swap_manual.cx(0, 1)  # |01>
qc_swap_manual.measure([0, 1], [0, 1])
res_manual = sim.run(qc_swap_manual, shots=100).result().get_counts()
print(f"  |10⟩ → 3×CNOT → {res_manual}  (预期: |01⟩)")

# ============================================================
# 示例7: 张量积 — 组合量子门作用于多比特系统
# ============================================================
print("\n" + "=" * 60)
print("[7] 示例7: 张量积 — H⊗I vs I⊗H")
print("=" * 60)

H = Operator.from_label('H').data
I = np.eye(2, dtype=complex)

HI = np.kron(H, I)   # 只作用第1个量子比特
IH = np.kron(I, H)   # 只作用第2个量子比特

print(f"\nH⊗I:\n{np.round(HI, 3)}\n")
print(f"I⊗H:\n{np.round(IH, 3)}\n")

# 用电路验证
qc_hi = QuantumCircuit(2)
qc_hi.h(0)           # H on qubit 0 = H⊗I
sv_hi = Statevector.from_instruction(qc_hi)

qc_ih = QuantumCircuit(2)
qc_ih.h(1)           # H on qubit 1 = I⊗H
sv_ih = Statevector.from_instruction(qc_ih)

print(f"H|0⟩⊗I|0⟩ = {sv_hi.data}")  # (|0>+|1>)/√2 ⊗ |0> = (|00>+|10>)/√2
print(f"I|0⟩⊗H|0⟩ = {sv_ih.data}")  # |0> ⊗ (|0>+|1>)/√2 = (|00>+|01>)/√2

print(f"\n两者不同! → 门的作用位置很重要")

# ============================================================
# 示例8: 旋转门
# ============================================================
print("\n" + "=" * 60)
print("[8] 示例8: 旋转门 Rx, Ry, Rz — 连续参数化旋转")
print("=" * 60)

angles_deg = [0, 45, 90, 135, 180]
gate_types = [('Rx', 'x'), ('Ry', 'y'), ('Rz', 'z')]

for gname, axis in gate_types:
    print(f"\n--- {gname}(θ) 绕{axis.upper()}轴旋转 ---")
    for deg in angles_deg:
        theta = np.radians(deg)
        qc_rot = QuantumCircuit(1)
        if axis == 'x': qc_rot.rx(theta, 0)
        elif axis == 'y': qc_rot.ry(theta, 0)
        elif axis == 'z': qc_rot.rz(theta, 0)
        sv_rot = Statevector.from_instruction(qc_rot)
        psi = sv_rot.data
        a, b = psi[0], psi[1]
        
        bx = 2*(a.conj()*b).real
        by = 2*(a.conj()*b).imag
        bz = (abs(a)**2-abs(b)**2).real
        
        p0 = abs(a)**2
        p1 = abs(b)**2
        print(f"  {gname}({deg:3d}°): Bloch=({bx:+.3f},{by:+.3f},{bz:+.3f}) "
              f"P(0)={p0:.3f} P(1)={p1:.3f}")

# 可视化 Ry 旋转
for i, deg in enumerate(angles_deg):
    qc_ry = QuantumCircuit(1)
    qc_ry.ry(np.radians(deg), 0)
    sv_ry = Statevector.from_instruction(qc_ry)
    fig_ry = sv_ry.draw("bloch")
    fig_ry.suptitle("Ry(%ddeg)" % deg)
    fig_ry.savefig("week5_ry_%ddeg.png" % deg, dpi=120, bbox_inches='tight')
print("\nSaved: week5_ry_*.png")

# ============================================================
# 示例9: 通用门集 — 任意单量子比特分解
# ============================================================
print("\n" + "=" * 60)
print("[9] 示例9: 通用量子门集概念验证")
print("=" * 60)

print("""
通用性定理:
  任意单量子比特门都可以分解为:  U = Rz(α) · Ry(β) · Rz(γ)
  或 Z-Y-Z 分解 (Euler角分解)

  通用集示例:
  - {H, T, CNOT}  — 用于容错量子计算
  - {任意单量子比特, CNOT}  — 最小通用集
  - {Rx, Ry, Rz, CNOT}  — 连续参数门集
""")

# 验证: 用 Euler 分解近似一个随机单量子比特门
np.random.seed(123)
random_phase = np.random.uniform(0, 2*np.pi)

# 目标: Rz(random) 门
target_qc = QuantumCircuit(1)
target_qc.rz(random_phase, 0)
target_op = Operator(target_qc)

print(f"目标门: Rz(θ={np.degrees(random_phase):.2f}°)")
print(f"目标矩阵:\n{np.round(target_op.data, 4)}")

print(f"\n→ 量子门都是可逆的(幺正), 可以精确合成任意变换")
print(f"→ 这是量子计算「普适性」的基础!")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("Week 5 实践总结")
print("=" * 60)
print("""
关键知识点:
  ✓ X 门: NOT门, XX=I
  ✓ √X (SX): 量子独有! (√X)²=X, (√X)⁴=I
  ✓ CNOT: 控制位=1时翻转目标位 (类XOR)
  ✓ CCX/Toffoli: 双控制位, 通用性核心组件
  ✓ SWAP: 交换两量子比特, 可用3个CNOT实现
  ✓ Bell态: H+CNOT产生最大纠缠, 测量完全关联
  ✓ 张量积 ⊗ 描述多比特门的作用位置
  ✓ Rx/Ry/Rz: 连续旋转门, 可实现任意角度旋转
  ✓ 通用集: {H,T,CNOT} 足以进行任意量子计算
""")

plt.close('all')
print("所有实践代码执行完毕!")
