from ase.build import bulk
from ase.calculators.emt import EMT

# Cu（4原子）
cu = bulk("Cu", "fcc", a=3.6, cubic=True)
cu.calc = EMT()
E_cu = cu.get_potential_energy()

# Ni（4原子）
ni = bulk("Ni", "fcc", a=3.52, cubic=True)
ni.calc = EMT()
E_ni = ni.get_potential_energy()

# Cu3Ni
alloy = bulk("Cu", "fcc", a=3.6, cubic=True)
alloy[0].symbol = "Ni"
alloy.calc = EMT()
E_alloy = alloy.get_potential_energy()

print("Cu4:", E_cu)
print("Ni4:", E_ni)
print("Cu3Ni:", E_alloy)

print("Cu 每原子:", E_cu / len(cu))
print("Ni 每原子:", E_ni / len(ni))
print("Cu3Ni 每原子:", E_alloy / len(alloy))
formation_energy = E_alloy - (3/4 * E_cu + 1/4 * E_ni)

print("形成能:", formation_energy, "eV")

formation_energy_per_atom = formation_energy / len(alloy)

print("每原子形成能:", formation_energy_per_atom, "eV/atom")