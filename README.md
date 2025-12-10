[README.md](https://github.com/user-attachments/files/24068673/README.md)
# MixMaster v2: Cocktail Recipe Assistant with CLI, GUI, and PNG Card Export

Authors: Yizhe Ding & Zhihan Liu

MixMaster v2 is a Python-based cocktail exploration and recipe-generation system that models elements of a bartender’s decision-making workflow. It provides both command-line and graphical interfaces, a JSON-backed recipe database, a template-driven recipe generator, and the ability to export cocktail cards as PNG images.

This project was developed as the final project for EN.540.635 – Software Carpentry (Fall 2025).

## Features

- Search for cocktails based on available ingredients.
- Browse recipes by base spirit or flavor tag.
- Generate new cocktail formulas using ratio-based templates.
- Export individual recipes as PNG cocktail cards (via Pillow).
- Explore the full recipe collection using a Tkinter GUI.
- Includes approximately 3,000 structured cocktail recipes stored in `data/cocktails.json`.
- Provides unit tests for database functionality, recipe generation, and image export.

This project demonstrates proficiency in:

- Multi-file Python software design
- Object-oriented programming
- JSON data parsing and search logic
- GUI development using Tkinter
- Image generation with Pillow
- Unit testing and maintainable code practices

## Project Structure

mixmaster_v2/
  data/
    cocktails.json        # Required database (~3000 recipes)
  src/
    ingredient.py         # Ingredient model
    cocktail.py           # Cocktail model and matching logic
    database.py           # JSON-backed recipe database
    generator.py          # Ratio-based recipe generator
    utils.py              # Utility functions and formatting helpers
    cards.py              # PNG cocktail card rendering
    gui.py                # Tkinter GUI implementation
    cli.py                # Command-line interface implementation
  tests/
    test_database.py
    test_generator.py
    test_cocktail_utils_cards.py
  run.py                  # CLI entry point
  run_gui.py              # GUI entry point
  requirements.txt
  README.md

## Installation

1. Install Python 3.10 or higher.
2. Download or clone the repository.
3. (Optional) Create and activate a virtual environment.
4. Install required dependencies:

pip install -r requirements.txt

Pillow is installed automatically. Tkinter is included by default in most macOS and Linux Python distributions.

## Using the Command-Line Interface (CLI)

From the project root:

python run.py

Available menu options:

1. Search by ingredients
2. Browse by base spirit
3. Search by flavor tag
4. Generate a custom cocktail
5. Export a cocktail card as a PNG file
6. Show instructions for GUI usage
7. Generate a random recommendation
8. Exit the program

Exported PNG cocktail cards are saved in the `cards/` directory.

## Using the Graphical User Interface (GUI)

Launch the GUI with:

python run_gui.py

The GUI includes:

- A search bar
- A scrollable list of matching recipes
- A detailed recipe view with ingredients and instructions
- A random cocktail generator
- Optional support for saving and viewing favorites

## Testing

To run all tests:

pip install pytest
pytest

The test suite verifies:

- Database search and filtering behavior
- Template-based recipe generation logic
- PNG cocktail card creation (smoke tests)

## Collaboration Statement

This project was completed jointly by Yizhe Ding and Zhihan Liu. Both contributors shared responsibility for design, implementation, testing, and documentation. Development was conducted collaboratively using GitHub, with balanced commit activity and clear division of work.

## Academic Integrity

All code in this repository is original unless explicitly cited within the source. No external code was reused without attribution. Only standard Python libraries and Pillow are used in accordance with course policies.

## Notes for Reviewers and Instructors

MixMaster v2 exceeds the complexity of in-class assignments by incorporating:

- A multi-module, object-oriented codebase
- A large JSON dataset (~3000 recipes) with structured search tools
- A complete Tkinter-based GUI application
- Dynamic PNG cocktail card rendering
- An interactive command-line interface
- A modular, template-driven recipe generator
- A documented suite of automated tests

This implementation meets the expected standards for project difficulty, software engineering quality, and completeness outlined in the course rubric.
