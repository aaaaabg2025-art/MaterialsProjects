import copy
import math
import random

# ---------- 参数 ----------
L = 20
J = -1.0
N = L * L

temperatures = [4.0, 3.0, 2.0, 1.0, 0.5, 0.3]

# 快冷：每个温度只有 1000 次尝试
fast_attempts_per_temperature = 1_000

# 慢冷：每个温度有 10000 次尝试
slow_attempts_per_temperature = 10_000
# --------------------------


def total_energy(spins):
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


def run_annealing(label, attempts_per_temperature, initial_spins, seed):
    """从相同初始构型执行一次退火。"""
    rng = random.Random(seed)

    # 每种冷却策略从相同初始构型开始
    spins = copy.deepcopy(initial_spins)
    energy = total_energy(spins)

    best_energy = energy
    best_spins = copy.deepcopy(spins)

    print(f"\n===== {label} =====")
    print(f"Attempts per temperature: {attempts_per_temperature}")
    print(f"Initial E/atom: {energy / N:.4f}")

    for temperature in temperatures:
        accepted_swaps = 0
        attempted_swaps = 0

        for _ in range(attempts_per_temperature):
            i1 = rng.randrange(L)
            j1 = rng.randrange(L)

            i2 = rng.randrange(L)
            j2 = rng.randrange(L)

            # 同种元素交换没有任何构型变化
            if spins[i1][j1] == spins[i2][j2]:
                continue

            attempted_swaps += 1

            # 试探性交换
            spins[i1][j1], spins[i2][j2] = (
                spins[i2][j2],
                spins[i1][j1],
            )

            new_energy = total_energy(spins)
            delta_e = new_energy - energy

            # Metropolis 规则
            if delta_e <= 0:
                accept = True
            else:
                probability = math.exp(-delta_e / temperature)
                accept = rng.random() < probability

            if accept:
                energy = new_energy
                accepted_swaps += 1

                if energy < best_energy:
                    best_energy = energy
                    best_spins = copy.deepcopy(spins)
            else:
                # 拒绝时恢复原构型
                spins[i1][j1], spins[i2][j2] = (
                    spins[i2][j2],
                    spins[i1][j1],
                )

        acceptance = accepted_swaps / attempted_swaps

        print(
            f"T = {temperature:3.1f} | "
            f"E/atom = {energy / N:.4f} | "
            f"A-B fraction = {unlike_bond_fraction(spins):.3f} | "
            f"Acceptance = {acceptance:.3f}"
        )

    return {
        "final_energy_per_atom": energy / N,
        "final_ab_fraction": unlike_bond_fraction(spins),
        "best_energy_per_atom": best_energy / N,
        "best_ab_fraction": unlike_bond_fraction(best_spins),
    }


# 创建一个固定成分、随机混合的共同初始构型
initial_rng = random.Random(20260906)

spins_1d = [1] * (N // 2) + [-1] * (N // 2)
initial_rng.shuffle(spins_1d)

initial_spins = [
    spins_1d[i * L:(i + 1) * L]
    for i in range(L)
]

fast_result = run_annealing(
    label="Fast cooling",
    attempts_per_temperature=fast_attempts_per_temperature,
    initial_spins=initial_spins,
    seed=100,
)

slow_result = run_annealing(
    label="Slow cooling",
    attempts_per_temperature=slow_attempts_per_temperature,
    initial_spins=initial_spins,
    seed=100,
)

print("\n===== Cooling-rate comparison =====")
print(
    f"Fast cooling | Final E/atom = "
    f"{fast_result['final_energy_per_atom']:.4f} | "
    f"A-B fraction = {fast_result['final_ab_fraction']:.3f}"
)

print(
    f"Slow cooling | Final E/atom = "
    f"{slow_result['final_energy_per_atom']:.4f} | "
    f"A-B fraction = {slow_result['final_ab_fraction']:.3f}"
)