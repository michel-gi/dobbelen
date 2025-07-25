#!/usr/bin/env python3
"""
Een GUI-applicatie voor het bewerken van tekst-databases.
Gebaseerd op tekstdb_bewerk.py.
"""

import tkinter as tk
from tkinter import messagebox, ttk

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
        self.bind("<Return>", self.ok)
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
        master.title("TekstDB Bewerker")
        master.geometry("600x400")  # Startgrootte

        # --- Database initialisatie ---
        # We gebruiken een hardcoded bestandsnaam, dit kan later dynamisch.
        self.db = TextDatabase("mijn_tekstdatabase.txt")

        # Hoofdframe
        self.main_frame = ttk.Frame(master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_menu()
        self.create_widgets()
        self.bind_keys()
        # Laad de data in de lijst bij het opstarten
        self.refresh_item_list()

    def create_menu(self):
        """Maakt de menubalk voor de applicatie."""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Bestand menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bestand", menu=file_menu, underline=0)
        file_menu.add_command(label="Sluiten", command=self.sluit_applicatie, accelerator="Ctrl+Q", underline=0)

        # Bewerken menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bewerken", menu=edit_menu, underline=1)
        edit_menu.add_command(label="Nieuw item...", command=self.nieuw_item, accelerator="Ctrl+N", underline=0)
        edit_menu.add_separator()
        edit_menu.add_command(label="Wijzig item...", command=self.wijzig_item, accelerator="Ctrl+W", underline=0)
        edit_menu.add_command(
            label="Verwijder item...", command=self.verwijder_item, accelerator="Ctrl+V", underline=0
        )

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
        self.btn_nieuw = ttk.Button(button_frame, text="Nieuw (N)", command=self.nieuw_item)
        self.btn_nieuw.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_wijzig = ttk.Button(button_frame, text="Wijzig (W)", command=self.wijzig_item)
        self.btn_wijzig.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_verwijder = ttk.Button(button_frame, text="Verwijder (V)", command=self.verwijder_item)
        self.btn_verwijder.pack(side=tk.LEFT, padx=5, pady=5)

        # Een 'spacer' om de sluiten-knop naar rechts te duwen
        spacer = ttk.Frame(button_frame)
        spacer.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_sluiten = ttk.Button(button_frame, text="Sluiten (S)", command=self.sluit_applicatie)
        self.btn_sluiten.pack(side=tk.RIGHT, padx=5, pady=5)

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

    def bind_keys(self):
        """Bindt toetsen aan de commando's."""
        # Sneltoetsen met Ctrl
        self.master.bind("<Control-n>", lambda event: self.nieuw_item())
        self.master.bind("<Control-w>", lambda event: self.wijzig_item())
        self.master.bind("<Control-v>", lambda event: self.verwijder_item())
        self.master.bind("<Control-q>", lambda event: self.sluit_applicatie())

        # Enkele letter sneltoetsen
        self.master.bind("n", lambda event: self.nieuw_item())
        self.master.bind("w", lambda event: self.wijzig_item())
        self.master.bind("v", lambda event: self.verwijder_item())
        self.master.bind("s", lambda event: self.sluit_applicatie())

    # --- Data-operaties ---

    def refresh_item_list(self):
        """Leest de data uit de database en vult de listbox."""
        # Maak de lijst leeg
        self.item_listbox.delete(0, tk.END)

        if not self.db.data:
            self.item_listbox.insert(tk.END, "Database is leeg. Gebruik 'Nieuw' om een item toe te voegen.")
            self.item_listbox.config(fg="gray")  # Maak de tekst grijs
            return

        self.item_listbox.config(fg="black")  # Zet de kleur terug naar standaard

        # Sorteer op index en vul de lijst
        for index, tekst in sorted(self.db.data.items()):
            preview = tekst.replace("\n", " ").strip()
            preview = (preview[:75] + "...") if len(preview) > 75 else preview
            self.item_listbox.insert(tk.END, f"{index: >3}: {preview}")

    # --- Commando's (placeholders) ---

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
        """Placeholder voor het wijzigen van een item."""
        messagebox.showinfo("Actie", "Functie 'Wijzig item' wordt aangeroepen.")

    def verwijder_item(self):
        """Placeholder voor het verwijderen van een item."""
        messagebox.showinfo("Actie", "Functie 'Verwijder item' wordt aangeroepen.")

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
