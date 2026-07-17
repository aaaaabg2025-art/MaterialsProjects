from ase.build import bulk
from ase.neighborlist import neighbor_list

cu = bulk("Cu", "fcc", a=3.6)

supercell = cu.repeat((3,3,3))

supercell[0].symbol = "Ni"

i, j = neighbor_list("ij", supercell, 3.0)

ni_cu = 0
ni_ni = 0

for center, neighbor in zip(i, j):

    if center == 0:

        if supercell[neighbor].symbol == "Cu":
            ni_cu += 1

        elif supercell[neighbor].symbol == "Ni":
            ni_ni += 1

print("Ni-Cu:", ni_cu)
print("Ni-Ni:", ni_ni)