from ase.io import read
from ase.io import write

atoms = read("POSCAR")

atoms[0].symbol = "Ni"

write("POSCAR_Ni", atoms)#保存成poscar文件

print("保存成功")