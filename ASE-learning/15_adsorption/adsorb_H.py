from ase.build import bulk
from ase.build import surface
from ase.build import add_adsorbate
from ase.visualize import view
from ase.build import fcc111

cu = bulk("Cu", "fcc", a=3.6)

slab = fcc111(
    "Cu",
    size=(3,3,4),
    vacuum=10
)
add_adsorbate(
    slab,
    "H",
    height=1.5,
    position="ontop"
)
view(slab)