from ase.build import fcc111
from ase.calculators.emt import EMT

slab = fcc111("Cu", size=(3,3,4), vacuum=10)

slab.calc = EMT()

E_slab = slab.get_potential_energy()

print("Surface:", E_slab)



from ase.build import molecule #EMT计算需要导入Atoms类

H2 = molecule("H2")

H2.calc = EMT()

E_H2 = H2.get_potential_energy()

print("H2:", E_H2)

from ase.build import add_adsorbate

slab_H = slab.copy()

add_adsorbate(
    slab_H,
    "H",
    height=1.5,
    position="ontop"
)

slab_H.calc = EMT()

E_total = slab_H.get_potential_energy()

print("Surface+H:", E_total)

print(slab_H)
print(slab_H.positions)

E_ads = slab_H.get_potential_energy() - E_slab - 0.5 * E_H2

print("Adsorption Energy:", E_ads)