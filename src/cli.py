"""Command-line interface for the MixMaster project."""

from __future__ import annotations

import os
import random

from src.database import CocktailDatabase
from src.generator import RecipeGenerator
from src.utils import print_recipe_display
from src.cards import render_cocktail_card


def _prompt_ingredients() -> list[str]:
    """Prompt the user to enter a comma-separated list of available ingredients."""
    raw = input(
        "Enter the ingredients you have (comma-separated, e.g. 'gin, lime juice, simple syrup'):\n> "
    )
    if not raw.strip():
        return []
    return [item.strip() for item in raw.split(",")]


def _prompt_base() -> str:
    """Prompt the user to choose a base spirit from the database."""
    return input(
        "Choose a base spirit (e.g. gin, rum, tequila, vodka, bourbon):\n> "
    ).strip()


def _prompt_style_or_flavor() -> str:
    """Prompt the user for a cocktail style or flavor tag when generating a custom recipe."""
    return input(
        "Optional style/flavor (sour / spirit_forward / highball / citrus / bitter / herbal / bubbly).\n"
        "Press Enter to accept the default: sour\n> "
    ).strip()


def _select_recipe_from_list(cocktails: list, prompt: str) -> None:
    """Interactively let the user choose and display a recipe from a provided list."""
    if not cocktails:
        print("No recipes found.\n")
        return

    print()
    for idx, cocktail in enumerate(cocktails, start=1):
        print(f"  {idx}) {cocktail.name}")

    answer = input(
        f"\n{prompt}\nYou can type a recipe name or its number.\n> "
    ).strip()
    if not answer:
        print()
        return

    if answer.isdigit():
        index = int(answer)
        if 1 <= index <= len(cocktails):
            chosen = cocktails[index - 1]
            print_recipe_display(chosen.to_display())
            return
        else:
            print("Index out of range. Returning to main menu.\n")
            return

    for cocktail in cocktails:
        if cocktail.name.lower() == answer.lower():
            print_recipe_display(cocktail.to_display())
            return

    print("No recipe with that name or index was found.\n")


def _select_recipe_and_export_card(db: CocktailDatabase) -> None:
    """Let the user pick a recipe by base and export it as a PNG cocktail card."""
    print("Available bases:", ", ".join(db.list_bases()))
    base = _prompt_base()
    cocktails = db.search_by_base(base)
    if not cocktails:
        print("No recipes found for that base spirit.\n")
        return

    print(f"\nRecipes using base '{base}':")
    for idx, cocktail in enumerate(cocktails, start=1):
        print(f"  {idx}) {cocktail.name}")

    answer = input(
        "\nType a recipe name or number to export as a PNG card, or press Enter to cancel:\n> "
    ).strip()
    if not answer:
        print("Card export cancelled.\n")
        return

    chosen = None
    if answer.isdigit():
        index = int(answer)
        if 1 <= index <= len(cocktails):
            chosen = cocktails[index - 1]
    else:
        for c in cocktails:
            if c.name.lower() == answer.lower():
                chosen = c
                break

    if chosen is None:
        print("No recipe with that name or index was found.\n")
        return

    display = chosen.to_display()
    cards_dir = os.path.join(os.getcwd(), "cards")
    os.makedirs(cards_dir, exist_ok=True)
    safe_name = chosen.name.replace(" ", "_").replace("#", "")
    output_path = os.path.join(cards_dir, f"{safe_name}.png")
    render_cocktail_card(display, output_path)
    print(f"Cocktail card exported to: {output_path}\n")


