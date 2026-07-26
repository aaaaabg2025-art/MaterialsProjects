from ase.build import molecule
from calculator import calculate_energy


def get_reference_energy(atom):

    if atom == "H":

        molecule_ref = molecule("H2")

        E = calculate_energy(
            molecule_ref
        )

        return 0.5 * E


    elif atom == "O":

        molecule_ref = molecule("O2")

        E = calculate_energy(
            molecule_ref
        )

        return 0.5 * E


    else:

        raise ValueError(
            "Reference energy not defined"
        )