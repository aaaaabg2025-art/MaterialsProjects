from ase.build import bulk
from ase.io import write
cu = bulk("Cu", "fcc", a=3.6, cubic=True)

supercell = cu.repeat((3,3,3))


supercell[0].symbol = "Ni"
supercell[1].symbol = "Ni"
supercell[2].symbol = "Ni"
supercell[3].symbol = "Ni"
print(supercell.symbols)
for i in range(10):
    print(i, supercell[i].symbol)
write("CuNi_alloy.xyz", supercell)

print("原子数:", len(supercell))