"""Ingredient module defines the Ingredient class used by MixMaster."""

from __future__ import annotations

from typing import List, Optional


class Ingredient:
    """Represents a single ingredient.

    This class is intentionally minimal. It can be extended in the future
    to include fields such as ABV, price, or more detailed flavor notes.
    """

    def __init__(
        self,
        name: str,
        category: Optional[str] = None,
        flavor_tags: Optional[List[str]] = None,
    ) -> None:
        """Create a new Ingredient instance.

        Args:
            name: Human-readable ingredient name.
            category: Optional category label (for example, "spirit", "citrus").
            flavor_tags: Optional list of flavor descriptors such as
                "bitter", "citrus", or "herbal".
        """
        self.name = name.lower()
        self.category = category or "misc"
        self.flavor_tags = flavor_tags or []

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the ingredient."""
        return f"Ingredient({self.name})"
