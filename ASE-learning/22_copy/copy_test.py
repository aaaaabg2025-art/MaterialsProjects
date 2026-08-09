from ase.build import molecule

results = []

atoms = molecule("H2")

results.append(atoms.copy())

print("第一次保存：")
print("atoms:", atoms.positions)
print("results:", results[0].positions)

# 修改第一个原子的位置
atoms[0].position[2] += 5

print("\n修改 atoms 后：")
print("atoms:", atoms.positions)
print("results:", results[0].positions)

print("\nresults 中保存的：")
print(results[0])