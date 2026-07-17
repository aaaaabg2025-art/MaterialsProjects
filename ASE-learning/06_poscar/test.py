from ase.io import read

atoms = read("POSCAR")

for atom in atoms:
    print(atom.index, atom.symbol)#atom.index原子编号