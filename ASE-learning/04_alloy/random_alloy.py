import random

from ase.build import bulk
from ase.io import write

cu = bulk("Cu", "fcc", a=3.6, cubic=True)

supercell = cu.repeat((3, 3, 3))

# 随机选4个原子

indices = random.sample(range(len(supercell)), 4)

print("被替换的位置：")

for i in indices:
    supercell[i].symbol = "Ni"
    print(i)

print()
print(supercell.symbols)

write("random_CuNi.xyz", supercell)
print(supercell.get_chemical_formula())