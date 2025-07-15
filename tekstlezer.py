# Importeer de class uit de nieuwe module
from database import TextDatabase

def main():
    """Hoofdfunctie voor de gebruikersinteractie."""
    # Maak één database object aan. Alle operaties gaan via dit object.
    db = TextDatabase("mijn_tekstdatabase.txt")

    print("\nVoer een nummer in om tekst te zien.")
    print("Typ 'nieuw' om een item toe te voegen, 'wijzig' om een item te wijzigen, 'stop' om te eindigen, of druk op Ctrl+C.")

    while True:
        try:
            gebruikers_invoer = input("\nVoer een commando of nummer in: ")
            invoer_lower = gebruikers_invoer.lower()

            if invoer_lower == 'stop':
                print("Programma gestopt.")
                break

            elif invoer_lower == 'nieuw':
                print("Voer de nieuwe tekst in. Typ 'EINDE_TEKST' op een nieuwe regel om op te slaan.")
                nieuwe_tekst_regels = []
                while True:
                    regel = input()
                    if regel.upper() == 'EINDE_TEKST':
                        break
                    nieuwe_tekst_regels.append(regel)
                
                nieuwe_tekst = "\n".join(nieuwe_tekst_regels)
                db.voeg_tekst_toe(nieuwe_tekst)
                continue

            elif invoer_lower == 'wijzig':
                try:
                    index_nummer = int(input("Voer het indexnummer in van de tekst die u wilt wijzigen: "))
                    if index_nummer not in db.data:
                        print(f"Fout: Geen tekst gevonden voor index {index_nummer}.")
                        continue

                    print("Voer de nieuwe tekst in. Typ 'EINDE_TEKST' op een nieuwe regel om op te slaan.")
                    nieuwe_tekst_regels = []
                    while True:
                        regel = input()
                        if regel.upper() == 'EINDE_TEKST':
                            break
                        nieuwe_tekst_regels.append(regel)
                    nieuwe_tekst = "\n".join(nieuwe_tekst_regels)
                    if not db.wijzig_tekst(index_nummer, nieuwe_tekst):
                        print(f"Fout: Kon tekst voor index {index_nummer} niet wijzigen.")
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
