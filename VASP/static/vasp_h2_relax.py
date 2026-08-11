import os
from datetime import datetime

from ase import Atoms
from ase.calculators.vasp import Vasp
from ase.optimize import BFGS
from ase.io import write


os.environ["VASP_PP_PATH"] = "/home/xv/apps/POT"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

vasp_command = "mpirun -np 2 /home/xv/apps/vasp.6.5.0/bin/vasp_std"
run_directory = f"vasp_h2_relax_{datetime.now():%Y%m%d_%H%M%S}"

# H2置于大真空盒中，初始键长0.74 Å
h2 = Atoms(
    "H2",
    positions=[
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.74],
    ],
    cell=[12.0, 12.0, 12.0],
    pbc=True
)

h2.center()

h2.calc = Vasp(
    command=vasp_command,
    directory=run_directory,
    txt="vasp.out",

    xc="PBE",
    encut=300,
    prec="Normal",

    kpts=(1, 1, 1),
    gamma=True,

    # H2是分子，不使用金属展宽
    ismear=0,
    sigma=0.05,

    ediff=1e-5,
    nelm=80,
    algo="Normal",

    # 由ASE的BFGS负责移动原子
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

print("===== H2 relaxation =====", flush=True)

optimizer = BFGS(
    h2,
    trajectory="h2_relax.traj",
    logfile="h2_relax.log"
)

optimizer.run(fmax=0.01, steps=30)

energy = h2.get_potential_energy()
forces = h2.get_forces()
bond_length = h2.get_distance(0, 1, mic=True)

write("h2_relaxed.xyz", h2)

print("\n===== H2 relaxation finished =====")
print(f"H2 energy: {energy:.8f} eV")
print(f"H-H bond length: {bond_length:.6f} Å")
print(f"Maximum force: {abs(forces).max():.6f} eV/Å")
print("Relaxed structure saved to: h2_relaxed.xyz")
print(f"VASP files saved in: {run_directory}")