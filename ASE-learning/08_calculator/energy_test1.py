from ase.build import bulk
from ase.calculators.emt import EMT

atoms = bulk("Cu", "fcc", a=3.6)

atoms.calc = EMT()

energy = atoms.get_potential_energy()

print("总能量：", energy)
print("原子数：", len(atoms))
print("每原子能量：", energy / len(atoms))