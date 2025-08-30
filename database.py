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
        self.dirty = False
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

    def save(self):
        """Interne methode om de volledige dataset naar het bestand te schrijven."""
        try:
            with open(self.bestandsnaam, "w", encoding="utf-8") as f:
                # Sorteer op index voor een voorspelbare volgorde in het bestand
                for index, tekst in sorted(self.data.items()):
                    f.write(f"###INDEX: {index}\n")
                    f.write(tekst)
                    f.write("\n\n")
            self.dirty = False
            return True
        except OSError as e:
            logging.error("Fout bij schrijven naar '%s': %s", self.bestandsnaam, e)
            return False

    def get_tekst(self, index_nummer):
        """Haalt een tekst op basis van indexnummer uit het geheugen."""
        return self.data.get(index_nummer)

    def voeg_tekst_toe(self, tekst):
        """Voegt een nieuwe tekst toe aan het einde van de database en herindexeert."""
        # De index is 1-gebaseerd, dus len(self.data) + 1 is de nieuwe laatste positie.
        return self.voeg_tekst_op_index_toe(len(self.data) + 1, tekst)

    def voeg_tekst_op_index_toe(self, index, tekst):
        """Voegt een tekst toe op een specifieke index en herindexeert."""
        if not (1 <= index <= len(self.data) + 1):
            logging.warning("Doelindex %d is buiten bereik (1-%d).", index, len(self.data) + 1)
            return False

        # Haal alle items op als een lijst van teksten, gesorteerd op index
        items = [v for k, v in sorted(self.data.items())]

        # Voeg het item in op de nieuwe positie
        # De lijst is 0-geïndexeerd, de database 1-geïndexeerd
        items.insert(index - 1, tekst)

        # Bouw de dictionary opnieuw op met een compacte, nieuwe index
        self.data = {i: text for i, text in enumerate(items, 1)}
        self.dirty = True
        return True

    def wijzig_tekst(self, index_nummer, nieuwe_tekst):
        """Wijzigt de tekst voor een gegeven indexnummer."""
        if index_nummer in self.data:
            self.data[index_nummer] = nieuwe_tekst
            self.dirty = True
            return True
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

        self.dirty = True
        return True

    def move_item(self, source_index, dest_index):
        """
        Verplaatst een item van source_index naar dest_index en herindexeert.
        """
        if source_index not in self.data:
            logging.warning("Bronindex %d niet gevonden voor verplaatsen.", source_index)
            return False

        num_items = len(self.data)
        if not (1 <= dest_index <= num_items):
            logging.warning("Doelindex %d is buiten bereik (1-%d).", dest_index, num_items)
            return False

        # Haal alle items op als een lijst van teksten, gesorteerd op index
        items = [v for k, v in sorted(self.data.items())]

        # Haal het te verplaatsen item uit de lijst
        # De lijst is 0-geïndexeerd, de database 1-geïndexeerd
        item_to_move = items.pop(source_index - 1)

        # Voeg het item in op de nieuwe positie
        items.insert(dest_index - 1, item_to_move)

        # Bouw de dictionary opnieuw op met een compacte, nieuwe index
        self.data = {i: text for i, text in enumerate(items, 1)}

        self.dirty = True
        return True
