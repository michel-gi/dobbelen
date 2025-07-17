#!/usr/bin/env python3
"""
Een testprogramma dat willekeurige tekstblokken uit een database toont.
"""

import argparse
import sys
import random
from database import TextDatabase

def run_tester(db):
    """
    Start de oneindige loop die willekeurige items toont.
    """
    if not db.data:
        print(f"Fout: Database '{db.bestandsnaam}' is leeg of kon niet worden gevonden.", file=sys.stderr)
        sys.exit(1)

    # De sleutels (indices) van de database. Omdat de database na verwijdering
    # her-indexeert, zijn de sleutels aaneengesloten van 1 tot N.
    # We kunnen dus een random getal kiezen tussen 1 en de maximale sleutel.
    try:
        max_index = max(db.data.keys())
    except ValueError:
        # Dit gebeurt als db.data leeg is, wat we hierboven al controleren.
        print(f"Fout: Database '{db.bestandsnaam}' bevat geen items.", file=sys.stderr)
        sys.exit(1)

    print(f"\nDruk op [Enter] voor een willekeurig item (1-{max_index}).")
    print("Druk op Ctrl+C om te stoppen.")

    try:
        while True:
            # Wacht op de gebruiker om op Enter te drukken
            input()

            # Genereer een willekeurig indexnummer
            random_index = random.randint(1, max_index)
            tekst = db.get_tekst(random_index)

            # Het zou altijd een tekst moeten vinden, maar voor de zekerheid controleren we.
            if tekst is not None:
                print(f"\n--- Item met Index: {random_index} ---")
                print(tekst)
                print("--------------------------")
            else:
                # Onwaarschijnlijk, maar kan gebeuren als de db corrupt is.
                print(f"\nWaarschuwing: Geen tekst gevonden voor willekeurige index {random_index}.")

    except KeyboardInterrupt:
        print("\n\nProgramma afgesloten. Tot ziens!")
        sys.exit(0)
    except Exception as e:
        print(f"\nEr is een onverwachte fout opgetreden: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Parse command-line argumenten en start de tester.
    """
    parser = argparse.ArgumentParser(
        description="Toont willekeurige tekstblokken uit een tekst-database."
    )
    parser.add_argument(
        "bestandsnaam",
        nargs="?",  # Optioneel
        default="mijn_tekstdatabase.txt",
        help="Het databasebestand om te gebruiken (standaard: mijn_tekstdatabase.txt)."
    )
    args = parser.parse_args()

    # Maak het database object aan. create_new is False omdat we alleen lezen.
    db = TextDatabase(args.bestandsnaam, create_new=False)
    run_tester(db)

if __name__ == "__main__":
    main()