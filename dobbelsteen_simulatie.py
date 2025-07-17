#!/usr/bin/env python3
"""
Een Python-script om de kansverdeling van dobbelsteenworpen te simuleren.
"""

import random
from collections import Counter

# Probeer matplotlib te importeren en geef een duidelijke foutmelding als het niet lukt.
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Fout: De 'matplotlib' bibliotheek is niet gevonden.")
    print("Installeer deze met het commando: python3 -m pip install matplotlib")
    exit()

# --- INSTELLINGEN ---
AANTAL_DOBBELSTENEN = 3  # Verander dit getal om met meer/minder dobbelstenen te gooien
AANTAL_WORPEN = 100000   # Een groot aantal worpen voor een duidelijke verdeling
AANTAL_ZIJDEN = 6        # Standaard 6-zijdige dobbelsteen
# --------------------

def simuleer_worpen(aantal_dobbelstenen, aantal_worpen, aantal_zijden):
    """
    Simuleert een serie worpen met een gegeven aantal dobbelstenen.

    Args:
        aantal_dobbelstenen (int): Het aantal dobbelstenen per worp.
        aantal_worpen (int): Het totale aantal worpen dat gesimuleerd wordt.
        aantal_zijden (int): Het aantal zijden van elke dobbelsteen.

    Returns:
        collections.Counter: Een object met de som van de worpen als sleutel
                             en de frequentie als waarde.
    """
    print(f"Simulatie gestart: {aantal_worpen} worpen met {aantal_dobbelstenen} dobbelsteen/dobbelstenen...")
    resultaten = []
    for _ in range(aantal_worpen):
        worp_totaal = 0
        for _ in range(aantal_dobbelstenen):
            # Gooi een enkele dobbelsteen en tel op bij het totaal
            worp_totaal += random.randint(1, aantal_zijden)
        resultaten.append(worp_totaal)

    # Counter telt automatisch hoe vaak elke unieke som voorkomt
    return Counter(resultaten)

def toon_verdeling_tekstueel(resultaten, schaal=100):
    """Toont de verdeling als een eenvoudige tekstuele histogram."""
    print("\n--- Tekstuele Verdeling van de Resultaten ---")
    # Sorteer de resultaten op basis van de som (de sleutel)
    gesorteerde_resultaten = sorted(resultaten.items())

    # Vind de hoogste frequentie voor het schalen van de balken
    max_frequentie = 0
    if gesorteerde_resultaten:
        max_frequentie = max(item[1] for item in gesorteerde_resultaten)

    for som, frequentie in gesorteerde_resultaten:
        # Bereken de lengte van de visuele balk
        balk_lengte = int((frequentie / max_frequentie) * schaal) if max_frequentie > 0 else 0
        balk = '#' * balk_lengte
        print(f"Som {som:2d}: {frequentie:6d} keer | {balk}")

def toon_verdeling_grafisch(resultaten, aantal_dobbelstenen, aantal_worpen):
    """
    Toont de verdeling van de resultaten in een staafdiagram met matplotlib.
    """
    # Sorteer de data op de som (sleutel) voor een logische grafiek
    gesorteerde_items = sorted(resultaten.items())
    sommen = [item[0] for item in gesorteerde_items]
    frequenties = [item[1] for item in gesorteerde_items]

    # Maak de plot
    plt.figure(figsize=(10, 6))  # Maak de grafiek wat breder
    plt.bar(sommen, frequenties, color='skyblue', edgecolor='black')

    # Voeg titels en labels toe
    plt.title(f'Kansverdeling van {aantal_worpen} worpen met {aantal_dobbelstenen} dobbelstenen')
    plt.xlabel('Som van de ogen')
    plt.ylabel('Frequentie')

    # Zorg ervoor dat alle integers op de x-as worden getoond
    min_som = aantal_dobbelstenen
    max_som = aantal_dobbelstenen * AANTAL_ZIJDEN
    plt.xticks(range(min_som, max_som + 1))

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def main():
    """Hoofdfunctie van het script."""
    resultaten = simuleer_worpen(AANTAL_DOBBELSTENEN, AANTAL_WORPEN, AANTAL_ZIJDEN)
    toon_verdeling_tekstueel(resultaten)
    toon_verdeling_grafisch(resultaten, AANTAL_DOBBELSTENEN, AANTAL_WORPEN)

if __name__ == "__main__":
    main()