from ase.build import fcc111
from ase.visualize import view

def build_surface(
    metal="Cu",
    size=(3,3,4),
    vacuum=10,
):

    slab = fcc111(
        metal,
        size=size,
        vacuum=vacuum
    )

    return slab

surface = build_surface()

print(surface)

surface = build_surface(metal="Ni")

print(surface)

surface = build_surface(size=(4, 4, 5))

print(surface)