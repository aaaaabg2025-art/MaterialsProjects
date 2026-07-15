from ase.build import bulk
from ase.io import write
cu = bulk("Cu", "fcc", a=3.6, cubic=True)

for i, atom in enumerate(cu):#依次访问每个原子
    print(i, atom.symbol)
    cu[0].symbol = "Ni"


write("CuNi.xyz", cu)

print(cu.symbols)