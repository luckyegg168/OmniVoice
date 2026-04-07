"""OmniVoice TTS App — main entry point."""

from __future__ import annotations

from pathlib import Path

from nicegui import app, ui

from app.config import APP_HOST, APP_PORT, APP_VERSION, OUTPUT_DIR
from app.core.edge_tts_engine import EdgeTTSEngine
from app.core.gtts_engine import GTTSEngine
from app.core.omnivoice_engine import OmniVoiceEngine
from app.i18n.translations import get_locale, set_locale, t
from app.pages.about_page import about_page
from app.pages.batch_page import batch_page
from app.pages.history_page import history_page
from app.pages.settings_page import settings_page
from app.pages.ssml_page import ssml_page
from app.pages.tts_page import tts_page
from app.pages.voice_clone_page import voice_clone_page

# ── Initialize engines ──
ENGINES: dict = {}


def _init_engines() -> dict:
    engines: dict = {}
    edge = EdgeTTSEngine()
    if edge.is_available():
        engines[edge.engine_id()] = edge
    gtts = GTTSEngine()
    if gtts.is_available():
        engines[gtts.engine_id()] = gtts
    omni = OmniVoiceEngine()
    if omni.is_available():
        engines[omni.engine_id()] = omni
    return engines


# ── Serve static output files ──
app.add_static_files("/output", str(OUTPUT_DIR))


# ── Layout builder ──
def _build_layout(page_func, engines: dict) -> None:
    """Build the shared app layout with left drawer navigation."""
    dark = ui.dark_mode(True)

    with ui.header().classes("bg-gray-900 text-white px-6 py-2"), ui.row().classes("w-full items-center"):
            ui.button(icon="menu", on_click=lambda: drawer.toggle()).props(
                "flat dense round color=white"
            )
            ui.label(f"🎙️ OmniVoice v{APP_VERSION}").classes("text-lg font-bold ml-2")
            ui.space()

            # Locale selector
            ui.select(
                options={"zh-TW": "繁中", "en": "EN", "ja": "日本語"},
                value=get_locale(),
                on_change=lambda e: _change_locale(e.value),
            ).classes("w-20").props("dense borderless dark")

            # Theme toggle
            ui.switch(
                "🌙",
                value=True,
                on_change=lambda e: dark.set_value(e.value),
            ).classes("ml-2")

    with ui.left_drawer(value=True).classes("bg-gray-800 text-white") as drawer:
        ui.label("OmniVoice").classes("text-xl font-bold p-4")
        ui.separator()

        nav_items = [
            ("🎙️", t("nav_tts"), "/"),
            ("🎤", t("nav_clone"), "/clone"),
            ("📦", t("nav_batch"), "/batch"),
            ("📝", t("nav_ssml"), "/ssml"),
            ("📜", t("nav_history"), "/history"),
            ("⚙️", t("nav_settings"), "/settings"),
            ("ℹ️", t("nav_about"), "/about"),
        ]
        for icon, label, path in nav_items:
            ui.button(
                f"{icon} {label}",
                on_click=lambda _, p=path: ui.navigate.to(p),
            ).classes("w-full justify-start text-white").props("flat")

    with ui.column().classes("w-full max-w-5xl mx-auto p-6"):
        page_func(engines)


def _change_locale(locale: str) -> None:
    set_locale(locale)
    ui.navigate.reload()


# ── Page routes ──
@ui.page("/")
def page_tts():
    engines = _init_engines()
    _build_layout(tts_page, engines)


@ui.page("/clone")
def page_clone():
    engines = _init_engines()
    _build_layout(voice_clone_page, engines)


@ui.page("/batch")
def page_batch():
    engines = _init_engines()
    _build_layout(batch_page, engines)


@ui.page("/ssml")
def page_ssml():
    engines = _init_engines()
    _build_layout(ssml_page, engines)


@ui.page("/history")
def page_history():
    engines = _init_engines()
    _build_layout(history_page, engines)


@ui.page("/settings")
def page_settings():
    engines = _init_engines()
    _build_layout(settings_page, engines)


@ui.page("/about")
def page_about():
    engines = _init_engines()
    _build_layout(about_page, engines)


def main() -> None:
    """Entry point for the OmniVoice TTS application."""
    # Ensure output directory exists
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    ui.run(
        title="OmniVoice TTS",
        host=APP_HOST,
        port=APP_PORT,
        reload=False,
        show=True,
        favicon="🎙️",
    )


if __name__ == "__main__":
    main()
