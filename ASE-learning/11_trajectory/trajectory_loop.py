from ase.io.trajectory import Trajectory
from ase.calculators.emt import EMT
traj = Trajectory("water.traj")

for atoms in traj:#遍历每一帧
    print(atoms.get_chemical_formula())
    

for atoms in traj:
    print("-----------")
    print(atoms.positions)

for i, atoms in enumerate(traj):#输出当前是第几帧 元素对象
    print("Step", i)
    print(atoms.get_chemical_formula())
for step, atoms in enumerate(traj):
    atoms.calc = EMT()  #每一帧重新绑定emt计算器
    print(step)
    print(atoms.get_potential_energy())