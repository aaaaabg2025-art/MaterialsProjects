import os
from datetime import datetime

from ase.build import fcc111, add_adsorbate
from ase.calculators.vasp import Vasp
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ase.io import write


# VASP运行环境
os.environ["VASP_PP_PATH"] = "/home/xv/apps/POT"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

vasp_command = "mpirun -np 2 /home/xv/apps/vasp.6.5.0/bin/vasp_std"
run_directory = f"vasp_h_bridge_relax_{datetime.now():%Y%m%d_%H%M%S}"


# 创建Cu(111)表面：2×2重复、3层，共12个Cu原子
slab = fcc111(
    symbol="Cu",
    size=(2, 2, 3),
    a=3.615,
    vacuum=12.0
)

# VASP要求三个方向都开启周期边界；
# z方向的12 Å真空层会隔开相邻表面。
slab.pbc = True

add_adsorbate(slab, "H", height=1.60, position="bridge")

# fcc111的tag：最底层Cu具有最大的tag值
tags = slab.get_tags()
bottom_layer = tags == tags.max()

slab.set_constraint(FixAtoms(mask=bottom_layer))

print(f"Fixed atoms: {bottom_layer.sum()}", flush=True)

print("===== H on Cu(111): bridge-site structural relaxation =====", flush=True)
print(f"Number of atoms: {len(slab)}", flush=True)
print(f"Cell:\n{slab.cell}", flush=True)
print(f"Calculation directory: {run_directory}", flush=True)


# 单点能计算：不移动原子
slab.calc = Vasp(
    command=vasp_command,
    directory=run_directory,
    txt="vasp.out",

    xc="PBE",
    encut=300,
    prec="Normal",

    # 表面沿z方向只需要1个k点
    kpts=(3, 3, 1),
    gamma=True,

    # Cu是金属，使用展宽
    ismear=1,
    sigma=0.2,

    ediff=1e-5,
    nelm=80,
    algo="Normal",

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

print("Starting VASP...", flush=True)

optimizer = BFGS(
    slab,
    trajectory="h_bridge_relax.traj",
    logfile="h_bridge_relax.log"
)

print("Starting structural relaxation...", flush=True)

optimizer.run(fmax=0.05, steps=60)

energy = slab.get_potential_energy()
forces = slab.get_forces()
max_force = abs(forces).max()

write("h_bridge_relaxed.xyz", slab)

print("\n===== Relaxation finished =====")
print(f"Final energy: {energy:.8f} eV")
print(f"Final maximum force: {max_force:.6f} eV/Å")
print("Relaxed structure saved to: h_bridge_relaxed.xyz")
print(f"VASP files saved in: {run_directory}")