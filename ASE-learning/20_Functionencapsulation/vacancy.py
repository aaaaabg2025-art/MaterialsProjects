def create_vacancy(
        slab,
        index
):

    slab_vac = slab.copy()

    del slab_vac[index]

    return slab_vac