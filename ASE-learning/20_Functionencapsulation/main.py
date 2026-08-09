from structure import build_surface
from vacancy import create_vacancy
from adsorption import add_adsorbate_atom
from calculator import calculate_energy
from analysis import find_best
from reference import get_reference_energy
import config
from ase.io import write




ads_atom = config.ads_atom
E_reference = get_reference_energy(
ads_atom
            )
results=[]

for site in config.sites:
    for index in config.vacancies:
            slab = build_surface(
                metal=config.metal,
                size=config.surface_size,
                vacuum=config.vacuum
            )

            vacancy = create_vacancy(
            slab,
            index
            )


            E_vacancy = calculate_energy(
            vacancy
            )


            

            slab_ads = add_adsorbate_atom(
                vacancy,
                ads_atom,
                height=config.ads_height,
                site=site
            )

            E_total = calculate_energy(
            slab_ads
            )
            E_ads = (
            E_total
            - E_vacancy
            - E_reference
            )
            results.append(
            {
            "site": site,
            "vacancy": index,
            "vacancy_energy": E_vacancy,
            "total_energy": E_total,
            "adsorption_energy": E_ads,
            "structure": slab_ads.copy()
            }
        )
print(len(results))

best_result = find_best(results)

print("Best Result:")
for key, value in best_result.items():
    print(f"  {key}: {value}")
write(
    "best_result.xyz",
    best_result["structure"]
)

print("Finished!")
for atom in best_result["structure"]:
    print(
        atom.index,
        atom.symbol,
        atom.tag,
        atom.position
    )