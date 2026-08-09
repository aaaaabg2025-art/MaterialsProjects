from ase.build import fcc111
from ase.io import write

slab = fcc111(
    "Cu",
    size=(3,3,4),
    vacuum=10
)

write(
    "Cu111.xyz",
    slab
)

print("Finished!")