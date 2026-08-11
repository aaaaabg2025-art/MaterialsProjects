energy_slab = -40.83922946
energy_slab_h = -44.16638216
energy_h2 = -6.72346129

adsorption_energy = energy_slab_h - energy_slab - 0.5 * energy_h2

print(f"Clean slab energy: {energy_slab:.8f} eV")
print(f"Slab + H energy: {energy_slab_h:.8f} eV")
print(f"H2 reference energy: {energy_h2:.8f} eV")
print(f"Adsorption energy: {adsorption_energy:.6f} eV")

if adsorption_energy < 0:
    print("Result: adsorption is exothermic under this model.")
else:
    print("Result: adsorption is endothermic under this model.")