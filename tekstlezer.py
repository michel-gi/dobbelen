import re

def lees_geindexeerde_tekstbestand(bestandsnaam):
    """
    Leest een tekstbestand met geïndexeerde tekst en retourneert een dictionary.

    Deze functie is robuuster en eenvoudiger dan de vorige versie.
    Het leest het hele bestand, splitst het op de '###INDEX:' marker,
    en verwerkt elk blokje.

    Args:
        bestandsnaam (str): De naam van het tekstbestand om te lezen.

    Returns:
        dict: Een dictionary met indexnummers (int) als sleutels en teksten (str) als waarden.
              Retourneert een lege dictionary bij een fout.
    """
    try:
        with open(bestandsnaam, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        # Dit is geen fatale fout meer, de gebruiker kan een nieuw bestand aanmaken.
        return {}
    except Exception as e:
        print(f"Er is een fout opgetreden bij het lezen van het bestand: {e}")
        return {}

    geindexeerde_data = {}
    # Split de tekst op de index marker. Het eerste element is leeg of tekst voor de eerste marker.
    blokken = content.split('###INDEX:')[1:]

    for blok in blokken:
        # Gebruik een reguliere expressie om het nummer en de tekst te scheiden.
        # re.DOTALL zorgt ervoor dat '.' ook newlines matcht.
        match = re.match(r'\s*(\d+)\s*\n(.*)', blok, re.DOTALL)
        if match:
            index_nummer = int(match.group(1))
            tekst = match.group(2).strip()
            geindexeerde_data[index_nummer] = tekst
        else:
            print(f"Waarschuwing: Ongeldig formaat gevonden in blok:\n---\n{blok.strip()}\n---")

    return geindexeerde_data

def voeg_tekst_toe_aan_bestand(bestandsnaam, index_nummer, tekst):
    """
    Voegt een nieuwe geïndexeerde tekst toe aan het einde van het bestand.

    Args:
        bestandsnaam (str): De naam van het tekstbestand.
        index_nummer (int): Het nieuwe indexnummer om toe te voegen.
        tekst (str): De tekst die bij de index hoort.

    Returns:
        bool: True als het toevoegen is gelukt, anders False.
    """
    try:
        # Open in 'append' mode ('a') om aan het einde toe te voegen.
        # Het bestand wordt aangemaakt als het niet bestaat.
        with open(bestandsnaam, 'a', encoding='utf-8') as f:
            # Zorg voor een lege regel tussen de vorige entry en de nieuwe.
            f.write(f"\n\n###INDEX: {index_nummer}\n")
            f.write(tekst)
        return True
    except IOError as e:
        print(f"Fout: Kon niet naar bestand '{bestandsnaam}' schrijven: {e}")
        return False

def main():
    """Hoofdfunctie voor de gebruikersinteractie."""
    bestandsnaam = "mijn_tekstdatabase.txt"
    data = lees_geindexeerde_tekstbestand(bestandsnaam)

    print("Tekstdatabase geladen.")
    print("Voer een nummer in om tekst te zien.")
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

                # Bepaal de volgende index
                volgende_index = max(data.keys()) + 1 if data else 1
                
                if voeg_tekst_toe_aan_bestand(bestandsnaam, volgende_index, nieuwe_tekst):
                    print(f"Tekst succesvol toegevoegd met index {volgende_index}.")
                    # Update de data in het geheugen zodat het direct beschikbaar is
                    data[volgende_index] = nieuwe_tekst
                else:
                    print("Toevoegen van tekst is mislukt.")
                
                continue # Ga terug naar de hoofdlus voor een nieuw commando

            # Als het geen commando is, probeer het als nummer
            index_nummer = int(gebruikers_invoer)

            if index_nummer in data:
                print(f"\n--- Tekst voor index {index_nummer} ---")
                print(data[index_nummer])
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
