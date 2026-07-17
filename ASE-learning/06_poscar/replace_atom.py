from ase.io import read

atoms = read("POSCAR")

print("修改前:")
print(atoms.get_chemical_formula())

atoms[0].symbol = "Ni"

print("修改后:")
print(atoms.get_chemical_formula())

print("修改前:")
print(atoms.positions)

atoms[0].position = [1, 1, 1]

print("修改后:")
print(atoms.positions)