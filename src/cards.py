"""Rendering utilities to export cocktail cards as vertical book-style pages (colored, with simple illustration)."""

from __future__ import annotations

import os
from typing import Dict

from PIL import Image, ImageDraw, ImageFont


def _text_size(draw: ImageDraw.ImageDraw, text: str, font):
    """Return the width and height of *text* for the given *font*.

    Newer versions of Pillow prefer :meth:`ImageDraw.textbbox`, but this is
    not supported for every bitmap font. To keep the card renderer robust
    across environments we try ``textbbox`` first and gracefully fall back
    to the older :meth:`ImageDraw.textsize` API if needed.
    """
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    except Exception:
        # Fallback path for environments where textbbox is not available
        # or does not support the current font type.
        return draw.textsize(text, font=font)


def _wrap_text(text: str, width: int) -> str:
    """Word-wrap text to a maximum number of characters per line."""
    words = text.split()
    lines = []
    current: list[str] = []
    count = 0
    for w in words:
        extra = 1 if current else 0
        if count + len(w) + extra > width:
            lines.append(" ".join(current))
            current = [w]
            count = len(w)
        else:
            current.append(w)
            count += len(w) + extra
    if current:
        lines.append(" ".join(current))
    return "\n".join(lines)


def _load_font(preferred: str, size: int):
    """Try to load a TrueType font; fall back to the default bitmap font."""
    try:
        return ImageFont.truetype(preferred, size)
    except Exception:
        return ImageFont.load_default()


def render_cocktail_card(
    display_dict: Dict,
    output_path: str,
    width: int = 900,
    height: int = 1400,
) -> None:
    """Render a cocktail card as a vertical book-style PNG image.

    Layout:
        - Soft colored background with a top banner.
        - Simple "glass" illustration in the banner.
        - Centered title + base.
        - INGREDIENTS section with aligned columns.
        - INSTRUCTIONS section with wrapped text.
    """

    # ------------------------------------------------------------------
    # Canvas and colors
    # ------------------------------------------------------------------
    # Soft warm background
    background_color = (248, 245, 238)   # off-white / paper-like
    header_color = (230, 210, 230)       # light mauve
    divider_color = (210, 210, 210)
    text_main = (30, 30, 30)
    text_muted = (90, 90, 90)

    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # ------------------------------------------------------------------
    # Fonts (try a TrueType font first, then fall back)
    # ------------------------------------------------------------------
    # On macOS, "Helvetica" or "Arial" are usually available.
    title_font = _load_font("Helvetica", 40)
    section_font = _load_font("Helvetica", 26)
    body_font = _load_font("Helvetica", 22)
    small_font = _load_font("Helvetica", 18)

    top_margin = 80
    side_margin = 90
    line_spacing = 34

    # ------------------------------------------------------------------
    # Top banner with simple illustration
    # ------------------------------------------------------------------
    banner_height = 220
    draw.rectangle(
        (0, 0, width, banner_height),
        fill=header_color,
    )

    # Draw a simple "cocktail glass" icon in the banner (centered)
    glass_center_x = width // 2
    glass_top_y = 40
    glass_bottom_y = banner_height - 40

    # Bowl of the glass
    bowl_width = 140
    bowl_height = 70
    bowl_top = glass_top_y + 30
    bowl_bottom = bowl_top + bowl_height
    draw.polygon(
        [
            (glass_center_x - bowl_width // 2, bowl_top),
            (glass_center_x + bowl_width // 2, bowl_top),
            (glass_center_x + bowl_width // 4, bowl_bottom),
            (glass_center_x - bowl_width // 4, bowl_bottom),
        ],
        fill=(255, 255, 255),
        outline=(180, 180, 180),
    )

    # Stem
    stem_top = bowl_bottom
    stem_bottom = glass_bottom_y - 25
    stem_width = 10
    draw.rectangle(
        (
            glass_center_x - stem_width // 2,
            stem_top,
            glass_center_x + stem_width // 2,
            stem_bottom,
        ),
        fill=(240, 240, 240),
        outline=(180, 180, 180),
    )

    # Base
    base_width = 80
    base_height = 8
    draw.rectangle(
        (
            glass_center_x - base_width // 2,
            stem_bottom,
            glass_center_x + base_width // 2,
            stem_bottom + base_height,
        ),
        fill=(240, 240, 240),
        outline=(180, 180, 180),
    )

    # Start content a bit below the banner
    y = banner_height + 40

    # ------------------------------------------------------------------
    # Title and base
    # ------------------------------------------------------------------
    name = display_dict.get("name", "Unnamed Recipe")
    base = display_dict.get("base", "")

    title_w, title_h = _text_size(draw, name, title_font)
    title_x = (width - title_w) // 2
    draw.text((title_x, y), name, font=title_font, fill=text_main)
    y += title_h + 8

    if base:
        base_text = f"(base: {base})"
        base_w, base_h = _text_size(draw, base_text, small_font)
        base_x = (width - base_w) // 2
        draw.text((base_x, y), base_text, font=small_font, fill=text_muted)
        y += base_h + 20

    # Divider under title
    draw.line(
        (side_margin, y, width - side_margin, y),
        fill=divider_color,
        width=1,
    )
    y += 36

    # ------------------------------------------------------------------
    # INGREDIENTS section
    # ------------------------------------------------------------------
    draw.text(
        (side_margin, y),
        "INGREDIENTS",
        font=section_font,
        fill=text_main,
    )
    y += line_spacing

    ingredients = display_dict.get("ingredients", {})

    # Column anchors: name, oz, ml
    name_x = side_margin
    oz_x = width // 2
    ml_x = oz_x + 130

    # Header row
    draw.text((name_x, y), "Item", font=small_font, fill=text_muted)
    draw.text((oz_x, y), "oz", font=small_font, fill=text_muted)
    draw.text((ml_x, y), "ml", font=small_font, fill=text_muted)
    y += 18

    draw.line(
        (side_margin, y, width - side_margin, y),
        fill=(225, 225, 225),
        width=1,
    )
    y += 18

    # Ingredient rows
    for ing_name, info in ingredients.items():
        oz = info.get("oz", "?")
        ml = info.get("ml", "?")

        draw.text((name_x, y), str(ing_name), font=body_font, fill=text_main)
        draw.text((oz_x, y), f"{oz}", font=body_font, fill=text_main)
        draw.text((ml_x, y), f"{ml}", font=body_font, fill=text_main)

        y += line_spacing

    y += 40

    # ------------------------------------------------------------------
    # INSTRUCTIONS section
    # ------------------------------------------------------------------
    draw.text(
        (side_margin, y),
        "INSTRUCTIONS",
        font=section_font,
        fill=text_main,
    )
    y += line_spacing

    instructions = display_dict.get("instructions", "No instructions provided.")
    wrapped_text = _wrap_text(instructions, width=75)

    for line in wrapped_text.split("\n"):
        draw.text((side_margin, y), line, font=body_font, fill=text_main)
        y += line_spacing

    # Subtle footer line
    footer_y = height - 60
    draw.line(
        (side_margin, footer_y, width - side_margin, footer_y),
        fill=(230, 230, 230),
        width=1,
    )

    # Ensure directory exists and save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, format="PNG")
