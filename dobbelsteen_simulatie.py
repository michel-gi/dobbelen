#!/usr/bin/env python3
"""
Een Python-script om de kansverdeling van dobbelsteenworpen te simuleren.
"""

import argparse
import sys
import random
import numpy as np
from collections import Counter

# Probeer matplotlib te importeren en geef een duidelijke foutmelding als het niet lukt.
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Fout: De 'matplotlib' bibliotheek is niet gevonden.")
    print("Installeer deze met het commando: python3 -m pip install matplotlib")
    exit()

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
    print(f"Simulatie gestart: {aantal_worpen:,} worpen met {aantal_dobbelstenen} d{aantal_zijden}-dobbelstenen...".replace(',', '.'))

    # Genereer alle worpen in één keer met NumPy voor hoge prestaties
    worpen = np.random.randint(1, aantal_zijden + 1, size=(aantal_worpen, aantal_dobbelstenen))
    # Tel de som per worp (langs de tweede as)
    sommen = np.sum(worpen, axis=1)
    # Counter telt automatisch hoe vaak elke unieke som voorkomt
    return Counter(sommen)

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

def bereken_theoretische_verdeling(aantal_dobbelstenen, aantal_zijden):
    """
    Berekent de exacte kansverdeling met behulp van convolutie.
    Geeft het aantal combinaties voor elke mogelijke som terug.
    Deze versie gebruikt NumPy voor efficiëntie.
    """
    # De verdeling van de combinaties voor 1 dobbelsteen.
    basis_verdeling = [1] * aantal_zijden

    # Startpunt voor de convolutie.
    huidige_verdeling = basis_verdeling

    # Voer de convolutie uit voor elke extra dobbelsteen
    for _ in range(1, aantal_dobbelstenen):
        huidige_verdeling = np.convolve(huidige_verdeling, basis_verdeling)

    # Converteer de lijst met combinaties naar een dictionary {som: combinaties}
    min_som = aantal_dobbelstenen
    return {i + min_som: combinaties for i, combinaties in enumerate(huidige_verdeling)}

def toon_verdeling_grafisch(simulatie_resultaten, aantal_dobbelstenen, aantal_worpen, aantal_zijden, theoretische_verdeling=None):
    """
    Toont de verdeling van de resultaten in een staafdiagram met matplotlib.
    Kan ook de theoretische verdeling als een lijn plotten.
    """
    # Sorteer de data op de som (sleutel) voor een logische grafiek
    gesorteerde_items = sorted(simulatie_resultaten.items())
    sommen = [item[0] for item in gesorteerde_items]
    frequenties = [item[1] for item in gesorteerde_items]

    # Maak de plot
    plt.figure(figsize=(12, 7))  # Maak de grafiek wat breder
    plt.bar(sommen, frequenties, color='skyblue', edgecolor='black', label='Simulatie')

    # Voeg titels en labels toe
    plt.title(f'Verdeling van {aantal_worpen:,} worpen met {aantal_dobbelstenen} d{aantal_zijden}-dobbelstenen'.replace(',', '.'))
    plt.xlabel('Som van de ogen')
    plt.ylabel('Frequentie')

    # Plot de theoretische verdeling als die is meegegeven
    if theoretische_verdeling:
        theoretische_sommen = sorted(theoretische_verdeling.keys())
        theoretische_combinaties = [theoretische_verdeling[s] for s in theoretische_sommen]

        # Schaal de theoretische data zodat deze vergelijkbaar is met de simulatie
        totaal_combinaties = sum(theoretische_combinaties)
        schaal_factor = aantal_worpen / totaal_combinaties
        geschaalde_frequenties = [c * schaal_factor for c in theoretische_combinaties]

        plt.plot(theoretische_sommen, geschaalde_frequenties, color='red', marker='o', linestyle='-', linewidth=2, label='Theorie')

    # Zorg ervoor dat alle integers op de x-as worden getoond
    min_som = aantal_dobbelstenen
    max_som = aantal_dobbelstenen * aantal_zijden
    # Als er veel mogelijke sommen zijn, toon niet elke tick om overlap te voorkomen
    if max_som - min_som < 35:
        plt.xticks(range(min_som, max_som + 1))
    else:
        # Toon bijvoorbeeld elke 5e of 10e tick
        stap_grootte = 5 if max_som - min_som < 100 else 10
        plt.xticks(range(min_som, max_som + 1, stap_grootte))

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

def vraag_getal(prompt, standaard):
    """Vraagt de gebruiker om een getal en valideert de invoer."""
    while True:
        invoer = input(f"{prompt} (standaard: {standaard}): ")
        if not invoer:
            return standaard
        try:
            getal = int(invoer)
            if getal > 0:
                return getal
            else:
                print("Fout: Voer a.u.b. een positief getal in.", file=sys.stderr)
        except ValueError:
            print("Fout: Ongeldige invoer. Voer a.u.b. een geheel getal in.", file=sys.stderr)

def run_simulatie(aantal_dobbelstenen, aantal_zijden, aantal_worpen):
    """Voert de daadwerkelijke simulatie en plotting uit."""
    simulatie_resultaten = simuleer_worpen(aantal_dobbelstenen, aantal_worpen, aantal_zijden)
    theoretische_verdeling = bereken_theoretische_verdeling(aantal_dobbelstenen, aantal_zijden)

    toon_verdeling_tekstueel(simulatie_resultaten)
    toon_verdeling_grafisch(simulatie_resultaten, aantal_dobbelstenen, aantal_worpen, aantal_zijden, theoretische_verdeling)

def main():
    """Hoofdfunctie van het script."""
    # sys.argv[0] is de naam van het script zelf. Als er meer argumenten zijn,
    # draaien we in non-interactieve (command-line) modus.
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            description="Simuleert dobbelsteenworpen en toont de kansverdeling.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument('-s', '--stenen', type=int, default=3, help="Het aantal dobbelstenen per worp.")
        parser.add_argument('-z', '--zijden', type=int, default=6, help="Het aantal zijden van elke dobbelsteen.")
        parser.add_argument('-w', '--worpen', type=int, default=100000, help="Het totale aantal worpen.")
        args = parser.parse_args()
        run_simulatie(args.stenen, args.zijden, args.worpen)
    else:
        # Geen argumenten: start interactieve modus
        print("--- Interactieve Dobbelsteen Simulatie ---")
        print("Geef de parameters op of druk op Enter om de standaardwaarde te gebruiken.\n")
        aantal_dobbelstenen = vraag_getal("Aantal dobbelstenen", 3)
        aantal_zijden = vraag_getal("Aantal zijden per dobbelsteen", 6)
        aantal_worpen = vraag_getal("Aantal worpen om te simuleren", 100000)
        run_simulatie(aantal_dobbelstenen, aantal_zijden, aantal_worpen)

if __name__ == "__main__":
    main()