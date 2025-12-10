MixMaster v2: Cocktail Recipe Assistant with CLI, GUI, and PNG Card Export

Authors: Yizhe Ding & Zhihan Liu

MixMaster v2 is a Python-based cocktail exploration and recipe-generation system that models elements of a bartender’s decision-making workflow. It provides both command-line and graphical user interfaces, a JSON-backed recipe database, a template-driven recipe generator, and functionality for exporting cocktail cards as PNG images.

This project was developed as the final project for EN.540.635 – Software Carpentry (Fall 2025).

Features

Search for cocktails based on available ingredients.

Browse recipes by base spirit or flavor tag.

Generate new cocktail formulas using ratio-based templates.

Export individual recipes as PNG cocktail cards (via Pillow).

Explore the full database through a Tkinter graphical interface.

Includes approximately 3,000 structured cocktail recipes in data/cocktails.json.

Contains unit tests for the database, generator, and card-rendering components.

The project demonstrates proficiency in:

Multi-file Python software design

Object-oriented programming

JSON data handling and search algorithms

GUI development with Tkinter

Image generation and layout

Unit testing and code organization

PEP8-style, maintainable code practices

Project Structure
mixmaster_v2/
  data/
    cocktails.json        # Required database (~3000 recipes)
  src/
    ingredient.py         # Ingredient model and representation
    cocktail.py           # Cocktail model and match/evaluation logic
    database.py           # JSON-backed database handler
    generator.py          # Ratio-based recipe generator
    utils.py              # Conversion utilities and formatting helpers
    cards.py              # Cocktail card rendering using Pillow
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


Note: data/cocktails.json must be present for both the CLI and GUI to function correctly.

Installation

Install Python 3.10 or higher.

Download or clone the repository.

(Optional) Create and activate a virtual environment.

Install dependencies:

pip install -r requirements.txt


Pillow will be installed automatically. Tkinter is included by default in most macOS and Linux Python distributions.

Using the Command-Line Interface (CLI)

From the project root directory:

python run.py


The CLI provides options to:

Search by ingredients

Browse by base spirit

Search by flavor tag

Generate a custom cocktail

Export a cocktail card as a PNG file

Display instructions for GUI usage

Generate a random recommendation

Quit the program

Exported cocktail cards are saved in the cards/ directory.

Using the Graphical User Interface (GUI)

Launch the GUI with:

python run_gui.py


The GUI includes:

A search bar

A scrollable recipe list

A detailed view with ingredients and instructions

A random recipe generator

Optional support for saving and viewing favorites

Testing

To execute the test suite:

pip install pytest
pytest


The tests validate:

Database lookup and filtering logic

Template-based recipe generation

Image rendering (smoke tests for card creation)

Collaboration Statement

This project was completed jointly by Yizhe Ding and Zhihan Liu. Both contributors participated equally in software design, implementation, testing, and documentation. Development was coordinated through GitHub with balanced commit activity and shared responsibility for all technical components.

Academic Integrity

All code in this repository is original unless explicitly cited within the source. No external code was reused without attribution. Only standard Python libraries and Pillow are used in accordance with course policy.

Notes for Reviewers and Instructors

MixMaster v2 extends significantly beyond all in-class programming assignments by incorporating:

A multi-module, object-oriented architecture

A large-scale JSON dataset (~3000 recipes) and structured search operations

A full Tkinter graphical application

Dynamic PNG card generation using Pillow

An interactive command-line interface

A modular, template-driven recipe creation engine

A documented suite of automated tests

This implementation meets the expectations for project complexity, software engineering quality, and completeness described in the assignment rubric.
