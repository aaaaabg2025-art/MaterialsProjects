from ase.build import bulk
from ase.build import surface

cu = bulk("Cu", "fcc", a=3.6)

slab = surface(cu, (1, 1, 1), 4, 10.0)#切4层原子，真空层10.0

print(slab)
print()

print("原子数：")
print(len(slab))

print()

print("晶胞：")
print(slab.cell)
from ase.visualize import view

view(slab)