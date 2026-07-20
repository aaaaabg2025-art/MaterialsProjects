from ase.build import bulk
from ase.calculators.emt import EMT

cu = bulk("Cu")
ni = bulk("Ni")

cu.calc = EMT()
ni.calc = EMT()

print("Cu:")
print(cu.get_potential_energy())

print()

print("Ni:")
print(ni.get_potential_energy())