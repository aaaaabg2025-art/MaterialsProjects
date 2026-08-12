import os
import json
from datetime import datetime

from ase import Atoms
from ase.build import add_adsorbate, fcc111
from ase.calculators.vasp import Vasp
from ase.constraints import FixAtoms
from ase.io import write
from ase.optimize import BFGS


# ---------- 运行环境 ----------
os.environ["VASP_PP_PATH"] = "/home/xv/apps/POT"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

vasp_command = "mpirun -np 2 /home/xv/apps/vasp.6.5.0/bin/vasp_std"
run_root = f"vasp_bridge_final_{datetime.now():%Y%m%d_%H%M%S}"


def create_vasp_calculator(directory, kpts, is_metal):
    """创建一套统一的 VASP 计算器。"""
    if is_metal:
        ismear = 1
        sigma = 0.2
    else:
        ismear = 0
        sigma = 0.05

    return Vasp(
        command=vasp_command,
        directory=directory,
        txt="vasp.out",

        xc="PBE",
        encut=450,
        prec="normal",

        kpts=kpts,
        gamma=True,

        ismear=ismear,
        sigma=sigma,

        ediff=1e-6,
        nelm=100,
        algo="Normal",

        # 原子位置由 ASE 的 BFGS 控制
        ibrion=-1,
        nsw=0,

        istart=0,
        icharg=2,

        lreal=False,
        lscalapack=False,
        ncore=1,

        lwave=False,
        lcharg=False
    )


def relax(atoms, calculator, fmax, name):
    """绑定计算器并进行 ASE-BFGS 优化。"""
    atoms.calc = calculator

    optimizer = BFGS(
        atoms,
        trajectory=f"{name}.traj",
        logfile="-"
    )
    print(f"Starting {name}: fmax target = {fmax} eV/Å", flush=True)

    optimizer.run(fmax=fmax, steps=80)

    energy = atoms.get_potential_energy()
    max_force = abs(atoms.get_forces()).max()

    return energy, max_force


# ---------- 1. 清洁 Cu(111) 表面 ----------
print("===== 1. Clean Cu(111) relaxation =====", flush=True)

slab = fcc111(
    symbol="Cu",
    size=(2, 2, 3),
    a=3.615,
    vacuum=12.0
)
slab.pbc = True

# 固定最底层的 4 个 Cu 原子
tags = slab.get_tags()
bottom_layer = tags == tags.max()
slab.set_constraint(FixAtoms(mask=bottom_layer))

print(f"Number of Cu atoms: {len(slab)}")
print(f"Fixed atoms: {bottom_layer.sum()}")

slab_energy, slab_force = relax(
    atoms=slab,
    calculator=create_vasp_calculator(
        directory=f"{run_root}/clean_slab",
        kpts=(3, 3, 1),
        is_metal=True
    ),
    fmax=0.05,
    name="clean_slab_relax"
)

write("clean_slab_relaxed.xyz", slab)

print(f"Clean slab energy: {slab_energy:.8f} eV")
print(f"Clean slab max force: {slab_force:.6f} eV/Å")


# ---------- 2. 桥位 H/Cu(111) ----------
print("\n===== 2. H on bridge-site relaxation =====", flush=True)

# 从已经优化的清洁表面出发，再加入 H
slab_h = slab.copy()
add_adsorbate(slab_h, "H", height=1.60, position="bridge")

slab_h_energy, slab_h_force = relax(
    atoms=slab_h,
    calculator=create_vasp_calculator(
        directory=f"{run_root}/bridge_h",
        kpts=(7, 7, 1),
        is_metal=True
    ),
    fmax=0.05,
    name="bridge_h_relax"
)

write("bridge_h_relaxed.xyz", slab_h)

print(f"Slab + H energy: {slab_h_energy:.8f} eV")
print(f"Slab + H max force: {slab_h_force:.6f} eV/Å")


# ---------- 3. H2 参考体系 ----------
print("\n===== 3. H2 relaxation =====", flush=True)

h2 = Atoms(
    "H2",
    positions=[
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.74]
    ],
    cell=[12.0, 12.0, 12.0],
    pbc=True
)
h2.center()

h2_energy, h2_force = relax(
    atoms=h2,
    calculator=create_vasp_calculator(
        directory=f"{run_root}/h2",
        kpts=(1, 1, 1),
        is_metal=False
    ),
    fmax=0.01,
    name="h2_relax"
)

h2_bond_length = h2.get_distance(0, 1, mic=True)
write("h2_final_relaxed.xyz", h2)

print(f"H2 energy: {h2_energy:.8f} eV")
print(f"H-H bond length: {h2_bond_length:.6f} Å")
print(f"H2 max force: {h2_force:.6f} eV/Å")


# ---------- 4. 吸附能 ----------
adsorption_energy = slab_h_energy - slab_energy - 0.5 * h2_energy

results = {
    "parameters": {
        "xc": "PBE",
        "encut_eV": 450,
        "kpts_slab": [3, 3, 1],
        "kpts_h2": [1, 1, 1],
        "surface": "Cu(111), 2x2x3",
        "site": "bridge"
    },
    "energies_eV": {
        "clean_slab": slab_energy,
        "slab_plus_H": slab_h_energy,
        "H2": h2_energy,
        "adsorption_energy": adsorption_energy
    },
    "final_max_forces_eV_per_A": {
        "clean_slab": slab_force,
        "slab_plus_H": slab_h_force,
        "H2": h2_force
    },
    "H2_bond_length_A": h2_bond_length
}

with open("bridge_adsorption_result.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2, ensure_ascii=False)

print("\n===== Final result =====")
print(f"Adsorption energy: {adsorption_energy:.6f} eV")

if adsorption_energy < 0:
    print("Result: exothermic adsorption under this model.")
else:
    print("Result: endothermic adsorption under this model.")

print("Summary saved to: bridge_adsorption_result.json")
print(f"VASP files saved in: {run_root}")