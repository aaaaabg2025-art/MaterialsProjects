from ase.build import molecule
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.optimize import BFGS

atoms = molecule("H2O")

# 拉长一个键
atoms.positions[1][0] += 0.5

# 固定氧原子（0号）
constraint = FixAtoms(indices=[0])
atoms.set_constraint(constraint)

atoms.calc = EMT()

print("优化前：")
print(atoms.positions)

optimizer = BFGS(atoms)
optimizer.run(fmax=0.05)

print()
print("优化后：")
print(atoms.positions)