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

    def get_tekst(self, index_nummer):
        """Haalt een tekst op basis van indexnummer uit het geheugen."""
        return self.data.get(index_nummer)

    def voeg_tekst_toe(self, tekst):
        """Voegt een nieuwe tekst toe met de volgende beschikbare index en slaat op."""
        volgende_index = max(self.data.keys()) + 1 if self.data else 1
        self.data[volgende_index] = tekst
        return self._schrijf_bestand()

    def wijzig_tekst(self, index_nummer, nieuwe_tekst):
        """Wijzigt de tekst voor een gegeven indexnummer."""
        if index_nummer in self.data:
            self.data[index_nummer] = nieuwe_tekst
            return self._schrijf_bestand()
        return False