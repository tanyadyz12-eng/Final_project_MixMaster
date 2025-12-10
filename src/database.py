"""Database module loads and queries the cocktail dataset."""

from __future__ import annotations

import json
import os
from typing import List, Tuple, Optional

from src.cocktail import Cocktail


class CocktailDatabase:
    """Simple JSON-backed cocktail database.

    The database is intentionally lightweight: it loads the entire JSON
    file into memory during initialization.
    """

    def __init__(self, path: str | None = None) -> None:
        """Load the cocktail database.

        Args:
            path: Optional path to the JSON file. If omitted, the function
                assumes the standard ``data/cocktails.json`` relative to
                the project root directory.
        """
        if path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            path = os.path.join(base_dir, "data", "cocktails.json")

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        self.cocktails: List[Cocktail] = [Cocktail(**item) for item in raw]

    def search_by_ingredients(
        self,
        available: List[str],
        max_missing: int = 2,
        min_matched: int = 1,
    ) -> List[Tuple[Cocktail, int, int]]:
        """Rank recipes by how well they match the available ingredients.

        Args:
            available: List of ingredients that the user has.
            max_missing: Maximum number of missing ingredients allowed.
            min_matched: Minimum number of required matches.

        Returns:
            A list of tuples ``(cocktail, matched, missing)`` sorted by
            descending matched count and ascending missing count.
        """
        results: List[Tuple[Cocktail, int, int]] = []
        for cocktail in self.cocktails:
            matched, missing = cocktail.match_score(available)
            if matched >= min_matched and missing <= max_missing:
                results.append((cocktail, matched, missing))

        results.sort(key=lambda item: (-item[1], item[2], item[0].name))
        return results

    def search_by_base(self, base: str) -> List[Cocktail]:
        """Return all cocktails that use the given base spirit."""
        base_lower = base.lower()
        return [c for c in self.cocktails if c.base == base_lower]

    def search_by_flavor_tag(self, tag: str) -> List[Cocktail]:
        """Return all cocktails that contain a given flavor tag."""
        tag_lower = tag.lower()
        return [c for c in self.cocktails if any(tag_lower == f.lower() for f in c.flavors)]

    def list_bases(self) -> List[str]:
        """Return a sorted list of unique base spirits found in the database."""
        return sorted({c.base for c in self.cocktails})

    def list_flavor_tags(self) -> List[str]:
        """Return a sorted list of all distinct flavor tags in the database."""
        tags = set()
        for c in self.cocktails:
            for f in c.flavors:
                tags.add(f.lower())
        return sorted(tags)

    def find_by_name(self, name: str) -> Optional[Cocktail]:
        """Find a cocktail by name (case-insensitive)."""
        target = name.lower().strip()
        for c in self.cocktails:
            if c.name.lower() == target:
                return c
        return None
