from ase.io.trajectory import Trajectory

traj = Trajectory("water.traj")

atoms = traj[0]

print(atoms)
print(atoms.positions)
print("轨迹共有：", len(traj), "帧")