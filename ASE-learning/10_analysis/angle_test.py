from ase.build import molecule

atoms = molecule("NH3")

for i, atom in enumerate(atoms):
    print(i, atom.symbol)

print(atoms.get_angle(1,0,2))
print(atoms.get_angle(1,0,3))
print(atoms.get_angle(2,0,3))
atoms.set_angle(    1,    0,    2,    120)
print(
    atoms.get_angle(1,0,2)
)