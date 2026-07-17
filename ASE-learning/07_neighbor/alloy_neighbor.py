from ase.build import bulk
from ase.neighborlist import neighbor_list

cu = bulk("Cu", "fcc", a=3.6)

supercell = cu.repeat((3,3,3))

# 掺杂一个Ni
supercell[0].symbol = "Ni"

i, j = neighbor_list("ij", supercell, 3.0)

print("0号原子:", supercell[0].symbol)

for center, neighbor in zip(i, j):

    if center == 0:

        print(
            neighbor,
            supercell[neighbor].symbol
        )