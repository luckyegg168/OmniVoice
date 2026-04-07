"""Audio player component."""

from __future__ import annotations

from nicegui import ui


def audio_player(src: str = "", visible: bool = True) -> ui.audio:
    """Create an audio player element."""
    player = ui.audio(src).classes("w-full")
    player.visible = visible
    return player
