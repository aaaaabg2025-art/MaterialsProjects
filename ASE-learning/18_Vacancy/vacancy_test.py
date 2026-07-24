from ase.build import fcc111
from ase.calculators.emt import EMT
from ase.visualize import view
from ase.build import molecule #EMT计算需要导入Atoms类
from ase.build import add_adsorbate
H2 = molecule("H2")

H2.calc = EMT()

E_H2 = H2.get_potential_energy()

print(f"H2: {E_H2:.6f} eV")
sites = [    "ontop",    "bridge",    "fcc",    "hcp"]
E_vacancy = {}
E_ads = {}
E_total = {}
results = []
slab = fcc111("Cu", size=(3,3,4), vacuum=10)
atoms_to_delete = [27, 18, 9, 0]
for site in sites:
        print(f"\nCurrent site: {site}")
        for i in atoms_to_delete:

            print(f"    Delete atom {i}")

            slab_new = slab.copy()   # 每次复制一个新的表面

            del slab_new[i]          # 删除第 i 个原子

            slab_new.calc = EMT()

            E_vacancy[i]= slab_new.get_potential_energy()

            print(f"删除 {i} 号原子")
            print(f"Vacancy Energy : {E_vacancy [i]:.6f} eV")

            slab_H = slab_new.copy()

            add_adsorbate(
            slab_H,
            "H",
            height=1.5,
            position=site
            )
            slab_H.calc = EMT()
            E_total[i] = slab_H.get_potential_energy()
            print(f"E_total: {i} {E_total[i]:.6f} eV")
            E_ads[i] = E_total[i] - E_vacancy[i] - 0.5 * E_H2
            results.append(
                     {
                     "site": site,
                     "vacancy": i,
                     "vacancy_energy": E_vacancy[i],
                     "total_energy": E_total[i],
                     "adsorption_energy": E_ads[i]
                     }
)
            print(f"Adsorption Energy: {i} {E_ads[i]:.6f} eV")
            print("-" * 40)
print("\n========== Summary ==========")
print(f"Adsorption Site : {site}")
print("-" * 65)
print(f"{'Index':<8}{'Vacancy(eV)':<18}{'Total(eV)':<18}{'Ads(eV)':<18}")
print("-" * 65)

for i in atoms_to_delete:
        print(
        f"{i:<8}"
        f"{E_vacancy[i]:<18.6f}"
        f"{E_total[i]:<18.6f}"
        f"{E_ads[i]:<18.6f}"
        )
for r in results:

    print(r)    