from ase.build import bulk
from ase.visualize import view

atoms = bulk("Cu", "fcc", a=3.6, cubic=True)

view(atoms)
