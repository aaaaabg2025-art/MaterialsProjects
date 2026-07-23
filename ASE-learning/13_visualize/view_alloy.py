from ase.build import bulk
from ase.visualize import view

atoms = bulk("Cu", "fcc", a=3.6, cubic=True)
atoms = atoms.repeat((3,3,3))
atoms[0].symbol = "Ni"

view(atoms)