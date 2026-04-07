"""Text statistics display component."""

from __future__ import annotations

from nicegui import ui

from app.core.audio_utils import count_text_stats, estimate_speech_duration
from app.i18n.translations import t


def text_stats_display(text: str = "", speed: float = 1.0, language: str = "zh-TW") -> ui.row:
    """Display text statistics: chars, words, estimated duration."""
    stats = count_text_stats(text)
    est = estimate_speech_duration(text, speed, language)

    with ui.row().classes("gap-4 text-sm text-gray-400") as row:
        ui.label(f"📝 {t('char_count')}: {stats['chars']}")
        ui.label(f"📖 {t('word_count')}: {stats['words']}")
        ui.label(f"⏱️ {t('est_duration')}: {est:.1f}s")
    return row
