from ase.build import molecule

atoms = molecule("NH3")

print("N-H1")

print(atoms.get_distance(0,1))

print()

print("N-H2")

print(atoms.get_distance(0,2))

print()

print("N-H3")

print(atoms.get_distance(0,3))

print()

print("H-H")

print(atoms.get_distance(1,2))