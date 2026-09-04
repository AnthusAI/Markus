"""Theme definitions and validation for Markus."""

from __future__ import annotations

from markusmd.errors import MarkusError

AVAILABLE_THEMES = {
    "default",
    "hackerman",
}


def validate_theme(name: str | None) -> str | None:
    """Validate that the theme name is recognized, returning canonical name or None."""
    if not name:
        return None
    normalized = str(name).strip().lower()
    if normalized not in AVAILABLE_THEMES:
        available = ", ".join(sorted(AVAILABLE_THEMES))
        raise MarkusError(f"Unknown theme '{name}'. Available themes: {available}")
    return normalized
