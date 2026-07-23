from ase.build import fcc111
from ase.calculators.emt import EMT
from ase.build import add_adsorbate
slab = fcc111("Cu", size=(3,3,4), vacuum=10)

slab.calc = EMT()

E_slab = slab.get_potential_energy()

print("Surface:", E_slab)

from ase.build import molecule 
H2 = molecule("H2")

H2.calc = EMT()

E_H2 = H2.get_potential_energy()

print("H2:", E_H2)


slab_H = slab.copy()
sites = ["ontop", "bridge", "fcc", "hcp"]

for site in sites:

    slab_H = fcc111(
        "Cu",
        size=(3,3,4),
        vacuum=10
    )

    add_adsorbate(
        slab_H,
        "H",
        height=1.5,
        position=site
    )
    slab_H.calc = EMT()


    E_ads = slab_H.get_potential_energy() - E_slab - 0.5 * E_H2

    print("Adsorption Energy:", E_ads)
    slab_H.calc = EMT()

    print(site)

    print(slab_H.get_potential_energy())
   

E_ads = slab_H.get_potential_energy() - E_slab - 0.5 * E_H2

print("Adsorption Energy:", E_ads)