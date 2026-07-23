from ase.build import molecule
from ase.visualize import view

atoms = molecule("H2O")

view(atoms)