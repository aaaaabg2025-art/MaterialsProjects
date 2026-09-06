import math
import random
import copy

# ---------- 可修改的参数 ----------
L = 20                 # 晶格边长：20×20 个自旋
TEMPERATURE = 2.5      # 温度（无量纲）
STEPS = 10_000         # Monte Carlo 尝试次数
J = 1.0                # 相邻自旋耦合强度
# ---------------------------------

# 每个格点的自旋：+1 或 -1
spins = [
    [random.choice([-1, 1]) for _ in range(L)]
    for _ in range(L)
]


def total_energy(spins):
    """计算整个 Ising 晶格的能量。"""
    energy = 0.0

    for i in range(L):
        for j in range(L):
            spin = spins[i][j]

            # 只算右侧、下侧邻居，避免同一对邻居重复计算
            right = spins[i][(j + 1) % L]
            down = spins[(i + 1) % L][j]

            energy -= J * spin * right
            energy -= J * spin * down

    return energy


def delta_energy_if_flip(spins, i, j):
    """假设翻转 (i, j) 的自旋，计算能量变化 ΔE。"""
    spin = spins[i][j]

    # 周期性边界：边缘格点也与另一侧相连
    neighbors = (
        spins[(i - 1) % L][j]
        + spins[(i + 1) % L][j]
        + spins[i][(j - 1) % L]
        + spins[i][(j + 1) % L]
    )

    return 2.0 * J * spin * neighbors


energy = total_energy(spins)
accepted_moves = 0

# 记录整个 MC 过程中发现的最低能构型
best_energy = energy
best_spins = copy.deepcopy(spins)
best_step = 0

print("===== Ising Monte Carlo simulation =====")
print(f"Lattice: {L} x {L}")
print(f"Temperature: {TEMPERATURE}")
print(f"Initial energy: {energy:.2f}")

for step in range(1, STEPS + 1):
    # 1. 随机挑选一个格点
    i = random.randrange(L)
    j = random.randrange(L)

    # 2. 尝试翻转该格点自旋，计算 ΔE
    delta_e = delta_energy_if_flip(spins, i, j)

    # 3. Metropolis 接受/拒绝规则
    if delta_e <= 0:
        accept = True
    else:
        probability = math.exp(-delta_e / TEMPERATURE)
        accept = random.random() < probability

    # 4. 若接受，真正翻转自旋并更新能量
    if accept:
        spins[i][j] *= -1
        energy += delta_e
        accepted_moves += 1

        # 若当前构型刷新历史最低能量，保存它
        if energy < best_energy:
            best_energy = energy
            best_spins = copy.deepcopy(spins)
            best_step = step

    # 每 1,000 步输出一次进度
    if step % 1000 == 0:
        print(
            f"Step {step:5d} | "
            f"Energy/spin = {energy / (L * L):.4f} | "
            f"Acceptance = {accepted_moves / step:.3f}"
        )

print("\n===== Final result =====")
print(f"Final energy: {energy:.2f}")
print(f"Best energy found: {best_energy:.2f}")
print(f"Best energy per spin: {best_energy / (L * L):.4f}")
print(f"Best structure found at step: {best_step}")
print(f"Acceptance rate: {accepted_moves / STEPS:.3f}")