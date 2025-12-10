"""Utility helpers for unit conversion and pretty-printing."""

from __future__ import annotations

from typing import Dict


OZ_TO_ML = 29.57  # Commonly used ounce-to-milliliter conversion factor.


# ---------------------------------------------------------------------------
# Ingredient name normalization helpers
# ---------------------------------------------------------------------------

# A small alias table so that users can type more natural ingredient names
# on the command line (e.g. "lime juice", "simple syrup") without having to
# memorize the exact database keys (e.g. "lime_juice", "simple_syrup").
INGREDIENT_ALIASES = {
    "lemon juice": "lemon_juice",
    "lemon": "lemon_juice",
    "lime juice": "lime_juice",
    "lime": "lime_juice",
    "grapefruit juice": "grapefruit_juice",
    "grapefruit": "grapefruit_juice",
    "simple syrup": "simple_syrup",
    "sugar syrup": "simple_syrup",
    "syrup": "simple_syrup",
    "honey syrup": "honey_syrup",
    "ginger syrup": "ginger_syrup",
    "agave": "agave_syrup",
    "agave syrup": "agave_syrup",
    "grenadine": "grenadine",
    "orgeat": "orgeat_syrup",
    "orgeat syrup": "orgeat_syrup",
    "ginger beer": "ginger_beer",
    "soda": "soda_water",
    "soda water": "soda_water",
    "club soda": "soda_water",
    "tonic": "tonic_water",
    "tonic water": "tonic_water",
    "dry vermouth": "dry_vermouth",
    "sweet vermouth": "sweet_vermouth",
    "white rum": "white_rum",
    "orange liqueur": "orange_liqueur",
    "triple sec": "triple_sec",
    "aperol": "aperol",
    "amaro nonino": "amaro_nonino",
    "elderflower liqueur": "elderflower_liqueur",
    "st germain": "elderflower_liqueur",
    "maraschino": "maraschino_liqueur",
    "maraschino liqueur": "maraschino_liqueur",
    "coffee liqueur": "coffee_liqueur",
    "chartreuse": "green_chartreuse",
    "green chartreuse": "green_chartreuse",
    # A very coarse mapping, but helpful for casual users typing "whiskey".
    "whiskey": "bourbon",
    "orange juice": "orange_juice",
    "oj": "orange_juice",
    "pineapple juice": "pineapple_juice",
    "pineapple": "pineapple_juice",
    "cranberry juice": "cranberry_juice",
    "cranberry": "cranberry_juice",
    "apple juice": "apple_juice",
    "apple": "apple_juice",
    "pear juice": "pear_juice",
    "mango juice": "mango_juice",
    "mango puree": "mango_puree",
    "passion fruit juice": "passionfruit_juice",
    "passionfruit juice": "passionfruit_juice",
    "grape juice": "grape_juice",
    "lychee juice": "lychee_juice",
    "cola": "cola",
    "coke": "cola",
    "diet coke": "cola",
    "lemon-lime soda": "lemon_lime_soda",
    "lemon lime soda": "lemon_lime_soda",
    "sprite": "lemon_lime_soda",
    "7up": "lemon_lime_soda",
    "ginger ale": "ginger_ale",
    "hojicha": "hojicha_tea",
    "hojicha tea": "hojicha_tea",
    "roasted green tea": "hojicha_tea",
    "matcha": "matcha",
    "matcha syrup": "matcha_syrup",
    "earl grey": "earl_grey_tea",
    "earl grey tea": "earl_grey_tea",
    "oolong": "oolong_tea",
    "oolong tea": "oolong_tea",
    "jasmine tea": "jasmine_tea",
    "black tea": "black_tea",
    "english breakfast": "black_tea",
    "espresso": "espresso",
    "cold brew": "cold_brew_coffee",
    "coffee": "coffee",
    "mocha": "mocha_syrup",
    "chocolate syrup": "chocolate_syrup",

}


def normalize_ingredient_name(name: str) -> str:
    """Normalize a free-form ingredient string to an internal key.

    This helper makes the CLI feel less fragile by allowing users to type
    human-friendly names such as ``"lemon juice"`` or ``"simple syrup"``.
    We first canonicalize spacing and case, then consult the
    :data:`INGREDIENT_ALIASES` table, and finally fall back to replacing
    spaces with underscores.

    Examples:
        >>> normalize_ingredient_name("Lime juice")
        'lime_juice'
        >>> normalize_ingredient_name("simple syrup")
        'simple_syrup'
    """
    key = name.strip().lower()
    # Treat dashes and underscores as spaces when normalizing.
    key = key.replace("-", " ").replace("_", " ")
    # Collapse repeated whitespace
    key = " ".join(key.split())
    if not key:
        return ""
    if key in INGREDIENT_ALIASES:
        return INGREDIENT_ALIASES[key]
    # Fallback: "lime juice" -> "lime_juice"
    return key.replace(" ", "_")


def scale_ratios_to_oz(ingredient_ratios: Dict[str, float], total_oz: float = 3.0) -> Dict[str, dict]:
    """Scale ingredient ratios to ounces and milliliters.

    This function assumes that each ingredient has a non-negative "ratio"
    which is scaled so that the total volume equals ``total_oz``.

    Args:
        ingredient_ratios: Mapping from ingredient names to numeric ratios.
        total_oz: Desired total volume in ounces.

    Returns:
        A mapping from ingredient name to a dictionary with fields
        ``ratio``, ``oz``, and ``ml``.
    """
    total_ratio = sum(ingredient_ratios.values())
    if total_ratio <= 0:
        return {}

    result: Dict[str, dict] = {}
    for name, ratio in ingredient_ratios.items():
        oz = total_oz * (ratio / total_ratio)
        ml = oz * OZ_TO_ML
        result[name] = {
            "ratio": ratio,
            "oz": round(oz, 2),
            "ml": round(ml, 1),
        }
    return result


def print_recipe_display(display_dict: dict) -> None:
    """Pretty-print a recipe dictionary on the command line.

    The input is expected to be the result of :meth:`Cocktail.to_display`
    or the recipe generator.

    Args:
        display_dict: Recipe dictionary with keys ``name``, ``base``,
            ``difficulty``, ``flavors``, ``ingredients``, and ``instructions``.
    """
    print("\n=== {} ===".format(display_dict.get("name", "Unnamed Recipe")))
    base = display_dict.get("base")
    if base:
        print("Base: {}".format(base))
    difficulty = display_dict.get("difficulty")
    if difficulty:
        print("Difficulty: {}".format(difficulty))
    flavors = display_dict.get("flavors") or []
    if flavors:
        print("Flavors: " + ", ".join(flavors))

    print("\nIngredients:")
    ingredients = display_dict.get("ingredients", {})
    for name, info in ingredients.items():
        oz = info.get("oz", "?")
        ml = info.get("ml", "?")
        print("  - {}: {} oz (~{} ml)".format(name, oz, ml))

    instructions = display_dict.get("instructions", "No instructions provided.")
    print("\nInstructions:")
    print("  " + instructions)
    print()