def _surprise_me(db: CocktailDatabase) -> None:
    """Pick a random cocktail (optionally filtered) and show it as a surprise."""
    print("\n=== Surprise Me ===")
    print("You can optionally narrow things down, or just press Enter for a completely random pick.")
    base_hint = input("Base spirit filter (e.g. gin, rum, tequila) or press Enter for any:\n> ").strip().lower()
    flavor_hint = input("Flavor tag filter (e.g. citrus, bitter, floral) or press Enter for any:\n> ").strip().lower()

    candidates = list(db.cocktails)

    if base_hint:
        candidates = [c for c in candidates if c.base.lower() == base_hint]
        if not candidates:
            print(f"No recipes found with base '{base_hint}'. Falling back to any base.\n")
            candidates = list(db.cocktails)

    if flavor_hint:
        filtered = []
        for c in candidates:
            if any(flavor_hint == f.lower() for f in c.flavors):
                filtered.append(c)
        if not filtered:
            print(
                f"No recipes found with flavor tag '{flavor_hint}'. Falling back to ignoring flavor filter.\n"
            )
        else:
            candidates = filtered

    if not candidates:
        print("No recipes available in the database.\n")
        return

    choice = random.choice(candidates)
    print("\nYour surprise cocktail is:")
    print_recipe_display(choice.to_display())


def run_cli() -> None:
    """Launch the main interactive command-line interface loop for MixMaster."""
    db = CocktailDatabase()
    generator = RecipeGenerator()

    print("Welcome to MixMaster - a simple cocktail recipe assistant.\n")

    while True:
        print("Please choose an option:")
        print("  1) Search recipes by available ingredients")
        print("  2) Browse recipes by base spirit")
        print("  3) Search recipes by flavor tag")
        print("  4) Generate a custom recipe")
        print("  5) Export a cocktail card as PNG")
        print("  6) Show GUI usage hint")
        print("  7) Surprise me with a random cocktail")
        print("  0) Exit")
        choice = input("> ").strip()

        if choice == "0":
            print("Goodbye! Cheers and happy mixing.\n")
            break

        elif choice == "1":
            available = _prompt_ingredients()
            if not available:
                print("No ingredients entered. Returning to main menu.\n")
                continue

            matches = db.search_by_ingredients(
                available,
                max_missing=2,
                min_matched=1,
            )
            if not matches:
                print("No suitable recipes found for your current ingredients.\n")
                continue

            cocktails = [c for (c, _, _) in matches[:10]]
            print("\nBest matching recipes (top 10):")
            _select_recipe_from_list(
                cocktails,
                "Type a recipe name or number to view full details, or press Enter to return to the menu.",
            )

        elif choice == "2":
            print("Available bases:", ", ".join(db.list_bases()))
            base = _prompt_base()
            cocktails = db.search_by_base(base)
            if not cocktails:
                print("No recipes found for that base spirit.\n")
                continue

            print(f"\nRecipes using base '{base}':")
            _select_recipe_from_list(
                cocktails,
                "Type a recipe name or number to view full details, or press Enter to return to the menu.",
            )

        elif choice == "3":
            print("Example flavor tags:", ", ".join(db.list_flavor_tags()))
            tag = input("Enter a flavor tag to search for:\n> ").strip()
            cocktails = db.search_by_flavor_tag(tag)
            if not cocktails:
                print("No recipes found with that flavor tag.\n")
                continue

            print(f"\nRecipes containing flavor tag '{tag}':")
            _select_recipe_from_list(
                cocktails,
                "Type a recipe name or number to view full details, or press Enter to return to the menu.",
            )

        elif choice == "4":
            base = _prompt_base()
            style_or_hint = _prompt_style_or_flavor()
            style = "sour"
            flavor_hint = None

            if style_or_hint in {"sour", "spirit_forward", "highball"}:
                style = style_or_hint
            elif style_or_hint:
                flavor_hint = style_or_hint

            recipe = generator.generate(
                base=base,
                style=style,
                flavor_hint=flavor_hint,
                total_oz=3.0,
            )
            print_recipe_display(recipe)

        elif choice == "5":
            _select_recipe_and_export_card(db)

        elif choice == "6":
            print(
                "\nTo launch the graphical user interface instead of the CLI, "
                "run the following command from the project root:\n"
                "    python3 run_gui.py\n"
            )

        elif choice == "7":
            _surprise_me(db)

        else:
            print("Unrecognized choice. Please enter a number between 0 and 7.\n")
