from ase.build import molecule
from ase.io.trajectory import Trajectory

atoms = molecule("H2O")

traj = Trajectory("water.traj", "w")

# Step 0
traj.write(atoms)

# Step 1
atoms.positions[0][0] += 0.2
traj.write(atoms)

# Step 2
atoms.positions[1][1] += 0.2
traj.write(atoms)

traj.close()

print("保存完成")