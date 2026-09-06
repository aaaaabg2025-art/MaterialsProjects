import copy
import math
import random

# ---------- 参数 ----------
L = 20
TEMPERATURE = 3.0
STEPS = 20_000

# J < 0：不同元素相邻更稳定，模拟“异种原子偏好近邻”
J = -1.0
# --------------------------

N = L * L

# 固定成分：一半 A 原子（+1），一半 B 原子（-1）
spins_1d = [1] * (N // 2) + [-1] * (N // 2)
random.shuffle(spins_1d)

spins = [
    spins_1d[i * L:(i + 1) * L]
    for i in range(L)
]


def total_energy(spins):
    """计算二元合金玩具模型的总能量。"""
    energy = 0.0

    for i in range(L):
        for j in range(L):
            atom_type = spins[i][j]

            # 周期性边界下的右侧、下侧邻居
            right = spins[i][(j + 1) % L]
            down = spins[(i + 1) % L][j]

            energy -= J * atom_type * right
            energy -= J * atom_type * down

    return energy

def unlike_bond_fraction(spins):
    """返回所有最近邻键中，A-B 异种键的比例。"""
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
best_step = 0

accepted_moves = 0
attempted_swaps = 0

print("===== Binary-alloy swap Monte Carlo =====")
print(f"Lattice: {L} x {L}")
print(f"Temperature: {TEMPERATURE}")
print(f"Composition: A = 50%, B = 50%")
print(f"J: {J}")
print(f"Initial energy: {energy:.2f}")

for step in range(1, STEPS + 1):
    # 1. 随机选两个格点
    i1 = random.randrange(L)
    j1 = random.randrange(L)

    i2 = random.randrange(L)
    j2 = random.randrange(L)

    # 2. 若两处是同种元素，交换没有意义，跳过
    if spins[i1][j1] == spins[i2][j2]:
        continue

    attempted_swaps += 1

    # 3. 先执行试探性交换
    spins[i1][j1], spins[i2][j2] = (
        spins[i2][j2],
        spins[i1][j1],
    )

    # 为了代码清楚，先重新计算总能量。
    # 以后会学习只计算局部 ΔE 的高效写法。
    new_energy = total_energy(spins)
    delta_e = new_energy - energy

    # 4. Metropolis 接受/拒绝规则
    if delta_e <= 0:
        accept = True
    else:
        probability = math.exp(-delta_e / TEMPERATURE)
        accept = random.random() < probability

    # 5. 接受则保留交换；拒绝则换回原构型
    if accept:
        energy = new_energy
        accepted_moves += 1

        if energy < best_energy:
            best_energy = energy
            best_spins = copy.deepcopy(spins)
            best_step = step
    else:
        spins[i1][j1], spins[i2][j2] = (
            spins[i2][j2],
            spins[i1][j1],
        )

    if step % 2000 == 0:
        acceptance = accepted_moves / attempted_swaps
        print(
            f"Step {step:5d} | "
            f"E/atom = {energy / N:.4f} | "
            f"Best E/atom = {best_energy / N:.4f} | "
            f"Acceptance = {acceptance:.3f}"
        )

print("\n===== Final result =====")
print(f"Final energy: {energy:.2f}")
print(f"Final energy per atom: {energy / N:.4f}")
print(f"Best energy: {best_energy:.2f}")
print(f"Best energy per atom: {best_energy / N:.4f}")
print(f"Best structure found at step: {best_step}")

if attempted_swaps > 0:
    print(f"Swap acceptance rate: {accepted_moves / attempted_swaps:.3f}")

final_unlike_fraction = unlike_bond_fraction(spins)
best_unlike_fraction = unlike_bond_fraction(best_spins)

print(f"Final A-B bond fraction: {final_unlike_fraction:.3f}")
print(f"Best A-B bond fraction: {best_unlike_fraction:.3f}")