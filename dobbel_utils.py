# /home/michel/projects/dobbelen/dobbel_utils.py
import numpy as np

def bereken_theoretische_verdeling(aantal_dobbelstenen, aantal_zijden):
    """
    Berekent de exacte kansverdeling met behulp van convolutie.
    Geeft het aantal combinaties voor elke mogelijke som terug.
    Deze versie gebruikt NumPy voor efficiëntie.
    """
    # We gebruiken dtype=object om NumPy te dwingen Python's arbitrary-precision
    # integers te gebruiken. Dit voorkomt integer overflow.
    basis_verdeling = np.array([1] * aantal_zijden, dtype=object)
    huidige_verdeling = basis_verdeling

    for _ in range(1, aantal_dobbelstenen):
        huidige_verdeling = np.convolve(huidige_verdeling, basis_verdeling)

    min_som = aantal_dobbelstenen
    return {i + min_som: combinaties for i, combinaties in enumerate(huidige_verdeling)}
