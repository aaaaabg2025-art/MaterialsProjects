import copy
import math
import random

# ---------- 参数 ----------
L = 20
J = -1.0

# 从高温逐步降至低温
temperatures = [4.0, 3.0, 2.0, 1.0, 0.5, 0.3]

# 每个温度下的交换尝试次数
steps_per_temperature = 5_000
# --------------------------

N = L * L

# 固定 50% A、50% B 的随机初始构型
spins_1d = [1] * (N // 2) + [-1] * (N // 2)
random.shuffle(spins_1d)

spins = [
    spins_1d[i * L:(i + 1) * L]
    for i in range(L)
]


def total_energy(spins):
    """计算总能量。J < 0 时，A-B 异种邻居更稳定。"""
    energy = 0.0

    for i in range(L):
        for j in range(L):
            atom_type = spins[i][j]

            right = spins[i][(j + 1) % L]
            down = spins[(i + 1) % L][j]

            energy -= J * atom_type * right
            energy -= J * atom_type * down

    return energy


def unlike_bond_fraction(spins):
    """计算最近邻键中 A-B 异种键的比例。"""
    unlike_bonds = 0
    total_bonds = 0

    for i in range(L):
        for j in range(L):
            atom_type = spins[i][j]

            right = spins[i][(j + 1) % L]
            down = spins[(i + 1) % L][j]

            if atom_type != right:
                unlike_bonds += 1

            if atom_type != down:
                unlike_bonds += 1

            total_bonds += 2

    return unlike_bonds / total_bonds


energy = total_energy(spins)

best_energy = energy
best_spins = copy.deepcopy(spins)
best_temperature = temperatures[0]
best_step = 0

global_step = 0

print("===== Binary-alloy simulated annealing =====")
print(f"Lattice: {L} x {L}")
print("Cooling schedule:", temperatures)
print(f"Initial E/atom: {energy / N:.4f}")

for temperature in temperatures:
    accepted_swaps = 0
    attempted_swaps = 0

    for _ in range(steps_per_temperature):
        global_step += 1

        # 随机选择两个位置
        i1 = random.randrange(L)
        j1 = random.randrange(L)

        i2 = random.randrange(L)
        j2 = random.randrange(L)

        # 只有异种原子交换才会改变构型
        if spins[i1][j1] != spins[i2][j2]:
            attempted_swaps += 1

            # 试探性交换
            spins[i1][j1], spins[i2][j2] = (
                spins[i2][j2],
                spins[i1][j1],
            )

            new_energy = total_energy(spins)
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

                # 保存整个退火过程中的最优构型
                if energy < best_energy:
                    best_energy = energy
                    best_spins = copy.deepcopy(spins)
                    best_temperature = temperature
                    best_step = global_step
            else:
                # 拒绝：恢复交换前构型
                spins[i1][j1], spins[i2][j2] = (
                    spins[i2][j2],
                    spins[i1][j1],
                )

    acceptance = accepted_swaps / attempted_swaps
    unlike_fraction = unlike_bond_fraction(spins)

    print(
        f"T = {temperature:3.1f} | "
        f"E/atom = {energy / N:.4f} | "
        f"A-B fraction = {unlike_fraction:.3f} | "
        f"Acceptance = {acceptance:.3f}"
    )

print("\n===== Annealing result =====")
print(f"Final E/atom: {energy / N:.4f}")
print(f"Final A-B bond fraction: {unlike_bond_fraction(spins):.3f}")
print(f"Best E/atom: {best_energy / N:.4f}")
print(f"Best A-B bond fraction: {unlike_bond_fraction(best_spins):.3f}")
print(f"Best structure: T = {best_temperature}, step = {best_step}")