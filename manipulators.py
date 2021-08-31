from itertools import chain

def correct_tddft_transition_number(result):
    if not result.get("orbital_energies"):
        return result

    occupied = result["orbital_energies"]["occupied"]

    if not result.get("TDDFT") and not result.get("TDDFT/TDA"):
        return result

    
    for state in chain(result.get("TDDFT", []), 
                            result.get("TDDFT/TDA", [])):
        for transition in state["transitions"]:
            transition["virtual"] += len(occupied)
    return result 
