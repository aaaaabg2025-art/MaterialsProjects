from ase.build import bulk

cu = bulk("Cu", "fcc", a=3.6, cubic=True)

print("元素:")
print(cu.symbols)

print()

print("原子数:")
print(len(cu))

print()

print("坐标:")
print(cu.positions)