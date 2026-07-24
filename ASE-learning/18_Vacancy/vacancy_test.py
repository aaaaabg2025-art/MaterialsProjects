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
print("-" * 80)
print(
    f"{'Site':<10}"
    f"{'Index':<8}"
    f"{'Vacancy(eV)':<15}"
    f"{'Total(eV)':<15}"
    f"{'Ads(eV)':<15}"
)
print("-" * 80)

for r in results:
    print(
        f"{r['site']:<10}"
        f"{r['vacancy']:<8}"
        f"{r['vacancy_energy']:<15.6f}"
        f"{r['total_energy']:<15.6f}"
        f"{r['adsorption_energy']:<15.6f}"
    )
best = min(
results,
key=lambda x: x["adsorption_energy"]
)
print("\n===== Best Structure =====")
print(f"Site      : {best['site']}")
print(f"Vacancy   : {best['vacancy']}")
print(f"Ads Energy: {best['adsorption_energy']:.6f} eV")
sorted_results = sorted(
    results,
    key=lambda x: x["adsorption_energy"]
)
print("\n===== Sorted by Adsorption Energy =====")

for r in sorted_results:
    print(
        f"{r['site']:<10}"
        f"{r['vacancy']:<8}"
        f"{r['adsorption_energy']:<12.6f}"
    )
print("\n===== Ranking =====")

for rank, r in enumerate(sorted_results, start=1):
    print(
        f"{rank:2d}. "
        f"{r['site']:<8}"
        f"Vacancy {r['vacancy']:<3d}"
        f"{r['adsorption_energy']:.6f} eV"
    )