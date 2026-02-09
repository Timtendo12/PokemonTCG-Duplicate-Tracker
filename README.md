# 🃏 PokemonTCGDeck

A simple desktop app built with **Python + Tkinter** that helps you track (duplicate) Pokémon TCG cards in your collection.

It connects directly to the **Pokémon TCG API**, automatically looks up card names from set + card number, and lets you quickly count, remove, import, and export your cards.

Perfect for collectors organizing bulk, trades, or deck building.

---

## ✨ Features

* 🔎 Auto-fetch card info using Pokémon TCG API
* 📦 Select any official Pokémon set
* ➕ Add cards by number
* 🎴 Track variants:

  * Holo
  * Reverse
  * Standard
* ➖ Remove cards
* 📄 Export collection to CSV
* 📥 Import collection from CSV
* 🖥️ Simple, fast Tkinter GUI

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/pokemon-duplicate-tracker.git
cd pokemon-duplicate-tracker
```

### 2. Install dependencies

```bash
pip install pokemontcgsdk python-dotenv
```

Tkinter comes preinstalled with most Python distributions.

---

## 🔑 API Setup

This app requires a free **Pokémon TCG API key**.

### Get a free key

👉 [https://pokemontcg.io](https://pokemontcg.io)

### Create a `.env` file

```env
POKEMONTCG_API_KEY=your_api_key_here
```

---

## ▶️ Running the App

```bash
python main.py
```

---

## 📖 How to Use

### Add cards

1. Select a set from dropdown
2. Enter card number
3. Choose variant
4. Press **Enter** or **Add**

### Remove cards

* Select an item in the list
* Click **Remove**

### Export

* Click **Export to CSV**
* Save your file

### Import

* Click **Import from CSV**
* Load a previously exported file

---

## 📂 CSV Format

Exports in this format:

```csv
Number,Card,Variant,Count
001,Bulbasaur,Standard,3
015,Pikachu,Reverse,2
```

You can edit manually or re-import later.

---

## 🛠 Tech Stack

* Python 3
* Tkinter
* pokemontcgsdk
* python-dotenv

---

## 📜 License

MIT — free to use and modify.
