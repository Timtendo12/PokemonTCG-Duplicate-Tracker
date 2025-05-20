import tkinter as tk
import csv
import os

from tkinter import ttk, filedialog, messagebox
from dotenv import load_dotenv

from pokemontcgsdk import Card,Set,RestClient, PokemonTcgException


class PokemonCardTracker:
    def __init__(self, root: tk.Tk):        
        self.root = root
        self.root.title("Pokémon Duplicate Tracker")
        self.card_data: dict[str, int] = {}

        self.currentSet = "sv9"
        self.set_options: dict[str, str] = {}
        
        self.fill_set_options()
        
        # Dropdown for set selection
        self.set_var = tk.StringVar(value=list(self.set_options.keys())[-1]) # Default to last set
        self.set_dropdown = ttk.Combobox(root, textvariable=self.set_var, values=list(self.set_options.keys()))
        self.set_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Entry for card number
        ttk.Label(root, text="Card Number:").grid(row=1, column=0, padx=5, pady=5)
        self.card_entry = ttk.Entry(root)
        self.card_entry.grid(row=1, column=1, padx=5, pady=5)

        # Radio buttons for variant
        self.variant = tk.StringVar(value="Standard")
        variants = ["Holo", "Reverse", "Standard"]
        for idx, v in enumerate(variants):
            ttk.Radiobutton(root, text=v, variable=self.variant, value=v).grid(row=2, column=idx, padx=5)

        # Add button
        self.add_button = ttk.Button(root, text="Add", command=self.add_card)
        self.add_button.grid(row=3, column=0, pady=10, padx=15)

        # Remove button
        self.remove_button = ttk.Button(root, text="Remove", command=self.remove_card)
        self.remove_button.grid(row=3, column=2, pady=10, padx=15)

        # Listbox to show current counts
        self.card_listbox = tk.Listbox(root, width=40)
        self.card_listbox.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        
        # Export button
        self.export_button = ttk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=5, column=0, pady=10, padx=15)

        self.import_button = ttk.Button(root, text="Import from CSV", command=self.import_from_csv)
        self.import_button.grid(row=5, column=2, pady=10, padx=15)

    def add_card(self) -> None:
        number = self.card_entry.get().strip()
        variant = self.variant.get()

        if not number:
            return  # Ignore empty input
        
        card = self.find_card(number)
        
        # always make number 3 digits
        if len(number) < 3:
            number = number.zfill(3)

        key = f"{number} - {card.name} ({variant})"
        self.card_data[key] = self.card_data.get(key, 0) + 1
        self.update_listbox()

        self.card_entry.delete(0, tk.END)

    def update_listbox(self) -> None:
        self.card_listbox.delete(0, tk.END)
        for key, count in sorted(self.card_data.items()):
            self.card_listbox.insert(tk.END, f"{count}x: {key}")

    def remove_card(self) -> None:
        selected = self.card_listbox.curselection()
        if selected:
            key = self.card_listbox.get(selected[0]).split(":")[1].strip()
            if key in self.card_data:
                self.card_data[key] -= 1
                if self.card_data[key] <= 0:
                    del self.card_data[key]
                self.update_listbox()

    def find_card(self, number: str) -> Card | None:
        selected_display = self.set_var.get()
        selected_set = self.set_options.get(selected_display, "sv9")  # fallback to sv9
        card_id = f"{selected_set}-{number}"
        try:
            card = Card.find(card_id)
            if card:
                return card
            else:
                print(f"Card not found with id {card_id}.")
                return None
        except PokemonTcgException as e:
            try:
                error_str = e.args[0].decode() if isinstance(e.args[0], bytes) else str(e)
            except Exception:
                error_str = "Unknown error"

            messagebox.showerror("Card Not Found", f"Could not find card ID {card_id}.\n\n{error_str}")
            return None
        
    def export_to_csv(self) -> None:
        if not self.card_data:
            print("No data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save CSV File")

        if not file_path:
            return  # User cancelled

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Card", "Variant", "Count"])
            for key, count in sorted(self.card_data.items()):
                number, card_info = key.split(" - ")
                card_name, variant = card_info.split(" (")
                card_name = card_name.strip()
                variant = variant.strip(")")
                writer.writerow([number, card_name, variant, count])

        print(f"Exported to {file_path}")

    def import_from_csv(self) -> None:
        file_path = filedialog.askopenfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")],
                                               title="Open CSV File")

        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                for row in reader:
                    if len(row) != 4:
                        print(f"Invalid row format: Expected 4 rows but got {len(row)}, skipping: {row}")
                        continue
                    number, card_name, variant, count = row
                    try:
                        count = int(count)
                        card = f"{number} - {card_name} ({variant})"
                        self.card_data[card] = self.card_data.get(card, 0) + count
                    except ValueError:
                        print(f"Invalid count for card '{card_name}': {count}")
            self.update_listbox()
            print(f"Imported from {file_path}")
        except Exception as e:
            print(f"Error importing CSV: {e}")

    def fill_set_options(self):
        sets = Set.all()
        print(f"Found {len(sets)} sets.")
        for s in sets:
            print(f"{s.id} - {s.name}")
            self.set_options[s.name] = s.id


if __name__ == "__main__":
    load_dotenv()

    api_key = os.getenv("POKEMONTCG_API_KEY")
    if api_key is None:
        messagebox.showerror("Error", "API key not found. Please set POKEMONTCG_API_KEY in the .env file")
        exit(0)

    RestClient.configure(api_key)
    
    root = tk.Tk()
    app = PokemonCardTracker(root)
    root.mainloop()
