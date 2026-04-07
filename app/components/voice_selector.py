"""Voice selector component."""

from __future__ import annotations

from nicegui import ui

from app.i18n.translations import t
from app.models.tts_request import VoiceInfo


def voice_selector(
    voices: list[VoiceInfo],
    value: str = "",
    on_change=None,
) -> ui.select:
    """Create a voice selection dropdown."""
    options = {v.id: f"{v.name} ({v.language})" for v in voices}
    select = ui.select(
        options=options,
        value=value or (voices[0].id if voices else ""),
        label=t("voice_label"),
        on_change=on_change,
    ).classes("w-full")
    return select
