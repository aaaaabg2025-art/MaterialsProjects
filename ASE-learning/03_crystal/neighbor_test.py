from ase.build import bulk
from ase.io import write

cu = bulk("Cu", "fcc", a=3.6, cubic=True)

write("Cu_unitcell.xyz", cu)