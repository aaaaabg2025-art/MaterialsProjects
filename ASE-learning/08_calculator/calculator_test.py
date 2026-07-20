from ase.build import bulk
from ase.calculators.emt import EMT#有效介质理论

cu = bulk("Cu")

cu.calc = EMT()#给Cu安装EMT计算器

print(cu.get_potential_energy())