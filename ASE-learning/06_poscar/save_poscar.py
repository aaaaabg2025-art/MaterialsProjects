from ase.io import read
from ase.io import write

atoms = read("POSCAR")

atoms[0].symbol = "Ni"

write("POSCAR_Ni", atoms)

print("保存成功")