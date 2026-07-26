from ase.calculators.emt import EMT


def calculate_energy(atoms):

    atoms.calc = EMT()

    energy = atoms.get_potential_energy()

    return energy