"""Theme definitions and validation for Markus."""

from __future__ import annotations

from typing import Literal

from markusmd.errors import MarkusError

ColorMode = Literal["both", "light", "dark"]

# Every bundled theme and the color modes it supports. A "both" theme carries a
# light and a dark palette and follows the reader's prefers-color-scheme setting
# (data-color-scheme="light" or "dark" on the root element forces one); the
# others always render in their single mode. Ordered as a picker lists them:
# adaptive families first, Solarized leading.
THEME_MODES: dict[str, ColorMode] = {
    "solarized": "both",
    "catppuccin": "both",
    "everforest": "both",
    "flexoki": "both",
    "github": "both",
    "gruvbox": "both",
    "kanagawa": "both",
    "one": "both",
    "rose-pine": "both",
    "tokyo-night": "both",
    "catppuccin-latte": "light",
    "flexoki-light": "light",
    "lupine": "light",
    "white": "light",
    "ethereal": "dark",
    "hackerman": "dark",
    "last-horizon": "dark",
    "lumon": "dark",
    "matte-black": "dark",
    "miasma": "dark",
    "nord": "dark",
    "osaka-jade": "dark",
    "retro-82": "dark",
    "ristretto": "dark",
    "solitude": "dark",
    "vantablack": "dark",
}

AVAILABLE_THEMES = {"default", *THEME_MODES}

ADAPTIVE_THEMES = {name for name, mode in THEME_MODES.items() if mode == "both"}


def validate_theme(name: str | None) -> str | None:
    """Validate that the theme name is recognized, returning canonical name or None."""
    if not name:
        return None
    normalized = str(name).strip().lower()
    if normalized not in AVAILABLE_THEMES:
        available = ", ".join(sorted(AVAILABLE_THEMES))
        raise MarkusError(f"Unknown theme '{name}'. Available themes: {available}")
    return normalized
