from ase.build import molecule
from ase.constraints import FixAtoms

atoms = molecule("H2O")

constraint = FixAtoms(indices=[0])

atoms.set_constraint(constraint)

print(atoms.constraints)