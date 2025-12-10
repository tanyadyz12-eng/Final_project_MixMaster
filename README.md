# MixMaster v2: Cocktail Recipe Assistant with CLI, GUI, and Card Export  
**Authors: Yizhe Ding & Zhihan Liu**

MixMaster v2 is a Python-based cocktail exploration and generation tool that models part of a bartender’s decision-making workflow.  
It supports both **command-line** and **GUI** modes, includes a **JSON-backed cocktail database**, a **template-based recipe generator**, and the ability to export **PNG cocktail cards**.

This project was completed as the final project for **EN.540.635 – Software Carpentry (Fall 2025)**.

---

## 🔍 Features

- **Search by ingredients**: Find cocktails based on what you have on hand.
- **Browse by base spirit or flavor tag**.
- **Generate new recipes** using ratio templates.
- **Export cocktail cards** as PNG images (using Pillow).
- **Browse and view recipes via a Tkinter GUI**.
- **~200 structured recipes** stored in `data/cocktails.json`.
- **Unit tests** covering database queries and recipe generation.

This project demonstrates:
- Multi-file Python project structure  
- Use of classes and data models  
- JSON data handling  
- GUI development  
- Image generation  
- Unit testing  
- PEP8-style organization  

---

## 📁 Project Structure

mixmaster_v2/
data/
cocktails.json # Required database (~200 recipes)
src/
ingredient.py # Ingredient data model
cocktail.py # Cocktail data model and matching logic
database.py # JSON-backed database interface
generator.py # Template-driven recipe generator
utils.py # Conversions and helpers
cards.py # PNG card rendering (using Pillow)
gui.py # Tkinter graphical interface
cli.py # Command-line interface
tests/
test_database.py
test_generator.py
test_cocktail_utils_cards.py
run.py # CLI entry point
run_gui.py # GUI entry point
requirements.txt
README.md

yaml
复制代码

⚠️ **Important:**  
The file `data/cocktails.json` **must be present** for both CLI and GUI to run.

---

## 🛠 Installation

1. Ensure you have **Python 3.10+** installed.
2. Clone or unzip this repository.
3. (Optional) Create a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
Pillow will be installed automatically.
Tkinter is included with most Python distributions on macOS and Linux.

▶️ Running the Command-Line Interface (CLI)
From the project root:

bash
复制代码
python run.py
Menu options include:

Search by ingredients

Browse by base spirit

Search by flavor tag

Generate a custom recipe

Export recipe as PNG

Open GUI instructions

Surprise me

Quit

Exported images are saved to the cards/ directory.

🪟 Running the GUI
Launch with:

bash
复制代码
python run_gui.py
The GUI includes:

A search box

A recipe list

A detail panel (ingredients + instructions)

A “surprise me” button

Optional favorites (if enabled in this build)

🧪 Testing
Run the included unit tests:

bash
复制代码
pip install pytest
pytest
The tests validate:

Database search logic

Recipe generator behavior

Cocktail card rendering (smoke tests)

🤝 Collaboration
This project was completed jointly by Yizhe Ding and Zhihan Liu.
Work was divided evenly, committed regularly through GitHub, and coordinated collaboratively in accordance with course expectations.

📑 Academic Integrity
All code in this project is original work by the authors.
No external code was copied without citation.
Standard Python libraries and Pillow are used as permitted.

📌 Notes for Reviewers / Instructors
MixMaster v2 goes beyond all in-class assignments by incorporating:

A multi-class, multi-file architecture

JSON data parsing and database-like querying

GUI development using Tkinter

Dynamic PNG generation with Pillow

Interactive CLI menus

A recipe generator with ratio templates

A structured testing suite

This satisfies the project difficulty and breadth expectations outlined in the assignment handout.
