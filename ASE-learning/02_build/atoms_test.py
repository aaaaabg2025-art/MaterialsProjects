from ase import Atoms

h2 = Atoms("H2",
positions=[
    (0,0,0),
    (0,0,0.74)
]
)
print("坐标：")
print(h2.positions)
print("元素：")
print(h2.symbols)
print("原子数：")
print(len(h2))
for atom in h2:
    print(atom.symbol, atom.position)
    print(type(h2.positions))# Python 中‌NumPy 库核心多维数组对象‌的类型表示，意为该变量是一个由 NumPy 创建的、存储同类型元素的 N 维数组实例 
    print(h2.positions[0])
    print(h2.positions[1])
 #   h2.positions[1] = [0, 0, 1.0]#对第二个原子位置坐标修改#

#print(h2.positions)#