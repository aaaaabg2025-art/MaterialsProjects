import copy
import math
import random

# ---------- 模拟参数 ----------
L = 20
N = L * L

TEMPERATURE = 1.0
STEPS = 20_000

# 元素编号：0 = A，1 = B，2 = C
ELEMENTS = ["A", "B", "C"]

# 不同元素对的示意性相互作用能
# 数值越负，说明这两种元素成为最近邻越有利。
PAIR_ENERGY = [
    [0.0, -1.0, -0.2],  # A-A, A-B, A-C
    [-1.0, 0.0, -0.6],  # B-A, B-B, B-C
    [-0.2, -0.6, 0.0],  # C-A, C-B, C-C
]
# ------------------------------


def total_energy(atoms):
    """计算全部最近邻键的总能量。"""
    energy = 0.0

    for i in range(L):
        for j in range(L):
            atom_type = atoms[i][j]

            # 周期性边界条件下的右、下邻居
            right = atoms[i][(j + 1) % L]
            down = atoms[(i + 1) % L][j]

            # 每对邻居只计算一次
            energy += PAIR_ENERGY[atom_type][right]
            energy += PAIR_ENERGY[atom_type][down]

    return energy


def pair_fractions(atoms):
    """统计 A-B、A-C、B-C 异种键在全部键中的比例。"""
    counts = {
        "A-B": 0,
        "A-C": 0,
        "B-C": 0,
    }
    total_bonds = 0

    for i in range(L):
        for j in range(L):
            atom_type = atoms[i][j]

            right = atoms[i][(j + 1) % L]
            down = atoms[(i + 1) % L][j]

            for neighbor in [right, down]:
                pair = "".join(sorted([
                    ELEMENTS[atom_type],
                    ELEMENTS[neighbor],
                ]))

                if pair == "AB":
                    counts["A-B"] += 1
                elif pair == "AC":
                    counts["A-C"] += 1
                elif pair == "BC":
                    counts["B-C"] += 1

                total_bonds += 1

    return {
        name: count / total_bonds
        for name, count in counts.items()
    }


# 固定成分：A、B、C 各占约三分之一
atoms_1d = (
    [0] * (N // 3)
    + [1] * (N // 3)
    + [2] * (N - 2 * (N // 3))
)

random.shuffle(atoms_1d)

atoms = [
    atoms_1d[i * L:(i + 1) * L]
    for i in range(L)
]

energy = total_energy(atoms)

best_energy = energy
best_atoms = copy.deepcopy(atoms)
best_step = 0

accepted_swaps = 0
attempted_swaps = 0

print("===== Ternary-alloy swap Monte Carlo =====")
print(f"Lattice: {L} x {L}")
print(f"Temperature: {TEMPERATURE}")
print("Composition: A ≈ 1/3, B ≈ 1/3, C ≈ 1/3")
print("Pair preference: A-B strongest, B-C moderate, A-C weak")
print(f"Initial E/atom: {energy / N:.4f}")

for step in range(1, STEPS + 1):
    # 随机选择两个格点
    i1 = random.randrange(L)
    j1 = random.randrange(L)

    i2 = random.randrange(L)
    j2 = random.randrange(L)

    # 同种元素交换后构型不变
    if atoms[i1][j1] == atoms[i2][j2]:
        continue

    attempted_swaps += 1

    # 试探性交换两个元素的位置
    atoms[i1][j1], atoms[i2][j2] = (
        atoms[i2][j2],
        atoms[i1][j1],
    )

    # 教学版本：重新计算总能量
    new_energy = total_energy(atoms)
    delta_e = new_energy - energy

    # Metropolis 接受/拒绝
    if delta_e <= 0:
        accept = True
    else:
        probability = math.exp(-delta_e / TEMPERATURE)
        accept = random.random() < probability

    if accept:
        energy = new_energy
        accepted_swaps += 1

        if energy < best_energy:
            best_energy = energy
            best_atoms = copy.deepcopy(atoms)
            best_step = step
    else:
        # 拒绝时恢复交换前的原子类型
        atoms[i1][j1], atoms[i2][j2] = (
            atoms[i2][j2],
            atoms[i1][j1],
        )

    if step % 2000 == 0:
        fractions = pair_fractions(atoms)
        acceptance = accepted_swaps / attempted_swaps

        print(
            f"Step {step:5d} | "
            f"E/atom = {energy / N:.4f} | "
            f"A-B = {fractions['A-B']:.3f} | "
            f"A-C = {fractions['A-C']:.3f} | "
            f"B-C = {fractions['B-C']:.3f} | "
            f"Acceptance = {acceptance:.3f}"
        )

final_fractions = pair_fractions(atoms)
best_fractions = pair_fractions(best_atoms)

print("\n===== Final result =====")
print(f"Final E/atom: {energy / N:.4f}")
print(f"Best E/atom: {best_energy / N:.4f}")
print(f"Best structure found at step: {best_step}")
print(f"Swap acceptance rate: {accepted_swaps / attempted_swaps:.3f}")

print("\nFinal pair fractions:")
print(f"A-B: {final_fractions['A-B']:.3f}")
print(f"A-C: {final_fractions['A-C']:.3f}")
print(f"B-C: {final_fractions['B-C']:.3f}")

print("\nBest-structure pair fractions:")
print(f"A-B: {best_fractions['A-B']:.3f}")
print(f"A-C: {best_fractions['A-C']:.3f}")
print(f"B-C: {best_fractions['B-C']:.3f}")