"""SSML editor page — advanced Speech Synthesis Markup Language editing."""

from __future__ import annotations

import html
import json
import uuid
from pathlib import Path

from nicegui import run, ui

from app.config import OUTPUT_DIR
from app.i18n.translations import t
from app.models.history import HistoryRecord
from app.models.tts_request import TTSRequest
from app.storage import db

# ── Quick-tag definitions: (label, open_tag, close_tag) ──
SSML_QUICK_TAGS = [
    ("<break/>", '<break time="500ms"/>', ""),
    ("<emphasis>", '<emphasis level="strong">', "</emphasis>"),
    ("<prosody>", '<prosody rate="slow">', "</prosody>"),
    ("<say-as>", '<say-as interpret-as="characters">', "</say-as>"),
    ("<sub>", '<sub alias="">', "</sub>"),
    ("<lang>", '<lang xml:lang="en-US">', "</lang>"),
    ("<voice>", '<voice name="zh-TW-HsiaoChenNeural">', "</voice>"),
]

SSML_TEMPLATES = {
    "basic": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        '  <voice name="zh-TW-HsiaoChenNeural">\n'
        "    你好，歡迎使用語音合成。\n"
        "  </voice>\n"
        "</speak>"
    ),
    "pause": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        "  第一段文字。\n"
        '  <break time="500ms"/>\n'
        "  第二段文字。\n"
        "</speak>"
    ),
    "emphasis": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        '  這是<emphasis level="strong">重點</emphasis>內容。\n'
        "</speak>"
    ),
    "prosody": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        '  <prosody rate="slow" pitch="high">\n'
        "    慢速高音的語音。\n"
        "  </prosody>\n"
        "</speak>"
    ),
}


def ssml_page(engines: dict) -> None:
    """Render the SSML editor page."""

    state = {"generating": False}

    def insert_template(name: str):
        template = SSML_TEMPLATES.get(name, "")
        if template:
            ssml_editor.value = template

    def convert_to_ssml():
        """Wrap plain text in basic SSML skeleton and populate the editor."""
        text = plain_input.value.strip()
        if not text:
            # If empty, use the focus hint
            ui.notify(t("input_placeholder"), type="warning")
            return
        # Escape HTML special chars so plain text & < > don't break SSML
        escaped = html.escape(text)
        # Split lines, wrap each non-empty line as a paragraph
        lines = [f"  {ln}" for ln in escaped.split("\n") if ln.strip()]
        body = "\n".join(lines) if lines else f"  {escaped}"
        ssml = (
            '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
            ' xml:lang="zh-TW">\n'
            f"{body}\n"
            "</speak>"
        )
        ssml_editor.value = ssml
        ui.notify("✅ SSML 已產生，可繼續編輯", type="positive")

    async def synthesize_ssml():
        if state["generating"]:
            return
        ssml_text = ssml_editor.value or ""
        if not ssml_text.strip():
            ui.notify(t("ssml_empty"), type="warning")
            return

        state["generating"] = True
        ssml_btn.disable()
        progress.visible = True

        try:
            eng = engines.get("edge-tts")
            if eng is None:
                ui.notify(t("engine_unavailable"), type="negative")
                return

            file_id = uuid.uuid4().hex[:12]
            out_path = str(OUTPUT_DIR / f"ssml_{file_id}.mp3")

            request = TTSRequest(
                text=ssml_text,
                voice="zh-TW-HsiaoChenNeural",
                language="zh-TW",
                engine="edge-tts",
                speed=1.0,
                pitch=1.0,
                volume=1.0,
                output_format="mp3",
                output_path=out_path,
                ssml=True,
            )

            result = await eng.synthesize(request)

            audio_player.set_source(f"/output/{Path(result.audio_path).name}")
            audio_player.visible = True

            record = HistoryRecord(
                text=ssml_text[:200],
                engine="edge-tts",
                voice="ssml",
                language="zh-TW",
                speed=1.0,
                pitch=1.0,
                volume=1.0,
                output_format="mp3",
                audio_path=result.audio_path,
                duration_seconds=result.duration_seconds,
            )
            await db.add_history_record(record)

            ui.notify(f"✅ {t('generate_success')}", type="positive")

        except Exception as exc:
            ui.notify(f"❌ {t('generate_error')}: {exc}", type="negative")
        finally:
            state["generating"] = False
            ssml_btn.enable()
            progress.visible = False

    # ── Layout ──
    ui.label(t("ssml_title")).classes("text-2xl font-bold mb-4")
    ui.label(t("ssml_description")).classes("text-gray-400 mb-4")

    # ── Plain text → SSML ──
    ui.separator().classes("my-4")
    ui.label(t("ssml_paste_label")).classes("text-lg font-semibold mb-2")
    plain_input = ui.textarea(label=t("input_placeholder")).classes("w-full").props("rows=4")
    with ui.row().classes("mt-2 mb-1"):
        ui.button(
            f"🔁 {t('ssml_convert_btn')}",
            on_click=convert_to_ssml,
        ).props("flat color=primary")

    ui.separator().classes("my-4")

    # ── SSML Templates & Editor ──
    with ui.row().classes("gap-2 mb-4"):
        ui.label(f"📝 {t('ssml_templates')}:").classes("self-center")
        for name in SSML_TEMPLATES:
            ui.button(
                name.capitalize(),
                on_click=lambda _, n=name: insert_template(n),
            ).props("flat dense")

    # ── Quick-tag buttons ──
    with ui.row().classes("gap-1 mb-2"):
        ui.label(f"🏷️ {t('ssml_quick_tags')}:").classes("self-center text-sm")
        for label, open_tag, close_tag in SSML_QUICK_TAGS:
            ui.button(
                label,
                on_click=lambda _, o=open_tag, c=close_tag: ui.run_javascript(
                    f"insertSSMLTag({json.dumps(o)}, {json.dumps(c)})"
                ),
            ).props("flat dense size=sm")

    # Inject JS helper for cursor-aware tag insertion
    ui.add_body_html("""
<script>
function insertSSMLTag(openTag, closeTag) {
    var ta = document.querySelector('.font-mono textarea');
    if (!ta) return;
    var start = ta.selectionStart;
    var end = ta.selectionEnd;
    var sel = ta.value.substring(start, end);
    ta.setRangeText(openTag + sel + closeTag, start, end, 'end');
    ta.dispatchEvent(new Event('input', {bubbles: true}));
}
</script>
""")

    ssml_editor = (
        ui.textarea(
            label=t("ssml_editor_label"),
            value=SSML_TEMPLATES["basic"],
        )
        .classes("w-full font-mono")
        .props("rows=12")
    )

    with ui.row().classes("mt-4"):
        ssml_btn = ui.button(
            f"🎙️ {t('ssml_generate')}",
            on_click=synthesize_ssml,
        ).classes("bg-blue-600 text-white px-6 py-2")

    progress = ui.linear_progress().classes("mt-2")
    progress.visible = False

    audio_player = ui.audio("").classes("w-full mt-4")
    audio_player.visible = False
