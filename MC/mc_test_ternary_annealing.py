import copy
import math
import random

# ---------- 参数 ----------
L = 20
N = L * L

# 从高温逐步降至低温
temperatures = [4.0, 3.0, 2.0, 1.0, 0.5, 0.3]
steps_per_temperature = 5_000

# 0 = A，1 = B，2 = C
ELEMENTS = ["A", "B", "C"]

# 数值越负，代表该原子对作为最近邻越稳定
PAIR_ENERGY = [
    [0.0, -1.0, -0.2],  # A-A, A-B, A-C
    [-1.0, 0.0, -0.6],  # B-A, B-B, B-C
    [-0.2, -0.6, 0.0],  # C-A, C-B, C-C
]
# --------------------------


def total_energy(atoms):
    """计算全部最近邻键的总能量。"""
    energy = 0.0

    for i in range(L):
        for j in range(L):
            atom_type = atoms[i][j]

            right = atoms[i][(j + 1) % L]
            down = atoms[(i + 1) % L][j]

            energy += PAIR_ENERGY[atom_type][right]
            energy += PAIR_ENERGY[atom_type][down]

    return energy


def pair_fractions(atoms):
    """统计三类异种原子对占全部最近邻键的比例。"""
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


# 固定成分：A、B、C 各约三分之一
initial_rng = random.Random(20260906)   #为了可重复性，固定随机种子

atoms_1d = (
    [0] * (N // 3)
    + [1] * (N // 3)
    + [2] * (N - 2 * (N // 3))
)

initial_rng.shuffle(atoms_1d)

atoms = [
    atoms_1d[i * L:(i + 1) * L]
    for i in range(L)
]

energy = total_energy(atoms)

best_energy = energy
best_atoms = copy.deepcopy(atoms)
best_temperature = temperatures[0]
best_step = 0
global_step = 0

print("===== Ternary-alloy simulated annealing =====")
print(f"Lattice: {L} x {L}")
print(f"Cooling schedule: {temperatures}")
print(f"Initial E/atom: {energy / N:.4f}")

for temperature in temperatures:
    accepted_swaps = 0
    attempted_swaps = 0

    for _ in range(steps_per_temperature):
        global_step += 1

        # 随机选择两个原子位置
        i1 = random.randrange(L)
        j1 = random.randrange(L)

        i2 = random.randrange(L)
        j2 = random.randrange(L)

        # 同种元素交换没有意义
        if atoms[i1][j1] == atoms[i2][j2]:
            continue

        attempted_swaps += 1

        # 试探性交换
        atoms[i1][j1], atoms[i2][j2] = (
            atoms[i2][j2],
            atoms[i1][j1],
        )

        new_energy = total_energy(atoms)
        delta_e = new_energy - energy

        # Metropolis 接受/拒绝规则
        if delta_e <= 0:
            accept = True
        else:
            probability = math.exp(-delta_e / temperature)
            accept = random.random() < probability

        if accept:
            energy = new_energy
            accepted_swaps += 1

            # 保存整个退火过程中的最低能构型
            if energy < best_energy:
                best_energy = energy
                best_atoms = copy.deepcopy(atoms)
                best_temperature = temperature
                best_step = global_step
        else:
            # 拒绝则恢复原构型
            atoms[i1][j1], atoms[i2][j2] = (
                atoms[i2][j2],
                atoms[i1][j1],
            )

    fractions = pair_fractions(atoms)
    acceptance = accepted_swaps / attempted_swaps

    print(
        f"T = {temperature:3.1f} | "
        f"E/atom = {energy / N:.4f} | "
        f"A-B = {fractions['A-B']:.3f} | "
        f"A-C = {fractions['A-C']:.3f} | "
        f"B-C = {fractions['B-C']:.3f} | "
        f"Acceptance = {acceptance:.3f}"
    )

final_fractions = pair_fractions(atoms)
best_fractions = pair_fractions(best_atoms)

print("\n===== Annealing result =====")
print(f"Final E/atom: {energy / N:.4f}")
print(f"Final A-B fraction: {final_fractions['A-B']:.3f}")
print(f"Final A-C fraction: {final_fractions['A-C']:.3f}")
print(f"Final B-C fraction: {final_fractions['B-C']:.3f}")

print(f"\nBest E/atom: {best_energy / N:.4f}")
print(f"Best A-B fraction: {best_fractions['A-B']:.3f}")
print(f"Best A-C fraction: {best_fractions['A-C']:.3f}")
print(f"Best B-C fraction: {best_fractions['B-C']:.3f}")
print(f"Best structure: T = {best_temperature}, step = {best_step}")