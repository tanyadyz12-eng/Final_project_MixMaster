"""Enhanced Tkinter-based GUI for MixMaster with friend opinions feature.

All interface text in English. Friend opinions based on real cocktail feedback.
"""

from __future__ import annotations

import random
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List

from src.database import CocktailDatabase
from src.cocktail import Cocktail
from src.cards import render_cocktail_card

BASE_DIR = Path(__file__).resolve().parent.parent
FAVORITES_PATH = BASE_DIR / "data" / "favorites.json"


class ModernStyle:
    """Modern color scheme and styling constants."""

    BG_PRIMARY = "#1a1a2e"
    BG_SECONDARY = "#16213e"
    BG_CARD = "#0f3460"
    ACCENT = "#e94560"
    ACCENT_HOVER = "#ff6b81"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a8b2d1"
    BORDER = "#2d3561"
    SUCCESS = "#00d9ff"

    FONT_TITLE = ("Segoe UI", 24, "bold")
    FONT_HEADING = ("Segoe UI", 16, "bold")
    FONT_BODY = ("Segoe UI", 11)
    FONT_SMALL = ("Segoe UI", 9)


class MixMasterEnhancedGUI:
    """Modern GUI for MixMaster with enhanced features."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("MixMaster Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg=ModernStyle.BG_PRIMARY)

        self.db = CocktailDatabase()
        self._all_cocktails = list(self.db.cocktails)
        self._all_names = [c.name for c in self._all_cocktails]
        self._current_cocktail: Optional[Cocktail] = None
        self._surprise_running = False
        self._favorites: List[str] = []
        self._load_favorites()


        self._setup_styles()
        self._create_ui()
        self._refresh_list(self._all_names)

    def _load_favorites(self) -> None:
        """Load favorites from local JSON file if present."""
        try:
            if FAVORITES_PATH.exists():
                with open(FAVORITES_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self._favorites = [name for name in data if isinstance(name, str)]
        except Exception as exc:
            print(f"[MixMaster] Warning: could not load favorites: {exc}")

    def _save_favorites(self) -> None:
        """Persist favorites to local JSON file."""
        try:
            FAVORITES_PATH.parent.mkdir(parents=True, exist_ok=True)
            unique = sorted(set(self._favorites))
            with open(FAVORITES_PATH, "w", encoding="utf-8") as f:
                json.dump(unique, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            print(f"[MixMaster] Warning: could not save favorites: {exc}")
    def _setup_styles(self) -> None:
        """Configure modern ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(
            "Accent.TButton",
            background=ModernStyle.ACCENT,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor='none',
            padding=10,
            font=ModernStyle.FONT_BODY
        )
        style.map("Accent.TButton",
                  background=[('active', ModernStyle.ACCENT_HOVER)])

        style.configure(
            "Secondary.TButton",
            background=ModernStyle.BG_CARD,
            foreground=ModernStyle.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor='none',
            padding=8,
            font=ModernStyle.FONT_BODY
        )

    def _create_ui(self) -> None:
        """Create the main UI layout."""
        main_container = tk.Frame(self.root, bg=ModernStyle.BG_PRIMARY)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_header(main_container)

        content = tk.Frame(main_container, bg=ModernStyle.BG_PRIMARY)
        content.pack(fill=tk.BOTH, expand=True, pady=20)

        self._create_left_panel(content)
        self._create_middle_panel(content)
        self._create_right_panel(content)

    def _create_header(self, parent: tk.Frame) -> None:
        """Create the header section."""
        header = tk.Frame(parent, bg=ModernStyle.BG_SECONDARY, height=100)
        header.pack(fill=tk.X, pady=(0, 10))
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text="🍹 MixMaster Pro",
            font=ModernStyle.FONT_TITLE,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        subtitle = tk.Label(
            header,
            text="Your Personal Bartending Assistant",
            font=ModernStyle.FONT_SMALL,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        )
        subtitle.pack(side=tk.LEFT, padx=(0, 20))

        stats_text = f"📚 {len(self._all_cocktails)} Recipes | 🥃 {len(self.db.list_bases())} Base Spirits"
        stats = tk.Label(
            header,
            text=stats_text,
            font=ModernStyle.FONT_SMALL,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        )
        stats.pack(side=tk.RIGHT, padx=20)

    def _create_left_panel(self, parent: tk.Frame) -> None:
        """Create the left panel with search and filters."""
        left = tk.Frame(parent, bg=ModernStyle.BG_SECONDARY, width=320)
        left.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left.pack_propagate(False)

        search_frame = tk.LabelFrame(
            left,
            text="🔍 Search",
            font=ModernStyle.FONT_HEADING,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            bd=0
        )
        search_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            search_frame,
            text="Name or Base Spirit:",
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        ).pack(anchor='w', pady=(5, 2))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=5
        )
        self.search_entry.pack(fill=tk.X, pady=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search_live)

        tk.Label(
            search_frame,
            text="🥃 Have These Ingredients:",
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        ).pack(anchor='w', pady=(10, 2))

        self.ingredient_text = tk.Text(
            search_frame,
            height=3,
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            insertbackground=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=5,
            wrap=tk.WORD
        )
        self.ingredient_text.pack(fill=tk.X, pady=(0, 5))

        tk.Label(
            search_frame,
            text="(comma-separated, e.g., gin, lime, sugar)",
            font=ModernStyle.FONT_SMALL,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        ).pack(anchor='w')

        ttk.Button(
            search_frame,
            text="🔎 Find Recipes",
            style="Accent.TButton",
            command=self._search_by_ingredients
        ).pack(fill=tk.X, pady=(10, 5))

        filter_frame = tk.LabelFrame(
            left,
            text="🎯 Quick Filters",
            font=ModernStyle.FONT_HEADING,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY,
            bd=0
        )
        filter_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            filter_frame,
            text="Base Spirit:",
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        ).pack(anchor='w', pady=(5, 2))

        self.base_var = tk.StringVar(value="all")
        bases = ["all"] + self.db.list_bases()

        base_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.base_var,
            values=bases,
            state="readonly",
            font=ModernStyle.FONT_BODY
        )
        base_combo.pack(fill=tk.X, pady=(0, 10))
        base_combo.bind("<<ComboboxSelected>>", self._on_filter_change)

        tk.Label(
            filter_frame,
            text="Flavor Profile:",
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        ).pack(anchor='w', pady=(5, 2))

        self.flavor_var = tk.StringVar(value="all")
        flavors = ["all"] + self.db.list_flavor_tags()

        flavor_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.flavor_var,
            values=flavors,
            state="readonly",
            font=ModernStyle.FONT_BODY
        )
        flavor_combo.pack(fill=tk.X, pady=(0, 10))
        flavor_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        self.show_favorites_only = tk.BooleanVar(value=False)
        fav_check = ttk.Checkbutton(
            filter_frame,
            text="⭐ Show favorites only",
            variable=self.show_favorites_only,
            command=self._apply_filters
        )
        fav_check.pack(anchor="w", pady=(5, 0))


        ttk.Button(
            filter_frame,
            text="🔄 Reset Filters",
            style="Secondary.TButton",
            command=self._reset_filters
        ).pack(fill=tk.X, pady=(5, 0))

        action_frame = tk.Frame(left, bg=ModernStyle.BG_SECONDARY)
        action_frame.pack(fill=tk.X, padx=15, pady=15, side=tk.BOTTOM)

        self.surprise_btn = ttk.Button(
            action_frame,
            text="🎰 Surprise Me!",
            style="Accent.TButton",
            command=self._on_surprise_me
        )
        self.surprise_btn.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(
            action_frame,
            text="❓ Help",
            style="Secondary.TButton",
            command=self._show_help
        ).pack(fill=tk.X)

    def _create_middle_panel(self, parent: tk.Frame) -> None:
        """Create the middle panel with recipe list."""
        middle = tk.Frame(parent, bg=ModernStyle.BG_SECONDARY, width=400)
        middle.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        middle.pack_propagate(False)

        header = tk.Frame(middle, bg=ModernStyle.BG_SECONDARY)
        header.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            header,
            text="📋 Recipes",
            font=ModernStyle.FONT_HEADING,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(side=tk.LEFT)

        self.result_count_label = tk.Label(
            header,
            text=f"({len(self._all_names)} total)",
            font=ModernStyle.FONT_SMALL,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY
        )
        self.result_count_label.pack(side=tk.LEFT, padx=(10, 0))

        list_frame = tk.Frame(middle, bg=ModernStyle.BG_SECONDARY)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(list_frame, bg=ModernStyle.BG_CARD)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            selectbackground=ModernStyle.ACCENT,
            selectforeground=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            activestyle='none'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _create_right_panel(self, parent: tk.Frame) -> None:
        """Create the right panel with recipe details."""
        right = tk.Frame(parent, bg=ModernStyle.BG_SECONDARY)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        header = tk.Frame(right, bg=ModernStyle.BG_SECONDARY)
        header.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            header,
            text="📄 Recipe Details",
            font=ModernStyle.FONT_HEADING,
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(side=tk.LEFT)

        action_frame = tk.Frame(header, bg=ModernStyle.BG_SECONDARY)
        action_frame.pack(side=tk.RIGHT, padx=10)

        top_row = tk.Frame(action_frame, bg=ModernStyle.BG_SECONDARY)
        top_row.pack(fill=tk.X, pady=(0, 5))

        self.favorite_btn = ttk.Button(
            top_row,
            text="⭐ Favorite",
            style="Secondary.TButton",
            command=self._toggle_favorite,
            width=13
        )
        self.favorite_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.export_btn = ttk.Button(
            top_row,
            text="💾 Export",
            style="Accent.TButton",
            command=self._export_card,
            width=13
        )
        self.export_btn.pack(side=tk.LEFT)

        self.friend_btn = ttk.Button(
            action_frame,
            text="💬 Ask Friends",
            style="Accent.TButton",
            command=self._show_friend_opinions,
            width=27
        )
        self.friend_btn.pack(fill=tk.X)

        text_frame = tk.Frame(right, bg=ModernStyle.BG_SECONDARY)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.detail_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=ModernStyle.FONT_BODY,
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=15,
            yscrollcommand=scrollbar.set,
            spacing1=5,
            spacing3=5
        )
        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.detail_text.yview)

        self.detail_text.tag_configure("title", font=("Segoe UI", 20, "bold"), foreground=ModernStyle.ACCENT)
        self.detail_text.tag_configure("heading", font=("Segoe UI", 14, "bold"), foreground=ModernStyle.SUCCESS,
                                       spacing1=10)
        self.detail_text.tag_configure("subtext", font=("Segoe UI", 10), foreground=ModernStyle.TEXT_SECONDARY)

        self._show_welcome()

    def _show_welcome(self) -> None:
        """Show welcome message."""
        welcome = """Welcome to MixMaster Pro! 🍹

Your personal bartending assistant with enhanced features.

🔍 SEARCH OPTIONS:
- Type a cocktail name or base spirit in the search box
- Enter ingredients you have to find matching recipes
- Use filters to browse by base spirit or flavor profile

📋 BROWSE & SELECT:
- Click any recipe in the middle panel to view details
- Use filters to narrow down your options

🎰 FEELING LUCKY?
- Click "Surprise Me!" for a random cocktail recommendation
- If you've entered ingredients, the surprise will prefer matching recipes

💬 FRIEND OPINIONS:
- Click "Ask Friends" to hear from Liz and Yizhe!
- Liz gives health & safety tips
- Yizhe shares taste insights

💾 EXPORT & SAVE:
- Export any recipe as a beautiful PNG card
- Mark favorites with the ⭐ button

🎯 PRO TIPS:
- Combine search with filters for better results
- Enter multiple ingredients separated by commas
- Keep the app open while mixing!

Ready to shake things up? Start exploring!"""

        self.detail_text.insert("1.0", welcome)

    def _refresh_list(self, names: List[str]) -> None:
        """Refresh the listbox."""
        self.listbox.delete(0, tk.END)
        for name in names:
            prefix = "⭐ " if name in self._favorites else ""
            self.listbox.insert(tk.END, f"{prefix}{name}")

        self.result_count_label.config(text=f"({len(names)} found)")

    def _on_search_live(self, event=None) -> None:
        """Live search."""
        text = self.search_var.get().strip().lower()

        if not text:
            self._apply_filters()
            return

        filtered = [
            c.name for c in self._all_cocktails
            if text in c.name.lower() or text in c.base.lower()
        ]

        self._refresh_list(filtered)

    def _search_by_ingredients(self) -> None:
        """Search by ingredients."""
        text = self.ingredient_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning(
                "No Ingredients",
                "Please enter at least one ingredient to search."
            )
            return

        ingredients = [i.strip().lower() for i in text.split(",") if i.strip()]

        if not ingredients:
            return

        results = self.db.search_by_ingredients(
            ingredients,
            max_missing=2,
            min_matched=1
        )

        if not results:
            messagebox.showinfo(
                "No Matches",
                f"No recipes found with ingredients: {', '.join(ingredients)}"
            )
            return

        names = [c.name for c, matched, missing in results]
        self._refresh_list(names)

        summary = f"Found {len(results)} recipes!\n\nSearching with: {', '.join(ingredients)}\n\nTop matches:\n"
        for i, (c, matched, missing) in enumerate(results[:5], 1):
            summary += f"{i}. {c.name} (✓{matched} ingredients, ✗{missing} missing)\n"

        messagebox.showinfo("Search Results", summary)

    def _on_filter_change(self, event=None) -> None:
        """Apply filters."""
        self._apply_filters()

    def _apply_filters(self) -> None:
        """Apply current filters."""
        base = self.base_var.get()
        flavor = self.flavor_var.get()
        search_text = self.search_var.get().strip().lower()
        show_favs_only = getattr(self, "show_favorites_only", None)

        filtered = self._all_cocktails

        if base != "all":
            filtered = [c for c in filtered if c.base == base]

        if flavor != "all":
            filtered = [
                c for c in filtered
                if any(flavor == f.lower() for f in c.flavors)
            ]

        if search_text:
            filtered = [
                c for c in filtered
                if search_text in c.name.lower() or search_text in c.base.lower()
            ]

        if show_favs_only is not None and show_favs_only.get():
            filtered = [c for c in filtered if c.name in self._favorites]

        names = [c.name for c in filtered]
        self._refresh_list(names)

    def _reset_filters(self) -> None:
        """Reset all filters."""
        self.base_var.set("all")
        self.flavor_var.set("all")
        self.search_var.set("")
        self.ingredient_text.delete("1.0", tk.END)

        if hasattr(self, "show_favorites_only"):
            self.show_favorites_only.set(False)

        self._refresh_list(self._all_names)

    def _get_cocktail_by_name(self, name: str) -> Optional[Cocktail]:
        """Get cocktail by name."""
        clean_name = name.replace("⭐ ", "")
        return self.db.find_by_name(clean_name)

    def _on_select(self, event=None) -> None:
        """Handle selection."""
        if not self.listbox.curselection():
            return

        index = self.listbox.curselection()[0]
        name = self.listbox.get(index)
        cocktail = self._get_cocktail_by_name(name)

        if cocktail:
            self._current_cocktail = cocktail
            self._show_cocktail(cocktail)

    def _show_cocktail(self, cocktail: Cocktail) -> None:
        """Display cocktail details."""
        self.detail_text.delete("1.0", tk.END)

        display = cocktail.to_display()
        name = display.get("name", "Unnamed Recipe")
        base = display.get("base", "")
        difficulty = display.get("difficulty", "unknown")
        flavors = display.get("flavors") or []
        ingredients = display.get("ingredients", {})
        instructions = display.get("instructions", "")

        self.detail_text.insert(tk.END, f"{name}\n", "title")

        meta = f"Base: {base.title()} | Difficulty: {difficulty.title()}"
        if flavors:
            meta += f" | Flavors: {', '.join(f.title() for f in flavors)}"
        self.detail_text.insert(tk.END, f"{meta}\n\n", "subtext")

        self.detail_text.insert(tk.END, "🥃 INGREDIENTS\n", "heading")
        for ing_name, info in ingredients.items():
            oz = info.get("oz", "?")
            ml = info.get("ml", "?")
            self.detail_text.insert(
                tk.END,
                f"  • {ing_name}: {oz} oz (~{ml} ml)\n"
            )

        self.detail_text.insert(tk.END, "\n📝 INSTRUCTIONS\n", "heading")
        self.detail_text.insert(tk.END, f"{instructions}\n")

        is_fav = name in self._favorites
        self.favorite_btn.config(text="⭐ Favorited" if is_fav else "☆ Favorite")

    def _toggle_favorite(self) -> None:
        """Toggle favorite."""
        if not self._current_cocktail:
            messagebox.showwarning("No Selection", "Please select a recipe first.")
            return

        name = self._current_cocktail.name

        if name in self._favorites:
            self._favorites.remove(name)
            self.favorite_btn.config(text="☆ Favorite")
        else:
            self._favorites.append(name)
            self.favorite_btn.config(text="⭐ Favorited")

        # Persist favorites to disk
        self._save_favorites()

        # Refresh list so that ⭐ markers update immediately
        try:
            self._apply_filters()
        except Exception:
            self._refresh_list(self._all_names)

    def _export_card(self) -> None:
        """Export as PNG."""
        if not self._current_cocktail:
            messagebox.showwarning("No Selection", "Please select a recipe first.")
            return

        filename = self._current_cocktail.name.replace(" ", "_").replace("/", "-")
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile=f"{filename}_card.png"
        )

        if not filepath:
            return

        try:
            display = self._current_cocktail.to_display()
            render_cocktail_card(display, filepath)
            messagebox.showinfo("Success", f"Recipe card exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export card:\n{str(e)}")

    def _create_character_avatar(self, color: str, parent: tk.Widget) -> tk.Canvas:
        """Create a simple female-style avatar with hair in the given parent."""
        canvas = tk.Canvas(
            parent,
            width=80,
            height=80,
            bg=ModernStyle.BG_SECONDARY,
            highlightthickness=0,
        )

        skin = "#ffd7c2"
        if color == "blue":
            hair = "#4a90e2"
            shirt = "#5ba3f5"
        else:
            hair = "#ff8b3d"
            shirt = "#ffb36b"


        canvas.create_oval(22, 18, 58, 54, fill=skin, outline=skin)


        canvas.create_arc(18, 10, 62, 46, start=0, extent=180,
                          fill=hair, outline=hair)
        canvas.create_rectangle(20, 30, 26, 58, fill=hair,
                                outline=hair)
        canvas.create_rectangle(54, 30, 60, 58, fill=hair,
                                outline=hair)


        canvas.create_oval(30, 30, 34, 34, fill="#000000")
        canvas.create_oval(46, 30, 50, 34, fill="#000000")
        canvas.create_arc(32, 36, 48, 46, start=0, extent=-180,
                          style=tk.ARC, outline="#000000", width=2)


        canvas.create_rectangle(30, 54, 50, 76,
                                fill=shirt, outline=shirt, width=1)

        return canvas

    def _generate_health_tips(self, cocktail: Cocktail) -> str:
        """Generate health tips."""
        display = cocktail.to_display()
        ingredients = display.get("ingredients", {})

        total_oz = 0
        for info in ingredients.values():
            try:
                total_oz += float(info.get("oz", "0"))
            except:
                pass

        tips = [f"Hey! About this {cocktail.name}, here are some things to keep in mind:"]

        if total_oz > 3:
            tips.append("\n⚠️ HIGH ALCOHOL CONTENT: This is a strong drink. Limit to 1-2 drinks per occasion.")
        elif total_oz > 2:
            tips.append("\n🥃 MODERATE STRENGTH: Contains moderate alcohol. Stick to 2-3 drinks max.")
        else:
            tips.append("\n✨ LIGHTER OPTION: Relatively mild, but moderation is still key!")

        safety = [
            "\n🚗 NEVER DRINK AND DRIVE: Always arrange safe transportation.",
            "\n💊 MEDICATION ALERT: Alcohol can interact with medications.",
            "\n🍕 EAT FIRST: Don't drink on an empty stomach.",
            "\n💧 STAY HYDRATED: Alternate with water to prevent hangovers."
        ]
        tips.append(random.choice(safety))

        if any("sugar" in ing.lower() for ing in ingredients.keys()):
            tips.append("\n🍬 SUGAR CONTENT: Be mindful if watching sugar intake.")

        tips.append("\n\n🚷 NOT FOR: Pregnant women, people under 21, or anyone driving.")
        tips.append("\n\nStay safe, drink responsibly, and enjoy! 💙")

        return "".join(tips)

    def _generate_taste_insights(self, cocktail: Cocktail) -> str:
        """Generate taste insights."""
        display = cocktail.to_display()
        flavors = display.get("flavors") or []
        base = display.get("base", "").lower()
        ingredients = display.get("ingredients", {})

        insights = [f"Ooh, {cocktail.name}! Let me tell you about it:"]

        base_profiles = {
            "vodka": "\n🥃 VODKA BASE: Clean and neutral, lets other flavors shine.",
            "gin": "\n🌿 GIN BASE: Botanical notes with juniper. Complex and aromatic.",
            "rum": "\n🍯 RUM BASE: Sweet molasses with Caribbean warmth.",
            "tequila": "\n🌵 TEQUILA BASE: Earthy agave with a peppery kick.",
            "whiskey": "\n🥃 WHISKEY BASE: Rich oak and caramel notes.",
            "bourbon": "\n🍂 BOURBON BASE: Vanilla and toasted oak flavors.",
            "mezcal": "\n🔥 MEZCAL BASE: Smoky and bold!"
        }

        if base in base_profiles:
            insights.append(base_profiles[base])

        if flavors:
            insights.append("\n\n✨ FLAVOR EXPERIENCE:")
            flavor_map = {
                "sweet": "Sweet and balanced",
                "sour": "Tart and refreshing",
                "bitter": "Pleasant bitterness",
                "spicy": "Has a kick!",
                "fruity": "Fruit-forward and vibrant",
                "herbal": "Herbal and botanical",
                "citrus": "Bright citrus zing"
            }
            for f in flavors[:3]:
                insights.append(f"\n  • {flavor_map.get(f.lower(), f.title())}")

        special = []
        for ing in ingredients.keys():
            if "lime" in ing.lower() or "lemon" in ing.lower():
                special.append("Citrus brightens everything")
            elif "mint" in ing.lower():
                special.append("Fresh mint adds coolness")

        if special:
            insights.append(f"\n\n🌟 SPECIAL NOTE: {special[0]}!")

        insights.append(random.choice([
            "\n\nOVERALL: Highly recommend!",
            "\n\nMY VERDICT: Solid choice!",
            "\n\nHONEST OPINION: Really tasty!"
        ]))

        insights.append(random.choice([
            "\n\nPERFECT FOR: Party vibes! 🎉",
            "\n\nBEST ENJOYED: Summer afternoons ☀️",
            "\n\nGREAT WHEN: You want to relax 🌙"
        ]))

        return "".join(insights)

    def _show_friend_opinions(self) -> None:
        """Show friend opinions."""
        if not self._current_cocktail:
            messagebox.showwarning("No Selection", "Pick a recipe first!")
            return

        opinion_window = tk.Toplevel(self.root)
        opinion_window.title(f"Friend Opinions: {self._current_cocktail.name}")
        opinion_window.geometry("1050x700")
        opinion_window.configure(bg=ModernStyle.BG_PRIMARY)
        opinion_window.transient(self.root)
        opinion_window.grab_set()

        opinion_window.update_idletasks()
        x = (opinion_window.winfo_screenwidth() // 2) - (opinion_window.winfo_width() // 2)
        y = (opinion_window.winfo_screenheight() // 2) - (opinion_window.winfo_height() // 2)
        opinion_window.geometry(f"+{x}+{y}")

        title_bar = tk.Frame(opinion_window, bg=ModernStyle.BG_SECONDARY, height=90)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text=f"💬 Friend Opinions on {self._current_cocktail.name}",
            font=("Segoe UI", 18, "bold"),
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_PRIMARY
        ).pack(pady=30)

        content_area = tk.Frame(opinion_window, bg=ModernStyle.BG_PRIMARY)
        content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        content_area.columnconfigure(0, weight=1)
        content_area.columnconfigure(1, weight=1)
        content_area.rowconfigure(0, weight=1)

        zhihan_panel = tk.Frame(
            content_area,
            bg=ModernStyle.BG_SECONDARY,
            relief=tk.RAISED,
            bd=2,
        )
        zhihan_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        zhihan_header = tk.Frame(zhihan_panel, bg=ModernStyle.BG_SECONDARY, height=170)
        zhihan_header.pack(fill=tk.X)
        zhihan_header.pack_propagate(False)

        zhihan_avatar_frame = tk.Frame(zhihan_header, bg=ModernStyle.BG_SECONDARY)
        zhihan_avatar_frame.pack(pady=(12, 5))

        zhihan_avatar = self._create_character_avatar("blue", zhihan_avatar_frame)
        zhihan_avatar.pack()

        tk.Label(
            zhihan_header,
            text="Zhihan 💙",
            font=("Segoe UI", 16, "bold"),
            bg=ModernStyle.BG_SECONDARY,
            fg="#4a90e2",
        ).pack(pady=(3, 1))
        tk.Label(
            zhihan_header,
            text="Health & Safety Tips",
            font=("Segoe UI", 10),
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY,
        ).pack()

        zhihan_text_container = tk.Frame(zhihan_panel, bg=ModernStyle.BG_SECONDARY)
        zhihan_text_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(5, 15))

        zhihan_scroll = tk.Scrollbar(zhihan_text_container)
        zhihan_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        zhihan_text = tk.Text(
            zhihan_text_container,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=12,
            yscrollcommand=zhihan_scroll.set,
            spacing1=4,
            spacing2=2,
            spacing3=4,
        )
        zhihan_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        zhihan_scroll.config(command=zhihan_text.yview)

        health_tips = self._generate_health_tips(self._current_cocktail)
        zhihan_text.insert("1.0", health_tips)
        zhihan_text.config(state=tk.DISABLED)

        yizhe_panel = tk.Frame(
            content_area,
            bg=ModernStyle.BG_SECONDARY,
            relief=tk.RAISED,
            bd=2,
        )
        yizhe_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)

        yizhe_header = tk.Frame(yizhe_panel, bg=ModernStyle.BG_SECONDARY, height=170)
        yizhe_header.pack(fill=tk.X)
        yizhe_header.pack_propagate(False)

        yizhe_avatar_frame = tk.Frame(yizhe_header, bg=ModernStyle.BG_SECONDARY)
        yizhe_avatar_frame.pack(pady=(12, 5))

        yizhe_avatar = self._create_character_avatar("orange", yizhe_avatar_frame)
        yizhe_avatar.pack()

        tk.Label(
            yizhe_header,
            text="Yizhe 🧡",
            font=("Segoe UI", 16, "bold"),
            bg=ModernStyle.BG_SECONDARY,
            fg="#ff9f43",
        ).pack(pady=(3, 1))
        tk.Label(
            yizhe_header,
            text="Taste & Flavor Insights",
            font=("Segoe UI", 10),
            bg=ModernStyle.BG_SECONDARY,
            fg=ModernStyle.TEXT_SECONDARY,
        ).pack()

        yizhe_text_container = tk.Frame(yizhe_panel, bg=ModernStyle.BG_SECONDARY)
        yizhe_text_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(5, 15))

        yizhe_scroll = tk.Scrollbar(yizhe_text_container)
        yizhe_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        yizhe_text = tk.Text(
            yizhe_text_container,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=ModernStyle.BG_CARD,
            fg=ModernStyle.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=12,
            yscrollcommand=yizhe_scroll.set,
            spacing1=4,
            spacing2=2,
            spacing3=4,
        )
        yizhe_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yizhe_scroll.config(command=yizhe_text.yview)

        taste_insights = self._generate_taste_insights(self._current_cocktail)
        yizhe_text.insert("1.0", taste_insights)
        yizhe_text.config(state=tk.DISABLED)

        button_frame = tk.Frame(opinion_window, bg=ModernStyle.BG_PRIMARY)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        ttk.Button(
            button_frame,
            text="Got it! 👍",
            style="Accent.TButton",
            command=opinion_window.destroy,
            width=22,
        ).pack()

    def _on_surprise_me(self) -> None:
        """Surprise me."""
        if self._surprise_running:
            return

        if not self._all_cocktails:
            return

        current_items = [self.listbox.get(i) for i in range(self.listbox.size())]
        candidates = [self._get_cocktail_by_name(name) for name in current_items]
        candidates = [c for c in candidates if c is not None]

        if not candidates:
            candidates = self._all_cocktails

        slot = tk.Toplevel(self.root)
        slot.title("🎰 Surprise Me!")
        slot.geometry("450x280")
        slot.configure(bg=ModernStyle.BG_PRIMARY)
        slot.transient(self.root)
        slot.grab_set()

        slot.update_idletasks()
        x = (slot.winfo_screenwidth() // 2) - (slot.winfo_width() // 2)
        y = (slot.winfo_screenheight() // 2) - (slot.winfo_height() // 2)
        slot.geometry(f"+{x}+{y}")

        msg_label = tk.Label(slot, text="🎲 Shaking the mixer...", font=("Segoe UI", 14),
                             bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.TEXT_PRIMARY)
        msg_label.pack(pady=(35, 12))

        name_label = tk.Label(slot, text="", font=("Segoe UI", 20, "bold"),
                              bg=ModernStyle.BG_PRIMARY, fg=ModernStyle.ACCENT, wraplength=400)
        name_label.pack(pady=25)

        close_btn = ttk.Button(slot, text="Close", style="Secondary.TButton", command=slot.destroy)
        close_btn.pack(pady=25)

        self._surprise_running = True
        self.surprise_btn.config(state=tk.DISABLED)

        def spin(count: int = 0) -> None:
            if count < 30:
                name_label.config(text=random.choice(candidates).name)
                slot.after(60, spin, count + 1)
            else:
                winner = random.choice(candidates)
                name_label.config(text=winner.name)
                msg_label.config(text="🍹 Your surprise cocktail:")
                self._current_cocktail = winner
                self._show_cocktail(winner)
                self._surprise_running = False
                self.surprise_btn.config(state=tk.NORMAL)

        spin()

    def _show_help(self) -> None:
        """Show help."""
        help_text = """🍹 MixMaster Pro - Help Guide
        SEARCH & FILTER:

        Name/Base Search: Type to filter in real-time
        Ingredient Search: Enter what you have (comma-separated)
        Quick Filters: Filter by base spirit or flavor

        BROWSE RECIPES:

        Click any recipe to view details
        Scroll through the list to explore

        SPECIAL FEATURES:

        🎰 Surprise Me: Random cocktail
        ⭐ Favorites: Mark recipes you love
        💾 Export: Save as PNG card
        💬 Ask Friends: Get tips from Liz and Yizhe!

        Enjoy mixing! 🍸"""
        messagebox.showinfo("Help - MixMaster Pro", help_text)

def run_gui() -> None:
    """Launch the GUI."""
    root = tk.Tk()
    app = MixMasterEnhancedGUI(root)
    root.mainloop()