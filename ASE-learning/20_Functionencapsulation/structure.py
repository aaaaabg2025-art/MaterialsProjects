from ase.build import fcc111


def build_surface(
        metal,
        size,
        vacuum
):

    slab = fcc111(
        metal,
        size=size,
        vacuum=vacuum
    )

    return slab
