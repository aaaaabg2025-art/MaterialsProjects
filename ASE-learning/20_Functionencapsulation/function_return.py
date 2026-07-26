from ase.build import fcc111
from ase.calculators.emt import EMT

def build_surface(
    metal="Cu",
    size=(3,3,4),
    vacuum=10,):

    slab = fcc111(
        metal,
        size=size,
        vacuum=vacuum
    )

    slab.calc = EMT()
    E = slab.get_potential_energy()
    return {
            "structure": slab,
            "energy": E,
            "metal": metal,
            "atoms": len(slab)
        }

result = build_surface(metal="Ni")


print(result["metal"])
print(result["energy"])
print(result["atoms"])