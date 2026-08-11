import os
import csv
from datetime import datetime

from ase.build import fcc111
from ase.calculators.vasp import Vasp


os.environ["VASP_PP_PATH"] = "/home/xv/apps/POT"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["I_MPI_PIN"] = "0"

vasp_command = "mpirun -np 2 /home/xv/apps/vasp.6.5.0/bin/vasp_std"

# 只改变ENCUT；其他参数和结构保持不变
encut_values = [300, 350, 400]
run_root = f"vasp_encut_test_{datetime.now():%Y%m%d_%H%M%S}"

results = []

print("===== ENCUT convergence test =====", flush=True)

for encut in encut_values:
    slab = fcc111(
        symbol="Cu",
        size=(2, 2, 3),
        a=3.615,
        vacuum=12.0
    )
    slab.pbc = True

    directory = f"{run_root}/encut_{encut}"

    slab.calc = Vasp(
        command=vasp_command,
        directory=directory,
        txt="vasp.out",

        xc="PBE",
        encut=encut,
        prec="Normal",

        kpts=(3, 3, 1),
        gamma=True,

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

    print(f"\nRunning ENCUT = {encut} eV ...", flush=True)

    energy = slab.get_potential_energy()
    energy_per_atom = energy / len(slab)

    if results:
        previous_energy = results[-1]["energy_per_atom"]
        difference = energy_per_atom - previous_energy
    else:
        difference = 0.0

    results.append({
        "encut_eV": encut,
        "energy_eV": energy,
        "energy_per_atom": energy_per_atom,
        "difference_from_previous": difference
    })

    print(f"Total energy: {energy:.8f} eV")
    print(f"Energy per atom: {energy_per_atom:.8f} eV/atom")
    print(f"Difference from previous: {difference:.8f} eV/atom")


with open("encut_convergence.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\n===== Summary =====")
for result in results:
    print(
        f"ENCUT = {result['encut_eV']:3d} eV | "
        f"E/atom = {result['energy_per_atom']:.8f} eV | "
        f"ΔE = {result['difference_from_previous']:.8f} eV/atom"
    )

print("\nResults saved to: encut_convergence.csv")