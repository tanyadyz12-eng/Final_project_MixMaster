"""Unit tests for the RecipeGenerator class."""

from __future__ import annotations

from src.generator import RecipeGenerator


def test_generate_basic_sour():
    """Generator should return a recipe dictionary for a simple sour."""
    gen = RecipeGenerator()
    recipe = gen.generate(base="gin", style="sour")
    assert isinstance(recipe, dict)
    assert recipe["base"] == "gin"
    assert "ingredients" in recipe
    assert len(recipe["ingredients"]) >= 2
