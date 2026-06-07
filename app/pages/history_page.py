"""History page — view, search, replay, and manage synthesis history."""

from __future__ import annotations

from pathlib import Path

from nicegui import run, ui

from app.i18n.translations import t
from app.storage import db


def history_page(engines: dict) -> None:  # noqa: ARG001
    """Render the history page."""

    state = {"records": [], "search": "", "filter_engine": ""}

    async def load_records():
        all_records = await db.load_history()
        filtered = all_records

        if state["search"]:
            query = state["search"].lower()
            filtered = [r for r in filtered if query in r.text.lower()]

        if state["filter_engine"]:
            filtered = [r for r in filtered if r.engine == state["filter_engine"]]

        state["records"] = filtered
        _refresh_table()

    def _refresh_table():
        table_container.clear()
        with table_container:
            if not state["records"]:
                ui.label(t("history_empty")).classes("text-gray-400 italic")
                return

            for record in state["records"]:
                with ui.card().classes("w-full p-3 mb-2"), ui.row().classes("w-full items-center gap-4"):
                        with ui.column().classes("flex-1"):
                            ui.label(record.text[:80] + ("..." if len(record.text) > 80 else ""))
                            with ui.row().classes("gap-2 text-xs text-gray-400"):
                                ui.label(f"🔧 {record.engine}")
                                ui.label(f"🎤 {record.voice}")
                                ui.label(f"⏱️ {record.duration_seconds:.1f}s")
                                ui.label(f"📅 {record.timestamp[:16]}")

                        with ui.row().classes("gap-1"):
                            if Path(record.audio_path).exists():
                                ui.button(
                                    icon="play_arrow",
                                    on_click=lambda _, r=record: _play(r),
                                ).props("flat dense")
                                ui.button(
                                    icon="download",
                                    on_click=lambda _, r=record: ui.download(r.audio_path),
                                ).props("flat dense")

                            fav_icon = "star" if record.is_favorite else "star_border"
                            ui.button(
                                icon=fav_icon,
                                on_click=lambda _, r=record: _toggle_fav(r.id),
                            ).props("flat dense color=yellow")

                            ui.button(
                                icon="delete",
                                on_click=lambda _, r=record: _delete(r.id),
                            ).props("flat dense color=red")

    def _play(record):
        audio_player.set_source(f"/output/{Path(record.audio_path).name}")
        audio_player.visible = True

    async def _toggle_fav(record_id: str):
        await db.toggle_favorite(record_id)
        await load_records()

    async def _delete(record_id: str):
        await db.delete_history_record(record_id)
        await load_records()

    async def _clear_all():
        await db.clear_history()
        await load_records()

    # ── Layout ──
    ui.label(t("history_title")).classes("text-2xl font-bold mb-4")

    with ui.row().classes("w-full gap-4 items-end mb-4"):
        ui.input(
            label=t("search_label"),
            placeholder=t("search_placeholder"),
            on_change=lambda e: (state.update(search=e.value), None)[-1],
        ).classes("flex-1")

        ui.select(
            options={"": t("all_engines"), "edge-tts": "Edge TTS", "gtts": "gTTS", "omnivoice": "OmniVoice"},
            value="",
            label=t("filter_engine"),
            on_change=lambda e: (state.update(filter_engine=e.value), None)[-1],
        ).classes("w-40")

        ui.button(
            f"🔍 {t('search_btn')}",
            on_click=load_records,
        ).classes("bg-blue-600 text-white")

        ui.button(
            f"🗑️ {t('clear_all_btn')}",
            on_click=_clear_all,
        ).props("flat color=red")

    audio_player = ui.audio("").classes("w-full mb-4")
    audio_player.visible = False

    table_container = ui.column().classes("w-full")

    ui.timer(0.1, load_records, once=True)
