def lees_geindexeerde_tekstbestand(bestandsnaam):
    """
    Leest een tekstbestand met geïndexeerde tekst en retourneert een dictionary
    waarin de indexen (integers) gekoppeld zijn aan de bijbehorende teksten (strings).

    Het bestand moet de volgende structuur hebben:
    Elke index begint met '###INDEX: [NUMMER]'
    De tekst volgt direct na de indexregel.

    Args:
        bestandsnaam (str): De naam van het tekstbestand om te lezen.

    Returns:
        dict: Een dictionary waarbij sleutels de indexnummers zijn en waarden de teksten.
              Retourneert een lege dictionary als het bestand niet kan worden gevonden of gelezen.
    """
    geindexeerde_data = {}
    huidige_index = None
    huidige_tekst_regels = []

    try:
        with open(bestandsnaam, 'r', encoding='utf-8') as f:
            for lijn in f:
                lijn = lijn.strip() # Verwijder witruimte aan het begin/einde van de regel

                if lijn.startswith("###INDEX:"):
                    # Verwerk de vorige index en tekst als die er was
                    if huidige_index is not None:
                        geindexeerde_data[huidige_index] = "\n".join(huidige_tekst_regels).strip()
                        huidige_tekst_regels = [] # Reset voor de volgende tekst

                    # Haal de nieuwe index op
                    try:
                        huidige_index = int(lijn.split(":")[1].strip())
                    except ValueError:
                        print(f"Waarschuwing: Ongeldige index gevonden in regel: {lijn}. Deze wordt overgeslagen.")
                        huidige_index = None # Zorg dat we geen tekst aan een ongeldige index koppelen
                elif huidige_index is not None:
                    # Voeg de regel toe aan de huidige tekst
                    huidige_tekst_regels.append(lijn)

            # Voeg de laatste index en tekst toe na het einde van het bestand
            if huidige_index is not None and huidige_tekst_regels:
                geindexeerde_data[huidige_index] = "\n".join(huidige_tekst_regels).strip()

    except FileNotFoundError:
        print(f"Fout: Bestand '{bestandsnaam}' niet gevonden.")
        return {}
    except Exception as e:
        print(f"Er is een fout opgetreden bij het lezen van het bestand: {e}")
        return {}

    return geindexeerde_data

# Hoofdprogramma
if __name__ == "__main__":
    bestandsnaam = "mijn_tekstdatabase.txt"
    data = lees_geindexeerde_tekstbestand(bestandsnaam)

    if not data:
        print("Kan geen gegevens laden. Controleer of het bestand bestaat en correct is geformatteerd.")
    else:
        while True:
            try:
                gebruikers_invoer = input("\nVoer een nummer in (of 'stop' om te eindigen): ")
                if gebruikers_invoer.lower() == 'stop':
                    break

                index_nummer = int(gebruikers_invoer)

                if index_nummer in data:
                    print(f"\n--- Tekst voor index {index_nummer} ---")
                    print(data[index_nummer])
                    print(f"--- Einde tekst voor index {index_nummer} ---")
                else:
                    print(f"Geen tekst gevonden voor index {index_nummer}.")
            except ValueError:
                print("Ongeldige invoer. Voer alstublieft een geldig nummer in of 'stop'.")
            except Exception as e:
                print(f"Er is een onverwachte fout opgetreden: {e}")
