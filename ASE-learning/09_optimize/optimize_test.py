from ase.build import bulk
from ase.calculators.emt import EMT
from ase.optimize import BFGS

# 建立 Cu3Ni
atoms = bulk("Cu", "fcc", a=3.6, cubic=True)
atoms[0].symbol = "Ni"
atoms[0].position += (0.2, 0.1, 0)

# 指定计算器
atoms.calc = EMT()

print("优化前能量：")
print(atoms.get_potential_energy())

# 建立优化器
opt = BFGS(atoms)

# 开始优化
opt.run(fmax=0.01)#最大的原子受力不能超过 0.01 eV/Å

print("优化后能量：")
print(atoms.get_potential_energy())