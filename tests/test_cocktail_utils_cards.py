"""Additional unit tests for Cocktail, utility helpers, and card rendering."""

from __future__ import annotations


from src.cocktail import Cocktail
from src.utils import scale_ratios_to_oz, normalize_ingredient_name
from src.cards import render_cocktail_card
from src.database import CocktailDatabase


def test_cocktail_match_score_full_and_partial():
    """match_score should correctly count matched and missing ingredients."""
    c = Cocktail(
        name="Test Martini",
        base="gin",
        ingredients={"gin": 2.0, "vermouth": 1.0},
        flavors=["spirit_forward"],
        instructions="Stir with ice and strain.",
    )

    matched, missing = c.match_score(["gin", "vermouth", "ice"])
    assert matched == 2
    assert missing == 0

    matched_partial, missing_partial = c.match_score(["gin"])
    assert matched_partial == 1
    assert missing_partial == 1


def test_scale_ratios_to_oz_preserves_total_volume():
    """Scaled ingredient volumes should sum approximately to total_oz."""
    ratios = {"a": 1.0, "b": 1.0}
    total_oz = 4.0
    scaled = scale_ratios_to_oz(ratios, total_oz=total_oz)

    oz_values = [info["oz"] for info in scaled.values()]
    assert abs(sum(oz_values) - total_oz) < 1e-6

    # Milliliter values should be positive and roughly oz * constant.
    for info in scaled.values():
        assert info["ml"] > 0
        assert abs(info["ml"] / info["oz"] - 29.57) < 0.5


def test_search_by_ingredients_returns_sorted_matches():
    """search_by_ingredients should return matches sorted by matched desc, missing asc."""
    db = CocktailDatabase()
    matches = db.search_by_ingredients(
        ["gin", "lime_juice", "simple_syrup"],
        max_missing=3,
        min_matched=1,
    )
    assert matches, "Expected at least one match for basic gin sour ingredients."

    # Ensure results are sorted by (matched desc, missing asc)
    scores = [(m, -miss) for _, m, miss in matches]
    assert scores == sorted(scores, reverse=True)


def test_render_cocktail_card_creates_png(tmp_path):
    """render_cocktail_card should produce a non-empty PNG file."""
    display = {
        "name": "Test Sour",
        "base": "gin",
        "difficulty": "easy",
        "flavors": ["citrus", "refreshing"],
        "ingredients": {
            "gin": {"oz": 2.0, "ml": 59.0},
            "lime_juice": {"oz": 0.75, "ml": 22.0},
        },
        "instructions": "Shake with ice and strain into a chilled coupe.",
    }

    output_path = tmp_path / "test_card.png"
    render_cocktail_card(display, str(output_path))

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_normalize_ingredient_name_aliases():
    """normalize_ingredient_name should map common human names to internal keys."""
    assert normalize_ingredient_name("Lime juice") == "lime_juice"
    assert normalize_ingredient_name("simple syrup") == "simple_syrup"
    assert normalize_ingredient_name("  TONIC  WATER ") == "tonic_water"
    # Fallback: unknown names just collapse spaces to underscores.
    assert normalize_ingredient_name("weird thing") == "weird_thing"


def test_match_score_with_human_friendly_ingredient_names():
    """match_score should work with human-friendly ingredient names like 'lime juice'."""
    c = Cocktail(
        name="Alias Sour",
        base="gin",
        ingredients={"gin": 2.0, "lime_juice": 1.0, "simple_syrup": 1.0},
        flavors=["citrus"],
        instructions="Shake with ice.",
    )
    matched, missing = c.match_score(["Gin", "lime juice", "simple syrup"])
    assert matched == 3
    assert missing == 0
