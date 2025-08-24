import logging
import re


class TextDatabase:
    """
    Beheert een geïndexeerde tekstdatabase in een bestand.

    Deze class bundelt de data en de operaties (lezen, schrijven, toevoegen)
    in één object.
    """

    def __init__(self, bestandsnaam, create_new=False):
        """
        Constructor: wordt aangeroepen als een nieuw TextDatabase object wordt gemaakt.

        Args:
            bestandsnaam (str): Het pad naar het databasebestand.
            create_new (bool): Indien True, start met een lege database, zelfs als
                               het bestand al bestaat. Het bestand wordt bij de
                               eerste schrijf-actie overschreven.
        """
        self.bestandsnaam = bestandsnaam
        if create_new:
            self.data = {}
            logging.info("Nieuwe, lege database '%s' wordt aangemaakt.", self.bestandsnaam)
        else:
            self.data = self._lees_bestand()
            logging.info("Database '%s' geladen. %d items gevonden.", self.bestandsnaam, len(self.data))

    def _lees_bestand(self):
        """
        Interne methode om het bestand te lezen en de data te parsen.
        (De underscore geeft aan dat deze methode bedoeld is voor intern gebruik).
        """
        try:
            with open(self.bestandsnaam, encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            return {}  # Bestand bestaat nog niet, begin met een lege database
        except OSError as e:
            logging.error("Fout bij lezen van '%s': %s", self.bestandsnaam, e)
            return {}

        geindexeerde_data = {}
        blokken = content.split("###INDEX:")[1:]
        for blok in blokken:
            match = re.match(r"\s*(\d+)\s*\n(.*)", blok, re.DOTALL)
            if match:
                index_nummer = int(match.group(1))
                tekst = match.group(2).strip()
                geindexeerde_data[index_nummer] = tekst
        return geindexeerde_data

    def _schrijf_bestand(self):
        """Interne methode om de volledige dataset naar het bestand te schrijven."""
        try:
            with open(self.bestandsnaam, "w", encoding="utf-8") as f:
                # Sorteer op index voor een voorspelbare volgorde in het bestand
                for index, tekst in sorted(self.data.items()):
                    f.write(f"###INDEX: {index}\n")
                    f.write(tekst)
                    f.write("\n\n")
            return True
        except OSError as e:
            logging.error("Fout bij schrijven naar '%s': %s", self.bestandsnaam, e)
            return False

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

    def verwijder_tekst(self, index_nummer):
        """
        Verwijdert een tekst op basis van indexnummer en hernummert de volgende items.
        """
        if index_nummer not in self.data:
            return False

        # Verwijder het gevraagde item
        del self.data[index_nummer]

        # Haal de overgebleven teksten, gesorteerd op hun oude index
        sorted_values = [v for k, v in sorted(self.data.items())]
        # Bouw een compleet nieuwe dictionary op met een compacte, nieuwe index
        self.data = {i: text for i, text in enumerate(sorted_values, 1)}

        # Schrijf de nieuwe, geherindexeerde data weg naar het bestand
        return self._schrijf_bestand()

    def swap_items(self, index1, index2):
        """
        Wisselt de teksten van twee gegeven indexnummers.
        """
        if index1 not in self.data or index2 not in self.data:
            logging.warning("Een of beide indexen (%d, %d) niet gevonden voor verwisselen.", index1, index2)
            return False

        # Wissel de teksten in het geheugen
        self.data[index1], self.data[index2] = self.data[index2], self.data[index1]

        # Schrijf de gewijzigde data weg naar het bestand
        return self._schrijf_bestand()
