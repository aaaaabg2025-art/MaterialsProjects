"""GRACE + ASE prediction smoke test and convenient structure predictor.

Examples
--------
# Built-in silicon test (downloads the selected official GRACE model once):
python grace_test_si.py

# Predict a POSCAR/CIF/XYZ structure and write an ASE extended-XYZ result:
python grace_test_si.py --input POSCAR --output prediction.extxyz
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
os.environ.setdefault("GRACE_CACHE", str(ROOT / "models"))

from ase.build import bulk
from ase.io import read, write
from tensorpotential.calculator.foundation_models import grace_fm


DEFAULT_MODEL = "GRACE-3L-OMAT-large"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an ASE-compatible GRACE foundation-model prediction."
    )
    parser.add_argument(
        "-i", "--input", type=Path, help="Input structure readable by ASE (POSCAR/CIF/XYZ)."
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=ROOT / "prediction.extxyz",
        help="Output extended-XYZ file (default: prediction.extxyz).",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"GRACE model (default: {DEFAULT_MODEL}).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    atoms = read(args.input) if args.input else bulk("Si", "diamond", a=5.43, cubic=True)
    atoms.calc = grace_fm(args.model)

    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()
    stress = atoms.get_stress(voigt=True)
    atoms.info["grace_model"] = args.model
    atoms.info["energy_eV"] = float(energy)
    atoms.arrays["forces_eV_A"] = forces
    atoms.info["stress_eV_A3"] = stress.tolist()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write(args.output, atoms, format="extxyz")
    print(f"GRACE prediction complete: {args.output}")
    print(f"model: {args.model}")
    print(f"atoms: {len(atoms)}")
    print(f"energy: {energy:.8f} eV")
    print(f"max |force|: {(forces**2).sum(axis=1).max()**0.5:.8f} eV/A")
    print(f"stress (xx, yy, zz, yz, xz, xy): {stress} eV/A^3")


if __name__ == "__main__":
    main()
