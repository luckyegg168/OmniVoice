"""Batch processing page — convert multiple texts or files."""

from __future__ import annotations

import uuid

from nicegui import run, ui

from app.config import OUTPUT_DIR
from app.core.audio_utils import preprocess_text
from app.i18n.translations import t
from app.models.history import HistoryRecord
from app.models.tts_request import TTSRequest
from app.storage import db


def batch_page(engines: dict) -> None:
    """Render the batch processing page."""

    state = {
        "engine_id": "edge-tts",
        "items": [],
        "processing": False,
    }

    def add_item():
        txt = item_input.value.strip()
        if txt:
            state["items"].append(txt)
            item_input.value = ""
            _refresh_list()

    def remove_item(idx: int):
        if 0 <= idx < len(state["items"]):
            state["items"].pop(idx)
            _refresh_list()

    def clear_all():
        state["items"].clear()
        _refresh_list()

    def _refresh_list():
        item_list.clear()
        with item_list:
            for i, txt in enumerate(state["items"]):
                with ui.row().classes("w-full items-center gap-2"):
                    ui.label(f"{i + 1}. {txt[:60]}{'...' if len(txt) > 60 else ''}").classes(
                        "flex-1"
                    )
                    ui.button(
                        icon="delete",
                        on_click=lambda _, idx=i: remove_item(idx),
                    ).props("flat dense color=red")

    async def handle_file_upload(e):
        if e.content is None:
            return
        content = e.content.read().decode("utf-8", errors="replace")
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        state["items"].extend(lines)
        _refresh_list()
        ui.notify(f"✅ {t('batch_file_loaded')}: {len(lines)} {t('items')}", type="positive")

    async def start_batch():
        if state["processing"] or not state["items"]:
            ui.notify(t("batch_empty"), type="warning")
            return

        state["processing"] = True
        batch_btn.disable()
        progress.visible = True
        total = len(state["items"])

        eng = engines.get(state["engine_id"])
        if eng is None:
            ui.notify(t("engine_unavailable"), type="negative")
            state["processing"] = False
            batch_btn.enable()
            progress.visible = False
            return

        voices = await eng.list_voices()
        voice_id = voices[0].id if voices else ""
        ext = "wav" if state["engine_id"] == "omnivoice" else "mp3"
        success_count = 0

        for i, raw_text in enumerate(state["items"]):
            try:
                processed = preprocess_text(raw_text)
                file_id = uuid.uuid4().hex[:12]
                out_path = str(OUTPUT_DIR / f"batch_{file_id}.{ext}")

                request = TTSRequest(
                    text=processed,
                    voice=voice_id,
                    language="zh-TW",
                    engine=state["engine_id"],
                    speed=1.0,
                    pitch=1.0,
                    volume=1.0,
                    output_format=ext,
                    output_path=out_path,
                )

                result = await eng.synthesize(request)

                record = HistoryRecord(
                    text=processed,
                    engine=state["engine_id"],
                    voice=voice_id,
                    language="zh-TW",
                    speed=1.0,
                    pitch=1.0,
                    volume=1.0,
                    output_format=ext,
                    audio_path=result.audio_path,
                    duration_seconds=result.duration_seconds,
                )
                await run.io_bound(db.add_history_record, record)
                success_count += 1

            except Exception as exc:
                ui.notify(f"❌ #{i + 1}: {exc}", type="negative")

            progress.value = (i + 1) / total

        ui.notify(
            f"✅ {t('batch_complete')}: {success_count}/{total}",
            type="positive",
        )
        state["processing"] = False
        batch_btn.enable()
        progress.visible = False

    # ── Layout ──
    ui.label(t("batch_title")).classes("text-2xl font-bold mb-4")

    with ui.row().classes("w-full gap-4 items-end"):
        ui.select(
            options={eid: eng.name() for eid, eng in engines.items()},
            value=state["engine_id"],
            label=t("engine_label"),
            on_change=lambda e: state.update(engine_id=e.value),
        ).classes("w-48")

    with ui.row().classes("w-full gap-2 mt-4"):
        item_input = ui.input(
            label=t("batch_input"),
            placeholder=t("batch_input_placeholder"),
        ).classes("flex-1")
        ui.button(t("add_btn"), on_click=add_item).classes("bg-blue-600 text-white")

    ui.upload(
        label=t("batch_upload_file"),
        on_upload=handle_file_upload,
        auto_upload=True,
    ).classes("w-full mt-2").props('accept=".txt,.csv"')

    ui.separator().classes("my-4")

    with ui.row().classes("w-full justify-between items-center"):
        ui.label(f"📋 {t('batch_queue')}").classes("font-semibold")
        ui.button(t("clear_all_btn"), on_click=clear_all).props("flat color=red")

    item_list = ui.column().classes("w-full gap-1")

    with ui.row().classes("mt-4"):
        batch_btn = ui.button(
            f"🚀 {t('batch_start')}",
            on_click=start_batch,
        ).classes("bg-blue-600 text-white px-6 py-2")

    progress = ui.linear_progress(value=0).classes("mt-2")
    progress.visible = False
