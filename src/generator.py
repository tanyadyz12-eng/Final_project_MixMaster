"""Recipe generator module."""

from __future__ import annotations

import random
from typing import Dict

from src.utils import scale_ratios_to_oz


class RecipeGenerator:
    """Generate custom cocktail recipes using simple templates."""

    TEMPLATES: Dict[str, Dict[str, float]] = {
        "sour": {"base": 2.0, "sour": 1.0, "sweet": 1.0},
        "spirit_forward": {"base": 2.5, "modifier": 0.5},
        "highball": {"base": 2.0, "long": 4.0},
    }

    SOUR_POOL = {
        "citrus": ["lime_juice", "lemon_juice"],
        "tropical": ["pineapple_juice", "passionfruit_puree"],
    }

    SWEET_POOL = {
        "classic": ["simple_syrup", "honey_syrup"],
        "orange": ["triple_sec", "orange_curacao"],
    }

    LONG_POOL = {
        "bubbly": ["soda_water", "tonic_water", "ginger_beer"],
        "soft": ["cola", "ginger_ale"],
    }

    MODIFIER_POOL = {
        "herbal": ["sweet_vermouth", "dry_vermouth"],
        "bitter": ["campari", "aperol"],
    }

    def generate(
        self,
        base: str,
        style: str = "sour",
        flavor_hint: str | None = None,
        total_oz: float = 3.0,
    ) -> dict:
        """Generate a new recipe."""
        base = base.lower().strip()
        style = style.lower().strip() or "sour"

        if style not in self.TEMPLATES:
            style = "sour"

        template = self.TEMPLATES[style]
        ingredients: Dict[str, float] = {base: template["base"]}

        if style == "sour":
            sour_key = "citrus"
            if flavor_hint == "tropical":
                sour_key = "tropical"
            sour_choice = random.choice(self.SOUR_POOL[sour_key])

            sweet_key = "classic"
            if flavor_hint == "orange":
                sweet_key = "orange"
            sweet_choice = random.choice(self.SWEET_POOL[sweet_key])

            ingredients[sour_choice] = template["sour"]
            ingredients[sweet_choice] = template["sweet"]
            name = f"Custom {base.title()} Sour"

        elif style == "spirit_forward":
            mod_key = "herbal"
            if flavor_hint == "bitter":
                mod_key = "bitter"
            modifier_choice = random.choice(self.MODIFIER_POOL[mod_key])
            ingredients[modifier_choice] = template["modifier"]
            name = f"{base.title()} House Mix"

        else:
            long_key = "bubbly"
            if flavor_hint == "soft":
                long_key = "soft"
            long_choice = random.choice(self.LONG_POOL[long_key])
            ingredients[long_choice] = template["long"]
            name = f"{base.title()} Highball"

        scaled = scale_ratios_to_oz(ingredients, total_oz=total_oz)

        return {
            "name": name,
            "base": base,
            "difficulty": "easy",
            "flavors": [style] + ([flavor_hint] if flavor_hint else []),
            "ingredients": scaled,
            "instructions": "Use the standard method for this style.",
        }
