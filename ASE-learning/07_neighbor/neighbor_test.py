from ase.build import bulk
from ase.neighborlist import neighbor_list

cu = bulk("Cu", "fcc", a=3.6)

supercell = cu.repeat((3,3,3))

i, j = neighbor_list("ij", supercell, 3.0)

count = 0

for center in i:
    if center == 0:
        count += 1

print("0号原子的配位数:")
print(count)