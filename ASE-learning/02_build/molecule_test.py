from ase.build import molecule#调用库中的分子，自动构建模型

h2o = molecule("H2O")

print("元素:")
print(h2o.symbols)

print("原子数:")
print(len(h2o))

print("坐标:")
print(h2o.positions)
print(type(h2o))
for atom in h2o:
    print(atom.symbol, atom.position)