from ase.build import bulk
from ase.io import write

cu = bulk("Cu", "fcc", a=3.6, cubic=True)

supercell = cu.repeat((3,3,3))

write("Cu_supercell.xyz", supercell)

print(len(supercell))