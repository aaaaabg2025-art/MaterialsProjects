from ase.build import molecule

atoms = molecule("H2O")

matrix = atoms.get_all_distances()

for row in matrix:
    print(row[0])