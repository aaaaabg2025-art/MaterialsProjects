from ase.build import bulk

primitive = bulk("Cu", "fcc", a=3.6)

cubic = bulk("Cu", "fcc", a=3.6, cubic=True)

supercell = cubic.repeat((2,2,2))

print("原胞")
print("原子数:", len(primitive))
print("体积:", primitive.get_volume())

print()

print("常规晶胞")
print("原子数:", len(cubic))
print("体积:", cubic.get_volume())

print()

print("超胞")
print("原子数:", len(supercell))
print("体积:", supercell.get_volume())