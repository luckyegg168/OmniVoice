"""Settings page — configure app preferences."""

from __future__ import annotations

from nicegui import run, ui

from app.i18n.translations import get_locale, set_locale, t
from app.storage import db


def settings_page(engines: dict) -> None:  # noqa: ARG001
    """Render the settings page."""

    async def load_settings():
        return await run.io_bound(db.load_settings)

    async def save_and_notify():
        settings_data = {
            "locale": locale_select.value,
            "default_engine": engine_select.value,
            "default_speed": speed_slider.value,
            "default_pitch": pitch_slider.value,
            "default_volume": volume_slider.value,
            "auto_play": auto_play_switch.value,
            "save_history": save_history_switch.value,
        }
        await run.io_bound(db.save_settings, settings_data)
        set_locale(locale_select.value)
        ui.notify(f"✅ {t('settings_saved')}", type="positive")

    async def export_settings():
        path = await run.io_bound(db.export_settings)
        ui.download(path)
        ui.notify(t("settings_exported"), type="positive")

    async def handle_import(e):
        if e.content is None:
            return
        import json

        try:
            data = json.loads(e.content.read())
            await run.io_bound(db.import_settings, data)
            ui.notify(t("settings_imported"), type="positive")
            ui.navigate.reload()
        except Exception as exc:
            ui.notify(f"❌ {exc}", type="negative")

    # ── Layout ──
    ui.label(t("settings_title")).classes("text-2xl font-bold mb-6")

    with ui.card().classes("w-full p-6"):
        ui.label(f"🌐 {t('language_settings')}").classes("text-lg font-semibold mb-2")
        locale_select = ui.select(
            options={"zh-TW": "繁體中文", "en": "English", "ja": "日本語"},
            value=get_locale(),
            label=t("language_label"),
        ).classes("w-64")

    ui.separator().classes("my-4")

    with ui.card().classes("w-full p-6"):
        ui.label(f"🔧 {t('default_settings')}").classes("text-lg font-semibold mb-2")

        engine_select = ui.select(
            options={"edge-tts": "Edge TTS", "gtts": "gTTS", "omnivoice": "OmniVoice"},
            value="edge-tts",
            label=t("engine_label"),
        ).classes("w-64")

        with ui.row().classes("w-full gap-6 mt-4"):
            with ui.column().classes("flex-1"):
                ui.label(t("speed_label"))
                speed_slider = ui.slider(min=0.5, max=2.0, step=0.1, value=1.0).classes("w-full")
            with ui.column().classes("flex-1"):
                ui.label(t("pitch_label"))
                pitch_slider = ui.slider(min=0.5, max=2.0, step=0.1, value=1.0).classes("w-full")
            with ui.column().classes("flex-1"):
                ui.label(t("volume_label"))
                volume_slider = ui.slider(min=0.1, max=1.0, step=0.1, value=1.0).classes("w-full")

    ui.separator().classes("my-4")

    with ui.card().classes("w-full p-6"):
        ui.label(f"⚙️ {t('general_settings')}").classes("text-lg font-semibold mb-2")
        auto_play_switch = ui.switch(t("auto_play"), value=True)
        save_history_switch = ui.switch(t("save_history"), value=True)

    ui.separator().classes("my-4")

    with ui.row().classes("gap-4"):
        ui.button(
            f"💾 {t('save_settings_btn')}",
            on_click=save_and_notify,
        ).classes("bg-blue-600 text-white px-6 py-2")

        ui.button(
            f"📤 {t('export_settings_btn')}",
            on_click=export_settings,
        ).classes("bg-green-600 text-white px-4 py-2")

    ui.separator().classes("my-4")

    with ui.card().classes("w-full p-4"):
        ui.label(f"📥 {t('import_settings')}").classes("font-semibold mb-2")
        ui.upload(
            label=t("import_settings_label"),
            on_upload=handle_import,
            auto_upload=True,
        ).props('accept=".json"')

    # ── Init ──
    async def _init():
        settings = await load_settings()
        if settings:
            locale_select.value = settings.get("locale", "zh-TW")
            engine_select.value = settings.get("default_engine", "edge-tts")
            speed_slider.value = settings.get("default_speed", 1.0)
            pitch_slider.value = settings.get("default_pitch", 1.0)
            volume_slider.value = settings.get("default_volume", 1.0)
            auto_play_switch.value = settings.get("auto_play", True)
            save_history_switch.value = settings.get("save_history", True)

    ui.timer(0.1, _init, once=True)
