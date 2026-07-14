from ase.build import bulk
from ase.io import write

cu = bulk("Cu", "fcc", a=3.6, cubic=True)
cu_2x2x2 = cu.repeat((2,2,2))

write("Cu_2x2x2.xyz", cu_2x2x2)