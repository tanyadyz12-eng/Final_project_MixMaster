"""Cocktail module defines the Cocktail class and helper methods."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .utils import scale_ratios_to_oz, normalize_ingredient_name


class Cocktail:
    """Represents a cocktail recipe loaded from the database.

    A cocktail stores its base spirit, ingredient ratio map, flavor tags,
    and plain-text mixing instructions.
    """

    def __init__(
        self,
        name: str,
        base: str,
        ingredients: Dict[str, float],
        flavors: List[str],
        instructions: str,
        difficulty: str = "medium",
    ) -> None:
        """Create a new Cocktail.

        Args:
            name: Recipe name.
            base: Base spirit name (e.g. "gin", "rum", "tequila").
            ingredients: Mapping from ingredient name to a ratio (not volume).
            flavors: List of flavor tags such as "bitter", "citrus", "sweet".
            instructions: Plain-text mixing instructions.
            difficulty: Free-text difficulty label.
        """
        self.name = name
        self.base = base.lower()
        self.ingredients = ingredients
        self.flavors = flavors
        self.instructions = instructions
        self.difficulty = difficulty

    def ingredient_names(self) -> List[str]:
        """Return the list of ingredient names used in this recipe."""
        return list(self.ingredients.keys())

    def match_score(self, available_ingredients: List[str]) -> Tuple[int, int]:
        """Compute how well this cocktail matches a set of available ingredients.

        Args:
            available_ingredients: List of ingredient names that the user has.

        Returns:
            A tuple (matched, missing) where:

            * matched – number of recipe ingredients that appear in the available set.
            * missing – number of recipe ingredients that are not available.
        """
        # Normalize both the available ingredient names and the recipe keys
        # so that users can type natural strings such as "lime juice" or
        # "simple syrup" on the command line.
        available = {normalize_ingredient_name(a) for a in available_ingredients if a.strip()}
        recipe = set(self.ingredients.keys())
        matched = len(recipe & available)
        missing = len(recipe - available)
        return matched, missing

    def to_display(self, total_oz: float = 3.0) -> dict:
        """Return a human-friendly representation of the cocktail.

        The method converts ingredient ratios into ounce/milliliter values
        using :func:`scale_ratios_to_oz`.

        Args:
            total_oz: Approximate total volume (in ounces) used for scaling.

        Returns:
            A dictionary with keys: name, base, difficulty, flavors,
            ingredients (detailed mapping), and instructions.
        """
        scaled = scale_ratios_to_oz(self.ingredients, total_oz=total_oz)
        return {
            "name": self.name,
            "base": self.base,
            "difficulty": self.difficulty,
            "flavors": self.flavors,
            "ingredients": scaled,
            "instructions": self.instructions,
        }

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the cocktail."""
        return "Cocktail({})".format(self.name)
