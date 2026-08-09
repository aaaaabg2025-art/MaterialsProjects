class Simulation:

    def __init__(self, metal, ads_atom, size, vacuum):
        self.metal = metal
        self.ads_atom = ads_atom
        self.size = size
        self.vacuum = vacuum

    def show_info(self):
        print("Metal:", self.metal)
        print("Adsorbate:", self.ads_atom)
        print("Surface size:", self.size)
        print("Vacuum:", self.vacuum)

    def change_adsorbate(self, new_ads_atom):
        self.ads_atom = new_ads_atom
        print("Adsorbate changed to:", self.ads_atom)


sim1 = Simulation("Cu", "H", (3, 3, 4), 10)
sim2 = Simulation("Ni", "O", (4, 4, 3), 12)

sim1.change_adsorbate("C")

sim1.show_info()
sim2.show_info()