# Importeer de class uit de nieuwe module
from database import TextDatabase

def toon_menu():
    """Toont het hoofdmenu met beschikbare opties."""
    print("\nVoer een itemnummer in om de bijbehorende tekst te zien.")
    print("Of kies een van de volgende menu opties:\n")
    print("[n]ieuw   - invoeren van een nieuw tekst item")
    print("[w]ijzig  - wijzigen van een bestaand tekst item")
    print("[v]erwijder - verwijderen van een tekst item")
    print("[s]top   - beëindig dit programma")
    print("[m]enu   - dit menu opnieuw weergeven")

def main():
    """Hoofdfunctie voor de gebruikersinteractie."""
    # Maak één database object aan. Alle operaties gaan via dit object.

    db = TextDatabase("mijn_tekstdatabase.txt")
    toon_menu()  # Toon het menu direct bij de start
    
    while True:
        try:
            gebruikers_invoer = input("\nVoer een commando of nummer in: ")
            invoer_lower = gebruikers_invoer.lower()

            if invoer_lower == 'stop' or invoer_lower == 's':
                print("Programma gestopt.")
                break

            elif invoer_lower == 'menu' or invoer_lower == 'm':
                toon_menu()  # Menu opnieuw tonen
                continue

            elif invoer_lower == 'nieuw' or invoer_lower == 'n':
                print("Voer de nieuwe tekst in. Laat een lege regel achter om op te slaan.")
                nieuwe_tekst_regels = []
                while True:
                    regel = input()
                    if not regel.strip():  # Controleer op een lege regel (na het strippen van whitespace)
                        break
                    nieuwe_tekst_regels.append(regel)
                
                nieuwe_tekst = "\n".join(nieuwe_tekst_regels)
                if db.voeg_tekst_toe(nieuwe_tekst):
                    print("Tekst succesvol toegevoegd.")
                    print(f"Totaal aantal items in de database nu: {len(db.data)}")
                else:
                    print("Fout: Kon de nieuwe tekst niet opslaan.")
                continue

            elif invoer_lower == 'wijzig' or invoer_lower == 'w':
                try:
                    index_nummer = int(input("Voer het indexnummer in van de tekst die u wilt wijzigen: "))
                    if index_nummer not in db.data:
                        print(f"Fout: Geen tekst gevonden voor index {index_nummer}.")
                        continue

                    # Toon de huidige tekst ter bevestiging en voor copy/paste
                    huidige_tekst = db.get_tekst(index_nummer)
                    print(f"\n--- Huidige tekst voor index {index_nummer} ---")
                    print(huidige_tekst)
                    print("--- Einde huidige tekst ---")
                    print("\nVoer nu de nieuwe tekst in. Laat een lege regel achter om op te slaan.")

                    nieuwe_tekst_regels = []
                    while True:
                        regel = input()
                        if not regel.strip():
                            break
                        nieuwe_tekst_regels.append(regel)
                    nieuwe_tekst = "\n".join(nieuwe_tekst_regels)
                    if db.wijzig_tekst(index_nummer, nieuwe_tekst):
                        print(f"Tekst voor index {index_nummer} succesvol gewijzigd.")
                    else:
                        print(f"Fout: Kon tekst voor index {index_nummer} niet wijzigen.")
                except ValueError:
                    print("Ongeldige invoer voor indexnummer. Voer een getal in.")
                    continue
                continue

            elif invoer_lower == 'verwijder' or invoer_lower == 'v':
                try:
                    index_nummer = int(input("Voer het indexnummer in van de tekst die u wilt verwijderen: "))
                    if index_nummer not in db.data:
                        print(f"Fout: Geen tekst gevonden voor index {index_nummer}.")
                        continue

                    # Toon de te verwijderen tekst ter bevestiging
                    huidige_tekst = db.get_tekst(index_nummer)
                    print(f"\n--- Tekst voor index {index_nummer} die verwijderd wordt ---")
                    print(huidige_tekst)
                    print("--- Einde tekst ---")

                    while True:
                        bevestiging = input(f"Weet u zeker dat u item {index_nummer} wilt verwijderen? (j/n): ")
                        antwoord = bevestiging.strip().lower()

                        if not antwoord: # Gebruiker heeft alleen op Enter gedrukt
                            print("Ongeldige invoer. Voer 'j' of 'n' in.")
                            continue

                        if antwoord.startswith('j'):
                            if db.verwijder_tekst(index_nummer):
                                print(f"Item {index_nummer} succesvol verwijderd.")
                                print(f"Totaal aantal items in de database nu: {len(db.data)}")
                            else:
                                print(f"Fout: Kon item {index_nummer} niet verwijderen.")
                            break # Verlaat de bevestigingslus
                        elif antwoord.startswith('n'):
                            print(f"Verwijdering van item {index_nummer} geannuleerd.")
                            break # Verlaat de bevestigingslus
                        else:
                            print("Ongeldige invoer. Voer 'j' of 'n' in.")
                except ValueError:
                    print("Ongeldige invoer voor indexnummer. Voer een getal in.")
                continue

            index_nummer = int(gebruikers_invoer)
            tekst = db.get_tekst(index_nummer)

            if tekst is not None:
                print(f"\n--- Tekst voor index {index_nummer} ---")
                print(tekst)
                print(f"--- Einde tekst voor index {index_nummer} ---")
            else:
                print(f"Geen tekst gevonden voor index {index_nummer}.")

        except ValueError:
            print(f"Ongeldige invoer. '{gebruikers_invoer}' is geen geldig nummer of commando.")
        except KeyboardInterrupt:
            print("\nProgramma onderbroken door gebruiker. Tot ziens!")
            break
        except Exception as e:
            print(f"Er is een onverwachte fout opgetreden: {e}")
            break

if __name__ == "__main__":
    main()
