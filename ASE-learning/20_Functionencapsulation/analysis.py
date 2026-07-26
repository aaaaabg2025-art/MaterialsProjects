def find_best(results):

    best = min(
        results,
        key=lambda x:x["adsorption_energy"]
    )

    return best