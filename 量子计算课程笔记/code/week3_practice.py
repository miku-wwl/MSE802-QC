"""
Week 3: 量子态向量、概率振幅与Dirac符号 - 实践代码 (Qiskit 2.x 兼容)
运行方式: python week3_practice.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Week 3: State Vectors, Probability Amplitudes & Dirac Notation")
print("=" * 60)

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

def make_circuit_1q(gate_list):
    """Helper: create 1-qubit circuit with given gate sequence."""
    qc = QuantumCircuit(1)
    for gate in gate_list:
        if gate == 'x': qc.x(0)
        elif gate == 'h': qc.h(0)
        elif gate == 'z': qc.z(0)
        elif gate == 'y': qc.y(0)
        elif gate == 's': qc.s(0)
        elif gate == 't': qc.t(0)
    return qc

# ============================================================
# 示例1: 获取并打印态向量
# ============================================================
print("\n" + "=" * 60)
print("[1] Example 1: Basic state vectors")
print("=" * 60)

states_config = {
    '|0>':      [],
    '|1>':      ['x'],
    '|+>':      ['h'],
    '|->':      ['x', 'h'],
}

print("\n{:<8s} {:22s} {:25s}".format("Name", "State Vec (a, b)", "Prob [|a|^2,|b|^2]"))
print("-" * 65)

for name, gates in states_config.items():
    qc = make_circuit_1q(gates)
    sv = Statevector.from_instruction(qc)
    a, b = sv.data[0], sv.data[1]
    pa, pb = abs(a)**2, abs(b)**2
    
    a_str = f"{a.real:.4f}" + (f"{a.imag:+.4f}i" if abs(a.imag)>1e-10 else "")
    b_str = f"{b.real:.4f}" + (f"{b.imag:+.4f}i" if abs(b.imag)>1e-10 else "")
    
    print(f"{name:<8s} [{a_str:>10s}, {b_str:>10s}]   [{pa:.4f}, {pb:.4f}]")

# 详细展示 |+>
print("\nDetailed analysis of |+> = (|0> + |1>)/sqrt(2):")
qc_plus = make_circuit_1q(['h'])
sv_plus = Statevector.from_instruction(qc_plus)
print(f"  State vector: {sv_plus.data}")
print(f"  Dimension: {len(sv_plus.data)}")
print(f"  Normalization check: |psi|^2 = {sum(np.abs(sv_plus.data)**2):.6f} (should be 1.0)")

# 可视化 (Qiskit 2.x: .draw() returns Figure)
fig_city = sv_plus.draw('city')
save_fig_city = 'week3_city.png'
fig_city.savefig(save_fig_city, dpi=120, bbox_inches='tight')
print(f"Saved: {save_fig_city}")

fig_qsphere = sv_plus.draw('qsphere')
save_fig_qsphere = 'week3_qsphere.png'
fig_qsphere.savefig(save_fig_qsphere, dpi=120, bbox_inches='tight')
print(f"Saved: {save_fig_qsphere}")

# Pauli vector (use probabilities_dict)
probs_pauli = sv_plus.probabilities()
print(f"  Probabilities: P(|0>)={probs_pauli[0]:.4f}, P(|1>)={probs_pauli[1]:.4f}")

# ============================================================
# 示例2: 概率振幅 vs 概率
# ============================================================
print("\n" + "=" * 60)
print("[2] Example 2: Amplitudes can be negative or complex!")
print("=" * 60)

test_amplitudes = {
    "(|0>+|1>)/sqrt(2)":  np.array([1/np.sqrt(2),  1/np.sqrt(2)]),
    "(|0>-|1>)/sqrt(2)":  np.array([1/np.sqrt(2), -1/np.sqrt(2)]),
    "(|0>+i|1>)/sqrt(2)": np.array([1/np.sqrt(2),  1j/np.sqrt(2)]),
}

print("\n{:<24s} {:22s} {:22s} {:8s}".format(
    "State", "Amplitudes [a,b]", "Probs [|a|^2,|b|^2]", "Same?"))
print("-" * 82)

for name, amps in test_amplitudes.items():
    probs = np.abs(amps)**2
    a_str = f"[{amps[0]:.4f}, {amps[1]:.4f}]"
    p_str = f"[{probs[0]:.4f}, {probs[1]:.4f}]"
    print(f"{name:<24s} {a_str:<22s} {p_str:<22s} YES!")

print("\nKey insight: Different amplitudes => same probability distribution!")
print("=> Phase info shows up in interference effects")

# ============================================================
# 示例3: 多量子比特系统的态向量维度
# ============================================================
print("\n" + "=" * 60)
print("[3] Example 3: Multi-qubit exponential growth")
print("=" * 60)

print(f"\n{'Qubits':<10s} {'State Vec Dim':<16s} {'Notes'}")
print("-" * 55)

for n in range(1, 7):
    dim = 2**n
    qc_n = QuantumCircuit(n)
    for i in range(n):
        qc_n.h(i)
    sv_n = Statevector.from_instruction(qc_n)
    
    note = f"each amp = {sv_n.data[0]:.4f}" if n <= 3 else "! Dimension explosion!"
    print(f"  n={n:<8d} {dim:<16d} {note}")

print(f"\n=> 30 qubits => dim = 2^30 = {2**30:,}")
print(f"  This is why classical computers struggle with large quantum systems!")

# ============================================================
# 示例4: 张量积运算
# ============================================================
print("\n" + "=" * 60)
print("[4] Example 4: Tensor Product computations")
print("=" * 60)

ket0 = np.array([1, 0], dtype=complex)
ket1 = np.array([0, 1], dtype=complex)

tensor_00 = np.kron(ket0, ket0)
print(f"|0> x |0> = {tensor_00}")

ket_plus = np.array([1, 1]) / np.sqrt(2)
tensor_plus0 = np.kron(ket_plus, ket0)
print(f"|+> x |0> = \n            {tensor_plus0}")

# 用Qiskit电路验证
qc_tensor = QuantumCircuit(2)
qc_tensor.h(0)
sv_tensor = Statevector.from_instruction(qc_tensor)
match = np.allclose(sv_tensor.data, tensor_plus0)
print(f"\nQiskit H(0)|00>: match manual tensor? {match}")

# ============================================================
# 示例5: 内积计算
# ============================================================
print("\n" + "=" * 60)
print("[5] Example 5: Inner products — orthonormality verification")
print("=" * 60)

basis_states = {
    '|0>': np.array([1, 0], dtype=complex),
    '|1>': np.array([0, 1], dtype=complex),
    '|+>': np.array([1, 1], dtype=complex)/np.sqrt(2),
    '|->': np.array([1,-1], dtype=complex)/np.sqrt(2),
}

names = list(basis_states.keys())
print("\nInner product matrix <i|j>:")
header = f"{'':8s}" + "".join(f" {n:<10s}" for n in names)
print(header)
print("-" * (len(header)-1))

for name_i in names:
    v_i = basis_states[name_i]
    row = f"{name_i:<8s}"
    for name_j in names:
        v_j = basis_states[name_j]
        ip = np.vdot(v_i, v_j)
        if abs(ip.imag)<1e-10:
            val = round(ip.real, 3)
        else:
            val = complex(round(ip.real,3), round(ip.imag,3))
        row += f" {str(val):<12s}"
    print(row)

print("\nDiagonal = 1 (normalized); orthogonal pairs = 0")

# ============================================================
# 示例6: probabilities_dict()
# ============================================================
print("\n" + "=" * 60)
print("[6] Example 6: Measurement probability distributions")
print("=" * 60)

qc_demo = QuantumCircuit(2)
qc_demo.h(0)
qc_demo.cx(0, 1)  # Bell state
sv_demo = Statevector.from_instruction(qc_demo)
probs = sv_demo.probabilities_dict()

print(f"\nCircuit: H(0) -> CNOT(0,1)  (Bell state |Phi+>)")
print(f"\nProbability distribution:")
for state, prob in sorted(probs.items()):
    bar = "#" * int(prob * 40)
    print(f"  |{state}>: {prob:.4f}  {bar}")
print(f"\nTotal prob: {sum(probs.values()):.4f} (should be 1.0)")

# 模拟器验证
qc_meas = QuantumCircuit(2, 2)
qc_meas.h(0); qc_meas.cx(0, 1)
qc_meas.measure([0,1],[0,1])
sim_counts = AerSimulator().run(qc_meas, shots=8192).result().get_counts()
print(f"\nSimulator (shots=8192): {dict(sorted(sim_counts.items()))}")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("Week 3 Summary")
print("=" * 60)
print("""
Key concepts:
  + State vector = normalized complex vec, dimension = 2^n
  + Dirac notation: ket(|psi>)=col vec, bra(<psi|)=conj(row vec)
  + |amplitude|^2 = measurement prob; phase affects interference
  + Computational basis forms orthonormal set
  + Tensor product (kron) combines subsystems
  + Inner product measures similarity between states
  + 30 qubits => ~1 billion amplitudes!
""")
print("All Week 3 code executed successfully!")
