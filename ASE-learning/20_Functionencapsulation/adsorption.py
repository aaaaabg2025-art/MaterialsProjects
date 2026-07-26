from ase.build import add_adsorbate


def add_adsorbate_atom(
        slab,
        atom,
        site="fcc",
        height=1.5
):

    slab_new = slab.copy()

    add_adsorbate(
        slab_new,
        atom,
        height=height,
        position=site
    )

    return slab_new