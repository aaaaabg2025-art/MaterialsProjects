import os
import csv
from datetime import datetime

from ase.build import fcc111
from ase.calculators.vasp import Vasp


# ---------- VASP 运行环境 ----------
os.environ["VASP_PP_PATH"] = "/home/xv/apps/POT"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

vasp_command = "mpirun -np 2 /home/xv/apps/vasp.6.5.0/bin/vasp_std"


# ---------- 只改变 k 点 ----------
kpoint_values = [
    (4, 4, 1),
    (5, 5, 1),
    (6, 6, 1),
    (7, 7, 1),
]

run_root = f"vasp_kpoint_test_{datetime.now():%Y%m%d_%H%M%S}"
results = []

print("===== K-point convergence test =====", flush=True)


for kpts in kpoint_values:
    # 每次都建立完全相同的 Cu(111) 表面
    slab = fcc111(
        symbol="Cu",
        size=(2, 2, 3),
        a=3.615,
        vacuum=12.0
    )

    # VASP 要求三个方向均为周期性
    slab.pbc = True

    # 例如 (3, 3, 1) 转为 "3x3x1"
    kpoint_name = f"{kpts[0]}x{kpts[1]}x{kpts[2]}"
    directory = f"{run_root}/kpts_{kpoint_name}"

    slab.calc = Vasp(
        command=vasp_command,
        directory=directory,
        txt="vasp.out",

        xc="PBE",
        encut=450,
        prec="Accurate",

        # 本次唯一改变的参数
        kpts=kpts,
        gamma=True,

        # Cu 是金属
        ismear=1,
        sigma=0.2,

        ediff=1e-6,
        nelm=80,
        algo="Normal",

        # 单点能计算，不优化原子
        ibrion=-1,
        nsw=0,

        # 不读取旧计算的重启文件
        istart=0,
        icharg=2,

        lreal=False,
        lscalapack=False,
        ncore=1,

        # 不生成大型重启文件
        lwave=False,
        lcharg=False
    )

    print(f"\nRunning k-points = {kpoint_name} ...", flush=True)

    energy = slab.get_potential_energy()
    energy_per_atom = energy / len(slab)

    # 与上一个 k 点结果比较
    if results:
        difference = energy_per_atom - results[-1]["energy_per_atom"]
    else:
        difference = 0.0

    results.append({
        "kpts": kpoint_name,
        "energy_eV": energy,
        "energy_per_atom": energy_per_atom,
        "difference_from_previous": difference
    })

    print(f"Total energy: {energy:.8f} eV")
    print(f"Energy per atom: {energy_per_atom:.8f} eV/atom")
    print(f"Difference from previous: {difference:.8f} eV/atom")


# 保存结果表格
with open("kpoint_convergence.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)


print("\n===== Summary =====")
for result in results:
    print(
        f"k-points = {result['kpts']} | "
        f"E/atom = {result['energy_per_atom']:.8f} eV | "
        f"ΔE = {result['difference_from_previous']:.8f} eV/atom"
    )

print("\nResults saved to: kpoint_convergence.csv")