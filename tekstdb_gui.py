#!/usr/bin/env python3
"""
Een GUI-applicatie voor het bewerken van tekst-databases.
Gebaseerd op tekstdb_bewerk.py.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from database import TextDatabase


class TextEntryDialog(tk.Toplevel):
    """Een modaal dialoogvenster voor het invoeren van meerdere regels tekst."""

    def __init__(self, parent, title=None, prompt=None, initial_text=""):
        """Initialiseert het dialoogvenster."""
        super().__init__(parent)
        self.transient(parent)  # Blijf boven het hoofdvenster
        self.parent = parent
        self.result = None

        if title:
            self.title(title)

        # Frame voor de inhoud
        body = ttk.Frame(self, padding="10")
        self.initial_focus = self.body(body, prompt, initial_text)
        body.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.buttonbox()

        self.grab_set()  # Maak modaal

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master, prompt, initial_text):
        """Creëert de inhoud van het dialoogvenster."""
        if prompt:
            ttk.Label(master, text=prompt).pack(pady=5, anchor=tk.W)

        text_frame = ttk.Frame(master, borderwidth=1, relief="sunken")
        self.text = tk.Text(text_frame, width=60, height=15, wrap=tk.WORD)
        self.text.insert("1.0", initial_text)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        self.text.config(yscrollcommand=scrollbar.set)

        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_frame.pack(fill=tk.BOTH, expand=True)

        return self.text  # Geef focus aan het tekstveld

    def buttonbox(self):
        """Creëert de OK en Annuleren knoppen."""
        box = ttk.Frame(self)
        ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(box, text="Annuleren", width=10, command=self.cancel).pack(side=tk.LEFT, padx=5, pady=5)
        # De onderstaande regel is verwijderd omdat deze het venster bij elke Enter-toetsdruk sloot,
        # wat ongewenst is in een multi-line Text widget.
        # self.bind("<Return>", self.ok)
        # Gebruik Ctrl+Enter om op te slaan, dit is een gangbare conventie die niet conflicteert met typen.
        self.bind("<Control-Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def ok(self, event=None):
        """Verwerkt de OK-knop."""
        self.result = self.text.get("1.0", tk.END).strip()
        self.parent.focus_set()
        self.destroy()

    def cancel(self, event=None):
        """Verwerkt de Annuleren-knop."""
        self.parent.focus_set()
        self.destroy()


class TekstDbGuiApp:
    """De Tkinter GUI voor de TekstDB bewerker."""

    def __init__(self, master):
        """Initialiseert de applicatie."""
        self.master = master
        master.geometry("600x400")  # Startgrootte

        # Variabele voor de zoekbalk
        self.search_var = tk.StringVar()

        # --- Database initialisatie ---
        # We gebruiken een hardcoded bestandsnaam, dit kan later dynamisch.
        self.db = TextDatabase("mijn_tekstdatabase.txt")
        self._update_title()

        # Hoofdframe
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Statusbalk onderaan het venster
        self.status_bar = ttk.Label(master, text="", relief=tk.SUNKEN, anchor=tk.W, padding=2)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.create_menu()
        self.create_widgets()
        self.bind_keys()
        # Laad de data in de lijst bij het opstarten
        self.refresh_item_list()

    def _update_title(self):
        """Updates the window title with the current database filename."""
        self.master.title(f"TekstDB Bewerker - {self.db.bestandsnaam}")

    def create_menu(self):
        """Maakt de menubalk voor de applicatie."""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Bestand menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bestand", menu=file_menu, underline=0)
        file_menu.add_command(label="Open...", command=self.open_database, accelerator="Ctrl+O", underline=0)
        file_menu.add_command(label="Opslaan", command=self.save_database, accelerator="Ctrl+S", underline=0)
        file_menu.add_command(
            label="Opslaan als...", command=self.save_database_as, accelerator="Ctrl+Shift+S", underline=1
        )
        file_menu.add_separator()
        file_menu.add_command(label="Sluiten", command=self.sluit_applicatie, accelerator="Ctrl+Q", underline=0)

        # Bewerken menu
        self.edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bewerken", menu=self.edit_menu, underline=1)
        self.edit_menu.add_command(label="Nieuw item...", command=self.nieuw_item, accelerator="Ctrl+N", underline=0)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Wijzig item...", command=self.wijzig_item, accelerator="Ctrl+W", underline=0)
        self.edit_menu.add_command(
            label="Verwijder item...", command=self.verwijder_item, accelerator="Ctrl+V", underline=0
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Zoek...", command=self.focus_search, accelerator="Ctrl+F", underline=0)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu, underline=0)
        help_menu.add_command(label="Over...", command=self.show_about, underline=0)

    def create_widgets(self):
        """Maakt de widgets (knoppen, etc.) in het hoofdvenster."""
        # Frame voor de knoppen, onderaan geplaatst
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Knoppen
        self.btn_nieuw = ttk.Button(button_frame, text="Nieuw", command=self.nieuw_item)
        self.btn_nieuw.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_wijzig = ttk.Button(button_frame, text="Wijzig", command=self.wijzig_item)
        self.btn_wijzig.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_verwijder = ttk.Button(button_frame, text="Verwijder", command=self.verwijder_item)
        self.btn_verwijder.pack(side=tk.LEFT, padx=5, pady=5)

        # Een 'spacer' om de sluiten-knop naar rechts te duwen
        spacer = ttk.Frame(button_frame)
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_sluiten = ttk.Button(button_frame, text="Sluiten", command=self.sluit_applicatie)
        self.btn_sluiten.pack(side=tk.RIGHT, padx=5, pady=5)

        # --- Frame voor de zoekbalk ---
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(pady=5, padx=0, fill=tk.X, side=tk.TOP)

        ttk.Label(search_frame, text="Zoek:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Live zoeken: update de lijst bij elke toetsaanslag
        self.search_var.trace_add("write", self.perform_search)

        ttk.Button(search_frame, text="Wissen", command=self.clear_search).pack(side=tk.LEFT, padx=(5, 0))

        # --- Frame voor de lijst en scrollbar ---
        list_frame = ttk.Frame(self.main_frame)
        # Plaats dit frame boven de knoppen
        list_frame.pack(pady=5, padx=0, fill=tk.BOTH, expand=True, side=tk.TOP)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox voor de items
        self.item_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
        self.item_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Koppel scrollbar aan listbox
        scrollbar.config(command=self.item_listbox.yview)

        # Voeg dubbelklik-event toe om een item te wijzigen
        self.item_listbox.bind("<Double-1>", lambda event: self.wijzig_item())

        # Update de knopstatus wanneer de selectie verandert
        self.item_listbox.bind("<<ListboxSelect>>", self._update_button_states)

    def bind_keys(self):
        """Bindt toetsen aan de commando's."""
        # Sneltoetsen met Ctrl
        self.master.bind("<Control-f>", lambda event: self.focus_search())
        self.master.bind("<Control-o>", lambda event: self.open_database())
        self.master.bind("<Control-s>", lambda event: self.save_database())
        self.master.bind("<Control-S>", lambda event: self.save_database_as())  # Control-Shift-S
        self.master.bind("<Control-n>", lambda event: self.nieuw_item())
        self.master.bind("<Control-w>", lambda event: self.wijzig_item())
        self.master.bind("<Control-v>", lambda event: self.verwijder_item())
        self.master.bind("<Control-q>", lambda event: self.sluit_applicatie())

    # --- Data-operaties ---

    def refresh_item_list(self):
        """Leest de data uit de database en vult de listbox."""
        # Zorgt ervoor dat de zoekbalk leeg is en de volledige lijst wordt getoond.
        self.clear_search()

    def _populate_listbox(self, items_to_display):
        """Hulpfunctie om de listbox te vullen met een gegeven set items."""
        # Maak de lijst leeg
        self.item_listbox.delete(0, tk.END)

        if not items_to_display:
            self.item_listbox.insert(tk.END, "Database is leeg. Gebruik 'Nieuw' om een item toe te voegen.")
            self.item_listbox.config(fg="gray")  # Maak de tekst grijs
        else:
            self.item_listbox.config(fg="black")  # Zet de kleur terug naar standaard
            # Sorteer op index en vul de lijst
            for index, tekst in sorted(items_to_display.items()):
                preview = tekst.replace("\n", " ").strip()
                preview = (preview[:75] + "...") if len(preview) > 75 else preview
                self.item_listbox.insert(tk.END, f"{index: >3}: {preview}")

        self._update_button_states()
        self._update_status_bar()

    def perform_search(self, *args):
        """Filtert de lijst op basis van de zoekterm."""
        search_term = self.search_var.get().lower()

        if not search_term:
            items_to_show = self.db.data
        else:
            items_to_show = {index: text for index, text in self.db.data.items() if search_term in text.lower()}

        self._populate_listbox(items_to_show)
        # Na het zoeken is er geen selectie, dus update de knoppen
        self._update_button_states()

    def _get_selected_index(self):
        """Haalt het indexnummer op van het geselecteerde item in de listbox."""
        selection = self.item_listbox.curselection()
        if not selection:
            return None

        selected_line = self.item_listbox.get(selection[0])
        try:
            # De lijn is opgebouwd als "   1: Preview van de tekst..."
            index_str = selected_line.split(":")[0].strip()
            return int(index_str)
        except (ValueError, IndexError):
            return None  # Mocht er iets misgaan met de parsing

    def _update_button_states(self, event=None):
        """Updates de status van knoppen en menu-items op basis van de selectie."""
        if self.item_listbox.curselection():
            new_state = tk.NORMAL
        else:
            new_state = tk.DISABLED

        # Update knoppen
        self.btn_wijzig.config(state=new_state)
        self.btn_verwijder.config(state=new_state)

        # Update menu-items
        self.edit_menu.entryconfig("Wijzig item...", state=new_state)
        self.edit_menu.entryconfig("Verwijder item...", state=new_state)

    def _update_status_bar(self):
        """Updates de tekst in de statusbalk."""
        aantal_items = len(self.db.data)
        status_text = f"  Totaal: {aantal_items} items"
        self.status_bar.config(text=status_text)

    def focus_search(self, event=None):
        """Zet de focus op de zoekbalk."""
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def clear_search(self):
        """Maakt de zoekbalk leeg en toont de volledige lijst."""
        self.search_var.set("")
        # De trace op search_var zorgt ervoor dat perform_search wordt aangeroepen.

    # --- Commando's (Bestand) ---

    def open_database(self):
        """Opent een bestandsdialoog om een nieuwe database te laden."""
        filepath = filedialog.askopenfilename(
            title="Open databasebestand",
            filetypes=(("Tekstbestanden", "*.txt"), ("Alle bestanden", "*.*")),
            defaultextension=".txt",
        )
        if not filepath:
            return  # Gebruiker heeft geannuleerd

        try:
            self.db = TextDatabase(filepath)
            self._update_title()
            self.refresh_item_list()
            messagebox.showinfo("Succes", f"Database '{filepath}' succesvol geladen.")
        except Exception as e:
            messagebox.showerror("Fout bij openen", f"Kon het bestand niet laden.\nFout: {e}")

    def save_database(self):
        """Slaat de huidige database op naar het huidige bestand."""
        if self.db._schrijf_bestand():
            messagebox.showinfo("Succes", f"Wijzigingen opgeslagen in '{self.db.bestandsnaam}'.")
        else:
            messagebox.showerror("Fout bij opslaan", f"Kon de database niet opslaan naar '{self.db.bestandsnaam}'.")

    def save_database_as(self):
        """Opent een bestandsdialoog om de database onder een nieuwe naam op te slaan."""
        filepath = filedialog.asksaveasfilename(
            title="Database opslaan als...",
            filetypes=(("Tekstbestanden", "*.txt"), ("Alle bestanden", "*.*")),
            defaultextension=".txt",
            initialfile=self.db.bestandsnaam,
        )
        if not filepath:
            return  # Gebruiker heeft geannuleerd

        # Update de bestandsnaam in het database-object en sla het op
        self.db.bestandsnaam = filepath
        if self.db._schrijf_bestand():
            self._update_title()
            messagebox.showinfo("Succes", f"Database succesvol opgeslagen als '{filepath}'.")
        else:
            messagebox.showerror("Fout bij opslaan", f"Kon de database niet opslaan naar '{filepath}'.")

    def nieuw_item(self):
        """Opent een dialoogvenster om een nieuw item toe te voegen."""
        dialog = TextEntryDialog(self.master, title="Nieuw Item", prompt="Voer de nieuwe tekst in:")
        nieuwe_tekst = dialog.result

        if nieuwe_tekst:  # Controleer of er tekst is ingevoerd
            if self.db.voeg_tekst_toe(nieuwe_tekst):
                messagebox.showinfo("Succes", "Nieuw item succesvol toegevoegd.")
                self.refresh_item_list()
            else:
                messagebox.showerror("Fout", "Kon het nieuwe item niet opslaan in het bestand.")
        else:
            print("Toevoegen geannuleerd door gebruiker.")  # Optionele feedback in console

    def wijzig_item(self):
        """Opent een dialoogvenster om een geselecteerd item te wijzigen."""
        index_nummer = self._get_selected_index()
        if index_nummer is None:
            messagebox.showwarning("Geen selectie", "Selecteer eerst een item om te wijzigen.")
            return

        huidige_tekst = self.db.get_tekst(index_nummer)
        if huidige_tekst is None:
            # Dit zou niet moeten gebeuren als de lijst synchroon is met de db
            messagebox.showerror("Fout", f"Kon de tekst voor index {index_nummer} niet vinden.")
            return

        dialog = TextEntryDialog(
            self.master,
            title=f"Wijzig Item {index_nummer}",
            prompt=f"Wijzig de tekst voor item {index_nummer}:",
            initial_text=huidige_tekst,
        )
        nieuwe_tekst = dialog.result

        # Controleer op None; een lege string is een geldige wijziging.
        if nieuwe_tekst is not None:
            if self.db.wijzig_tekst(index_nummer, nieuwe_tekst):
                messagebox.showinfo("Succes", f"Item {index_nummer} succesvol gewijzigd.")
                self.refresh_item_list()
            else:
                messagebox.showerror("Fout", f"Kon item {index_nummer} niet wijzigen.")
        else:
            print(f"Wijziging van item {index_nummer} geannuleerd.")

    def verwijder_item(self):
        """Verwijdert het geselecteerde item na bevestiging."""
        index_nummer = self._get_selected_index()
        if index_nummer is None:
            messagebox.showwarning("Geen selectie", "Selecteer eerst een item om te verwijderen.")
            return

        bevestiging = messagebox.askyesno(
            "Bevestig Verwijdering",
            f"Weet u zeker dat u item {index_nummer} wilt verwijderen?\nDeze actie kan niet ongedaan worden gemaakt.",
        )

        if bevestiging:
            if self.db.verwijder_tekst(index_nummer):
                messagebox.showinfo(
                    "Succes", f"Item {index_nummer} succesvol verwijderd.\nDe database is geherindexeerd."
                )
                self.refresh_item_list()
            else:
                messagebox.showerror("Fout", f"Kon item {index_nummer} niet verwijderen.")

    def sluit_applicatie(self):
        """Sluit de applicatie."""
        self.master.quit()

    def show_about(self):
        """Toont het 'Over' dialoogvenster."""
        messagebox.showinfo(
            "Over TekstDB Bewerker", "TekstDB Bewerker v0.1\n\nEen GUI voor het beheren van tekst-databases."
        )


def main():
    """Start de applicatie."""
    root = tk.Tk()
    TekstDbGuiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
