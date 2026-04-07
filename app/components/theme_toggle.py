"""Theme toggle component."""

from __future__ import annotations

from nicegui import ui

from app.i18n.translations import t


def theme_toggle(dark_mode: ui.dark_mode) -> ui.switch:
    """Create a dark/light theme toggle switch."""
    switch = ui.switch(
        t("theme_dark"),
        value=True,
        on_change=lambda e: dark_mode.set_value(e.value),
    ).classes("ml-2")
    return switch
