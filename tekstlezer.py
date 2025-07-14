import re

class TextDatabase:
    """
    Beheert een geïndexeerde tekstdatabase in een bestand.
    
    Deze class bundelt de data en de operaties (lezen, schrijven, toevoegen)
    in één object.
    """
    def __init__(self, bestandsnaam):
        """
        Constructor: wordt aangeroepen als een nieuw TextDatabase object wordt gemaakt.
        
        Args:
            bestandsnaam (str): Het pad naar het databasebestand.
        """
        self.bestandsnaam = bestandsnaam
        self.data = self._lees_bestand()
        print(f"Database '{self.bestandsnaam}' geladen. {len(self.data)} items gevonden.")

    def _lees_bestand(self):
        """
        Interne methode om het bestand te lezen en de data te parsen.
        (De underscore geeft aan dat deze methode bedoeld is voor intern gebruik).
        """
        try:
            with open(self.bestandsnaam, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            return {} # Bestand bestaat nog niet, begin met een lege database
        except Exception as e:
            print(f"Fout bij lezen van '{self.bestandsnaam}': {e}")
            return {}

        geindexeerde_data = {}
        blokken = content.split('###INDEX:')[1:]
        for blok in blokken:
            match = re.match(r'\s*(\d+)\s*\n(.*)', blok, re.DOTALL)
            if match:
                index_nummer = int(match.group(1))
                tekst = match.group(2).strip()
                geindexeerde_data[index_nummer] = tekst
        return geindexeerde_data

    def voeg_tekst_toe(self, tekst):
        """
        Voegt een nieuwe tekst toe met de volgende beschikbare index en slaat deze op.
        """
        volgende_index = max(self.data.keys()) + 1 if self.data else 1
        
        # 1. Update de data in het geheugen
        self.data[volgende_index] = tekst
        
        # 2. Voeg de nieuwe entry toe aan het fysieke bestand
        try:
            # Gebruik 'append' mode ('a') voor efficiëntie
            with open(self.bestandsnaam, 'a', encoding='utf-8') as f:
                # Zorg voor witruimte als het bestand al inhoud had
                if volgende_index > 1:
                    f.write("\n\n")
                f.write(f"###INDEX: {volgende_index}\n")
                f.write(tekst)
            print(f"Tekst succesvol toegevoegd met index {volgende_index}.")
            return True
        except IOError as e:
            print(f"Fout: Kon niet naar bestand '{self.bestandsnaam}' schrijven: {e}")
            # Draai de wijziging in het geheugen terug als schrijven mislukt
            del self.data[volgende_index]
            return False

    def get_tekst(self, index_nummer):
        """Haalt een tekst op basis van indexnummer uit het geheugen."""
        return self.data.get(index_nummer)

def main():
    """Hoofdfunctie voor de gebruikersinteractie."""
    # Maak één database object aan. Alle operaties gaan via dit object.
    db = TextDatabase("mijn_tekstdatabase.txt")

    print("\nVoer een nummer in om tekst te zien.")
    print("Typ 'nieuw' om een item toe te voegen, 'stop' om te eindigen, of druk op Ctrl+C.")

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
