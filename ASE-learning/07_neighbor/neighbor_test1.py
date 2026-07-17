from ase.build import bulk
from ase.neighborlist import neighbor_list

cu = bulk("Cu", "fcc", a=3.6)

supercell = cu.repeat((3,3,3))

i, j, d = neighbor_list("ijd", supercell, 3.0)

for center, neighbor, distance in zip(i, j, d):

    if center == 0:

        print(
            "邻居:",
            neighbor,
            "距离:",
            distance
        )