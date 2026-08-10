import os
from datetime import datetime

from ase.build import bulk
from ase.calculators.vasp import Vasp


os.environ["VASP_PP_PATH"] = "/home/xv/apps/POT"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

run_directory = f"vasp_smoke_cu_{datetime.now():%Y%m%d_%H%M%S}"

# 创建一个原子的Cu面心立方原胞
cu = bulk("Cu", crystalstructure="fcc", a=3.615)

cu.calc = Vasp(
    command="mpirun -np 2 /home/xv/apps/vasp.6.5.0/bin/vasp_std",
    directory=run_directory,
    txt="vasp.out",

    xc="PBE",
    encut=300,
    prec="Normal",

    kpts=(4, 4, 4),
    gamma=True,

    # 金属体系使用展宽
    ismear=1,
    sigma=0.2,

    ediff=1e-5,
    nelm=60,
    algo="Normal",

    # 只进行单点能计算
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

print("Starting Cu calculation...", flush=True)

energy = cu.get_potential_energy()
forces = cu.get_forces()

print("\n===== Cu test passed =====")
print(f"Total energy: {energy:.8f} eV")
print(f"Energy per atom: {energy / len(cu):.8f} eV/atom")
print("Forces:")
print(forces)
print(f"Results saved in: {run_directory}")