"""About page — app info, engine status, and usage guide."""

from __future__ import annotations

from nicegui import ui

from app.config import APP_VERSION
from app.i18n.translations import t


def about_page(engines: dict) -> None:
    """Render the about page."""

    ui.label(t("about_title")).classes("text-2xl font-bold mb-6")

    # ── App Info ──
    with ui.card().classes("w-full p-6 mb-4"):
        ui.label("OmniVoice TTS App").classes("text-xl font-bold")
        ui.label(f"📌 {t('version')}: {APP_VERSION}")
        ui.label(f"📜 {t('license')}: Apache-2.0")
        ui.link(
            "GitHub: k2-fsa/OmniVoice",
            "https://github.com/k2-fsa/OmniVoice",
            new_tab=True,
        )

    # ── Engine Status ──
    with ui.card().classes("w-full p-6 mb-4"):
        ui.label(f"🔧 {t('engine_status')}").classes("text-lg font-semibold mb-2")

        # Install dialog (shared across all unavailable engines)
        with ui.dialog() as install_dialog, ui.card().classes("p-6"):
            ui.label(f"📦 {t('omnivoice_install_btn')}").classes("text-lg font-bold mb-2")
            ui.label(t("install_cmd_hint")).classes("mb-1")
            ui.code("pip install omnivoice torch torchaudio", language="bash").classes("my-2")
            with ui.row().classes("gap-2"):
                ui.button(
                    t("copy_btn"),
                    on_click=lambda: ui.run_javascript(
                        "navigator.clipboard.writeText('pip install omnivoice torch torchaudio')"
                    ),
                ).props("flat color=primary")
                ui.button(t("close"), on_click=install_dialog.close).props("flat")

        for _eid, eng in engines.items():
            available = eng.is_available()
            icon = "✅" if available else "❌"
            with ui.row().classes("items-center gap-2"):
                ui.label(f"{icon} {eng.name()}")
                ui.badge(
                    t("available") if available else t("unavailable"),
                    color="green" if available else "red",
                )
                if not available:
                    ui.button(
                        f"📦 {t('omnivoice_install_btn')}",
                        on_click=install_dialog.open,
                    ).props("flat dense color=primary")

    # ── Feature List ──
    with ui.card().classes("w-full p-6 mb-4"):
        ui.label(f"🌟 {t('features')}").classes("text-lg font-semibold mb-2")
        features = [
            t("feature_multi_engine"),
            t("feature_voice_clone"),
            t("feature_batch"),
            t("feature_ssml"),
            t("feature_history"),
            t("feature_i18n"),
            t("feature_dark_mode"),
            t("feature_export_import"),
            t("feature_audio_preview"),
            t("feature_text_stats"),
        ]
        for feat in features:
            ui.label(f"  • {feat}").classes("ml-4")

    # ── Usage Guide ──
    with ui.card().classes("w-full p-6"):
        ui.label(f"📖 {t('usage_guide')}").classes("text-lg font-semibold mb-2")
        ui.markdown(t("usage_guide_content"))

    # ── Tech Stack ──
    with ui.card().classes("w-full p-6 mt-4"):
        ui.label(f"🛠️ {t('tech_stack')}").classes("text-lg font-semibold mb-2")
        techs = [
            "NiceGUI (Vue/Quasar/FastAPI)",
            "Edge-TTS (Microsoft)",
            "gTTS (Google)",
            "OmniVoice (k2-fsa, 600+ languages)",
            "Pydantic v2 (Data validation)",
            "Python 3.10+",
        ]
        for tech in techs:
            ui.label(f"  • {tech}").classes("ml-4")
