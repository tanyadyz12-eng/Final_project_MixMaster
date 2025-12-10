"""Unit tests for the CocktailDatabase class."""

from __future__ import annotations

from src.database import CocktailDatabase


def test_database_loads():
    """Database should load at least one cocktail from the JSON file."""
    db = CocktailDatabase()
    assert len(db.cocktails) >= 50


def test_search_by_base_returns_results_for_known_base():
    """Searching by a known base spirit should return at least one recipe."""
    db = CocktailDatabase()
    results = db.search_by_base("gin")
    assert isinstance(results, list)
    assert any("gin" in c.base for c in results)
