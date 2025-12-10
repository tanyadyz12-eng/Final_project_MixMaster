# MixMaster v2: Cocktail Recipe Assistant with Cards and GUI

MixMaster is a Python project that models part of a bartender's
decision-making process. It allows a user to:

* Search for recipes based on the ingredients they have on hand.
* Browse recipes by base spirit or flavor tag.
* Generate new cocktail formulas using simple ratio templates.
* Export individual recipes as PNG "cocktail cards".
* Browse the recipe database using a basic Tkinter GUI.

The project is designed as a final project for a software carpentry
course and demonstrates multi-file Python organization, basic testing,
data handling, and both CLI and GUI interfaces.

## Project Structure

```text
mixmaster_v2/
  data/
    cocktails.json        # Structured cocktail database (~200 recipes)
  src/
    __init__.py
    ingredient.py         # Ingredient data model (currently minimal)
    cocktail.py           # Cocktail data model and matching logic
    database.py           # JSON-backed cocktail database
    generator.py          # Template-based custom recipe generator
    utils.py              # Unit conversion and pretty-print helpers
    cards.py              # Export cocktail cards as PNG using Pillow
    gui.py                # Tkinter graphical user interface
    cli.py                # Command-line interface
  tests/
    __init__.py
    test_database.py      # Example unit tests for the database
    test_generator.py     # Example unit tests for the generator
  run.py                  # CLI entry point
  run_gui.py              # GUI entry point
  README.md
  requirements.txt
```

## Installation

1. Ensure you have Python 3.10+ installed.
2. Clone or unzip the project into a directory of your choice.
3. (Optional) Create and activate a virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt
```

This will install `Pillow` (for image export). Tkinter is part of the
standard library on most Python installations and is used for the GUI.

## Usage: Command-Line Interface

From the project root (the directory containing `run.py`), run:

```bash
python run.py
```

You will see a text-based menu that lets you:

* Search recipes by ingredients.
* Browse recipes by base spirit.
* Search recipes by flavor tag.
* Generate a custom recipe based on a base spirit and style.
* Export a cocktail card as a PNG file (saved to the `cards/` folder).

## Usage: Graphical User Interface

To launch the Tkinter GUI instead of the CLI, run:

```bash
python run_gui.py
```

The GUI provides:

* A simple search box to filter by name or base spirit.
* A list of matching recipe names.
* A detail panel that shows ingredients and instructions for the
  selected recipe.

## Testing

You can run the small test suite using `pytest` (or Python's built-in
`unittest` runner if you prefer):

```bash
pip install pytest
pytest
```

The tests are intentionally lightweight and serve mainly to demonstrate
that the modules can be imported and used without errors.
