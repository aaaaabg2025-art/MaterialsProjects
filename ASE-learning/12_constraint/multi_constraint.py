from ase.build import molecule
from ase.constraints import FixAtoms
from ase.calculators.emt import EMT
from ase.optimize import BFGS

atoms = molecule("H2O")

# 故意拉动两个 H
atoms.positions[1][0] += 0.5
atoms.positions[2][1] -= 0.5

print("优化前：")
print(atoms.positions)

atoms.calc = EMT()

# 固定 O 和一个 H
mask = [True, True, False]
constraint = FixAtoms(mask=mask)

atoms.set_constraint(constraint)

optimizer = BFGS(atoms)

optimizer.run(fmax=0.05)

print()
print("优化后：")
print(atoms.positions)