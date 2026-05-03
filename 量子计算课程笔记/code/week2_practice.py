"""
Week 2: Bloch球与单量子比特可视化 - 实践代码 (Qiskit 2.x 兼容)
运行方式: python week2_practice.py
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Week 2: Bloch Sphere & Single-Qubit Visualization")
print("=" * 60)

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def coords_to_sv(x, y, z):
    """Convert Bloch coordinates [x,y,z] to Statevector."""
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    phi = np.arctan2(y, x) if abs(z) < 0.9999 else 0.0
    alpha = np.cos(theta / 2)
    beta = np.exp(1j * phi) * np.sin(theta / 2)
    return Statevector(np.array([alpha, beta]))

def save_fig(fig, filename):
    """Save matplotlib figure to file."""
    fig.savefig(filename, dpi=120, bbox_inches='tight')
    print("Saved:", filename)

# ============================================================
# 示例1: Bloch球基本绘制 — |0> 和 |1>
# ============================================================
print("\n" + "=" * 60)
print("[1] Example 1: Bloch Sphere basics - |0> and |1>")
print("=" * 60)

fig0 = coords_to_sv(0, 0, 1).draw("bloch")
fig0.suptitle("|0> state (North Pole)")
save_fig(fig0, "week2_bloch_00.png")

fig1 = coords_to_sv(0, 0, -1).draw("bloch")
fig1.suptitle("|1> state (South Pole)")
save_fig(fig1, "week2_bloch_01.png")

print("""
  |0> -> Bloch coords [0, 0, 1]   (+z / North Pole)
  |1> -> Bloch coords [0, 0, -1]  (-z / South Pole)
""")

# ============================================================
# 示例2: 各量子门的Bloch球效果
# ============================================================
print("=" * 60)
print("[2] Example 2: Quantum gates on Bloch sphere")
print("=" * 60)

gate_configs = [
    ("Identity (I)", []),
    ("Pauli-X",     ["x"]),
    ("Hadamard (H)",["h"]),
    ("Pauli-Z",     ["z"]),
    ("S Gate",      ["s"]),
    ("T Gate",      ["t"]),
]

for gate_name, gates in gate_configs:
    qc = QuantumCircuit(1)
    for g in gates:
        if g == "x": qc.x(0)
        elif g == "h": qc.h(0)
        elif g == "z": qc.z(0)
        elif g == "s": qc.s(0)
        elif g == "t": qc.t(0)
    
    sv = Statevector.from_instruction(qc)
    psi = sv.data
    a, b = psi[0], psi[1]
    bx = 2*(a.conjugate()*b).real
    by = 2*(a.conjugate()*b).imag
    bz = (abs(a)**2 - abs(b)**2).real
    
    print("  %15s: Bloch=(%+.4f, %+.4f, %+.4f)" % (gate_name, bx, by, bz))
    
    fig_gate = sv.draw("bloch")
    short_name = gate_name.split()[0].lower()
    fig_gate.suptitle(gate_name)
    save_fig(fig_gate, "week2_bloch_" + short_name + ".png")

# ============================================================
# 示例3: 手动构建任意Bloch矢量
# ============================================================
print("\n" + "=" * 60)
print("[3] Example 3: Arbitrary states via theta & phi")
print("=" * 60)

test_cases = [
    (np.pi/2, 0,       "Equator +x (90deg, 0deg)"),
    (np.pi/2, np.pi/2,  "Equator +y (90deg, 90deg)"),
    (np.pi/2, np.pi,    "Equator -x (90deg, 180deg)"),
    (np.pi/3, np.pi/4,  "General (60deg, 45deg)"),
]

for i, (theta, phi, desc) in enumerate(test_cases):
    x = np.sin(theta)*np.cos(phi)
    y = np.sin(theta)*np.sin(phi)
    z = np.cos(theta)
    
    print("  theta=%5.1fdeg, phi=%5.1fdeg -> (%+.4f, %+.4f, %+.4f)" %
          (np.degrees(theta), np.degrees(phi), x, y, z))
    
    sv_custom = coords_to_sv(x, y, z)
    fig_custom = sv_custom.draw("bloch")
    title_str = "%s\n(%.2f,%.2f,%.2f)" % (desc, x, y, z)
    fig_custom.suptitle(title_str)
    save_fig(fig_custom, "week2_bloch_custom" + str(i+1) + ".png")

# ============================================================
# 示例4: 绕Z轴旋转序列
# ============================================================
print("\n" + "=" * 60)
print("[4] Example 4: Z-axis rotation sequence")
print("=" * 60)

angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
for i, angle in enumerate(angles):
    qc_rz = QuantumCircuit(1)
    qc_rz.h(0)
    qc_rz.rz(angle, 0)
    sv_rz = Statevector.from_instruction(qc_rz)
    
    psi = sv_rz.data
    a, b = psi[0], psi[1]
    bx = 2*(a.conj()*b).real; by = 2*(a.conj()*b).imag
    bz = (abs(a)**2-abs(b)**2).real
    print("  Rz(%5.1fdeg): (%+.4f, %+.4f, %+.4f)" % (np.degrees(angle), bx, by, bz))
    
    fig_rz = sv_rz.draw("bloch")
    fig_rz.suptitle("Rz(%ddeg)" % int(np.degrees(angle)))
    save_fig(fig_rz, "week2_bloch_rz" + str(i) + ".png")

print("\nNote: Rz rotates in XY-plane; Z-coordinate stays constant!")

# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("Week 2 Summary")
print("=" * 60)
print("""
Key concepts:
  + Bloch sphere = unit sphere representation of single-qubit pure states
  + North pole = |0>, South pole = |1>, Equator = equal superposition
  + X-gate: rotate 180 around X-axis
  + Y-gate: rotate 180 around Y-axis
  + Z-gate: rotate 180 around Z-axis  
  + H-gate: special combination rotation
  + Any state uniquely determined by (theta, phi)
  + Global phase does not affect Bloch position (unobservable)
""")
print("All Week 2 code executed successfully!")
