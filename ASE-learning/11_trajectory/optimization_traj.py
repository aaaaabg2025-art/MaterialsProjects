from ase.build import molecule
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from ase.io.trajectory import Trajectory

atoms = molecule("H2O")

# 故意拉长一个键，让优化有事情可做
atoms.positions[1][0] += 0.5

atoms.calc = EMT()

traj = Trajectory("optimize.traj", "w")

optimizer = BFGS(atoms)

print("优化前能量：")
print(atoms.get_potential_energy())

for i in range(10):

    traj.write(atoms)

    optimizer.run(steps=1)#只优化一步，然后立即返回程序

print("优化后能量：")
print(atoms.get_potential_energy())

traj.close()
