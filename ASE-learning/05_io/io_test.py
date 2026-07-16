from ase.io import read
from ase.io import write

atoms = read("water.xyz")

print("修改前:")
print(atoms.symbols)

atoms[1].symbol = "F"

print("修改后:")
print(atoms.symbols)

write("modified.xyz", atoms)
for i, atom in enumerate(atoms):
    print(i, atom.symbol)