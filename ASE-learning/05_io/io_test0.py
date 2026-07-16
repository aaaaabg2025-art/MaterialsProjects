from ase.io import read

atoms = read("water.xyz")

print(atoms)

print("元素:")
print(atoms.symbols)

print("原子数:")
print(len(atoms))

print("坐标:")
print(atoms.positions)