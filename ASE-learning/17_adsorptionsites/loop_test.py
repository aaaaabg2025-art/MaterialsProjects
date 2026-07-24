sites = ["ontop", "bridge", "fcc", "hcp"]

atoms_to_delete = [27, 18, 9, 0]

for site in sites:

    print(f"\nCurrent site: {site}")

    for i in atoms_to_delete:

        print(f"    Delete atom {i}")