from ase.build import bulk

cu = bulk("Cu", "fcc", a=3.6)

print("元素:")
print(cu.symbols)

print()

print("原子数:")
print(len(cu))

print()

print("坐标:")
print(cu.positions)

print()

print("晶胞:")
print(cu.cell)

print()

print("PBC:")
print(cu.pbc)

print()

print("晶胞体积:")
print(cu.get_volume())