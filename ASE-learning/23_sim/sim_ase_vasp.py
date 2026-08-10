from ase.build import fcc111, add_adsorbate, molecule
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from ase.constraints import FixAtoms
import csv
from ase.io import write
from ase.calculators.vasp import Vasp

class Simulation:

    def __init__(self, metal, ads_atom, size, vacuum, site="ontop", fixed_layers=2):
        self.metal = metal
        self.ads_atom = ads_atom
        self.size = size
        self.vacuum = vacuum
        self.site = site
        self.fixed_layers = fixed_layers

        self.structure = None
        self.clean_structure = None
        self.energy = None
        self.clean_surface_energy = None
        self.reference_energy = None
        self.adsorption_energy = None

    def build_surface(self):
        self.structure = fcc111(
            self.metal,
            size=self.size,
            vacuum=self.vacuum
        )

        self.structure.pbc = [True, True, True]

        print("Surface created")
        print("Number of atoms:", len(self.structure))
    def apply_constraints(self):

        layer_count = self.size[2]

        first_fixed_tag = (
            layer_count
            - self.fixed_layers
            + 1
        )

        mask = self.structure.get_tags() >= first_fixed_tag

        self.structure.set_constraint(FixAtoms(mask=mask))

        print("Fixed atoms:", mask.sum())
    def relax_clean_surface(self, fmax=0.05):

        self.structure.calc = self.create_calculator()

        optimizer = BFGS(self.structure, logfile=None)
        optimizer.run(fmax=fmax)

        self.clean_structure = self.structure.copy()
        self.clean_surface_energy = (
            self.structure.get_potential_energy()
        )

        print("Clean surface relaxed.")
        print("Clean surface energy:",
            self.clean_surface_energy, "eV")
    def calculate_clean_surface_energy(self):

        if self.clean_structure is None:
            print("Please build the surface first.")
            return None

        self.clean_structure.calc = self.create_calculator()

        self.clean_surface_energy = (
            self.clean_structure.get_potential_energy()
        )

        print("Clean surface energy:",
            self.clean_surface_energy, "eV")

        return self.clean_surface_energy
    def calculate_h_reference_energy(self):

        h2 = molecule("H2")
        h2.center(vacuum=8.0)
        h2.pbc = [True, True, True]

        h2.calc = self.create_calculator()

        energy_h2 = h2.get_potential_energy()

        self.reference_energy = energy_h2 / 2

        print("H reference energy:",
            self.reference_energy, "eV")

        return self.reference_energy
    
    def add_adsorbate(self):

        if self.structure is None:
            print("Please build the surface first.")
            return

        add_adsorbate(
            self.structure,
            self.ads_atom,
            height=1.8,
            position=self.site
        )

        print(f"{self.ads_atom} added at {self.site}.")
    def relax_adsorbed_structure(self, fmax=0.05):

        self.structure.calc = self.create_calculator()

        optimizer = BFGS(self.structure, logfile=None)
        optimizer.run(fmax=fmax)

        self.energy = self.structure.get_potential_energy()

        print("Adsorbed structure relaxed.")
        print("Adsorbed structure energy:",
            self.energy, "eV")
    def calculate_energy(self):

        if self.structure is None:
            print("Please build the structure first.")
            return None

        self.structure.calc = self.create_calculator()

        self.energy = self.structure.get_potential_energy()

        print("Potential energy:", self.energy, "eV")

        return self.energy
    def calculate_adsorption_energy(self):

        if self.energy is None:
            print("Adsorbed structure energy is missing.")
            return None

        if self.clean_surface_energy is None:
            print("Clean surface energy is missing.")
            return None

        if self.reference_energy is None:
            print("Reference energy is missing.")
            return None

        self.adsorption_energy = (
            self.energy
            - self.clean_surface_energy
            - self.reference_energy
        )

        print("Adsorption energy:",
            self.adsorption_energy, "eV")

        return self.adsorption_energy
    def save_structure(self, filename):#保存单个结构

        if self.structure is None:
            print("No structure to save.")
            return

        write(filename, self.structure)

        print("Structure saved to:", filename)
    def create_calculator(self):
        return Vasp(
            xc="PBE",
            encut=450,
            kpts=(4, 4, 1),
            gamma=True,
            lscalapack=False,
            lreal="Auto",
            directory="vasp_test_mpi2_fresh"
        )       
    
    def run(self):
        self.build_surface()
        self.apply_constraints()
        self.relax_clean_surface()

        self.add_adsorbate()
        self.relax_adsorbed_structure()

        self.calculate_h_reference_energy()
        adsorption_energy = self.calculate_adsorption_energy()

        print("Simulation finished.")
        return adsorption_energy
def export_results(results, filename):#导出批量结果的函数

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "rank",
                "site",
                "adsorption_energy_eV"
            ])

            for rank, result in enumerate(results, start=1):
                writer.writerow([
                    rank,
                    result["site"],
                    result["adsorption_energy"]
                ])

        print("Results saved to:", filename)


# sim = Simulation("Cu", "H", (3, 3, 4), 10)

# sim.build_surface()
# sim.add_adsorbate()
# sim.calculate_energy()

# print(sim.structure)

# print("Saved energy:", sim.energy, "eV")

# sim = Simulation("Cu", "H", (3, 3, 4), 10, site="bridge")

# adsorption_energy = sim.run()

# print("Adsorbed structure total energy:", sim.energy, "eV")
# print("Final adsorption energy:", sim.adsorption_energy, "eV")
sites = ["ontop"]

results = []

for site in sites:
    print("\nRunning site:", site)

    sim = Simulation(
        "Cu", "H", (3, 3, 4), 10,
        site=site
    )

    adsorption_energy = sim.run()

    results.append({
        "site": site,
        "adsorption_energy": adsorption_energy,
        "simulation": sim
    })


results.sort(key=lambda item: item["adsorption_energy"])

print("\n===== Adsorption-energy ranking =====")

for rank, result in enumerate(results, start=1):
    print(
        rank,
        result["site"],
        result["adsorption_energy"],
        "eV"
    )


best_result = results[0]

print("\nBest site:", best_result["site"])
print(
    "Best adsorption energy:",
    best_result["adsorption_energy"],
    "eV"
)
export_results(results, "adsorption_results.csv")

best_sim = best_result["simulation"]

best_filename = f"best_{best_result['site']}.xyz"

best_sim.save_structure(best_filename)