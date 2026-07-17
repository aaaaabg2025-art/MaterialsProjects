from ase.io import read

atoms = read("POSCAR")

print("化学式:")
print(atoms.get_chemical_formula())#输出化学式

print()

print("原子数:")
print(len(atoms))

print()

print("晶胞:")
print(atoms.cell)

print()

print("体积:")
print(atoms.get_volume())

print()

print("坐标:")
print(atoms.positions)

print()

for atom in atoms:
    print(atom.symbol, atom.position)
    
print()
