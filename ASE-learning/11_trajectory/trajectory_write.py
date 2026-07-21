from ase.build import molecule
from ase.io.trajectory import Trajectory

atoms = molecule("H2O")

traj = Trajectory("water.traj", "w")

traj.write(atoms)

traj.close()

print("轨迹保存成功")